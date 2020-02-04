# -*- coding: utf-8 -*-
from __future__ import absolute_import

# basic system configuration
import sys

# interaction with file system
import os

# call executable
import subprocess

# remove directory content
import shutil

# read configuration of test suite
if sys.version_info[0] == 3:
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser

# logging
import logging

# parse command line
import getopt

# current time
from datetime import datetime

# file pattern
import re

# to hash path
import hashlib

# has_key wrapping for python 2/3 compatibility
def has_key(dictionnary, key):
    if sys.version_info[0] == 3:
        return key in dictionnary
    else:
        return dictionnary.has_key(key)

# read specific section of configuration file
def readConfigSection(filename, section):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

# check if a file exists and raise an exception with given message otherwise
def shouldFileExists(filename, message):
    # check if file exit
    if not os.path.exists(filename):
        raise Exception('File {0} does not exist for {1}'.format(filename, message))

# check dictionnary structure against mandatory and optional keys
# in case of optionalKeys (which is a dict), put the default value if dictionnary does not contain an optional key
def shouldDictonnaryContains(name, dictionnary, mandatoryKeys, optionalKeys):
    consumedMandatoryKeys = set(mandatoryKeys)
    consumedOptionalKeys = set(optionalKeys.keys())

    # for each key in dictionnary
    for key in dictionnary.keys():
        if not key in consumedMandatoryKeys:
            if not key in consumedOptionalKeys:
                raise Exception('Dictionnay {0} cannot contains key {1}'.format(name, key))
            else:
                consumedOptionalKeys.remove(key)
        else:
            consumedMandatoryKeys.remove(key)

    if len(consumedMandatoryKeys) > 0:
        raise Exception('Dictionnay {0} should contains keys {1}'.format(name, repr(consumedMandatoryKeys)))

    for optional in consumedOptionalKeys:
        dictionnary[optional] = optionalKeys[optional]

def shouldDirectoryExistsOrCreate(targetDir):
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    else:
        if not os.path.isdir(targetDir):
            raise Exception('Directory {0} should be a directory and not a file'.format(targetDir))

def loadAndValidate(configFile):

    # config should exists
    shouldFileExists(configFile, "configuration file")

    # read global section
    globalConfig = readConfigSection(configFile, "global")
    shouldDictonnaryContains("global", globalConfig, [], {"log.dir":".", "trash.dir":"trash", "report.path" : "rapport.csv"})

    # read reference section
    referenceConfig = readConfigSection(configFile, "reference")
    shouldDictonnaryContains("reference", referenceConfig, ["exe.path"], {"skip.run":"False"})
    shouldFileExists(referenceConfig["exe.path"], "reference.exe.path")

    # read reference section
    newConfig = readConfigSection(configFile, "new")
    shouldDictonnaryContains("new", newConfig, ["exe.path"], {"skip.run":"False", "clean.run":"True"})
    shouldFileExists(newConfig["exe.path"], "new.exe.path")

    # read studies section
    studiesConfig = readConfigSection(configFile, "studies")
    shouldDictonnaryContains("studies", studiesConfig, ["list"], {"pass":[], "big":[]})

    # for each studies of the list separated by ","
    studies = []
    for rawStudyName in studiesConfig["list"].split(","):
        studyName = rawStudyName.strip()
        if len(studyName) > 0:
            # read studies section
            studyConfig = readConfigSection(configFile, studyName)
            shouldDictonnaryContains("study %s" % studyName, studyConfig, ["reference.path", "new.path"],{"name":studyName})
            # check paths
            shouldFileExists(studyConfig["reference.path"], "reference directory for study %s" % studyName)
            shouldFileExists(studyConfig["new.path"], "new directory for study %s" % studyName)
            # add study to pool
            studies.append(studyConfig)

    # display number of studies
    logging.info("Config contains %d studies" % len(studies))

    logDir = os.path.normpath(globalConfig["log.dir"])
    shouldDirectoryExistsOrCreate(logDir)

    trashDir = os.path.normpath(globalConfig["trash.dir"])
    shouldDirectoryExistsOrCreate(trashDir)

    # build final config
    config = {}
    config["global"] = globalConfig
    config["reference"] = referenceConfig
    config["new"] = newConfig
    config["studies"] = studiesConfig

    # return config and studies
    return config, studies
# display timedelta as string
def displayDuration(duration):
    return str(duration.total_seconds())

