// Copyright 2010 Jussi Lepisto

#include <Python.h>

#include "matrix/matrix2f.h"
#include "matrix/matrix3f.h"
#include "matrix/matrix4f.h"
#include "vector/rowvector2f.h"
#include "vector/rowvector3f.h"
#include "vector/rowvector4f.h"
#include "vector/vector2f.h"
#include "vector/vector3f.h"
#include "vector/vector4f.h"

// Uncomment for row-major matrix / vector classes
// #define EIGEN_DEFAULT_TO_ROW_MAJOR

static PyMethodDef methods[] = {
	{NULL}
};


#ifndef PyMODINIT_FUNC
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC initpyeigen()
{
	PyObject* module;

	module = Py_InitModule3("pyeigen", methods,
"PyEigen is a Python wrapper for the C++ linear algebra library Eigen.");

	if(PyType_Ready(&Matrix2fType) >= 0)
	{
		Py_INCREF(&Matrix2fType);
		PyModule_AddObject(module, "Matrix2f", (PyObject*)&Matrix2fType);
	}
	if(PyType_Ready(&Matrix3fType) >= 0)
	{
		Py_INCREF(&Matrix3fType);
		PyModule_AddObject(module, "Matrix3f", (PyObject*)&Matrix3fType);
	}
	if(PyType_Ready(&Matrix4fType) >= 0)
	{
		Py_INCREF(&Matrix4fType);
		PyModule_AddObject(module, "Matrix4f", (PyObject*)&Matrix4fType);
	}

	if(PyType_Ready(&RowVector2fType) >= 0)
	{
		Py_INCREF(&RowVector2fType);
		PyModule_AddObject(module, "RowVector2f",
			(PyObject*)&RowVector2fType);
	}
	if(PyType_Ready(&RowVector3fType) >= 0)
	{
		Py_INCREF(&RowVector3fType);
		PyModule_AddObject(module, "RowVector3f",
			(PyObject*)&RowVector3fType);
	}
	if(PyType_Ready(&RowVector4fType) >= 0)
	{
		Py_INCREF(&RowVector4fType);
		PyModule_AddObject(module, "RowVector4f",
			(PyObject*)&RowVector4fType);
	}

	if(PyType_Ready(&Vector2fType) >= 0)
	{
		Py_INCREF(&Vector2fType);
		PyModule_AddObject(module, "Vector2f", (PyObject*)&Vector2fType);
	}
	if(PyType_Ready(&Vector3fType) >= 0)
	{
		Py_INCREF(&Vector3fType);
		PyModule_AddObject(module, "Vector3f", (PyObject*)&Vector3fType);
	}
	if(PyType_Ready(&Vector4fType) >= 0)
	{
		Py_INCREF(&Vector4fType);
		PyModule_AddObject(module, "Vector4f", (PyObject*)&Vector4fType);
	}
}
