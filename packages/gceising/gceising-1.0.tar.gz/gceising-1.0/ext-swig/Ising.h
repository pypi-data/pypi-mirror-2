/*
 * Ising.h
 *
 *  Created on: Jun 2, 2009
 *      Author: Alwin Tsui,alwintsui@gmail.com
 *      Hamitonian for Ising model
 *      H=-j \sigma_<ij> s_i*s_j-B\sigma_i s_i
 */

#ifndef _Ising_H
#define _Ising_H

#include "Random.h"

#define TO32       4294967296.0  //2^32
//J=1
class Ising {
protected:
	double _dDeltaExp[5];//-8,-4,0,4,8
public:
	enum {
		AI_TEMPER = 0,
		AI_HAMI,
		AI_DELT_HAMI,
		AI_MAG,
		AI_DELT_MAG,
		AI_RANDOM,
		AI_EXP_DELT_HAMI,
		AI_NUM
	//the last one define the element number of this enum
	};//derived class can extend this enum
	double m_aArgIO[AI_NUM];

	unsigned int m_uDim0, m_uDim1, m_uN, m_uCurTrial;
	int m_initConf;
	char * m_pcStates;//< external point
	//m_uN:size of model,m_EN: the total number of energy levels
	double m_dBeta, m_dAlpha, m_dUn;//for Generalized canonical ensemble (m_dUn=U/N).
	unsigned long long m_ullCurMove;
	int m_EN, m_curHami, m_curMag, m_accepted;//< Dimension and size
	int m_lowEBound, m_highEBound;//[m_lowEBound, m_highEBound],for flat histogram:WL,Mul
	int m_deltaE, m_deltaMag;

	Random m_ran, m_ran2;//< random number generator

	Ising();
	virtual ~Ising();

	void InitParameters();
	void SetArg(int site, double df);
	double GetArg(int site);

	void SetConf(char * pcStates, int dim0, int dim1);
	void InitConf(int d);//d<0 ground state;d==0 random state;d>0 anti-ground state
	bool DumpConf(const char * fileName);
	bool LoadConf(const char * fileName);

	void Gauge();
	int Delt();
	void DeltS(unsigned int CTrial);//for Enumerating Conf.

	int * m_pE;//energy space
	bool SetEnergyRange(int *pData, int len);
	int E2i(int e);
	int I2e(int i);
	int En2e(double en);
	int M2i(int m);
	int I2m(int i);
	void WarmupToBound();
	int SetBound(double lb, double hb);//return range.
	bool ETraj2Hist(int * pData, unsigned int uLen, int* pData1, int hlen,
			int h0, int *pE0, int *pE1);//return histdata[],e0,e1,h0=0
	//========== NVT ===========//
	void SetTemperature(double T);
	void MetroplisTrial(int moves);//NVT
	//========== GE ===========//
	double * m_pdSE, *m_pdBE;//store generalized S(e) function versus Energy
	bool SetSefun(double * pdSE, int size);
	bool SetSeBefun(double * pdSE, double * pdBE, int size);
	bool SetGCESe();
	bool SetGCEBe();
	double GetGCEBe(double e);
	double GetGCESe(double e);
	bool DumpSe(const char * fileName, bool bBin = true);
	bool LoadSe(const char * fileName, bool bBin = true);
	bool DumpBe(const char * fileName, bool bBin = true);
	bool LoadBe(const char * fileName, bool bBin = true);
	bool DiffSe();
	bool IntegBe();

	void RunSe(int* pData, unsigned int samples, unsigned int stride);
	void RunSe(const char* fileName, unsigned int samples, unsigned int stride,
			int offset = 0);
	void RunSeBound(int* pData, unsigned int samples, unsigned int stride);
	void WolffClusterSE(int moves);
	void RunWolffSe(char* file, unsigned int samples, unsigned int stride);
	//input m_pdSE,Traj;output U,sigma,effN
	double EnsAvgSe2Se(int *pData, unsigned int uLen, unsigned int start,
			double *pdSE, int lE, int hE, int refE, double *o_pdAvgU,
			double *o_pdSigma, unsigned int * effN);
	double EnsAvgSe2NVT(int *pData, unsigned int uLen, unsigned int start,
			double beta, int lE, int hE, int refE, double *o_pdAvgU,
			double *o_pdSigma, unsigned int * effN);
	double EnsAvgSe2GCE(int *pData, unsigned int uLen, unsigned int start,
			double beta, double alpha, double U0, int lE, int hE, int refE,
			double *o_pdAvgU, double *o_pdSigma, unsigned int * effN);
	bool DosAvgSe2NVT(double beta, int lE, int hE, int refE,
			double *o_pdAvgU, double *o_pdAvgF, double *o_pdAvgC,
			double *o_pdAvgS);
	//bool CheckBelowAVGBound(int *pData, int lE, int hE, double frate);
	int GetRoundtimes(int *pData, unsigned int uLen, int lE, int hE,
			unsigned int *rN);//return rN: the total number of sweep between
	void MetroplisTrialSe(int moves);
	void MetroplisTrialSeBound(int moves);
	//========== GCE Metroplis===========//
	void MetroplisTrialGCE(int moves);
	//========== NVT Heat Bath===========//
	unsigned int m_auLocalFieldPro[5];//[-4,-2,0,2,4]
	void SetHeatBath(double T);
	void HeatBathTrial(int moves);//NVT
	//======== Wang-Landau ==========//
	double * m_pdLnGe;//ln(g[e])
	unsigned int *m_puGeN;//visited number of g[e]
	double m_dLnf, m_dLnfPrecision, m_dFlatRate;//percent
	//double dLowBound, dHighBound;

	void SetWL(double * pdLnGe, unsigned int *puGeN, int size,
			double lnfPrecision, double flatRate);
	void WLResetGeN();
	bool WLCheckBelowAVG();
	void WangLandauTrial(int moves);//Wand-Landau

	void WLResetGeNBound();
	bool WLCheckBelowAVGBound();
	void WangLandauTrialBound(int moves);
	//===========Wolff Cluster=======//
	int * m_pClusterStack;//<
	double m_dPadd;
	//	int downBonds, upBonds;
	void WolffCluster(int moves);//NVT

	int * m_pClusterSeq;//roll back if GCE cluster flipping refused.

	int m_csp;//the size of current cluster
	int m_segAccumCS;//accumulate size a part of cluster
	double m_dAccumCS;

	int m_GCEWFavgC;//the time of updating m_dGCEWFavgE.
	double m_dGCEWFavgE, m_dGCEWFsegAccumE;
	void ClusterDelt(unsigned int CTrial);
	void WolffClusterGCE(int moves);//GCE cluster flipping with acceptance rates.
	//======== Random walk in Energy space ==========//
	int m_curEindex;
	void RanWalkTrailEBound(int * pData, unsigned int samples,
			unsigned int stride);
};

#endif
