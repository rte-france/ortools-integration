#include "ortools/linear_solver/linear_solver.h"

using operations_research::MPSolver;
using operations_research::MPObjective;

int main(int argc, char** argv){
	MPSolver * solver = new MPSolver("simple_lp_program", MPSolver::XPRESS_LINEAR_PROGRAMMING);
	auto x = solver->MakeNumVar(0., 5., "testVar");
	
	MPObjective* const objective = solver->MutableObjective();
	objective->SetCoefficient(x, 1.);
	objective->SetMaximization();
	objective->SetOffset(3.0);
	
	solver->Solve();

	double objValue_l = solver->Objective().Value();

	std::cout << "Objective = " << solver->Objective().Value() << std::endl;
	
	delete solver;
	
	return (objValue_l != 5.);
}