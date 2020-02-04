function lookForLibTest() {
	path="$1" ; name="$2" ; specificFile="$3"
	if [ -f "${path}/${specificFile}" ]
	then
		return 0
	else
		return 1
	fi
}

function lookForLib() {
	path="$1" ; name="$2" ; specificFile="$3"
	if [ -f "${path}/${specificFile}" ]
	then
		echo "${name} found in ${path}"
	else
		echo "*** ERROR *** : ${name} were not found in ${path}, please edit this script" ; exit -1
	fi
}

function fixTemplateVisualStudioProblem(){
	grep -q "^\s*template <bool only_allow_zero_cost_column>" ${ORTOOLS_SRC_PATH}/ortools/glop/initial_basis.*
	res=$?

	if [ $res -eq 0 ]
	then
		sed -i "s/.*template <bool only_allow_zero_cost_column>.*//g" ${ORTOOLS_SRC_PATH}/ortools/glop/initial_basis.*

		sed -i "s/void CompleteTriangularBasis(ColIndex/void CompleteTriangularBasis(bool only_allow_zero_cost_column, ColIndex/g" ${ORTOOLS_SRC_PATH}/ortools/glop/initial_basis.h
		sed -i "s/void GetMarosBasis(ColIndex/void GetMarosBasis(bool only_allow_zero_cost_column, ColIndex/g" ${ORTOOLS_SRC_PATH}/ortools/glop/initial_basis.h

		sed -i "s/return GetMarosBasis<\(\w\+\)>(/return GetMarosBasis(\1, /g" ${ORTOOLS_SRC_PATH}/ortools/glop/initial_basis.cc
		sed -i "s/return CompleteTriangularBasis<\(\w\+\)>(/return CompleteTriangularBasis(\1, /g" ${ORTOOLS_SRC_PATH}/ortools/glop/initial_basis.cc

		sed -i "s/InitialBasis::CompleteTriangularBasis(ColIndex/InitialBasis::CompleteTriangularBasis(bool only_allow_zero_cost_column, ColIndex/g" ${ORTOOLS_SRC_PATH}/ortools/glop/initial_basis.cc
		sed -i "s/InitialBasis::GetMarosBasis(ColIndex/InitialBasis::GetMarosBasis(bool only_allow_zero_cost_column, ColIndex/g" ${ORTOOLS_SRC_PATH}/ortools/glop/initial_basis.cc
	fi
}