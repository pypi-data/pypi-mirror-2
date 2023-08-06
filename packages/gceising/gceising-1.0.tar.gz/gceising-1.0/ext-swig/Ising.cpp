/*
 * Ising.cpp
 *
 *  Created on: May 20, 2009
 *      Author: Alwin Tsui,alwintsui@gmail.com
 *   0---N-->
 * (0,0)----y,dim1--->
 *   |
 *   |
 *   x,
 *  dim0
 *   |
 *   v
 * Energy Levels(N+1):
 * -2N,,-2N-8,2N-12,..,2N-8,2N
 * for(int n=0;n<=N;n++)
 * 		E[n]= 4*n-2*N;
 * hisE[(2N + hami) / 4)]++
 * M:lev=N+1
 * -N,-N-2,...,0,2,...,N-2,N
 */
#include "Ising.h"
#include "nvector.h"
#include <iostream> //< for cout
#include <cmath>

using namespace std;

Ising::Ising() {
}

Ising::~Ising() {
}
void Ising::InitParameters() {
	m_ullCurMove = 0;
	m_pcStates = NULL;
	for (int i = 0; i < AI_NUM; i++)
		m_aArgIO[i] = 0;
	m_aArgIO[AI_TEMPER] = 1;
}
void Ising::SetConf(char * pcStates, int dim0, int dim1) {
	m_uDim0 = dim0;
	m_uDim1 = dim1;
	m_uN = m_uDim0 * m_uDim1;
	m_EN = m_uN + 1;
	/*  m_EN/4 ->min non-zero Delta E=4
	 *2*m_uN+ 1 +2*m_uN                 m_uDim0,m_uDim0:both even
	 *2*m_uN+ 1 +2*m_uN-2*both_odd_dim  m_uDim0,m_uDim0:both odd
	 *2*m_uN+ 1 +2*m_uN-2*even_dim      m_uDim0,m_uDim0:one of them odd
	 */
	m_lowEBound = -2 * m_uN;
	m_highEBound = 2 * m_uN;
	m_pcStates = pcStates;
}
void Ising::InitConf(int d) {
	//m_ran.Srand(123487);
	if (m_pcStates == NULL) {
		cout << "#Error: Set configures first by \'SetConf()\'" << endl;
		return;
	}
	m_initConf = d;
	if (d == 0) {
		for (unsigned int n = 0; n < m_uN; n++) {
			m_pcStates[n] = (m_ran.Real() > 0.5) ? 1 : -1;
		}
	} else if (d > 0) {//TODO:NO guaranty to get anti-ground state:"four-colour problem"
		int m, k = 1;
		for (unsigned int x = 0; x < m_uDim0; x++) {
			k *= -1;
			m = k;
			for (unsigned int y = 0; y < m_uDim1; y++) {
				m_pcStates[x * m_uDim1 + y] = m;
				m *= -1;
			}
		}
	} else {
		for (unsigned int n = 0; n < m_uN; n++) {
			m_pcStates[n] = -1;
		}
	}
}

bool Ising::DumpConf(const char * fileName) {
	if (m_pcStates == NULL || fileName == NULL)
		return false;
	nvector<char> nvec(m_pcStates, m_uN);
	nvec.dump_bin(fileName);
	return true;
}
bool Ising::LoadConf(const char * fileName) {
	if (m_pcStates == NULL || fileName == NULL)
		return false;
	nvector<char> nvec(m_pcStates, m_uN);
	return nvec.load_bin(fileName, m_uN, 0, false) != -1;//set last conf
}
bool Ising::DumpSe(const char * fileName, bool bBin) {
	if (m_pdSE == NULL || fileName == NULL)
		return false;
	nvector<double> nvec(m_pdSE, m_EN);
	if (bBin) {
		nvec.dump_bin(fileName);
	} else {
		nvec.dump(fileName);
	}
	return true;
}

bool Ising::LoadSe(const char * fileName, bool bBin) {
	if (m_pdSE == NULL || fileName == NULL)
		return false;
	nvector<double> nvec(m_pdSE, m_EN);
	int res = 0;
	if (bBin) {
		res = nvec.load_bin(fileName, m_EN, 0, false);
	} else {
		res = nvec.load(fileName, 0, false);//col=0
	}
	return res != -1;
}

bool Ising::DumpBe(const char * fileName, bool bBin) {
	if (m_pdBE == NULL || fileName == NULL)
		return false;
	nvector<double> nvec(m_pdBE, m_EN);
	if (bBin) {
		nvec.dump_bin(fileName);
	} else {
		nvec.dump(fileName);
	}
	return true;
}
bool Ising::LoadBe(const char * fileName, bool bBin) {
	if (m_pdBE == NULL || fileName == NULL)
		return false;
	nvector<double> nvec(m_pdBE, m_EN);
	int res = 0;
	if (bBin) {
		res = nvec.load_bin(fileName, m_EN, 0, false);
	} else {
		res = nvec.load(fileName, 0, false);//col=0
	}
	return res != -1;
}
bool Ising::DiffSe() {
	if (m_pdBE == NULL || m_pdSE == NULL)
		return false;
	nvector<double> nvec(m_pdSE, m_EN);
	bool res = nvec.diff(m_pdBE, m_EN);
	if (res) {
		for (unsigned int i = 0; i < nvec.m_uLen; i++)
			m_pdBE[i] /= 4.0;
	}
	return res;
}
bool Ising::IntegBe() {
	if (m_pdBE == NULL || m_pdSE == NULL)
		return false;
	nvector<double> nvec(m_pdBE, m_EN);
	bool res = nvec.integral(m_pdSE, m_EN);
	if (res) {
		for (unsigned int i = 0; i < nvec.m_uLen; i++)
			m_pdSE[i] *= 4.0;
	}
	return res;
}

int Ising::En2e(double en) {
	int Eni = int((2 + en) * m_uN / 4);
	return I2e(Eni);
}