# Class used to run a test given an executable
class Runner:
    def __init__(self, exePath, options):
        self.exePath = exePath
        self.options = {
            "skip" : False,
            "trashDir" : "."
        }
        self.options.update(options)

        # In case this current python program is run on Windows, preventing error window
        # from popping up, leading the python program to wait the end of ANTARES exeuction eternally.
        if sys.platform.startswith("win"):
            import ctypes
            SEM_NOGPFAULTERRORBOX = 0x0002
            ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX);
            self.subprocess_flags = 0x08000000
        else:
            self.subprocess_flags = 0

    def normalizePath(self, path):
        return os.path.normpath(path)

    def isResult(self, x):
        return "eco" in x or "adq" in x or "test-result" in x

    # run exe on study and return stats on this run
    def runOnSingleStudy(self, studyPath):
        # we will compute some stats
        stats = {"display_runtime":"n/a"}

        # normalize study path
        studyBaseDir = self.normalizePath(studyPath)

        # check if we have to skip the run
        if self.options["skip"]:
            stats.update(self.computeStats(studyPath))
            stats["returnCode"] = 0
            return stats

        # we prepare run
        self.prepareRun(studyBaseDir)

        # perform run
        startTime = datetime.now()
        ret = self.performRunItself(studyBaseDir)
        endTime = datetime.now()

        # compute run stats
        stats["returnCode"] = ret
        stats["duration"] = endTime - startTime
        stats["display_runtime"] = displayDuration(stats["duration"])

        # post process run if run is ok
        if ret == 0:
            stats.update(self.postProcessRun(studyBaseDir))
        else:
            logging.error('Run failed on {0} with executable {1}'.format(studyBaseDir, self.exePath))

        # return accumulated stats
        return stats

    def removeDir(self, dirToClean):
        try:
            shutil.rmtree(dirToClean)
        except WindowsError:
            logging.warning('Cleaning failed on {0}'.format(dirToClean))
            trashDir = self.options["trashDir"]
            m = hashlib.md5()
            m.update(dirToClean)
            dirInTrash = self.normalizePath(os.path.join(trashDir, "echec-suppression_%s" % m.hexdigest()))
            os.rename(dirToClean, dirInTrash)

    # clean study output and logs directory
    def prepareRun(self, studyBaseDir):

        # clean output directory
        outputDir = os.path.join(studyBaseDir, "output")
        if os.path.isdir(outputDir):
            for runDir in filter(lambda x: self.isResult(x), os.listdir(outputDir)):
                self.removeDir(os.path.join(outputDir, runDir))

        # clean logs directory
        logsDir = os.path.join(studyBaseDir, "logs")
        if os.path.isdir(logsDir):
            for solverFile in filter(lambda x:"solver-" in x, os.listdir(logsDir)):
                os.remove(os.path.join(logsDir, solverFile))
        else:
            os.makedirs(logsDir)

    # launch executable on study base directory and trace run in simulation.log
    def performRunItself(self, studyBaseDir):
        logFile = os.path.join(studyBaseDir,"logs","simulation.log")
        command = '"%s" "%s" --year-by-year > "%s"' % (self.exePath, studyBaseDir, logFile)
        ret = subprocess.call(command, shell=True, creationflags=self.subprocess_flags)
        return ret

    # rename output dir and retrieve cpu and memory consumption per solver call
    def postProcessRun(self, studyBaseDir):

        # rename output dir
        # clean output directory
        outputDir = os.path.join(studyBaseDir, "output")
        for i,runDir in enumerate(filter(lambda x : self.isResult(x), os.listdir(outputDir))):
            os.rename(os.path.join(outputDir, runDir), os.path.join(outputDir, "test-result_%d" % i))

        # return computed stats
        return self.computeStats(studyBaseDir)

    # retrieve cpu and memory consumption per solver call
    def computeStats(self, studyBaseDir):
        # initializeing result
        stats = {}

        # computing simulation log path
        simulationLog = os.path.join(studyBaseDir, "output", "test-result_0","simulation.log")

        # if simulation.log exists (meaning that the has took place)
        if os.path.exists(simulationLog):
            # we will get all elapsed time in this list
            stats["elapsed-list"]=[]
            stats["memory-list"]=[]

            # read lines of simulation.log
            simulationLines = open(simulationLog,"r").readlines()

            # for each line, we deal with several case
            for line in simulationLines:
                # case for getting dimensions of canonical form
                if "Problem Size" in line:
                    sline = line.split(" ")
                    stats["variables"] = sline[9].replace(":","")
                    stats["constraints"] = sline[11]

                # case for getting non-zero terms of canonical form
                if "Non-zero terms" in line:
                    sline = line.split(" ")
                    stats["non-zero"] = sline[15][:-1]

                # case for getting elapsed time
                if "Elapsed time" in line:
                    sline = line.split(":")
                    elapsed = sline[-1][:-3]
                    label = sline[-2].strip()
                    stats["elapsed-list"].append((label, elapsed))

                # case for getting memory consumption
                if "system memory report" in line:
                    sline = line.split(" ")
                    i = sline.index("report:")
                    free, total = int(sline[i+1]), int(sline[i+4])
                    stats["memory-list"].append(total-free)


            # all lines have been parse, we consolidate time statics
            study_elapsed,mc_export_elapsed,mc_elapsed,export_elapsed = "0","0","0","0"
            solve_time_by_run, mc_done = {}, False
            for label, time in stats["elapsed-list"]:
                if label == "Study loading":
                    study_elapsed = time
                elif label == "MC Years":
                    mc_elapsed, mc_done = time, True
                elif label == "Survey report":
                    if not mc_done:
                        mc_export_elapsed = time
                    else:
                        export_elapsed = time
                else:
                    key = tuple(filter(lambda x:x.isdigit(), label.replace(",","=").split("=")))
                    solve_time_by_run[key] = float(time)

            stats["solve_time"] = sum(solve_time_by_run.values()) / 1000.0
            stats["solve_time_by_run"] = solve_time_by_run
            stats["loading_time"] = float(study_elapsed)/1000.0 # load time is the first elapsed time
            stats["mc_time"] = float(mc_elapsed)/1000.0 - float(mc_export_elapsed)/1000.0 # second elapsed time is the solve time minus the export of results
            stats["export_time"] = float(mc_export_elapsed)/1000.0 + float(export_elapsed)/1000.0 # export time is the export of results and export of survey
            stats["total_time"] = stats["loading_time"]  + stats["mc_time"] + stats["export_time"] # total time is the sum of the previous three elapsed time

            # consistency of statistics
            if len(stats["memory-list"]) > 0:
                stats["memory_indicator"] = max(stats["memory-list"]) - min(stats["memory-list"])
            else:
                stats["memory_indicator"] = 0

            if not has_key(stats, "variables"):
                stats["variables"] = 0
                stats["constraints"] = 0
                stats["non-zero"] = 0

        # we return stats
        return stats


