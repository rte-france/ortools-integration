source $(dirname $0)/config.sh

if [ "${ORTOOLS_SIRIUS_SWITCH}x" == "ONx" ]
then

	if [ ! -d "${SIRIUS_GIT_PATH}" ]; then
		git clone ${SIRIUS_REPO} -b ${SIRIUS_BRANCH} "${SIRIUS_GIT_PATH}"
	fi
	
	#configuring
	cmake \
		-G "${CHOSEN_COMPILER}" \
		-B ${SIRIUS_BUILD_DIR} \
		-S ${SIRIUS_SRC_PATH}

	#building and installing
	cmake --build ${SIRIUS_BUILD_DIR} --config Release --target install
fi
