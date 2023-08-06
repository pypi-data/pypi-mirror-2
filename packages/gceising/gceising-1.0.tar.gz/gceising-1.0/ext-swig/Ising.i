%module (docstring="This is a Python SWIG-wrapped C++ program") Ising
%{
#include <Python.h>
#include <numpy/arrayobject.h>   /* numpy  as seen from C */
#include "nvector.h"
#include "Ising.h"
#ifndef SWIG_IsOK
    #define SWIG_IsOK(r)	 (r >= 0)
#endif
%}

//defined before %include
%define %npswig_typemaps(DATA_TYPE, NPSWIG_DATA_IN, DATA_PY_TYPE)
%typemap(in) DATA_TYPE * NPSWIG_DATA_IN {
	if (PyArray_Check($input))
	{
		PyArrayObject * par=(PyArrayObject *)$input;

		if (par->descr->type_num != DATA_PY_TYPE) {
			PyErr_Format(PyExc_ValueError,"argument must be DATA_PY_TYPE=%d,%d",DATA_PY_TYPE,par->descr->type_num);
			return NULL;
		}
		$1 = ($1_ltype)par->data;
	}else
	{
		int res_np=SWIG_ConvertPtr($input, (void **) &$1, $1_descriptor, 0|0);
	 	if (!SWIG_IsOK(res_np)) {
			PyErr_SetString(PyExc_ValueError,"argument must be Numpy Array or $1_descriptor");
			return NULL;
		}
	}
}
%enddef
//NPY_INT=5,NPY_INT32=7
%npswig_typemaps(double, NPSWIG_DATA_DBLIN, NPY_DOUBLE)
%npswig_typemaps(int, NPSWIG_DATA_INTIN, NPY_INT32)
%npswig_typemaps(char, NPSWIG_DATA_CHRIN, NPY_BYTE)
%npswig_typemaps(unsigned int, NPSWIG_DATA_UIN, NPY_UINT32)

%apply char * NPSWIG_DATA_CHRIN {char * pData,char * pcStates};
%apply int * NPSWIG_DATA_INTIN {int * pData};

%include "typemaps.i"
%apply double *OUTPUT {double * pOutVar};

%include "Random.h"
%include "Ising.h"
%include "nvector.h"


%ignore operator <<;
%template(nvdbl) nvector<double>;
%template(nvint) nvector<int>;
#define QUOTE(s) # s      /* turn s into string "s" */
#define NDIM_CHECK(a, expected_ndim) \
       if (a->nd != expected_ndim) { \
          PyErr_Format(PyExc_ValueError, "%s array is %d-dimensional, expected to be %d-dimensional",\
                         QUOTE(a), a->nd, expected_ndim); \
          return NULL; \
       }
#define DIM_CHECK(a, dim, expected_length) \
       if (a->dimensions[dim] != expected_length) { \
          PyErr_Format(PyExc_ValueError, "%s array has wrong %d-dimension=%d (expected %d)", \
                     QUOTE(a),dim,a->dimensions[dim],expected_length); \
          return NULL; \
       }
#define DIM_GT_CHECK(a, dim, expected_length) \
       if (a->dimensions[dim] < expected_length) { \
          PyErr_Format(PyExc_ValueError, "%s array has wrong %d-dimension=%d (expected %d)", \
                     QUOTE(a),dim,a->dimensions[dim],expected_length); \
          return NULL; \
       }
#define TYPE_CHECK(a, tp) \
       if (a->descr->type_num != tp) { \
          PyErr_Format(PyExc_TypeError, "%s array is not of correct type (%d)", QUOTE(a), tp); \
          return NULL; \
       }
#define NULL_CHECK(a,message) \
		if (a==NULL) {\
			PyErr_Format(PyExc_TypeError, "%s is NULL, %s", QUOTE(a),message); \
          	return NULL;\
     	}
     	