def compareOutputs(study, skipPatterns):
    # get paths
    refDir = os.path.normpath(study["reference.path"])
    newDir = os.path.normpath(study["new.path"])

    # output path
    refDirPath = os.path.join(refDir, "output")
    newDirPath = os.path.join(newDir, "output")

    # what to return
    notExisting = []
    difference = []
    same = []
    skipped = []

    # for each file in reference directory
    for root, dirs, files in os.walk(refDirPath):
        for fileName in files:

            # check if we skip file due to patterns
            skipFile = False
            for skipPattern in skipPatterns:
                if re.match(skipPattern,fileName):
                    skipFile = True

            # we determine paths for both file in reference and new directory
            refFilePath = os.path.join(refDirPath, root, fileName)
            newFilePath = refFilePath.replace(refDirPath, newDirPath)

            # we continue walking dir
            if skipFile:
                skipped.append(newFilePath)
                continue

            # we compute file status
            if not os.path.exists(newFilePath):
                notExisting.append(newFilePath)
            else:
                refContent = open(refFilePath).read()
                newContent = open(newFilePath).read()
                if refContent != newContent:
                    difference.append(newFilePath)
                else:
                    same.append(newFilePath)

    # return compared output
    return notExisting, difference, same, skipped

def compareRuns(study, shouldCleanNew):
    # result dictionnary
    stats = { "comparison": {}}

    # compare outputs
    notExisting, difference, same, skipped = compareOutputs(study, [r"criterion-.*", r"problem.*",r"(simulation.log|study.ini|info.antares-output)"])

    # compute status
    status = "OK" if len(notExisting) == 0 and len(difference) == 0 else "KO"

    # enrich result
    stats["comparison"]["status"] = status
    stats["comparison"]["notExisting"] = notExisting
    stats["comparison"]["difference"] = difference
    stats["comparison"]["same"] = same
    stats["comparison"]["skipped"] = skipped

    # clean new for keeping reference
    if shouldCleanNew:
        for f in same:
            if os.path.exists(f):
                os.remove(f)
        for f in skipped:
            if os.path.exists(f):
                os.remove(f)

    # return comparison
    return stats

