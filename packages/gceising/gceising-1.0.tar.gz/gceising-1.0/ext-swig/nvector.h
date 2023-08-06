/*
 ============================================================================
 Name        : numvector.h
 Author      : Alwin Tsui,alwintsui@gmail.com
 Version     :
 Copyright   : APCTP
 Description :
 ============================================================================
 */

#ifndef _NVECTOR_H
#define _NVECTOR_H

#include <string>
#include <string.h>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <cmath>

template<class T>
bool nv_split(const std::string &input, T &res, int c,
		const std::string& delimiters) {
	std::string token = "";
	std::string::size_type lastPos = input.find_first_not_of(delimiters, 0);
	// Find first "non-delimiter".
	std::string::size_type pos = input.find_first_of(delimiters, lastPos);

	while (std::string::npos != pos || std::string::npos != lastPos) {
		// Found a token, add it to the vector.
		if (c-- == 0) {
			token = input.substr(lastPos, pos - lastPos);
			break;
		}
		// Skip delimiters.  Note the "not_of"
		lastPos = input.find_first_not_of(delimiters, pos);
		// Find next "non-delimiter"
		pos = input.find_first_of(delimiters, lastPos);
	}
	if (token == "")
		return false;
	std::istringstream ss(token);
	ss >> res;
	return true;
}

template<class DataType>
class nvector {
	bool m_bOwn;

private:
	nvector(const nvector & other);
	nvector & operator =(const nvector & other);
public:
	DataType *m_pData;
	std::string m_sDelim;
	unsigned int m_uLen;
public:
	nvector() {
		m_uLen = 0;
		m_pData = NULL;
		m_sDelim = ",";
		m_bOwn = false;
	}
	nvector(unsigned int uLen, bool bOwn = true) {
		m_bOwn = false;
		m_uLen = uLen;
		m_pData = new DataType[m_uLen];
		if (m_pData == NULL) {
			std::cerr << "New DataType error, size=" << m_uLen << std::endl;
			return;
		}
		m_sDelim = ",";
		m_bOwn = bOwn;
	}
	nvector(DataType *pData, unsigned int uLen) {
		m_uLen = uLen;
		m_pData = pData;
		m_sDelim = ",";
		m_bOwn = false;
	}
	int reset(DataType *pData, unsigned int uLen) {
		if (m_bOwn) {
			delete[] m_pData;
			std::cout << "~nvector" << m_uLen << std::endl;
		}
		m_uLen = uLen;
		m_pData = pData;
		m_sDelim = ",";
		m_bOwn = false;
		return m_uLen;
	}

