#include <sys/param.h>

#include <Python.h>
#include "py3c/py3c.h"

PyDoc_STRVAR(Module_Doc,
"Module for helping verify string-related *Check functions."
);

/*
 * I'd really love to DRY this via function pointers, but given that PyBytes_Check,
 * etc, are macros, this is non-trivial
 *
 * I don't care enough to jump through hoops to make this work.
 */

PyObject*
is_pybytes(PyObject *self, PyObject *args)
{
	PyObject *test_obj = NULL;

	if (!PyArg_ParseTuple(args, "O:test_obj", &test_obj))
		return NULL;

	if (PyBytes_Check(test_obj))
		Py_RETURN_TRUE;
	Py_RETURN_FALSE;
}

PyObject*
is_pystr(PyObject *self, PyObject *args)
{
	PyObject *test_obj = NULL;

	if (!PyArg_ParseTuple(args, "O:test_obj", &test_obj))
		return NULL;

	if (PyStr_Check(test_obj))
		Py_RETURN_TRUE;
	Py_RETURN_FALSE;
}

#if	PY2
PyObject*
is_pystring(PyObject *self, PyObject *args)
{
	PyObject *test_obj = NULL;

	if (!PyArg_ParseTuple(args, "O:test_obj", &test_obj))
		return NULL;

	if (PyString_Check(test_obj))
		Py_RETURN_TRUE;
	Py_RETURN_FALSE;
}
#endif

PyObject*
is_pyunicode(PyObject *self, PyObject *args)
{
	PyObject *test_obj = NULL;

	if (!PyArg_ParseTuple(args, "O:test_obj", &test_obj))
		return NULL;

	if (PyUnicode_Check(test_obj))
		Py_RETURN_TRUE;
	Py_RETURN_FALSE;
}

static PyMethodDef Module_Methods[] = {
	{"is_PyBytes", is_pybytes, METH_VARARGS, "Run PyBytes_Check"},
	{"is_PyStr", is_pystr, METH_VARARGS, "Run PyStr_Check."},
#if	PY2
	{"is_PyString", is_pystring, METH_VARARGS, "Run PyString_Check."},
#endif
	{"is_PyUnicode", is_pyunicode, METH_VARARGS, "Run PyUnicode_Check."},
	{}
};

static PyModuleDef module_definition = {
	.m_base = PyModuleDef_HEAD_INIT,
	.m_name = "pystr_demo_c_ext",
	.m_doc = Module_Doc,
	.m_size = -1,
	.m_methods = Module_Methods
};

MODULE_INIT_FUNC(pystr_demo_c_ext)
{
	PyObject *mod = NULL;

	mod = PyModule_Create(&module_definition);
	if (mod == NULL)
		goto out;

out:
	return mod;
}
