/* Hadamard Transform

   Usage: w = hadamard(x)
   x must be a REAL VALUED COLUMN VECTOR or MATRIX
   m = size(x,1) must be a POWER OF TWO
   
   Notes:
   1) This implementation uses exactly m*log2(m) additions/subtractions.
   2) This is symmetric and orthogonal. To invert, apply again and
   divide by vector length.
*/

#include "Python.h"
#include "arrayobject.h"

#define DIND1(a, i) *((double *) PyArray_GETPTR1(a, i))
#define DIND2(a, i, j) *((double *) PyArray_GETPTR2(a, i, j))

static PyObject *fht1(PyObject *self, PyObject *args);
static PyObject *fht2(PyObject *self, PyObject *args);
void hadamard_apply_vector(PyArrayObject *y, PyArrayObject *x, unsigned m);

static PyMethodDef _py_hadamardMethods[] = {
  {"fht1", fht1, METH_VARARGS},
  {"fht2", fht2, METH_VARARGS},
  {NULL, NULL}     /* Sentinel - marks the end of this structure */
};

void init_C_fht()  {
  (void) Py_InitModule("_C_fht", _py_hadamardMethods);
  import_array();  // Must be present for NumPy.  Called first after above line.
  Py_Initialize();
}

static PyObject *fht1(PyObject *self, PyObject *args)
{
  /* Input and output matrices to be extracted from args */
  PyArrayObject *vector_in, *vector_out;
  /*integers : dimension of the input and output array */
  int dim0;
  unsigned bit, j, k;
  double temp;
  /* Parse tuples separately since args will differ between C fcns */
  if (!PyArg_ParseTuple(args, "O!O!", &PyArray_Type, &vector_in,
			&PyArray_Type, &vector_out))
    return NULL;
  /*Raise errors if input vector is missing*/
  /* Get vector dimensions. */
  dim0 = vector_in->dimensions[0];
  for (j = 0; j < dim0; j+=2) {
    k = j+1;
    DIND1(vector_out, j) = DIND1(vector_in, j) + DIND1(vector_in, k);
    DIND1(vector_out, k) = DIND1(vector_in, j) - DIND1(vector_in, k);
  }
  for (bit = 2; bit < dim0; bit <<= 1) {   
    for (j = 0; j < dim0; j++) {
      if( (bit & j) == 0 ) {
	k = j | bit;
	temp = DIND1(vector_out, j);
	DIND1(vector_out, j) = DIND1(vector_out, j) + DIND1(vector_out, k);
	DIND1(vector_out, k) = temp - DIND1(vector_out, k);
      }
    }
  }
  return Py_BuildValue("d", 1.);
}

static PyObject *fht2(PyObject *self, PyObject *args) {
  PyArrayObject *arr1, *oarr;
  int dim1, dim2;
  unsigned bit, i, j, k;
  double temp;
  if (!PyArg_ParseTuple(args, "O!O!", &PyArray_Type, &arr1,
			&PyArray_Type, &oarr)) return NULL;
  dim1 = arr1->dimensions[0];
  dim2 = arr1->dimensions[1];
  /* First loop on the first axis (time) */
  #pragma omp parallel shared(arr1, oarr, dim1, dim2) private(i, j, k, bit, temp)
  #pragma omp for
  for (i = 0; i < dim1; i++) {
    /* Hadamard transform on the other axis*/
    for (j = 0; j < dim2; j+=2) {
      k = j+1;
      DIND2(oarr, i, j) = DIND2(arr1, i, j) + DIND2(arr1, i, k);
      DIND2(oarr, i, k) = DIND2(arr1, i, j) - DIND2(arr1, i, k);
    }
    for (bit = 2; bit < dim2; bit <<= 1) {   
      for (j = 0; j < dim2; j++) {
	if( (bit & j) == 0 ) {
	  k = j | bit;
	  temp = DIND2(oarr, i, j);
	  DIND2(oarr, i, j) = DIND2(oarr, i, j) + DIND2(oarr, i, k);
	  DIND2(oarr, i, k) = temp - DIND2(oarr, i, k);
	}
      }
    }
  }
  return Py_BuildValue("d", 1.);
}
