#include "../../cppTestsUtils.h"

int main(int argc, char** argv){
	MPSolver * solver = createSimpleLP(5.0);
	
	// The test core
	CHECK(solver->SetSolverSpecificParametersAsString("MAXTIME 10"));
	CHECK_EQ(false, solver->SetSolverSpecificParametersAsString("MAXTIME 10 BADPARAM 2"));
	CHECK_EQ(false, solver->SetSolverSpecificParametersAsString("MAXTIME"));
	CHECK(solver->SetSolverSpecificParametersAsString("MAXTIME 10 MIPTOL 0.1"));
	
	solver->Solve();

	CHECK_EQ(5.0, solver->Objective().Value());
	delete solver;
	
	return 0;
}