	///////////////
	~nvector() {
		if (m_bOwn) {
			delete[] m_pData;
			std::cout << "~nvector" << m_uLen << std::endl;
		}
	}
	void fill(DataType val) {
		for (unsigned int i = 0; i < m_uLen; i++)
			m_pData[i] = val;
	}
	void dump(const char *file, char linesep = '\n', unsigned int end = 0) {
		std::ofstream ofile(file);
		ofile << std::setprecision(15) << std::fixed;
		for (unsigned int i = 0; i < m_uLen - end; i++) {
			ofile << m_pData[i];
			if (i < m_uLen - 1 - end)
				ofile << linesep;
		}
		ofile.close();
	}
	void dump_bin(const char *file, std::ios::openmode mode = std::ios::out
			| std::ios::binary) {//| std::ios::app
		std::ofstream ofile(file, mode);
		ofile.write((char *) m_pData, m_uLen * sizeof(DataType));
		ofile.close();
	}
	int load(const char * filename, int col = 0, bool o = true, char linesep =
			'\n', const std::string &sep = "\t") {
		std::ifstream In_f(filename);
		if (In_f.fail()) {
			std::cerr << "Failure in opening file:" << filename << std::endl;
			return -1;
		}

		char szLine[1024];
		DataType res;
		if (o) {
			std::vector<DataType> vData;
			while (In_f.getline(szLine, 1024, linesep)) {
				if (nv_split(std::string(szLine), res, col, sep)) {
					vData.push_back(res);
				}
			}
			if (m_bOwn)
				delete[] m_pData;
			m_pData = new DataType[vData.size()];
			m_bOwn = true;
			for (m_uLen = 0; m_uLen < vData.size(); m_uLen++)
				m_pData[m_uLen] = vData[m_uLen];

		} else {
			unsigned int l = 0;
			while (In_f.getline(szLine, 1024, linesep)) {
				if (nv_split(std::string(szLine), res, col, sep)) {
					if (l >= m_uLen) {
						std::cerr << "too much items:" << l << std::endl;
						break;
					}
					m_pData[l] = res;
					l++;
				}
			}
			m_uLen = l;

		}
		In_f.close();
		return m_uLen;
	}
	int load_bin(const char *file, unsigned int size = 0, int offset = 0,
			bool own = true) {
		std::ifstream infile(file, std::ifstream::binary);
		if (infile.fail()) {
			std::cerr << "Failure in opening file:" << file << std::endl;
			return -1;
		}

		if (size == 0) {//to the end
			infile.seekg(0, std::ios::end);
			size = int(infile.tellg()) - offset * sizeof(DataType);
			size /= sizeof(DataType);
		}
		infile.seekg(offset * sizeof(DataType));

		if (own) {
			if (m_bOwn && m_uLen != 0) {
				delete[] m_pData;
			}
			m_pData = new DataType[size];
			m_bOwn = true;
			infile.read((char *) m_pData, size * sizeof(DataType));
		} else {
			if (size != m_uLen) {
				std::cerr << "too much items:" << m_uLen << std::endl;
				return -1;
			} else {
				infile.read((char *) m_pData, size * sizeof(DataType));
			}
		}
		if (infile.eof()) {
			//m_uLen = strlen(m_pData);
			m_uLen = size;
			std::cout << "size" << m_uLen << std::endl;
		} else {
			m_uLen = size;
		}
		infile.close();
		return m_uLen;
	}
	friend std::ostream &operator<<(std::ostream &os, nvector &nv) {
		for (unsigned int i = 0; i < nv.m_uLen; i++) {
			os << nv.m_pData[i];
			if (i < nv.m_uLen - 1)
				os << nv.m_sDelim;
		}
		return os;
	}
	void print_cout() {
		for (unsigned int i = 0; i < m_uLen; i++) {
			std::cout << m_pData[i];
			if (i < m_uLen - 1)
				std::cout << m_sDelim;
		}
		std::cout << std::endl;
	}
	DataType sum() {
		DataType m = 0;
		for (unsigned int i = 0; i < m_uLen; i++)
			m += m_pData[i];
		return m;
	}
	bool integral(double * pdSE, unsigned int dim) {
		if (dim < 3 || dim != m_uLen || pdSE == NULL || m_pData == NULL)
			return false;
		pdSE[0] = 0;
		pdSE[1] = (m_pData[1] + m_pData[0]) / 2;//trapezoidal
		for (unsigned int i = 2; i < dim; i++) {
			pdSE[i] = pdSE[i - 2] + (m_pData[i - 2] + 4 * m_pData[i - 1]
					+ m_pData[i]) / 3.0;//simpson integration
		}
		return true;
	}

