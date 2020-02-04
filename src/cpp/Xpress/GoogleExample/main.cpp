#include "ortools/linear_solver/linear_solver.h"

using namespace std;
using namespace operations_research;

int main(int argc, char **argv)
{
	// Create the linear solver with the GLOP backend.
	MPSolver solver("simple_lp_program", MPSolver::XPRESS_LINEAR_PROGRAMMING);

	// Create the variables x and y.
	MPVariable *const x = solver.MakeNumVar(0.0, 1, "x");
	MPVariable *const y = solver.MakeNumVar(0.0, 2, "y");

	CHECK_EQ(2, solver.NumVariables());

	// Create a linear constraint, 0 <= x + y <= 2.
	MPConstraint *const ct = solver.MakeRowConstraint(0.0, 2.0, "ct");
	ct->SetCoefficient(x, 1);
	ct->SetCoefficient(y, 1);

	CHECK_EQ(1, solver.NumConstraints());

	// Create the objective function, 3 * x + y.
	MPObjective *const objective = solver.MutableObjective();
	objective->SetCoefficient(x, 3);
	objective->SetCoefficient(y, 1);
	objective->SetMaximization();

	solver.Solve();

	CHECK_EQ(4.0, objective->Value());
	CHECK_EQ(1.0, x->solution_value());
	CHECK_EQ(1.0, y->solution_value());
	
	return 0;
}