int Ising::E2i(int e) {
	return (2 * m_uN + e) / 4;
}
int Ising::I2e(int i) {
	return 4 * i - int(2 * m_uN);//E(n)
}
int Ising::M2i(int m) {
	return (m_uN + m) / 2;
}
int Ising::I2m(int i) {
	return 2 * i - m_uN;
}
//========== FAFE ===========//
bool Ising::SetSefun(double * pdSE, int size) {
	if (m_EN > size) {
		cerr << "#Error: Size too small:" << size << endl;
		return false;
	} else {
		m_pdSE = pdSE;
		return true;
	}
}
bool Ising::SetSeBefun(double * pdSE, double * pdBE, int size) {
	if (m_EN > size) {
		cerr << "#Error: Size too small:" << size << endl;
		return false;
	} else {
		m_pdSE = pdSE;
		m_pdBE = pdBE;
		return true;
	}
}
double Ising::GetGCEBe(double e) {
	return m_dBeta + m_dAlpha * (e - m_dUn * m_uN) / (m_uN);
}
double Ising::GetGCESe(double e) {
	return m_dBeta * e + m_dAlpha * (e - m_dUn * m_uN) * (e - m_dUn * m_uN)
			/ (2 * m_uN);
}
bool Ising::SetGCESe() {
	if (m_EN < 1 || m_pdSE == NULL)
		return false;

	for (int n = 0; n < m_EN; n++) {
		m_pdSE[n] = GetGCESe(I2e(n));
	}
	return true;
}
bool Ising::SetGCEBe() {
	if (m_EN < 1 || m_pdBE == NULL)
		return false;
	for (int n = 0; n < m_EN; n++) {
		m_pdBE[n] = GetGCEBe(I2e(n));
	}
	return true;
}

void Ising::RunSe(const char* file, unsigned int samples, unsigned int stride,
		int offset) {
	double dDeltE_old2new;
	std::ofstream ofile;
	if (offset == -1) {
		ofile.open(file, ios::out | ios::app);
	} else {
		ofile.open(file, ios::out);
	}
	unsigned int Stride = m_uN * stride;
	int ei0, ei1;
	for (unsigned int s = 0; s < samples; s++) {
		for (unsigned int CurStep = 0; CurStep < Stride; CurStep++) {
			Delt();
			ei0 = (2 * m_uN + m_curHami) / 4;
			ei1 = (2 * m_uN + m_curHami + m_deltaE) / 4;
			dDeltE_old2new = m_pdSE[ei0] - m_pdSE[ei1];
			if (m_ran.Real() < exp(dDeltE_old2new)) {
				m_pcStates[m_uCurTrial] *= -1;//< accepted
				m_curHami += m_deltaE;
				m_curMag += m_deltaMag;
			} //else refused
		}
		ofile << m_curHami << endl;
	}
	ofile.close();
	m_ullCurMove += Stride * samples;
	m_aArgIO[AI_HAMI] = m_curHami;
}
void Ising::RunSe(int* etr, unsigned int samples, unsigned int stride) {
	double dDeltE_old2new;
	unsigned int Stride = m_uN * stride;
	int ei0, ei1;
	for (unsigned int s = 0; s < samples; s++) {
		for (unsigned int CurStep = 0; CurStep < Stride; CurStep++) {
			Delt();
			ei0 = (2 * m_uN + m_curHami) / 4;
			ei1 = (2 * m_uN + m_curHami + m_deltaE) / 4;
			dDeltE_old2new = m_pdSE[ei0] - m_pdSE[ei1];

			if (m_ran.Real() < exp(dDeltE_old2new)) {
				m_pcStates[m_uCurTrial] *= -1;//< accepted
				m_curHami += m_deltaE;
				m_curMag += m_deltaMag;
			} //else refused
		}
		etr[s] = m_curHami;
	}
	m_ullCurMove += Stride * samples;
	m_aArgIO[AI_HAMI] = m_curHami;
	m_aArgIO[AI_MAG] = m_curMag;
}
void Ising::RunWolffSe(char* file, unsigned int samples, unsigned int stride) {
	std::ofstream ofile(file);
	for (unsigned int s = 0; s < samples; s++) {
		WolffClusterSE(stride);
		ofile << m_curHami << '\t' << m_curMag << endl;
	}
	ofile.close();
	m_ullCurMove += stride * samples;
	m_aArgIO[AI_HAMI] = m_curHami;
	m_aArgIO[AI_MAG] = m_curMag;
}
/*
 int Ising::GetRoundtimes(int *pData, unsigned int uLen, int lE, int hE) {
 int eE = (lE + 2 * m_uN) / 4;//0,0,0,0,1
 lE = 4 * eE - 2 * m_uN;
 eE = (hE + 2 * m_uN) / 4;
 hE = 4 * eE - 2 * m_uN;
 int ri = 0, i = 0, cE = 0;
 while (i < uLen) {
 if (pData[i] <= lE) {
 cE = hE;
 ri++;
 break;
 } else if (pData[i] >= hE) {
 cE = lE;
 ri++;
 break;
 }
 i++;
 }
 if (ri == 0) {
 return ri;
 } else {
 while (i < uLen) {
 if (pData[i] == cE) {
 ri++;
 cE = (cE == lE) ? hE : lE;//exchange
 }
 i++;
 }
 }
 return ri;
 }
 */
int Ising::GetRoundtimes(int *pData, unsigned int uLen, int lE, int hE,
		unsigned int *rN) {
	int ri = 0;
	unsigned int i = 0;
	*rN = 0;
	while (i < uLen) {
		if (pData[i] <= lE) {
			while (pData[i] < hE) {
				if (pData[i] >= lE)
					(*rN)++;
				i++;
				if (i == uLen)
					goto end;
			}//the first <=lE found
			ri++;
		} else if (pData[i] >= hE) {
			while (pData[i] > lE) {
				if (pData[i] <= hE)
					(*rN)++;
				i++;
				if (i == uLen)
					goto end;
			}//the first >=hE found
			ri++;
		} else {
			i++;//skip
		}
	}
	end: return ri;
}
/*
 int Ising::GetRoundtimes(int *pData, unsigned int uLen, int lE, int hE) {
 int ri = 0, i = 0;
 //from l -> h
 while (i < uLen) {
 while (pData[i] > lE) {
 i++;
 if (i == uLen)
 goto end;
 }
 ri++;
 while (pData[i] < hE) {
 i++;
 if (i == uLen)
 goto end;
 }
 ri++;
 }
 end: return ri;
 }
 */
