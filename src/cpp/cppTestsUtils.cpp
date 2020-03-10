#include "cppTestsUtils.h"

using operations_research::MPObjective;
using operations_research::MPVariable;

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

MPSolver * createLP1()
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
	std::vector<std::string> name = { "PROD_H", "PROD_B", "PROD_H", "PROD_B", "PROD_H", "PROD_B", "CONSO", "CONSO", "CONSO", "CONSO", "CONSO", "CONSO", "LCC_H", "LCC_B" };
	std::vector<double> cost = { 0, 0, 0, 0, 0, 0, 13000, 13000, 13000, 13000, 13000, 13000, 0.1, 0.1 };
	std::vector<double> lb = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
	std::vector<double> ub = { 1100, 900, 600, 0, 0, 0, 0, 0, 0, 480, 900, 0, 1011, 1011 };
	std::vector<double> coef1 = { 1, -1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1 , 0, 0 };
	std::vector<double> coef2 = { 0.166667, -0.166667, -0.0833336, 0, 0, 0, 0, 0, 0, 0.166667, -0.333334, 0, -0.5, 0.5 };

	MPObjective* const objective = solver->MutableObjective();
	
	auto c1 = solver->MakeRowConstraint(0., 0.);
	auto c2 = solver->MakeRowConstraint(-MPSolver::infinity(), -50.0013);
	
	std::vector<MPVariable *> variables;
	for (int idxVar = 0; idxVar < name.size(); ++idxVar)
	{
		auto v = solver->MakeNumVar(lb[idxVar], ub[idxVar], name[idxVar]);
		variables.push_back(v);
		objective->SetCoefficient(v, cost[idxVar]);
		c1->SetCoefficient(v, coef1[idxVar]);
		c2->SetCoefficient(v, coef2[idxVar]);
	}
	

	return solver;
}