	bool diff(double * pdBE, unsigned int dim) {
		if (dim < 3 || dim != m_uLen || m_pData == NULL || pdBE == NULL)
			return false;
		pdBE[0] = (-3 * m_pData[0] + 4 * m_pData[1] - m_pData[2]) / 2;//three-point forward difference
		for (unsigned int i = 1; i < dim - 1; i++) {
			pdBE[i] = (m_pData[i + 1] - m_pData[i - 1]) / 2;// two-point central difference
		}
		pdBE[dim - 1] = (m_pData[dim - 3] - 4 * m_pData[dim - 2] + 3
				* m_pData[dim - 1]) / 2;//three-point backward difference
		return true;
	}
	double mean() {
		double m = 0;
		for (unsigned int i = 0; i < m_uLen; i++)
			m += m_pData[i];
		return m / m_uLen;
	}
	double std() {
		double m = 0;
		double m2 = 0;
		for (unsigned int i = 0; i < m_uLen; i++) {
			m += m_pData[i];
			m2 += m_pData[i] * m_pData[i];
		}
		return sqrt(m_uLen * (m2 / m_uLen - (m / m_uLen) * (m / m_uLen))
				/ (m_uLen - 1));
	}
	int jk_mean_std_err_tau(int nblo, double *pdTauCorr, int tauMax,
			double *mean, double *std, double *meanErr, double *ptau,
			unsigned int start) {
		//return tau
		if (pdTauCorr == NULL) {
			std::cerr << "Failure: allocating memory for pdTauCorr:"
					<< std::endl;
			return -1;
		}
		DataType *data_p = m_pData + start;
		unsigned int N = m_uLen - start;
		int block = N / nblo;
		N = block * nblo;
		data_p = data_p + (m_uLen - N);

		if (tauMax > block) {
			std::cerr << "Failure tauMax too large:" << tauMax << ',' << block
					<< std::endl;
			return -1;
		}
		int tau, ti;
		//average N  blocks
		*mean = 0;
		double m2 = 0;
		for (unsigned int e = 0; e < N; e++) {
			*mean += data_p[e];
			m2 += data_p[e] * data_p[e];
		}
		*mean /= N;
		m2 = m2 / N - (*mean) * (*mean);
		*std = sqrt(m2 * N / (N - 1));

		//all Corr
		for (tau = 0; tau < tauMax; tau++) {
			pdTauCorr[tau] = 0;
			//for every block every tau
			for (ti = 0; ti < block - tau; ti++) {
				for (int bi = 0; bi < nblo; bi++) {
					pdTauCorr[tau] += (data_p[bi * block + ti] - *mean)
							* (data_p[bi * block + ti + tau] - *mean);
				}
			}
			pdTauCorr[tau] /= block - tau;

		}
		for (tau = tauMax - 1; tau >= 0; tau--) //Go backwards to avoid spoiling t=0 value
		{//Go from C(t) to rho(t). Normalization is automatic.
			pdTauCorr[tau] /= pdTauCorr[0];
		}

		double pippo, value;
		int tauWin = 4;
		pippo = 0.5;
		tau = 1;
		while ((tau < tauWin * pippo) && (tau < tauMax)) {
			value = pdTauCorr[tau];
			if (fabs(value) > 0.36787944117144233) {
				pippo += value;
			}
			tau++;
		}
		if ((tau < tauWin * pippo) && (tau >= tauMax)) {
			std::cerr << "#warning: tau >= tauMax" << std::endl;
		}
		*meanErr = sqrt(m2 * (2 * pippo) / (N - 1));
		*ptau = pippo;
		return tau;
	}
	unsigned int mean_std(double *mean, double *std, bool flag,//false=std,true=1/N
			unsigned int start = 0, unsigned int step = 1) {
		DataType *data_p = m_pData + start;
		unsigned int N = m_uLen - start;
		*mean = 0;
		double m2 = 0;
		for (unsigned int k = 0; k < N; k += step) {
			*mean += data_p[k];
			m2 += data_p[k] * data_p[k];
		}
		unsigned int n = (N - 1) / step + 1;
		*mean /= n;
		m2 = m2 / n - (*mean) * (*mean);
		if (!flag)
			m2 = m2 * n / (n - 1);//
		*std = sqrt(m2);
		return n;
	}

	unsigned int mean_std_err(double *mean, double *std, double *meanErr,
			unsigned int start = 0, unsigned int tau = 0) {
		DataType *data_p = m_pData + start;
		unsigned int N = m_uLen - start;
		*mean = 0;
		double m2 = 0;
		for (unsigned int k = 0; k < N; k++) {
			*mean += data_p[k];
			m2 += data_p[k] * data_p[k];
		}
		*mean /= N;
		m2 = m2 / N - (*mean) * (*mean);
		*meanErr = sqrt(m2 * (1 + 2 * tau) / (N - 1));//estimate of variance of sample mean
		*std = sqrt(m2 * N / (N - 1));
		return N;
	}
	unsigned int mean_std_err_blk(double *mean, double *std, double *meanErr,
			unsigned int start = 0, unsigned int blk = 1) {
		DataType *data_p = m_pData + start;
		unsigned int N = m_uLen - start;
		*mean = 0;
		double lmean, m2 = 0;
		unsigned int nBlk = N / blk;
		for (unsigned int b = 0; b < N; b += nBlk) {
			lmean = 0;
			for (unsigned int i = b * blk; i < (b + 1) * blk; i++) {
				lmean += data_p[i];
			}
			lmean /= blk;
			*mean += lmean;
			m2 += lmean * lmean;
		}
		*mean /= nBlk;
		m2 = m2 / nBlk - (*mean) * (*mean);
		*meanErr = sqrt(m2 / (nBlk - 1));
		*std = sqrt(m2 * nBlk / (nBlk - 1));
		return nBlk;
	}

