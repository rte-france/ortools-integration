#include "cppTestsUtils.h"

using operations_research::MPObjective;

MPSolver * createSimpleLP(double targetObjectiveValue)
{
	MPSolver * solver = 
#ifdef USE_XPRESS
	new MPSolver("simple_lp_program", MPSolver::XPRESS_LINEAR_PROGRAMMING);
#else
#ifdef USE_SIRIUS
	new MPSolver("simple_lp_program", MPSolver::SIRIUS_LINEAR_PROGRAMMING);
#else
	new MPSolver("simple_lp_program", MPSolver::CBC_MIXED_INTEGER_PROGRAMMING);
#endif
#endif
	auto x = solver->MakeNumVar(targetObjectiveValue, targetObjectiveValue + 10., "testVar");
	
	MPObjective* const objective = solver->MutableObjective();
	objective->SetCoefficient(x, 1.);

	auto c = solver->MakeRowConstraint(0., 100.);
	c->SetCoefficient(x,1.);
	
	return solver;
}