void Ising::RunSeBound(int* etr, unsigned int samples, unsigned int stride) {
	double dDeltE_old2new;
	unsigned int Stride = m_uN * stride;
	int ei0, ei1;
	unsigned int CurStep;
	for (unsigned int s = 0; s < samples; s++) {
		CurStep = 0;
		while (CurStep < Stride) {
			Delt();
			if ((m_curHami + m_deltaE) < m_lowEBound || (m_curHami + m_deltaE)
					> m_highEBound)
				continue;
			ei0 = (2 * m_uN + m_curHami) / 4;
			ei1 = (2 * m_uN + m_curHami + m_deltaE) / 4;
			dDeltE_old2new = m_pdSE[ei0] - m_pdSE[ei1];

			if (m_ran.Real() < exp(dDeltE_old2new)) {
				m_pcStates[m_uCurTrial] *= -1;//< accepted
				m_curHami += m_deltaE;
				m_curMag += m_deltaMag;
			} //else refused
			CurStep += 1;
		}
		etr[s] = m_curHami;
	}
	m_ullCurMove += Stride * samples;
	m_aArgIO[AI_HAMI] = m_curHami;
	m_aArgIO[AI_MAG] = m_curMag;
}
void Ising::MetroplisTrialSe(int moves) {
	double dDeltE_old2new;
	for (int CurStep = 0; CurStep < moves; CurStep++) {
		Delt();
		dDeltE_old2new = m_pdSE[E2i(m_curHami)] - m_pdSE[E2i(m_curHami
				+ m_deltaE)];
		if (m_ran.Real() < exp(dDeltE_old2new)) {
			m_pcStates[m_uCurTrial] *= -1;//< accepted
			m_curHami += m_deltaE;
			m_curMag += m_deltaMag;
		} //else refused
	}
	m_aArgIO[AI_HAMI] = m_curHami;
	m_aArgIO[AI_MAG] = m_curMag;
}
void Ising::MetroplisTrialSeBound(int moves)//[m_lowEBound, m_highEBound]
{
	int CurStep = 0;
	double dDeltE_old2new;
	int E1, E2;
	while (CurStep < moves) {
		Delt();//Assume m_lowEBound<=m_curHami<=m_highEBound
		if ((m_curHami + m_deltaE) < m_lowEBound || (m_curHami + m_deltaE)
				> m_highEBound)
			continue;
		//if (m_deltaE > 0) {
		E1 = (2 * m_uN + m_curHami) / 4;
		E2 = (2 * m_uN + m_curHami + m_deltaE) / 4;

		dDeltE_old2new = m_pdSE[E1] - m_pdSE[E2];
		if (m_ran.Real() < exp(dDeltE_old2new)) {
			m_pcStates[m_uCurTrial] *= -1;//< accepted
			m_curHami += m_deltaE;
			m_curMag += m_deltaMag;
		} //else refused
		/*
		 } else {
		 m_pcStates[m_uCurTrial] *= -1;//< accepted
		 m_curHami += m_deltaE;
		 m_curMag += m_deltaMag;
		 }*/
		m_ullCurMove++;
		CurStep += 1;
	}
	m_aArgIO[AI_HAMI] = m_curHami;
	m_aArgIO[AI_MAG] = m_curMag;
}
double Ising::EnsAvgSe2Se(int *pData, unsigned int uLen, unsigned int start,
		double *Se_tar, int lE, int hE, int refE, double *o_pdAvgU,
		double *o_pdSigma, unsigned int * effN) {

	int *data_E = pData + start;
	unsigned int N = uLen - start;

	double res_ze = 0;
	double res_ze2 = 0;
	double res_z = 0;
	double res_z2 = 0;
	double e_t = 0;

	if (lE < -2 * int(m_uN))
		lE = -2 * m_uN;
	if (hE > 2 * int(m_uN))
		hE = 2 * m_uN;

	int ei = E2i(refE);
	double ref = m_pdSE[ei] - Se_tar[ei];
	*effN = 0;
	//cout << ei << '\t' << lE << '\t' << hE << '\t' << ref << endl;
	for (unsigned int n = 0; n < N; n++) {
		if (data_E[n] < lE || data_E[n] > hE)
			continue;
		ei = E2i(data_E[n]);
		//cout << data_E[n] / double(m_uN) << '\t' << m_pdSE[ei] - Se_tar[ei] - ref	<< '\t' << exp(m_pdSE[ei] - Se_tar[ei] - ref) << endl;
		e_t = exp(m_pdSE[ei] - Se_tar[ei] - ref);
		if (e_t == HUGE_VAL)
			continue;
		(*effN)++;
		res_ze += e_t * data_E[n];
		res_ze2 += e_t * data_E[n] * data_E[n];
		res_z += e_t;
		res_z2 += e_t * e_t;
	}

	*o_pdAvgU = res_ze / res_z;
	*o_pdSigma = sqrt(res_ze2 / res_z - (res_ze / res_z) * (res_ze / res_z));
	return (res_z * res_z) / res_z2;//B 0/0~inf
}
bool Ising::DosAvgSe2NVT(double beta, int lE, int hE, int refE,
		double *o_pdAvgU, double *o_pdAvgF, double *o_pdAvgC, double *o_pdAvgS) {
	if (m_pE == NULL || m_pdSE == NULL)
		return false;

	double res_ze = 0;
	double res_ze2 = 0;
	double res_z = 0;
	double res_z2 = 0;
	double e_t = 0;

	if (lE < -2 * int(m_uN))
		lE = -2 * m_uN;
	if (hE > 2 * int(m_uN))
		hE = 2 * m_uN;

	int ei = E2i(refE);
	double ref = m_pdSE[ei] - beta * refE;

	for (int n = 0; n < m_EN; n++) {
		if (n == 1 || n == m_EN - 2 || m_pE[n] < lE || m_pE[n] > hE)
			continue;//skip the null energy
		ei = E2i(m_pE[n]);
		e_t = exp(m_pdSE[ei] - beta * m_pE[n] - ref);
		if (e_t == HUGE_VAL)
			continue;
		res_ze += e_t * m_pE[n];
		res_ze2 += e_t * m_pE[n] * m_pE[n];
		res_z += e_t;
		res_z2 += e_t * e_t;
	}
	*o_pdAvgU = res_ze / res_z;
	*o_pdAvgF = -(log(res_z) + ref) / beta;
	*o_pdAvgC = (res_ze2 / res_z - (*o_pdAvgU) * (*o_pdAvgU)) * beta * beta;
	*o_pdAvgS = ((*o_pdAvgU) - (*o_pdAvgF)) * beta;
	return true;
}

