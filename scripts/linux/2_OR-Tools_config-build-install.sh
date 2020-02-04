source $(dirname $0)/config.sh

#checking pathes for libs are correct
if [ "${ORTOOLS_SIRIUS_SWITCH}x" == "ONx" ]; then
	lookForLib "${SIRIUS_INSTALL_DIR}" "Sirius lib" "lib/libbib_solveur.so" ; fi
if [ "${ORTOOLS_CPLEX_SWITCH}x" == "ONx" ]; then
	lookForLib "${CPLEXDIR}" "Cplex lib" "/bin/x64_win64/cplex1270.dll" ; fi
if [ "${ORTOOLS_XPRESS_SWITCH}x" == "ONx" ]; then
	lookForLib "${XPRESSDIR}" "Xpress lib" "/lib/xprs.lib" ; fi

if [ "${ORTOOLS_BUILD_DEPS}x" == "OFFx" ]
then
	lookForLibTest "${ORTOOLS_DEPENDENCIES_INSTALL_PATH}" "Ortools pre-build dependencies" "lib/libCbc.a"
	if [ $? -ne 0 ]; then
		mkdir -p "${ORTOOLS_DEPENDENCIES_INSTALL_PATH}"
		cd "${ORTOOLS_DEPENDENCIES_INSTALL_PATH}"
		unzip ../../../../../install.zip
		cd -
	fi
fi
echo "ORTOOLS_SRC_PATH : ${ORTOOLS_SRC_PATH}"
mkdir -p ${ORTOOLS_BUILD_PATH}
cd ${ORTOOLS_BUILD_PATH}
#configuring and building dependencies if needed
cmake \
	-G "${CHOSEN_COMPILER}" \
	-DBUILD_DEP_NB_PROC="$(nproc)" \
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
	-DBUILD_TESTING=${ORTOOLS_TESTING_SWITCH} \
	"${ORTOOLS_SRC_PATH}"

lookForLib "${ORTOOLS_DEPENDENCIES_INSTALL_PATH}" "Ortools pre-build dependencies" "lib/libCbc.a"

fixTemplateVisualStudioProblem

cmake --build ${ORTOOLS_BUILD_PATH} --config Release --target install -- -j $(nproc)

if [ "${ORTOOLS_TESTING_SWITCH}x" == "ONx" ]; then
	export PATH="$PATH:${ORTOOLS_DEPENDENCIES_INSTALL_PATH}/bin/:${CPLEXDIR}/bin/x64_win64/:${SIRIUS_INSTALL_DIR}/lib/Release/"

	cmake --build ${ORTOOLS_BUILD_PATH} --config Release
	cmake --build ${ORTOOLS_BUILD_PATH} --config Release --target RUN_TESTS
fi
