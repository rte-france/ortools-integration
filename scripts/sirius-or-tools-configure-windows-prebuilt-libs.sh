source $(dirname $0)/config.sh

export ORTOOLSDEPDIR="C:/Dev/RTE/ortoolsDepInstall"
export SIRIUSDIR="C:/Dev/RTE/2019/SiriusAntaresV7"
export CPLEXDIR="C:/Program Files/IBM/ILOG/CPLEX_Studio127/cplex"
#export XPRESSDIR="C:/xpressmp"

# Repertoire ou seront installes les lib ortools compilees
export ORTOOLSINSTALLDIR="ortools_install_dir"

lookForLib "${ORTOOLSDEPDIR}" "Ortools pre-build dependencies" "/lib/glog.lib"
lookForLib "${SIRIUSDIR}" "Sirius lib" "lib/Release/bib_solveur.lib"
#lookForLib "${CPLEXDIR}" "Cplex lib" "/lib/x64_windows_vs2015/stat_mda/cplex1270.lib"
lookForLib "${XPRESSDIR}" "Xpress lib" "/lib/xprs.lib"

[ "xxx$ORTOOLSINSTALLDIR" == "xxx" ] && echo "*** ERROR *** : ORTOOLSINSTALLDIR not defined, please edit this script" && exit -1

cmake	-S. -Bbuild -G"Visual Studio 15 2017 Win64" -DBUILD_DEPS=OFF \
		-DCMAKE_PREFIX_PATH="${ORTOOLSDEPDIR}" \
		-DCMAKE_INSTALL_PREFIX="${ORTOOLSINSTALLDIR}" \
		-DUSE_SIRIUS=ON -DUSE_CPLEX=OFF -DUSE_XPRESS=ON -DBUILD_PYTHON=OFF #-DBUILD_TESTING=OFF