double Ising::EnsAvgSe2NVT(int *pData, unsigned int uLen, unsigned int start,
		double beta, int lE, int hE, int refE, double *o_pdAvgU,
		double *o_pdSigma, unsigned int * effN) {

	int *data_E = pData + start;
	unsigned int N = uLen - start;

	double res_ze = 0;
	double res_ze2 = 0;
	double res_z = 0;
	double res_z2 = 0;
	double e_t = 0;

	if (lE < -2 * int(m_uN))
		lE = -2 * m_uN;
	if (hE > 2 * int(m_uN))
		hE = 2 * m_uN;

	int ei = E2i(refE);
	double ref = m_pdSE[ei] - beta * refE;
	*effN = 0;
	//cout << ei << '\t' << lE << '\t' << hE << '\t' << ref << endl;
	for (unsigned int n = 0; n < N; n++) {
		if (data_E[n] < lE || data_E[n] > hE)
			continue;
		ei = E2i(data_E[n]);
		//cout << m_pdSE[ei] - beta * data_E[n] << ':' << ref << ' ';
		e_t = exp(m_pdSE[ei] - beta * data_E[n] - ref);
		if (e_t == HUGE_VAL)
			continue;
		(*effN)++;
		res_ze += e_t * data_E[n];
		res_ze2 += e_t * data_E[n] * data_E[n];
		res_z += e_t;
		res_z2 += e_t * e_t;
	}

	*o_pdAvgU = res_ze / res_z;
	*o_pdSigma = sqrt(res_ze2 / res_z - (res_ze / res_z) * (res_ze / res_z));
	return (res_z * res_z) / res_z2;//B 0/0~inf
}
double Ising::EnsAvgSe2GCE(int *pData, unsigned int uLen, unsigned int start,
		double beta, double alpha, double U0, int lE, int hE, int refE,
		double *o_pdAvgU, double *o_pdSigma, unsigned int * effN) {
	int *data_E = pData + start;
	unsigned int N = uLen - start;

	double res_ze = 0;
	double res_ze2 = 0;
	double res_z = 0;
	double res_z2 = 0;
	double e_t = 0;

	if (lE < -2 * int(m_uN))
		lE = -2 * m_uN;
	if (hE > 2 * int(m_uN))
		hE = 2 * m_uN;

	int ei = E2i(refE);
	double ref = m_pdSE[ei] - (beta * refE + alpha * (refE - U0) * (refE - U0)
			/ 2.0 / m_uN);
	*effN = 0;
	//cout << ei << '\t' << lE / double(m_uN) << '\t' << hE / double(m_uN) << '\t'<< U0 / m_uN << '\t' << ref << endl;
	for (unsigned int n = 0; n < N; n++) {
		if (data_E[n] > hE || data_E[n] < lE)
			continue;
		ei = E2i(data_E[n]);
		//cout << m_pdSE[ei] - (beta * data_E[n] + alpha * (data_E[n] - U0)* (data_E[n] - U0) / 2.0 / m_uN) - ref << ' ';
		e_t = exp(m_pdSE[ei] - (beta * data_E[n] + alpha * (data_E[n] - U0)
				* (data_E[n] - U0) / 2.0 / m_uN) - ref);
		if (e_t == HUGE_VAL)
			continue;
		(*effN)++;
		res_ze += e_t * data_E[n];
		res_ze2 += e_t * data_E[n] * data_E[n];
		res_z += e_t;
		res_z2 += e_t * e_t;
	}

	*o_pdAvgU = res_ze / res_z;
	*o_pdSigma = sqrt(res_ze2 / res_z - (res_ze / res_z) * (res_ze / res_z));
	return (res_z * res_z) / res_z2;//B 0/0~inf
}
void Ising::SetArg(int site, double df) {
	if (site >= 0 && site < AI_NUM)
		m_aArgIO[site] = df;
}
double Ising::GetArg(int site) {
	if (site >= 0 && site < AI_NUM)
		return m_aArgIO[site];
	else {
		cout << "#Boundary error:" << site << endl;
		return 0;
	}
}

void Ising::Gauge() {
	m_curHami = 0;
	m_curMag = 0;
	unsigned int neib;
	for (unsigned int n = 0; n < m_uN; n++) {
		neib = n + 1;//right
		if (neib % m_uDim1 == 0)
			neib -= m_uDim1;
		m_curHami += m_pcStates[n] * m_pcStates[neib];

		neib = n + m_uDim1;//down
		if (neib >= m_uN)
			neib -= m_uN;
		m_curHami += m_pcStates[n] * m_pcStates[neib];
		m_curMag += m_pcStates[n];
	}
	m_curHami *= -1;
	m_aArgIO[AI_HAMI] = m_curHami;
	m_aArgIO[AI_MAG] = m_curMag;
}

int Ising::Delt() {
	m_deltaE = 0;
	m_uCurTrial = m_ran.Number(0, m_uN - 1);

	unsigned int neib = m_uCurTrial + 1;//right
	if (neib % m_uDim1 == 0)
		neib -= m_uDim1;
	m_deltaE += m_pcStates[neib];

	neib = m_uCurTrial - 1;//left
	if (m_uCurTrial % m_uDim1 == 0)
		neib += m_uDim1;
	m_deltaE += m_pcStates[neib];

	neib = m_uCurTrial - m_uDim1;//up
	if (m_uCurTrial < m_uDim1)
		neib += m_uN;
	m_deltaE += m_pcStates[neib];

	neib = m_uCurTrial + m_uDim1;//down
	if (neib >= m_uN)
		neib -= m_uN;
	m_deltaE += m_pcStates[neib];

	m_deltaE *= (m_pcStates[m_uCurTrial] << 1);
	m_deltaMag = -(m_pcStates[m_uCurTrial] << 1);
	m_aArgIO[AI_DELT_MAG] = m_deltaMag;
	m_aArgIO[AI_DELT_HAMI] = m_deltaE;
	return m_uCurTrial;
}

