if [ "x${OSTYPE}" == "linux-gnu" ]; then
	export WINDOWS_FLAG="OFF"
	export CHOSEN_COMPILER="Unix Makefiles"
	
	export ORTOOLS_BUILD_DEPS="ON"
else
	export WINDOWS_FLAG="ON"
	export CHOSEN_COMPILER="Visual Studio 15 2017 Win64"
	
	export ORTOOLS_BUILD_DEPS="OFF"
fi

# OR-Tools flags
export ORTOOLS_BUILD_DEPENDENCIES_MP="ON" # activate parallel build of dependencies if possible (/MP)
export ORTOOLS_PYTHON_SWITCH="OFF" # build python version of OR-Tools
export ORTOOLS_TESTING_SWITCH="OFF" # build and run tests after building OR-Tools

export ORTOOLS_SIRIUS_SWITCH="ON" # activate Sirius interface
export ORTOOLS_XPRESS_SWITCH="ON" # activate Xpress interface
export ORTOOLS_CPLEX_SWITCH="OFF"  # activate Cplex interface

# Pathes to extern solver installs
#export CPLEXDIR="C:/Program Files/IBM/ILOG/CPLEX_Studio127/cplex"
#export XPRESSDIR="C:/xpressmp81"

if [ "${ORTOOLS_XPRESS_SWITCH}x" == "ONx" ]; then
	echo "XPRESSDIR : ${XPRESSDIR}"; fi
if [ "${ORTOOLS_CPLEX_SWITCH}x" == "ONx" ]; then
	echo "CPLEXDIR : ${CPLEXDIR}"; fi

####                                ####
#### DO NOT CHANGE BELOW THIS POINT ####
####                                ####

# Sirius variables
export SIRIUS_GIT_PATH="$PWD/subrepos/Sirius"
export SIRIUS_REPO="https://github.com/rte-france/temp-pne.git"
export SIRIUS_BRANCH="metrix"

export SIRIUS_SRC_PATH="$PWD/subrepos/Sirius/src"
export SIRIUS_BUILD_DIR="$PWD/subrepos/Sirius/buildLinux"
export SIRIUS_INSTALL_DIR="$PWD/subrepos/Sirius/buildLinux/install"

# OR-Tools variables
export ORTOOLS_GIT_PATH="$PWD/subrepos/OR-Tools"
export ORTOOLS_REPO="https://github.com/rte-france/or-tools.git"
export ORTOOLS_BRANCH="rte-antares-ortools-sirius"

export ORTOOLS_SRC_PATH="$PWD/subrepos/OR-Tools"
export ORTOOLS_BUILD_PATH="$PWD/subrepos/OR-Tools/buildLinux"
export ORTOOLS_INSTALL_PATH="$PWD/subrepos/OR-Tools/install"
export ORTOOLS_DEPENDENCIES_INSTALL_PATH="${ORTOOLS_BUILD_PATH}/dependencies/install"
export ORTOOLS_TESTS_SRC_PATH="$PWD"
export ORTOOLS_TESTS_BUILD_PATH="$PWD/buildLinux"

export ANTARES_SRC_PATH="$PWD/src"
export ANTARES_BUILD_PATH="$PWD/src"

source $(dirname $0)/../utils.sh