def computeReportContent(study, stats):
    try:
        td = stats["new"]["solve_time"] - stats["reference"]["solve_time"]
        if stats["reference"]["solve_time"] <= 0:
            if stats["new"]["solve_time"] == stats["reference"]["solve_time"]:
                tdr=0
            else:
                tdr=100
        else:
            tdr = 100.0 * float(stats["new"]["solve_time"] - stats["reference"]["solve_time"]) / stats["reference"]["solve_time"]
        mi = stats["new"]["memory_indicator"] - stats["reference"]["memory_indicator"]
        mir = 100.0 * float(stats["new"]["memory_indicator"] - stats["reference"]["memory_indicator"]) / stats["reference"]["memory_indicator"] if stats["reference"]["memory_indicator"] else 100.0 * float(stats["new"]["memory_indicator"])
        summary="""\tStatus for %s: [%s] time delta=%.3f (%.2f%%), memory indicator=%d (%.2f%%)""" % (study["name"], stats["comparison"]["status"], td, tdr, mi, mir)
        logging.info(summary)
    except KeyError as e:
        summary="""\tStatus for %s: [KO] time delta=n/a (n/a%%), memory indicator=n/a (n/a%%)""" % (study["name"])
        logging.info(summary)
        return ["Unable to access staticis %s" % str(e)]

    # create report
    reportContent = [
"""Problem structure
    reference:
        variables: %s
        constraints: %s
        non-zeros: %s
    new:
        variables: %s
        constraints: %s
        non-zeros: %s

Run statitics:
    reference:
        loading time: %f
        solve time: %f
        export time: %f
        memory indicator: %d
    new:
        loading time: %f
        solve time: %f
        export time: %f
        memory indicator: %d
"""	% (
        stats["reference"]["variables"],
        stats["reference"]["constraints"],
        stats["reference"]["non-zero"],
        stats["new"]["variables"],
        stats["new"]["constraints"],
        stats["new"]["non-zero"],
        stats["reference"]["loading_time"],
        stats["reference"]["solve_time"],
        stats["reference"]["export_time"],
        stats["reference"]["memory_indicator"],
        stats["new"]["loading_time"],
        stats["new"]["solve_time"],
        stats["new"]["export_time"],
        stats["new"]["memory_indicator"]
    )
    ]

    reportContent.append("""\nResolution time""")
    for version in ["reference", "new"]:
        reportContent.append("\t%s" % version)
        solve_time_by_run = stats[version]["solve_time_by_run"]
        reportContent.append("\t\tnumber of runs: %d" % len(solve_time_by_run))
        for key in sorted(solve_time_by_run.keys()):
            pne, year, week, interval, optim = key
            reportContent.append("\t\t\tpne=%s,year=%s,week=%s,interval=%s,optim=%s: %f" % (pne, year, week, interval, optim, solve_time_by_run[key]) )

    # Report files which do not exists in new whereas it should
    reportContent.append("\n\nFiles of reference not existing in new:")
    for path in stats["comparison"]["notExisting"]:
        reportContent.append("\t%s" % path)

    # Report files which are different in new whereas it should
    reportContent.append("Files in new with a difference from reference:")
    for path in stats["comparison"]["difference"]:
        reportContent.append("\t%s" % path)

    # Report files which are the same in new and in reference
    reportContent.append("Same in both version:")
    for path in stats["comparison"]["same"]:
        reportContent.append("\t%s" % path)

    # Report skipped files
    reportContent.append("Skipped files in new:")
    for path in stats["comparison"]["skipped"]:
        reportContent.append("\t%s" % path)

    return reportContent

def report(study, stats, logDir):
    if stats["reference"]["returnCode"] == 0 and stats["new"]["returnCode"] == 0:
        reportContent = computeReportContent(study, stats)
        status = stats["comparison"]["status"]
    else:
        summary="""\tStatus for %s: [ERROR] time delta=n/a (n/a%%), memory indicator=n/a (n/a%%)""" % study["name"]
        logging.info(summary)
        reportContent = ["""Studies are not comparable due to return codes:
    reference: %d
    new: %d
    """ % (stats["reference"]["returnCode"], stats["new"]["returnCode"])]
        status = "ERROR"

    logFilePath = os.path.join(logDir,"report_%s.log" % study["name"])
    reportFile = open(logFilePath, "w")
    reportFile.write("\n".join(reportContent))
    reportFile.close()

    return status