void Ising::DeltS(unsigned int CTrial) {
	m_deltaE = 0;

	unsigned int neib = CTrial + 1;//right
	if (neib % m_uDim1 == 0)
		neib -= m_uDim1;
	m_deltaE += m_pcStates[neib];

	neib = CTrial - 1;//left
	if (CTrial % m_uDim1 == 0)
		neib += m_uDim1;
	m_deltaE += m_pcStates[neib];

	neib = CTrial - m_uDim1;//up
	if (CTrial < m_uDim1)
		neib += m_uN;
	m_deltaE += m_pcStates[neib];

	neib = CTrial + m_uDim1;//down
	if (neib >= m_uN)
		neib -= m_uN;
	m_deltaE += m_pcStates[neib];

	m_deltaE *= (2 * m_pcStates[CTrial]);

	//	m_aArgIO[AI_DELT_HAMI] = m_deltaE;
}
void Ising::SetTemperature(double T) {
	m_aArgIO[AI_TEMPER] = T;//dE=2JS@s4,[-8,-4,0,4,8]
	for (int dE = -8; dE <= 8; dE += 4) {
		_dDeltaExp[2 + dE / 4] = exp(-1 * dE / m_aArgIO[AI_TEMPER]);//exp_de
	}
}
void Ising::MetroplisTrial(int moves) {
	int CurStep = 0;
	while (CurStep < moves) {
		Delt();
		//Accepted();//1 absolutely accepted,0 modestly accepted,-1  refused
		if (m_deltaE > 0) {
			m_aArgIO[AI_EXP_DELT_HAMI] = _dDeltaExp[2 + m_deltaE / 4];
			//exp(-1 * m_aArgIO[AI_DELT_HAMI]/ m_aArgIO[AI_TEMPER]);//time-consuming instead of hash index
			//m_aArgIO[AI_RANDOM] = m_ran.Real();//< random double value in the interval [0,1]
			if (m_ran.Real() < m_aArgIO[AI_EXP_DELT_HAMI]) {
				m_pcStates[m_uCurTrial] *= -1;//< accepted
				m_curHami += m_deltaE;
				m_curMag += m_deltaMag;
				m_accepted = 0;
			} else {//< refused
				m_accepted = -1;
			}
		} else {
			m_pcStates[m_uCurTrial] *= -1;//< accepted
			m_curHami += m_deltaE;
			m_curMag += m_deltaMag;
			m_accepted = 1;
		}
		m_ullCurMove++;
		CurStep++;
	}
	m_aArgIO[AI_HAMI] = m_curHami;
	m_aArgIO[AI_MAG] = m_curMag;
}
void Ising::MetroplisTrialGCE(int moves) {
	int CurStep = 0;
	double dDeltE_old2new;

	while (CurStep < moves) {
		Delt();
		//if (m_deltaE > 0) {
		//dDeltE_old2new = m_pdSE[m_EN - 1 + m_curHami] - m_pdSE[m_EN - 1 + m_curHami + m_deltaE];
		dDeltE_old2new = -m_deltaE * m_dBeta - m_dAlpha / m_uN * ((2
				* m_curHami + m_deltaE - 2 * m_dUn * m_uN) * m_deltaE) / 2.0;
		if (m_ran.Real() < exp(dDeltE_old2new)) {
			m_pcStates[m_uCurTrial] *= -1;//< accepted
			m_curHami += m_deltaE;
			m_curMag += m_deltaMag;

		} //else refused
		/*
		 } else {
		 m_pcStates[m_uCurTrial] *= -1;//< accepted
		 m_curHami += m_deltaE;
		 m_curMag += m_deltaMag;
		 }*/
		m_ullCurMove++;
		CurStep++;
	}
	m_aArgIO[AI_HAMI] = m_curHami;
	m_aArgIO[AI_MAG] = m_curMag;
}
void Ising::WolffCluster(int moves) {
	int CurStep = 0;
	int sp, oldspin, newspin;
	unsigned int neib;
	//int oldbonds = 0, newbonds = 0;
	while (CurStep < moves) {
		m_uCurTrial = m_ran.Number(0, m_uN - 1);
		m_pClusterStack[0] = m_uCurTrial;
		sp = 1;
		oldspin = m_pcStates[m_uCurTrial];
		newspin = -oldspin;
		m_pcStates[m_uCurTrial] = newspin;

		while (sp) {
			m_uCurTrial = m_pClusterStack[--sp];
			neib = m_uCurTrial + 1;//right
			if (neib % m_uDim1 == 0)
				neib -= m_uDim1;
			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					m_pcStates[neib] = newspin;
				}//oldbonds++;
			}
			neib = m_uCurTrial - 1;//left
			if (m_uCurTrial % m_uDim1 == 0)
				neib += m_uDim1;
			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					m_pcStates[neib] = newspin;
				}
			}
			neib = m_uCurTrial - m_uDim1;//up
			if (m_uCurTrial < m_uDim1)
				neib += m_uN;
			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					m_pcStates[neib] = newspin;
				}
			}

			neib = m_uCurTrial + m_uDim1;//down
			if (neib >= m_uN)
				neib -= m_uN;
			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {

					m_pClusterStack[sp++] = neib;
					m_pcStates[neib] = newspin;
				}

			}
		}
		m_ullCurMove++;
		CurStep++;
	}
}
void Ising::ClusterDelt(unsigned int CTrial) {
	//m_deltaE = 0;
	unsigned int neib = CTrial + 1;//right
	int nDE = 0;
	if (neib % m_uDim1 == 0)
		neib -= m_uDim1;
	nDE += m_pcStates[neib];

	neib = CTrial - 1;//left
	if (CTrial % m_uDim1 == 0)
		neib += m_uDim1;
	nDE += m_pcStates[neib];

	neib = CTrial - m_uDim1;//up
	if (CTrial < m_uDim1)
		neib += m_uN;
	nDE += m_pcStates[neib];

	neib = CTrial + m_uDim1;//down
	if (neib >= m_uN)
		neib -= m_uN;
	nDE += m_pcStates[neib];

	m_deltaE += nDE * (m_pcStates[CTrial] << 1);
	m_deltaMag += -(m_pcStates[CTrial] << 1);

	//m_aArgIO[AI_DELT_HAMI] = m_deltaE;
	//return m_deltaE;
}
void Ising::WolffClusterGCE(int moves) {
	//set first m_dBeta, m_dAlpha, m_dUn;
	int CurStep = 0;
	int sp = -1, oldspin, newspin;

	unsigned int neib;
	//int oldbonds = 0, newbonds = 0;
	while (CurStep < moves) {
		sp = 0;
		m_csp = 0;
		m_deltaE = 0;
		m_deltaMag = 0;
		m_uCurTrial = m_ran.Number(0, m_uN - 1);
		m_pClusterStack[sp++] = m_uCurTrial;
		//E_v-E_u=2J(m-n),for ising
		//Ev-Eu=J(m-n),for potts

		m_dPadd = 1 - exp(-2.0 * (m_dBeta + m_dAlpha * (m_dGCEWFavgE - m_dUn
				* m_uN) / m_uN));
		oldspin = m_pcStates[m_uCurTrial];
		// switch to the spin state
		newspin = -oldspin;
		ClusterDelt(m_uCurTrial);
		m_pClusterSeq[m_csp++] = m_uCurTrial;
		m_pcStates[m_uCurTrial] = newspin;

		while (sp) {
			m_uCurTrial = m_pClusterStack[--sp];
			neib = m_uCurTrial + 1;//right
			if (neib % m_uDim1 == 0)
				neib -= m_uDim1;

			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					ClusterDelt(neib);
					m_pClusterSeq[m_csp++] = neib;
					m_pcStates[neib] = newspin;
				}
			}

			neib = m_uCurTrial - 1;//left
			if (m_uCurTrial % m_uDim1 == 0)
				neib += m_uDim1;
			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					ClusterDelt(neib);
					m_pClusterSeq[m_csp++] = neib;
					m_pcStates[neib] = newspin;
				}
			}

			neib = m_uCurTrial - m_uDim1;//up
			if (m_uCurTrial < m_uDim1)
				neib += m_uN;
			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					ClusterDelt(neib);
					m_pClusterSeq[m_csp++] = neib;
					m_pcStates[neib] = newspin;
				}
			}

			neib = m_uCurTrial + m_uDim1;//down
			if (neib >= m_uN)
				neib -= m_uN;
			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					ClusterDelt(neib);
					m_pClusterSeq[m_csp++] = neib;
					m_pcStates[neib] = newspin;
				}

			}

		}//cluster formed now
		if (m_ran2.Real() < exp(-m_dAlpha * m_deltaE * (m_curHami + m_deltaE
				/ 2.0 - m_dGCEWFavgE) / m_uN)) {//accepted
			m_curHami += m_deltaE;
			m_curMag += m_deltaMag;
			m_aArgIO[AI_HAMI] = m_curHami;
			m_aArgIO[AI_MAG] += m_deltaMag;

		} else {//refused
			for (int p = 0; p < m_csp; p++) {
				m_pcStates[m_pClusterSeq[p]] = oldspin;
			}//roll back.
		}
		//m_deltaE = 0;
		m_ullCurMove++;
		CurStep += 1;
		m_dGCEWFsegAccumE += m_curHami;
		m_segAccumCS += m_csp;
		if (m_ullCurMove % m_GCEWFavgC == 0) {
#ifdef _DEBUG
			cout << m_ullCurMove << '\t' << m_csp << '\t' << m_dPadd << '\t' << exp(
					-m_dAlpha * m_deltaE
					* (m_curHami + m_deltaE / 2.0 - m_dGCEWFavgE) / m_uN)
			<< '\t' << m_deltaE << '\t' << m_dGCEWFavgE << '\t'
			<< m_SegAccumCS / double(m_GCEWFavgC) << endl;//2.0!!
#endif

			m_dGCEWFavgE = m_dGCEWFsegAccumE / m_GCEWFavgC;
			m_dGCEWFsegAccumE = 0;

			m_dAccumCS += m_segAccumCS / double(m_GCEWFavgC);
			m_segAccumCS = 0;

		}
	}
}
void Ising::WolffClusterSE(int moves) {
	//set first m_dBeta, m_dAlpha, m_dUn;
	int CurStep = 0;
	int sp = -1, oldspin, newspin;
	int avgei, e0i, e1i;
	unsigned int neib;
	//int oldbonds = 0, newbonds = 0;
	while (CurStep < moves) {
		sp = 0;
		m_csp = 0;
		m_deltaE = 0;
		m_deltaMag = 0;
		m_uCurTrial = m_ran.Number(0, m_uN - 1);
		m_pClusterStack[sp++] = m_uCurTrial;
		//E_v-E_u=2J(m-n),for ising
		//Ev-Eu=J(m-n),for potts
		avgei = int((2 * m_uN + m_dGCEWFavgE) / 4);
		m_dPadd = 1 - exp(-2.0 * m_pdBE[avgei]);
		oldspin = m_pcStates[m_uCurTrial];
		// switch to the spin state
		newspin = -oldspin;
		ClusterDelt(m_uCurTrial);
		m_pClusterSeq[m_csp++] = m_uCurTrial;
		m_pcStates[m_uCurTrial] = newspin;

		while (sp) {
			m_uCurTrial = m_pClusterStack[--sp];
			neib = m_uCurTrial + 1;//right
			if (neib % m_uDim1 == 0)
				neib -= m_uDim1;

			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					ClusterDelt(neib);
					m_pClusterSeq[m_csp++] = neib;
					m_pcStates[neib] = newspin;
				}
			}

			neib = m_uCurTrial - 1;//left
			if (m_uCurTrial % m_uDim1 == 0)
				neib += m_uDim1;
			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					ClusterDelt(neib);
					m_pClusterSeq[m_csp++] = neib;
					m_pcStates[neib] = newspin;
				}
			}

			neib = m_uCurTrial - m_uDim1;//up
			if (m_uCurTrial < m_uDim1)
				neib += m_uN;
			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					ClusterDelt(neib);
					m_pClusterSeq[m_csp++] = neib;
					m_pcStates[neib] = newspin;
				}
			}

			neib = m_uCurTrial + m_uDim1;//down
			if (neib >= m_uN)
				neib -= m_uN;
			if (m_pcStates[neib] == oldspin) {
				if (m_ran.Real() < m_dPadd) {
					m_pClusterStack[sp++] = neib;
					ClusterDelt(neib);
					m_pClusterSeq[m_csp++] = neib;
					m_pcStates[neib] = newspin;
				}

			}

		}//cluster formed now
		e0i = int((2 * m_uN + m_curHami) / 4);
		e1i = int((2 * m_uN + m_curHami + m_deltaE) / 4);
		if (m_ran2.Real() < exp(m_pdSE[e0i] - m_pdSE[e1i] + m_pdBE[avgei]
				* m_deltaE)) {
			m_curHami += m_deltaE;
			m_curMag += m_deltaMag;
			m_aArgIO[AI_HAMI] = m_curHami;
			m_aArgIO[AI_MAG] += m_deltaMag;

		} else {//refused
			for (int p = 0; p < m_csp; p++) {
				m_pcStates[m_pClusterSeq[p]] = oldspin;
			}//roll back.
		}
		//m_deltaE = 0;
		m_ullCurMove++;
		CurStep += 1;
		m_dGCEWFsegAccumE += m_curHami;
		m_segAccumCS += m_csp;
		if (m_ullCurMove % m_GCEWFavgC == 0) {
#ifdef _DEBUG
			cout << m_ullCurMove << '\t' << m_csp << '\t' << m_dPadd << '\t' << exp(m_pdSE[e0i] - m_pdSE[e1i] + m_pdBE[avgei] * m_deltaE)
			<< '\t' << m_deltaE << '\t' << m_dGCEWFavgE << '\t'
			<< m_SegAccumCS / double(m_GCEWFavgC) << endl;//2.0!!
#endif

			m_dGCEWFavgE = m_dGCEWFsegAccumE / m_GCEWFavgC;
			m_dGCEWFsegAccumE = 0;

			m_dAccumCS += m_segAccumCS / double(m_GCEWFavgC);
			m_segAccumCS = 0;

		}
	}
}
//======== Wang-Landau ==========//