	unsigned int get_eq(unsigned int EQwin, unsigned int start = 0) {
		//get T_eq,EQwin>Tau correlation time
		DataType *data_p = m_pData + start;
		unsigned int N = m_uLen - start;

		if (EQwin > N)
			return 0;

		double E0, S0, ErrorE0;
		//mean_std(&E0, &S0, false, start + N - EQwin);
		//ErrorE0 = S0 / sqrt(EQwin);
		mean_std_err(&E0, &S0, &ErrorE0, start + N - EQwin);

		double m = 0;
		unsigned int s = 0;
		while (s < N - EQwin) {
			m = 0;
			for (unsigned int k = s; k < s + EQwin; k++) {
				m += data_p[k];
			}
			m /= EQwin;
			if (fabs(m - E0) < ErrorE0) {
				break;

			} else {
				s++;
			}
		}
		return s;
	}

	bool auto_corr(double *Xt, unsigned int nLags, unsigned int &tau,
			unsigned int start) {
		DataType *data_p = m_pData + start;
		unsigned int N = m_uLen - start;

		if (nLags > N - 1)
			return false;//lags 'nLags' must not exceed 'Series' length - 1.

		double avm = 0;
		for (unsigned int i = 0; i < N; i++)
			avm += data_p[i];
		avm /= N;

		tau = 0;
		double mit, mitk;
		for (unsigned int k = 0; k <= nLags; k++) {
			//Xt[k] = _summ2(m, N, k, avm) / N;
			//def	_summ2(m_pData, N, k, avm):
			Xt[k] = 0;
			mit = 0;
			mitk = 0;

			for (unsigned int it = 0; it < N - k; it++) {
				Xt[k] += data_p[it] * data_p[it + k];
				mit += data_p[it];
				mitk += data_p[it + k];
			}

			Xt[k] /= N - k;
			Xt[k] -= mit / (N - k) * mitk / (N - k);

			if (tau == 0 && (Xt[k] / Xt[0] < 0.135335283236613))//0.36787944117144233)//)//1/exp(1),)//1 / exp(1):
			{
				tau = (k + 1) / 2;//!=0
				break;
			}
		}
		return true;//although tau==0;
	}
	unsigned int tunnelup_times(DataType lE, DataType hE, unsigned int start =
			0) {
		DataType *data_p = m_pData + start;
		unsigned int N = m_uLen - start;
		unsigned int ri = 0;
		unsigned int i = 0;
		bool tunnel = false;
		while (i < N) {
			if (tunnel) {
				if (data_p[i] <= lE) {
					ri++;
					tunnel = false;
				}
			} else if (data_p[i] >= hE) {
				tunnel = true;
			}
			i++;
		}
		return ri;
	}

