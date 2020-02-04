#include "srs_api.h"

int main(int argc, char ** argv) {
	SRS_PROBLEM * srsProb = SRScreateprob();
	SRSfreeprob(srsProb);
	srsProb = SRScreateprob();
	
#define nbCols 2
#define nbRows 2
	
	{
		double obj[nbCols] = { 1.0, 2.0 };
		int colTypes[nbCols] = { SRS_CONTINUOUS_VAR, SRS_CONTINUOUS_VAR };
		double lb[nbCols] = { -1.0, -2.0 };
		double ub[nbCols] = { 1.0, 2.0 };
		char * colNames[nbCols] = { "X1", "x2" };

		double rhs[nbRows] = { 0.5, 0.5 };
		double range[nbRows] = { 0.0, 0.0 };
		char sense[nbRows] = { SRS_GREATER_THAN, SRS_LESSER_THAN };
		char * rowNames[nbRows] = { "c1", "C2" };

		int rowDebInds[2] = { 0, 2 };
		int nbCoefPerRow[2] = { 2, 2 };
		int colInds[4] = { 0, 1, 0, 1 };
		double coefs[4] = { 0.5, 1.0, 1.0, 0.5 };

		SRScreatecols(srsProb, nbCols, obj, colTypes, lb, ub, colNames);
		SRScreaterows(srsProb, nbRows, rhs, range, sense, rowNames);
		SRSsetcoefs(srsProb, rowDebInds, nbCoefPerRow, colInds, coefs);

		SRSoptimize(srsProb);

		double objVal = -1.0;
		int nbIter = -1;
		SRSgetobjval(srsProb, &objVal);
		SRSgetspxitercount(srsProb, &nbIter);
		printf("Objective value : %lf, nb iter %d\n", objVal, nbIter);

		// HOTSTART
		int rowIndexes[1] = {0};
		double newRhs[1] = {0.7};
		SRSchgrhs(srsProb, 1, rowIndexes, newRhs);
		SRSoptimize(srsProb);

		objVal = -1.0;
		nbIter = -1;
		SRSgetobjval(srsProb, &objVal);
		SRSgetspxitercount(srsProb, &nbIter);
		printf("Objective value : %lf, nb iter %d\n", objVal, nbIter);

		SRSfreeprob(srsProb);
	}

	// *** MIP ***
	srsProb = SRScreateprob();

	double obj[nbCols] = { 2.0, 1.0 };
	int colTypesMip[nbCols] = { SRS_INTEGER_VAR, SRS_INTEGER_VAR };
	double lbMip[nbCols] = { 0. , 0. };
	double ubMip[nbCols] = { 1. , 1. };
	char * colNames[nbCols] = { "X1", "x2" };

	double rhsMip[nbRows] = { 1., 0.5 };
	double range[nbRows] = { 0.0, 0.0 };
	char sense[nbRows] = { SRS_GREATER_THAN, SRS_LESSER_THAN };
	char * rowNames[nbRows] = { "c1", "C2" };

	int rowDebInds[2] = { 0, 2 };
	int nbCoefPerRow[2] = { 2, 2 };
	int colInds[4] = { 0, 1, 0, 1 };
	double coefs[4] = { 3., 1.0, 0.3, 3. };

	SRScreatecols(srsProb, nbCols, obj, colTypesMip, lbMip, ubMip, colNames);
	SRScreaterows(srsProb, nbRows, rhsMip, range, sense, rowNames);
	SRSsetcoefs(srsProb, rowDebInds, nbCoefPerRow, colInds, coefs);
	//SRSwritempsprob(srsProb->problem_mps, "problemMip.mps");

	SRSoptimize(srsProb);

	{
		double objVal = -1.0;
		int nbIter = -1;
		SRSgetobjval(srsProb, &objVal);
		SRSgetmipitercount(srsProb, &nbIter);
		printf("Objective value : %lf, nb iter mip %d\n", objVal, nbIter);
	}

	SRSfreeprob(srsProb);

	exit(0);

	// *** read MPS MIP ***
	{
		srsProb = SRScreateprob();
		SRSreadmpsprob(srsProb, "pb_topase_long_A_JEU_DE_DONNEES");
		//SRSreadmpsprob(srsProb, "Donnees_Probleme_Solveur.mps");

		SRSoptimize(srsProb);

		double objVal = -1.0;
		int nbIter = -1;
		SRSgetobjval(srsProb, &objVal);
		SRSgetmipitercount(srsProb, &nbIter);
		printf("Objective value : %lf, nb iter mip %d\n", objVal, nbIter);

		SRSfreeprob(srsProb);
	}
	return 0;
}