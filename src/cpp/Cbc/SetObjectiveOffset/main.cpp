#include "../../cppTestsUtils.h"

using operations_research::MPObjective;

int main(int argc, char** argv){
	MPSolver * solver = createSimpleLP(5.0);
	MPObjective* const objective = solver->MutableObjective();
	objective->SetOffset(3.0);
	
	solver->Solve();

	CHECK_EQ(8.0, solver->Objective().Value());
	delete solver;
	
	return 0;
}