	unsigned int statis(unsigned int uInitLags, unsigned int Win,
			unsigned int &uTeq, unsigned int &utau) //start,stop,step:MCS/site [0,M-1]
	{
		if (Win > m_uLen)
			return 0;
		uTeq = get_eq(Win, 0);//Win>Tau
		utau = 0;
		unsigned int uLags = uInitLags;
		double * dXT_p;
		do {
			dXT_p = new double[uLags + 1];
			if (!auto_corr(dXT_p, uLags, utau, uTeq)) {
				std::cerr << "#Failure in auto_corr(),'nLags':" << uLags
						<< " must not exceed 'Series' length - 1:" << m_uLen
						- uTeq << std::endl;
				return 0;
			} else if (utau == 0) {
				uLags *= 2;//(unsigned int) (pow(m_uN, 0.25));
			}
			delete[] dXT_p;
		} while (utau == 0);
		return uLags;
	}
	unsigned int jk_statis(int start, unsigned int nblo, int tauMax,
			unsigned int &uTeq, double &time, double &error_time,
			unsigned int &utau) //start,stop,step:MCS/site [0,M-1]
	{
		/*
		 if (start > m_uLen or en - start)
		 return 0;
		 uTeq = get_eq(Win, 0);//Win>Tau
		 utau = 0;
		 unsigned int uLags = uInitLags;
		 do {
		 //delete[] dXT_p;dXT_p = new double[uLags + 1];
		 double dXT_p[uLags + 1];
		 if (!auto_corr(dXT_p, uLags, utau, uTeq)) {
		 std::cerr << "#Failure in auto_corr(),'nLags':" << uLags
		 << " must not exceed 'Series' length - 1:" << m_uLen
		 - uTeq << std::endl;
		 return 0;
		 } else if (utau == 0) {
		 uLags *= 2;//(unsigned int) (pow(m_uN, 0.25));
		 }
		 } while (utau == 0);
		 return uLags;

		 double *pdTauCorr;
		 double *blkAve;

		 unsigned int win;
		 if (start > 0) {
		 win = (m_uLen - start) / 30;
		 get_eq(win, start);
		 } else {
		 win = m_uLen / 30;
		 get_eq(win, 0);
		 }

		 if (win < 2) {
		 cout << "Samples too little" << m_uLen << endl;
		 return -1;
		 }

		 start = rdb.get_eq(start, 0);

		 if (win_start < 0) {
		 start = m_uLen / 30;
		 if (start < 2) {
		 cout << "Samples too little" << rdb.m_uLen << endl;
		 return -1;
		 }
		 start = rdb.get_eq(start, 0);
		 }

		 int start2 = rdb.jack_knife_mean_error(nblocks, tauMax, pdTauCorr,
		 blkAve, start);
		 cout << "%jack_knife: start_mean_error:" << start2 << '\t'
		 << blkAve[nblocks] << '\t' << blkAve[nblocks + 1] << endl;
		 nvector<double> rdb_e(pdTauCorr, (nblocks + 2) * tauMax);
		 double times, error_time;
		 int tau = rdb_e.integrated_time(nblocks, tauMax, &times, &error_time);
		 cout << "%jack_knife: rho=" << times << "\trho_err=" << error_time
		 << "\ttau=" << tau << endl;
		 */
		return 0;
	}
	//Calculate errors for a correlation function
	//sigma_jk(<E^2>-<E>^2),reduce_factor=(Delta_t/2_Tau) ref. to Newman
	//for small group of sample
	double jack_knife2(unsigned int start = 0, int reduce_factor = 1) {
		unsigned int N = m_uLen - start;
		DataType *data_p = m_pData + (m_uLen - N);
		//average error
		double sum = 0;
		double sum2 = 0;
		double r = 0;
		for (int m = 0; m < N; m++) {
			sum += data_p[m];
			sum2 += data_p[m] * data_p[m];
		}
		sum /= N;
		double c = (sum2 / N - sum * sum);
		double ci_c2 = 0;
		for (int n = 0; n < N; n++) {
			sum = 0;
			sum2 = 0;
			for (int m = 0; m < N; m++) {
				if (n != m) {
					sum += data_p[m];
					sum2 += data_p[m] * data_p[m];
				}
			}
			sum /= (N - 1);
			r = sum2 / (N - 1) - sum * sum;
			ci_c2 += (r - c) * (r - c);
		}
		return sqrt(reduce_factor * ci_c2);
	}
	//Calculate errors for a correlation function
	int jack_knife_mean_error(unsigned int nblo, int tauMax,
			double *&pdTauCorr, double*&blkAve, unsigned int start = 0) {
		//pdTauCorr[(nblo + 2) * tauMax]: nblo*tauMax,mean_Tau,Tau_err
		//blkAve[nblo+2]: (nblo-1)*nblo_1_ave,nblo_ave,nblo_ave_error

		unsigned int N = m_uLen - start;
		int block = N / nblo;
		N = block * nblo;
		DataType *data_p = m_pData + (m_uLen - N);

		if (tauMax > block / 3) {
			std::cerr << "Failure tauMax too large:" << tauMax << ',' << block
					/ 3 << std::endl;
			return -1;
		}
		pdTauCorr = new double[(nblo + 2) * tauMax];
		blkAve = new double[nblo + 2];//average
		if (pdTauCorr == NULL) {
			std::cerr << "Failure: allocating memory for pdTauCorr:"
					<< std::endl;
			return -1;
		}

		int tau, ti;
		unsigned int eb, e, b, bi;
		double sum, sum2;
		//average (N-1)  blocks
		for (b = 0; b < nblo; b++) {
			blkAve[b] = 0;
			for (e = 0; e < b * block; e++) {
				blkAve[b] += data_p[e];
			}
			for (e = (b + 1) * block; e < N; e++) {
				blkAve[b] += data_p[e];
			}

			blkAve[b] /= (nblo - 1) * block;

		}
		//average N  blocks
		/*
		 blkAve[nblo] = 0;
		 for (e = 0; e < N; e++) {
		 blkAve[nblo] += data_p[e];
		 }
		 blkAve[nblo] /= N;
		 */
		blkAve[nblo] = 0;
		for (b = 0; b < nblo; b++) {
			blkAve[nblo] += blkAve[b];
		}
		blkAve[nblo] /= nblo;

		//average error
		sum = 0;
		sum2 = 0;
		for (b = 0; b < nblo; b++) {
			sum += blkAve[b];
			sum2 += blkAve[b] * blkAve[b];
		}
		sum /= nblo;
		sum2 /= nblo;
		blkAve[nblo + 1] = sqrt((nblo - 1) * (sum2 - sum * sum));//save error to the last one

		//Corr
		for (b = 0; b < nblo; b++) {
			for (tau = 0; tau < tauMax; tau++) {
				eb = b * tauMax + tau;
				pdTauCorr[eb] = 0;
				//for every block every tau
				for (ti = 0; ti < block - tau; ti++) {
					for (bi = 0; bi < b; bi++) {
						pdTauCorr[eb] += (data_p[bi * block + ti] - blkAve[b])
								* (data_p[bi * block + ti + tau] - blkAve[b]);
					}
					for (bi = (b + 1); bi < nblo; bi++) {
						pdTauCorr[eb] += (data_p[bi * block + ti] - blkAve[b])
								* (data_p[bi * block + ti + tau] - blkAve[b]);
					}
				}
				pdTauCorr[eb] /= block - tau;
			}
		}

		//all Corr
		for (tau = 0; tau < tauMax; tau++) {
			eb = nblo * tauMax + tau;
			pdTauCorr[eb] = 0;
			//for every block every tau
			for (ti = 0; ti < block - tau; ti++) {
				for (bi = 0; bi < nblo; bi++) {
					pdTauCorr[eb] += (data_p[bi * block + ti] - blkAve[nblo])
							* (data_p[bi * block + ti + tau] - blkAve[nblo]);
				}
			}
			pdTauCorr[eb] /= block - tau;
			//std::cout << pdTauCorr[eb] << '\t';
		}

		for (tau = tauMax - 1; tau >= 0; tau--) //Go backwards to avoid spoiling t=0 value
		{//Go from C(t) to rho(t). Normalization is automatic.
			for (b = 0; b <= nblo; b++) {
				pdTauCorr[b * tauMax + tau] /= pdTauCorr[b * tauMax];
			}
		}

		//for error
		double pippo;
		for (tau = 0; tau < tauMax; tau++) {
			sum = sum2 = 0;
			for (b = 0; b < nblo; b++) {
				pippo = pdTauCorr[b * tauMax + tau];
				sum += pippo;
				sum2 += pippo * pippo;
			}
			sum /= nblo;
			sum2 /= nblo;
			pdTauCorr[(nblo + 1) * tauMax + tau] = sqrt((nblo - 1) * (sum2
					- sum * sum));//save error to the last one
		}

		return m_uLen - N;//start

	}
	//Given an autocorrelation function and its error, this function
	//calculates its autocorrelation time with a window of size tauWin*tau_int
	//It return the time in variable "time" and the error estimate in "error_time"
	int integrated_time(unsigned int nblo, int tauMax, double *time,
			double *error_time, int tauWin = 6) {

		double sum, sum2, pippo, value;
		int tau;
		unsigned int b;
		sum = sum2 = 0;
		for (b = 0; b < nblo; b++) {
			pippo = 0.5;
			tau = 1;
			while ((tau < tauWin * pippo) && (tau < tauMax)) {
				value = m_pData[b * tauMax + tau];
				if (fabs(value) > 2. * m_pData[(nblo + 1) * tauMax + tau]) {
					pippo += value; //Add only if signal-to-noise ratio > 2
				}
				tau++;
			}

			sum += pippo;
			sum2 += pippo * pippo;
		}
		sum /= nblo;
		sum2 /= nblo;
		error_time[0] = sqrt((nblo - 1) * (sum2 - sum * sum));
		pippo = 0.5;
		tau = 1;
		while ((tau < tauWin * pippo) && (tau < tauMax)) {
			value = m_pData[nblo * tauMax + tau];
			if (fabs(value) > 2. * m_pData[(nblo + 1) * tauMax + tau]) {
				pippo += value;
			}
			tau++;
		}
		if ((tau < tauWin * pippo) && (tau >= tauMax)) {
			std::cerr << "#warning: tau >= tauMax" << std::endl;
		}

		time[0] = pippo;
		return tau;
	}

