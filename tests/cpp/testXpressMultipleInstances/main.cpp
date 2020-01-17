#include "ortools/linear_solver/linear_solver.h"

using operations_research::MPSolver;
using operations_research::MPObjective;

int main(int argc, char** argv){
	double objValue_l = 0.;
	{
		MPSolver * solver = new MPSolver("simple_lp_program", MPSolver::XPRESS_LINEAR_PROGRAMMING);
		auto x = solver->MakeNumVar(0., 5., "testVar");
		
		MPObjective* const objective = solver->MutableObjective();
		objective->SetCoefficient(x, 1.);
		objective->SetMaximization();
		
		solver->Solve();
		
		objValue_l += solver->Objective().Value();

		std::cout << "Objective = " << solver->Objective().Value() << std::endl;
		
		{
			MPSolver * solver = new MPSolver("simple_lp_program", MPSolver::XPRESS_LINEAR_PROGRAMMING);
			VLOG(1) << "testVlog" << std::endl;
			auto x = solver->MakeNumVar(0., 5., "testVar");
			
			MPObjective* const objective = solver->MutableObjective();
			objective->SetCoefficient(x, 1.);
			objective->SetMaximization();
			
			solver->Solve();
			
			objValue_l += solver->Objective().Value();

			std::cout << "Objective = " << solver->Objective().Value() << std::endl;
		
			delete solver;
		}
	
		delete solver;
	}
	
	return (objValue_l != 10.);
}