#include "../../cppTestsUtils.h"

int main(int argc, char** argv){
	MPSolver * solver = createSimpleLP(5.0);
	
	solver->set_time_limit(1000);
	solver->Solve();

	CHECK_EQ(5.0, solver->Objective().Value());
	delete solver;
	
	return 0;
}