%extend Ising
{

	PyObject* PySetWolff()
	{
		PyArrayObject *stack; npy_intp dims[1];
		dims[0]  = self->m_uN;
		stack = (PyArrayObject *) PyArray_SimpleNew(1, dims, NPY_INT);
		self->m_pClusterStack=(int *)stack->data;
		self->m_dPadd=1-exp(-2.0/self->m_aArgIO[self->AI_TEMPER]);
		return PyArray_Return(stack);
	}
	PyObject* PySetGEWolff()
	{
		PyArrayObject *Seq_p,*Stack_p; npy_intp dims[1];
		dims[0]  = self->m_uN;
		Stack_p = (PyArrayObject *) PyArray_SimpleNew(1, dims, NPY_INT);
		self->m_pClusterStack=(int *)Stack_p->data;
		Seq_p = (PyArrayObject *) PyArray_SimpleNew(1, dims, NPY_INT);
		self->m_pClusterSeq=(int *)Seq_p->data;
		return Py_BuildValue("(OO)",Stack_p,Seq_p);
	}
	PyObject* PyGetEnergyRange()
	{
		PyArrayObject *e; npy_intp dims[1];
		dims[0]  = self->m_uN+1;
		e = (PyArrayObject *) PyArray_SimpleNew(1, dims, NPY_INT);
		int *x;
		for(int n=0;n<dims[0];n++)
		{
			x=(int *)e->data +n;//E(n)
			*x= 4*n-2*self->m_uN;
		}
		return PyArray_Return(e);
	}
	 // hisE[(2N + hami) / 4)]++
	PyObject* PyETraj2Hist(PyObject* _traj,PyObject* _hist,int h0=0)
	{
		PyArrayObject* traj = (PyArrayObject*) PyArray_ContiguousFromObject(_traj, NPY_INT, 0, 0);
		NULL_CHECK(traj,"PyETraj2Hist(traj:numpy.int)");
		NDIM_CHECK(traj,1);

		PyArrayObject* hist = (PyArrayObject*) PyArray_ContiguousFromObject(_hist, NPY_INT, 0, 0);
		NULL_CHECK(hist,"PyETraj2Hist(hist:numpy.int)");
		DIM_CHECK(hist,0,self->m_EN);

        int *trajdata =(int*)traj->data;
        int *histdata =(int*)hist->data;

        for (int n=0;n<self->m_EN;n++)
        	histdata[n]=0;

        for (int c=0; c<traj->dimensions[0]; c++)
            histdata[(2*self->m_uN  + trajdata[c])/4] ++;

        int e0 = 0, e1 = 0;
        for (int c=0;c<self->m_EN;c++)
        {
                if (histdata[c] > h0)
                {
                    e0 = 4*c -2* self->m_uN;
                    break;
                 }
        }
        for (int c=0;c<self->m_EN;c++)
        {
                if (histdata[self->m_EN - c - 1] > h0)
                {
 					e1 =2*self->m_uN -4*c;
                    break;
                 }
        }
        Py_DECREF(traj);
        return Py_BuildValue("(iiO)",e0,e1,hist);
	}
	PyObject* PyMTraj2Hist(PyObject* _traj,PyObject* _hist)
	{
		PyArrayObject* traj = (PyArrayObject*) PyArray_ContiguousFromObject(_traj, NPY_INT, 0, 0);
		NULL_CHECK(traj,"PyTraj2Hist(traj:numpy.int)");
		NDIM_CHECK(traj,1);

		int m_uLen=self->m_uN+1;
		PyArrayObject* hist = (PyArrayObject*) PyArray_ContiguousFromObject(_hist, NPY_INT, 0, 0);
		NULL_CHECK(hist,"PyMTraj2Hist(hist:numpy.int)");
		DIM_CHECK(hist,0,m_uLen);

        int *trajdata =(int*)traj->data;
        int *histdata =(int*)hist->data;

        for (int n=0;n<m_uLen;n++)
        	histdata[n]=0;

        for (int c=0; c<traj->dimensions[0]; c++)
            histdata[(self->m_uN  + trajdata[c])/2] ++;

        int e0 = 0, e1 = 0;
        for (int c=0;c<m_uLen;c++)
        {
                if (histdata[c] > 0)
                {
                    e0 = 2*c- self->m_uN;
                    break;
                 }
        }
        for (int c=0;c<m_uLen;c++)
        {
                if (histdata[m_uLen - c-1] > 0)
                {
 					e1 =self->m_uN -2*c;
                    break;
                 }
        }
        Py_DECREF(traj);
        return Py_BuildValue("(iiO)",e0,e1,hist);
	}

}
%init%{
    import_array();
%}