def globalReport(study, stats, status, accumulator):

    # we define a dictonnary by study
    entry = {}

    # we fill the structure
    entry["Nom"] = study["name"]
    entry["Statut"] = status
    for version in ["reference", "new"]:
        solve_time_by_run = stats[version]["solve_time_by_run"] if has_key(stats[version], "solve_time_by_run") else {}
        entry["Temps total toutes résolutions %s" % version] = "%.3f" % (sum(solve_time_by_run.values()) / 1000.0)
        entry["Indicateur mémoire %s" % version] = "%.2f" % stats[version]["memory_indicator"] if has_key(stats[version], "solve_time_by_run") else ""
        key_spx = [key for key in filter(lambda x : x[0] == "0", solve_time_by_run.keys())]
        key_pne = [key for key in filter(lambda x : x[0] == "1", solve_time_by_run.keys())]
        entry["Nombre résolutions PNE %s" % version] = "%d" % len(key_pne)
        entry["Nombre résolutions SPX %s" % version] = "%d" % len(key_spx)
        entry["Temps total résolution SPX %s" % version] = "%.3f" % (sum([solve_time_by_run[key] for key in key_spx]) / 1000.0)
        entry["Temps première résolution SPX %s" % version] = "%.3f" % (solve_time_by_run[key_spx[0]] / 1000.0) if len(key_spx) > 0 else ""
        entry["Temps première résolution PNE %s" % version] = "%.3f" % (solve_time_by_run[key_pne[0]] / 1000.0) if len(key_pne) > 0 else ""

        run_data = []
        for key in solve_time_by_run.keys():
            pne, year, week, interval, optim = key
            run_data.append("%s;%s;%s;%s;%s;%s;%f" % (study["name"], pne, year, week, interval, optim, solve_time_by_run[key] / 1000.0))
        entry["run_data"] = ("\n".join(run_data) + "\n") if len(run_data) else ""

    accumulator.append(entry)
    return

""" Pour le rapport global on veut les indicateurs suivants (par étude) :
- nom de l'étude
- status de la comparaison
- temps total toutes résolutions confondues ref/new
- indicateur mémoire ref/new
- temps première résolution PNE ref/new
- temps première résolution SPX ref/new
- temps total résolution SPX ref/new
- indicateur mémoire PNE ref/new
- nb résolution PNE  ref/new
- nb résolution SPX  ref/new
"""
def writeGlobalReport(accumulator, reportPath):
    f = open(reportPath, "w")
    headers = ["Nom", "Statut"] + ["%s %s" % (item, version) for item in [
        "Temps total toutes résolutions",
        "Indicateur mémoire",
        "Temps première résolution SPX",
        "Temps première résolution PNE",
        "Temps total résolution SPX",
        "Nombre résolutions PNE",
        "Nombre résolutions SPX"
    ] for version in ["reference", "new"]]
    f.write(";".join(headers)+"\n")
    for entry in accumulator:
        f.write(";".join([entry[header] for header in headers])+"\n")
    f.close()

    if reportPath.endswith("csv"):
        f = open(reportPath.replace(".csv","_runs.csv"), "w")
        f.write(";".join(["name","pne", "year", "week", "interval", "optim"])+"\n")
        for entry in accumulator:
            f.write(entry["run_data"])
        f.close()

    return

def toBoolean(strBool):
    return strBool == "True"

def runAndCompare(configFile):

    # load configuration
    logging.info("Load configuration %s" % configFile)
    config, studies = loadAndValidate(configFile)
    shouldCleanNew = toBoolean(config["new"]["clean.run"])
    trashDir = config["global"]["trash.dir"]

    # instantiate runner
    runnerForReference = Runner(config["reference"]["exe.path"], {"skip":toBoolean(config["reference"]["skip.run"]), "trashDir" : trashDir})
    runnerForNew = Runner(config["new"]["exe.path"], {"skip":toBoolean(config["new"]["skip.run"]), "trashDir" : trashDir})

    # for each study
    statusList = []
    globalStats = []
    for i,study in enumerate(studies):
        stats = {}
        logging.info("\tProcessing study %d/%d: '%s'" % (1+i,len(studies),study["name"]))

        # run
        logging.info("\tRun reference for %s" % study["name"])
        stats["reference"] = runnerForReference.runOnSingleStudy(study["reference.path"])
        logging.info("\tRun took %s" % stats["reference"]["display_runtime"])

        logging.info("\tRun new for %s" % study["name"])
        stats["new"] = runnerForNew.runOnSingleStudy(study["new.path"])
        logging.info("\tRun took %s" % stats["new"]["display_runtime"])

        # compare results
        logging.info("\tComparison for %s" % study["name"])
        stats.update(compareRuns(study, shouldCleanNew))

        # write report
        status = report(study, stats, config["global"]["log.dir"])
        statusList.append(status)

        globalReport(study, stats, status, globalStats)
        writeGlobalReport(globalStats, config["global"]["report.path"])

    # display summary
    logging.info("Summary of test suite:")
    logging.info("	OK    : %d" % len([s for s in filter(lambda x:x == "OK", statusList)]))
    logging.info("	KO    : %d" % len([s for s in filter(lambda x:x == "KO", statusList)]))
    logging.info("	ERROR : %d" % len([s for s in filter(lambda x:x == "ERROR", statusList)]))

    # write csv reporting
    logging.info("Write report in file %s" %  config["global"]["report.path"])
    #writeGlobalReport(globalStats, config["global"]["report.path"])

    # clean trash directory
    logging.info("Clean trash directory")
    try:
        shutil.rmtree(trashDir)
    except WindowsError as e:
        logging.error("Fail to clean trash director : %s" % str(e))

