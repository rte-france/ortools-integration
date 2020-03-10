#include "../../cppTestsUtils.h"

int main(int argc, char** argv){
	MPSolver * solver = createLP1();
	
	solver->Solve();

	std::cout << "Obj : " << solver->Objective().Value() << std::endl;
	for (auto v : solver->variables())
	{
		std::cout 
			<< v->solution_value()
			<< ";" << v->basis_status()
			<< ";" << v->reduced_cost()
			<< std::endl;
	}
	CHECK_EQ(0.0, solver->Objective().Value());
	delete solver;
	
	return 0;
}