void Ising::SetWL(double * lnGe_p, unsigned int *geN_p, int size,
		double lnfPrecision, double flatRate) {
	if (m_EN > size) {
		cout << "#Error: Size too small:" << size << endl;
		return;
	}
	m_dLnfPrecision = lnfPrecision;
	m_dFlatRate = flatRate;
	m_pdLnGe = lnGe_p;
	m_puGeN = geN_p;
	m_dLnf = 1;
	for (int n = 0; n < m_EN; n++) {
		m_puGeN[n] = 0;
		m_pdLnGe[n] = 0;
	}
}

bool Ising::WLCheckBelowAVG() {
	double dAvg = m_ullCurMove;
	dAvg /= m_EN - 2;
	dAvg *= m_dFlatRate;
	/*
	 for (int n = 0; n < m_EN; n++) {
	 cout << m_puGeN[n] << '\t';
	 }
	 cout << endl;
	 */
	//skip the unaccessible E
	if (m_puGeN[0] < dAvg)
		return false;
	if (m_puGeN[m_EN - 1] < dAvg)
		return false;
	for (int n = 2; n < m_EN - 2; n++) {
		if (m_puGeN[n] < dAvg)
			return false;
	}
	return true;
}
void Ising::WLResetGeN() {
	m_ullCurMove = 0;
	for (int n = 0; n < m_EN; n++) {
		m_puGeN[n] = 0;
		m_pdLnGe[n] -= m_pdLnGe[0];//save precisions as far as possible
	}

}
void Ising::WangLandauTrial(int moves) {
	int CurStep = 0;
	int E1, E2;
	double dDeltLnGE_old2new;

	while (CurStep < moves) {
		Delt();
		//cout << (2 * m_uN + m_curHami + m_deltaE) << endl;
		E1 = (2 * m_uN + m_curHami) / 4;
		E2 = (2 * m_uN + m_curHami + m_deltaE) / 4;

		dDeltLnGE_old2new = m_pdLnGe[E1] - m_pdLnGe[E2];
		if (dDeltLnGE_old2new < 0) {
			if (m_ran.Real() < exp(dDeltLnGE_old2new)) {
				m_pdLnGe[E2] += m_dLnf;
				m_puGeN[E2] += 1;
				m_pcStates[m_uCurTrial] *= -1;//< accepted
				m_curHami += m_deltaE;
				//m_accepted = 0;
			} else {
				m_pdLnGe[E1] += m_dLnf;
				m_puGeN[E1] += 1;
				//m_accepted = -1;
			}
		} else {
			m_pdLnGe[E2] += m_dLnf;
			m_puGeN[E2] += 1;
			m_pcStates[m_uCurTrial] *= -1;//< accepted
			m_curHami += m_deltaE;
			//m_accepted = 1;
		}
		m_ullCurMove++;
		CurStep += 1;
	}
	m_aArgIO[AI_HAMI] = m_curHami;
}
//==========
bool Ising::WLCheckBelowAVGBound() {
	double dAvg = m_ullCurMove;

	int lEi = (2 * m_uN + m_lowEBound) / 4;
	int hEi = (2 * m_uN + m_highEBound) / 4;
	//assume (lEi >= 6)
	dAvg /= (m_highEBound - m_lowEBound) / 4 + 1;
	dAvg *= m_dFlatRate;
	for (int n = lEi; n <= hEi; n++) {
		if (m_puGeN[n] < dAvg)
			return false;
	}
	return true;
}
void Ising::WLResetGeNBound() {
	m_ullCurMove = 0;
	int lei = E2i(m_lowEBound);
	int hei = E2i(m_highEBound);
	double reflnGe = m_pdLnGe[lei];
	for (int n = 0; n < lei; n++) {
		m_puGeN[n] = 0;
		m_pdLnGe[n] = 0;//save precisions as far as possible
	}
	for (int n = lei; n <= hei; n++) {
		m_puGeN[n] = 0;
		m_pdLnGe[n] -= reflnGe;//save precisions as far as possible
	}
	reflnGe = m_pdLnGe[hei];
	for (int n = hei + 1; n < m_EN; n++) {
		m_puGeN[n] = 0;
		m_pdLnGe[n] = reflnGe;//save precisions as far as possible
	}
}