def generateConfig(configFile, refDir, newDir):
    logging.info("Generating configuration %s with directories %s and %s" % (configFile, refDir, newDir))

    marker = "study.antares"
    refDirPath = os.path.abspath(os.path.normpath(refDir))
    newDirPath = os.path.abspath(os.path.normpath(newDir))

    logging.info("Walking through %s" %  refDirPath)
    refCandidates = {}
    for root, dirs, files in os.walk(refDirPath):
        if marker in files:
            refCandidates[os.path.basename(root)] = root

    logging.info("Walking through %s" %  newDirPath)
    newCandidates = {}
    for root, dirs, files in os.walk(newDirPath):
        if marker in files:
            newCandidates[os.path.basename(root)] = root

    studies = set(refCandidates.keys()).intersection(set(newCandidates.keys()))

    print(studies)
    config="""[studies]
list=%s

""" % ",".join(map(lambda x:"study_%d" % x[0], enumerate(sorted(studies))))

    for i, study in enumerate(sorted(studies)):
        config +="""[study_%d]
name=%s
reference.path=%s
new.path=%s

""" % (i, study, refCandidates[study], newCandidates[study])

    f = open(configFile,"w")
    f.write(config)
    f.close()

def help():

    example = """
[global]
log.dir=<path to log directory>

[reference]
exe.path=<path to reference exectuable>
skip.run=True

[new]
exe.path=<path to executable we want to compare>
skip.run=False
clean.run=True

[studies]
list=study_1,study_2
pass=study_3

[study_1]
name=<study #1 name>
reference.path=<path to study #1 reference>
new.path=<path to study #1 new>

[study_2]
name=<study #2 name>
reference.path=<path to study #2 reference>
new.path=<path to study #2 new>

[study_3]
name=<study #3 name>
reference.path=<path to study #3 reference>
new.path=<path to study #3 new>
"""

    print("Usage: %s [options]" % sys.argv[0])
    print("With options among:")
    print("\t-c,--config : configuration file (default: config.ini)")
    print("\nconfig.ini should be structured as: %s" % example)

    sys.exit(0)

def configureLogging(logFilePath):
    if logFilePath == None:
        logging.basicConfig(stream=sys.stdout,level=logging.INFO,format='%(levelname)s - %(asctime)s: %(message)s')
    else:
        # clean log file
        open(logFilePath,"w").close()
        # configure logging to write in it
        logging.basicConfig(filename=logFilePath,level=logging.INFO,format='%(levelname)s - %(asctime)s: %(message)s')


def main(argv):
    longoptions = ["help", "config=","generate=","log="]
    opts, args = getopt.getopt(argv,"h",longoptions)

    if len(opts) == 0:
        help()

    configFile, generate, logFilePath = "config.ini", False, None
    for option,arg in opts:
        if option in ("-h","--help"):
            help()

        if option in ("--config"):
            configFile = arg

        if option in ("--generate"):
            configFile = arg
            generate = True
            refDir = args[0]
            newDir = args[1]

        if option in ("--log"):
            logFilePath = arg

    configureLogging(logFilePath)

    startingDate = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M")
    logging.info("Starting test suite at %s" % startingDate)

    if generate:
        generateConfig(configFile, refDir, newDir)
    else:
        runAndCompare(configFile)

    endingDate = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M")
    logging.info("Ending test suite at %s" % endingDate)

if __name__ == "__main__":
    main(sys.argv[1:])
    #main(['--config=mini.ini'])
