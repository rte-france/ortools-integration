source $(dirname $0)/config.sh

#checking pathes for libs are correct
if [ "${ORTOOLS_SIRIUS_SWITCH}x" == "ONx" ]; then
	lookForLib "${SIRIUS_INSTALL_DIR}" "Sirius lib" "lib/Release/bib_solveur.lib" ; fi
if [ "${ORTOOLS_CPLEX_SWITCH}x" == "ONx" ]; then
	lookForLib "${CPLEXDIR}" "Cplex lib" "/bin/x64_win64/cplex1270.dll" ; fi
if [ "${ORTOOLS_XPRESS_SWITCH}x" == "ONx" ]; then
	lookForLib "${XPRESSDIR}" "Xpress lib" "/lib/xprs.lib" ; fi

lookForLib "${ORTOOLS_INSTALL_PATH}" "Ortools lib" "/lib/ortools.lib"


cmake \
	-G "${CHOSEN_COMPILER}" \
	-S"${ANTARES_SRC_PATH}" \
	-B"${ANTARES_BUILD_PATH}" \
	-DORTOOLS_INSTALL_DIR="${ORTOOLS_INSTALL_PATH}" \
	-DLIBS_INSTALL_DIR="${ORTOOLS_DEPENDENCIES_INSTALL_PATH}"\
	-DUSE_SIRIUS=${ORTOOLS_SIRIUS_SWITCH} \
	-DSIRIUSDIR="${SIRIUS_INSTALL_DIR}" \
	-DUSE_CPLEX=${ORTOOLS_CPLEX_SWITCH} \
	-DCPLEXDIR="${CPLEXDIR}" \
	-DUSE_XPRESS=${ORTOOLS_XPRESS_SWITCH} \
	-DXPRESSDIR=${XPRESSDIR} \
	-DCMAKE_BUILD_TYPE=release
	
cmake --build "${ANTARES_BUILD_PATH}" --config Release --target antares-7.0-solver