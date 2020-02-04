source $(dirname $0)/utils.sh

export ORTOOLSDEPDIR="C:/Dev/RTE/ortoolsDepInstall"
export SIRIUSDIR="C:/Dev/RTE/2019/SiriusAntaresV7"
export CPLEXDIR="C:/Program Files/IBM/ILOG/CPLEX_Studio127/cplex"

lookForLib "${SIRIUSDIR}" "Sirius lib" "build/Release/bib_solveur.dll"
lookForLib "${CPLEXDIR}" "Cplex lib" "/bin/x64_win64/cplex1270.dll"

grep -q "^\s*template <bool only_allow_zero_cost_column>" ortools/glop/initial_basis.*
res=$?

if [ $res -eq 0 ]
then
	sed -i "s/.*template <bool only_allow_zero_cost_column>.*//g" ortools/glop/initial_basis.*

	sed -i "s/void CompleteTriangularBasis(ColIndex/void CompleteTriangularBasis(bool only_allow_zero_cost_column, ColIndex/g" ortools/glop/initial_basis.h
	sed -i "s/void GetMarosBasis(ColIndex/void GetMarosBasis(bool only_allow_zero_cost_column, ColIndex/g" ortools/glop/initial_basis.h

	sed -i "s/return GetMarosBasis<\(\w\+\)>(/return GetMarosBasis(\1, /g" ortools/glop/initial_basis.cc
	sed -i "s/return CompleteTriangularBasis<\(\w\+\)>(/return CompleteTriangularBasis(\1, /g" ortools/glop/initial_basis.cc

	sed -i "s/InitialBasis::CompleteTriangularBasis(ColIndex/InitialBasis::CompleteTriangularBasis(bool only_allow_zero_cost_column, ColIndex/g" ortools/glop/initial_basis.cc
	sed -i "s/InitialBasis::GetMarosBasis(ColIndex/InitialBasis::GetMarosBasis(bool only_allow_zero_cost_column, ColIndex/g" ortools/glop/initial_basis.cc
fi

cmake --build build --config Release

cp ${ORTOOLSDEPDIR}/bin/zlib.dll build/examples/cpp/
cp "$CPLEXDIR/bin/x64_win64/cplex1270.dll" build/examples/cpp/
cp "$SIRIUSDIR/build/Release/bib_solveur.dll" build/examples/cpp/

cp ${ORTOOLSDEPDIR}/bin/zlib.dll build/
cp "$CPLEXDIR/bin/x64_win64/cplex1270.dll" build/
cp "$SIRIUSDIR/build/Release/bib_solveur.dll" build/

export PATH="$PATH:$(pwd)/build"

cmake --build build --config Release --target INSTALL
#cmake --build build --config Release --target RUN_TESTS