	//Given an autocorrelation function and its error, this function
	//calculates  two estimators (and their errors) for the exponential
	//autocorrelation time
	void expo_times(unsigned int nblo, int tauMax, double *timeA,
			double *errorA, double *timeB, double *errorB) {
		//tauMax:timeA, errorA, timeB, errorB
		double sumA, sumA2, sumB, sumB2, pippo, value1, value2;
		int tau;
		unsigned int b;

		timeA[0] = 0;
		errorA[0] = 0;
		for (tau = 1; tau < tauMax - 1; tau++) {
			sumA = sumA2 = 0;
			for (b = 0; b < nblo; b++) {
				value1 = fabs(double(m_pData[b * tauMax + tau]));//Take absolute values, in case
				pippo = -tau / log(value1);
				sumA += pippo;
				sumA2 += pippo * pippo;
			}
			value1 = fabs(double(m_pData[nblo * tauMax + tau]));
			timeA[tau] = -tau / log(value1);
			sumA /= nblo;
			sumA2 /= nblo;
			errorA[tau] = sqrt((nblo - 1) * (sumA2 - sumA * sumA));
		}

		for (tau = 0; tau < tauMax - 1; tau++) {
			sumB = sumB2 = 0;
			for (b = 0; b < nblo; b++) {
				value1 = fabs(double(m_pData[b * tauMax + tau]));//Take absolute values, in case
				value2 = fabs(double(m_pData[b * tauMax + tau + 1]));//of anticorrelations.
				pippo = 1.0 / log(value1 / value2);
				sumB += pippo;
				sumB2 += pippo * pippo;
			}
			value1 = fabs(double(m_pData[nblo * tauMax + tau]));
			value2 = fabs(double(m_pData[nblo * tauMax + tau + 1]));
			timeB[tau] = 1.0 / log(value1 / value2);
			sumB /= nblo;
			sumB2 /= nblo;
			errorB[tau] = sqrt((nblo - 1) * (sumB2 - sumB * sumB));
			//std::cout << value1 << '\t' << value2 << '\t' << timeB[tau] << '\t'<< errorB[tau] << std::endl;
		}
	}

};

template<class T1, class T2>
int nv_dump(const nvector<T1> &v1, const nvector<T2> &v2, std::string file,
		char linesep = '\n', const std::string &sep = "\t") {
	if (v1.m_uLen != v2.m_uLen)
		return -1;
	std::ofstream ofile(file.c_str());
	for (unsigned int i = 0; i < v1.m_uLen; i++)
		ofile << v1.m_pData[i] << sep << v2.m_pData[i] << linesep;
	ofile.close();
	return v1.m_uLen;
}

template<class DataType>
void nv_dump(DataType * d, unsigned int l, std::string file, char linesep =
		'\n') {
	nvector<DataType> out(d, l);
	out.dump(file, linesep);
}
template<class DataType>
void nv_load(DataType * d, unsigned int l, std::string file, int col = 0,
		bool o = true, char linesep = '\n', const std::string &sep = "\t") {
	nvector<DataType> out(d, l);
	out.load(file, col, o, linesep, sep);
}

#endif