void Ising::WangLandauTrialBound(int moves) {
	int CurStep = 0;
	int E1, E2;
	double dDeltLnGE_old2new;

	while (CurStep < moves) {
		Delt();//Assume m_lowEBound<=m_curHami<=m_highEBound
		if ((m_curHami + m_deltaE) < m_lowEBound || (m_curHami + m_deltaE)
				> m_highEBound)
			continue;

		E1 = (2 * m_uN + m_curHami) / 4;
		E2 = (2 * m_uN + m_curHami + m_deltaE) / 4;

		dDeltLnGE_old2new = m_pdLnGe[E1] - m_pdLnGe[E2];

		if (dDeltLnGE_old2new < 0) {
			if (m_ran.Real() < exp(dDeltLnGE_old2new)) {
				m_pdLnGe[E2] += m_dLnf;
				m_puGeN[E2] += 1;
				m_pcStates[m_uCurTrial] *= -1;//< accepted
				m_curHami += m_deltaE;
				m_curMag += m_deltaMag;
				//m_accepted = 0;
			} else {
				m_pdLnGe[E1] += m_dLnf;
				m_puGeN[E1] += 1;
				//m_accepted = -1;
			}
		} else {
			m_pdLnGe[E2] += m_dLnf;
			m_puGeN[E2] += 1;
			m_pcStates[m_uCurTrial] *= -1;//< accepted
			m_curHami += m_deltaE;
			m_curMag += m_deltaMag;
			//m_accepted = 1;
		}
		m_ullCurMove++;
		CurStep += 1;
	}
	m_aArgIO[AI_HAMI] = m_curHami;
	m_aArgIO[AI_MAG] = m_curMag;
}
int Ising::SetBound(double lb, double hb) {
	if (lb < -2)
		lb = -2;
	if (hb > 2)
		hb = 2;

	if (lb > hb) {
		cout << "lb>hb" << lb << ' ' << hb << endl;
		lb = hb;
	}
	m_lowEBound = int((2 + lb) * m_uN / 4);
	m_lowEBound = I2e(m_lowEBound);//E(n)
	m_highEBound = int((2 + hb) * m_uN / 4);
	m_highEBound = I2e(m_highEBound);//E(n)

	return m_highEBound - m_lowEBound;
}
void Ising::WarmupToBound() {
	InitConf(-1);//warm up
	Gauge();
	while (true) {
		Delt();
		m_pcStates[m_uCurTrial] *= -1;//< accepted,T=0
		m_curHami += m_deltaE;
		//cout << m_curHami << endl;
		if ((m_lowEBound <= m_curHami) && (m_curHami <= m_highEBound)) {
			break;
		}
	}
}
//========== HEAT Bath ===========//
void Ising::SetHeatBath(double T) {
	m_aArgIO[AI_TEMPER] = T;
	double h;
	int i;
	for (i = 0; i < 5; i++) //Table for heat bath
	{
		h = (-4 + 2 * i) / T;//for current spin=-1,J=1

		m_auLocalFieldPro[i] = (unsigned int) (TO32 * (exp(-h) / (exp(h) + exp(
				-h))));//for j=1,map to uint32_t space,
#ifdef _DEBUG
		cout << h << '\t' << m_auLocalFieldPro[i] << endl;
#endif
	}
}
void Ising::HeatBathTrial(int moves) {
	int LCField = 0, XTotalField = 0;
	unsigned int neib;

	for (int CurStep = 0; CurStep < moves; CurStep++) {
		LCField = 0;
		m_uCurTrial = m_ran.Number(0, m_uN - 1);

		neib = m_uCurTrial + 1;//right
		if (neib % m_uDim1 == 0)
			neib -= m_uDim1;
		LCField += m_pcStates[neib];

		neib = m_uCurTrial - 1;//left
		if (m_uCurTrial % m_uDim1 == 0)
			neib += m_uDim1;
		LCField += m_pcStates[neib];

		neib = m_uCurTrial - m_uDim1;//up
		if (m_uCurTrial < m_uDim1)
			neib += m_uN;
		LCField += m_pcStates[neib];

		neib = m_uCurTrial + m_uDim1;//down
		if (neib >= m_uN)
			neib -= m_uN;
		LCField += m_pcStates[neib];

		//index in the probability table according to h=(4+local_field)/2
		/*
		 if (m_ran.uNumber32() < m_auLocalFieldPro[(4 + LCField) >> 1]) {
		 XTotalField += LCField * (m_pcStates[m_uCurTrial] != -1);
		 m_pcStates[m_uCurTrial] = -1;
		 } else {
		 XTotalField -= LCField * (m_pcStates[m_uCurTrial] != 1);
		 m_pcStates[m_uCurTrial] = 1;
		 }
		 */

		m_ullCurMove++;

	}
	m_deltaE = (XTotalField << 1);
	m_aArgIO[AI_DELT_HAMI] = m_deltaE;
	m_aArgIO[AI_HAMI] += m_aArgIO[AI_DELT_HAMI];
}
/*
 bool Ising::GetEnergyRange(int *pData, int size) {
 if (m_EN > size || pData == NULL) {
 return false;
 }
 for (int n = 0; n < m_EN; n++) {
 pData[n] = 4 * n - 2 * m_uN;
 cout << pData[n] << endl;
 }
 return true;
 }
 */
