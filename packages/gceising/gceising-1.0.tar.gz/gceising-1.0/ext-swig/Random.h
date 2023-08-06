#ifndef _RANDOM_H_
#define _RANDOM_H_

//Author: Alwin Tsui,alwintsui@gmail.com
// int assumed 32bits

class Random {
private:
	/* Period parameters */
	static const unsigned int N = 624;
	static const int M = 397;
	static const unsigned int MATRIX_A = (unsigned int) 0x9908b0df; /* constant vector a */
	static const unsigned int UPPER_MASK = (unsigned int) 0x80000000; /* most significant w-r bits */
	static const unsigned int LOWER_MASK = (unsigned int) 0x7fffffff; /* least significant r bits */
	unsigned int mag01[2];
	unsigned int mt[N]; /* the array for the state vector  */
	unsigned int mti; /* mti==N+1 meansmt[N] is not initialized*/
public:
	unsigned int Seed;
	Random(); /* initializes mt[N] with a seed */
	void Srand(unsigned int s);
	// Int31: a random number on [0,0x7fffffff]-Interval
	int Number(int nLow, int nHigh);
	//a random number on [0,1]-real-Interval */

	double Real();
	double Real(double dfLow, double dfHigh);//poor!!
	//"Unsigned Int 32bit on [0,0xffffffff]-Interval */
	unsigned int uNumber32();
};

#endif
