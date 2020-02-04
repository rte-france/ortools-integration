source $(dirname $0)/config.sh

#checking pathes for libs are correct
if [ "${ORTOOLS_SIRIUS_SWITCH}x" == "ONx" ]; then
	lookForLib "${SIRIUS_INSTALL_DIR}" "Sirius lib" "lib/Release/bib_solveur.lib" ; fi
if [ "${ORTOOLS_CPLEX_SWITCH}x" == "ONx" ]; then
	lookForLib "${CPLEXDIR}" "Cplex lib" "/bin/x64_win64/cplex1270.dll" ; fi
if [ "${ORTOOLS_XPRESS_SWITCH}x" == "ONx" ]; then
	lookForLib "${XPRESSDIR}" "Xpress lib" "/lib/xprs.lib" ; fi
	
if [ ! -d "${ORTOOLS_GIT_PATH}" ]; then
	git clone ${ORTOOLS_REPO} -b ${ORTOOLS_BRANCH} "${ORTOOLS_GIT_PATH}"
fi

if [ "${ORTOOLS_BUILD_DEPS}x" == "OFFx" ]
then
	lookForLibTest "${ORTOOLS_DEPENDENCIES_INSTALL_PATH}" "Ortools pre-build dependencies" "lib/Cbc.lib"
	if [ $? -ne 0 ]; then
		mkdir -p "${ORTOOLS_DEPENDENCIES_INSTALL_PATH}"
		cd "${ORTOOLS_DEPENDENCIES_INSTALL_PATH}"
		unzip ../../../../../install.zip
		cd -
	fi
fi

#configuring and building dependencies if needed
cmake \
	-G "${CHOSEN_COMPILER}" \
	-S"${ORTOOLS_SRC_PATH}" \
	-B"${ORTOOLS_BUILD_PATH}" \
	-DBUILD_DEP_MP=${ORTOOLS_BUILD_DEPENDENCIES_MP} \
	-DBUILD_DEPS=${ORTOOLS_BUILD_DEPS} \
	-DCMAKE_INSTALL_PREFIX="${ORTOOLS_INSTALL_PATH}" \
	-DUSE_SIRIUS=${ORTOOLS_SIRIUS_SWITCH} \
	-DSIRIUSDIR="${SIRIUS_INSTALL_DIR}" \
	-DUSE_CPLEX=${ORTOOLS_CPLEX_SWITCH} \
	-DCPLEXDIR="${CPLEXDIR}" \
	-DUSE_XPRESS=${ORTOOLS_XPRESS_SWITCH} \
	-DXPRESSDIR=${XPRESSDIR} \
	-DBUILD_PYTHON=${ORTOOLS_PYTHON_SWITCH} \
	-DBUILD_TESTING=${ORTOOLS_TESTING_SWITCH}

lookForLib "${ORTOOLS_DEPENDENCIES_INSTALL_PATH}" "Ortools pre-build dependencies" "lib/Cbc.lib"

fixTemplateVisualStudioProblem

cmake --build ${ORTOOLS_BUILD_PATH} --config Release --target install

if [ "${ORTOOLS_TESTING_SWITCH}x" == "ONx" ]; then
	export PATH="$PATH:${ORTOOLS_DEPENDENCIES_INSTALL_PATH}/bin/:${CPLEXDIR}/bin/x64_win64/:${SIRIUS_INSTALL_DIR}/lib/Release/"

	cmake --build ${ORTOOLS_BUILD_PATH} --config Release
	cmake --build ${ORTOOLS_BUILD_PATH} --config Release --target run_tests
fi