bool Ising::SetEnergyRange(int *energy, int elen) {//input empty array,out energy range
	if (energy == NULL || m_EN == 0 || elen != m_EN)
		return false;
	for (int n = 0; n < m_EN; n++) {
		energy[n] = I2e(n);//E(n)
	}
	m_pE = energy;
	return true;
}
bool Ising::ETraj2Hist(int * trajdata, unsigned int uLen, int* histdata,
		int hlen, int h0, int *pE0, int *pE1) {

	if (trajdata == NULL || histdata == NULL || hlen != m_EN) {
		return false;
	}

	for (int n = 0; n < m_EN; n++)
		histdata[n] = 0;

	for (unsigned int c = 0; c < uLen; c++)
		histdata[(2 * m_uN + trajdata[c]) / 4]++;

	*pE0 = 0, *pE1 = 0;
	for (int c = 0; c < m_EN; c++) {
		if (histdata[c] > h0) {
			*pE0 = 4 * c - 2 * m_uN;
			break;
		}
	}
	for (int c = 0; c < m_EN; c++) {
		if (histdata[m_EN - c - 1] > h0) {
			*pE1 = 2 * m_uN - 4 * c;
			break;
		}
	}

	return true;
}
void Ising::RanWalkTrailEBound(int * e_traj, unsigned int samples,
		unsigned int stride) {

	int moves;
	for (unsigned int s = 0; s < samples; s++) {
		moves = m_uN * stride;
		while (moves--) {
			//Assume m_lowEBound<=m_curHami<=m_highEBound
			//the visited number at two bounds near half of the ones of other energy levels
			//cout << m_CurEindex;
			if (m_pE[m_curEindex] <= m_lowEBound) {
				m_curEindex += 1;
			} else if (m_pE[m_curEindex] >= m_highEBound) {
				m_curEindex -= 1;
			} else if (m_ran.Real() < 0.5) {
				m_curEindex -= 1;
			} else {
				m_curEindex += 1;
			}
			//cout << '!' << m_CurEindex << endl;
		}
		m_curHami = m_pE[m_curEindex];
		e_traj[s] = m_curHami;
	}
	m_ullCurMove += m_uN * stride * samples;
	m_aArgIO[AI_HAMI] = m_curHami;

}

