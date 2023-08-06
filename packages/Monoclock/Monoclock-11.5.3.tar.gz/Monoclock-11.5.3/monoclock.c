#include <Python.h>
#include <time.h>


static PyObject *
nano_count(PyObject *self, PyObject *args) {
	struct timespec t;
	int ret;
	PY_LONG_LONG nanoseconds;

	if(!PyArg_ParseTuple(args, "")) {
		return NULL;
	}

	ret = clock_gettime(CLOCK_MONOTONIC, &t);
	if(ret != 0) {
		PyErr_SetString(PyExc_SystemError,
			"clock_gettime failed");
		return NULL;
	}
	nanoseconds = (PY_LONG_LONG)t.tv_sec * 1000000000 + t.tv_nsec;
	return PyLong_FromUnsignedLongLong(nanoseconds);
}


static PyMethodDef MonoclockMethods[] = {
	{"nano_count", nano_count, METH_VARARGS,
	"Get the monotonic clock value, in nanoseconds."},
	{NULL, NULL, 0, NULL} /* Sentinel */
};


PyMODINIT_FUNC
initmonoclock(void)
{
	(void) Py_InitModule("monoclock", MonoclockMethods);
}
