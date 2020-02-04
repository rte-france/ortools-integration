#include "../../cppTestsUtils.h"

int main(int argc, char** argv){
	MPSolver * solver = createSimpleLP(5.0);
		
	solver->Solve();
	
	CHECK_EQ(5.0, solver->Objective().Value());
	{
		MPSolver * solver = createSimpleLP(4.0);
		
		solver->Solve();
		
		CHECK_EQ(4.0, solver->Objective().Value());
		delete solver;
	}
	CHECK_EQ(5.0, solver->Objective().Value());

	delete solver;
	
	return 0;
}