// Copyright 2010 Jussi Lepisto

#ifndef MATRIX2F_H
#define MATRIX2F_H

#include <Python.h>
#include <Eigen/Core>

#include "config.h"

typedef struct
{
	PyObject_HEAD
	Eigen::Matrix2f matrix;
} Matrix2f;

extern PyTypeObject Matrix2fType;

// Helpers
int Matrix2f_Check(PyObject* p);
int Matrix2f_ParseKey(PyObject* key, int& key1, int& key2);

// Construction
PyObject* Matrix2f_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int Matrix2f_init(Matrix2f* self, PyObject* args, PyObject* kwds);
void Matrix2f_dealloc(Matrix2f* self);

// Properties
PyObject* Matrix2f_get_inverse(Matrix2f* self, void* closure);
PyObject* Matrix2f_get_transpose(Matrix2f* self, void* closure);
int Matrix2f_set_transpose(Matrix2f* self, PyObject* value, void* closure);

// Methods
PyObject* Matrix2f_zero(PyTypeObject* cls, PyObject* args);
PyObject* Matrix2f_ones(PyTypeObject* cls, PyObject* args);
PyObject* Matrix2f_constant(PyTypeObject* cls, PyObject* args);
PyObject* Matrix2f_identity(PyTypeObject* cls, PyObject* args);
PyObject* Matrix2f_random(PyTypeObject* cls, PyObject* args);

PyObject* Matrix2f_set(Matrix2f* self, PyObject* args);
PyObject* Matrix2f_set_zero(Matrix2f* self, PyObject* noargs);
PyObject* Matrix2f_set_ones(Matrix2f* self, PyObject* noargs);
PyObject* Matrix2f_set_identity(Matrix2f* self, PyObject* noargs);
PyObject* Matrix2f_set_constant(Matrix2f* self, PyObject* args);
PyObject* Matrix2f_set_random(Matrix2f* self, PyObject* noargs);

PyObject* Matrix2f_get_col(Matrix2f* self, PyObject* args);
PyObject* Matrix2f_set_col(Matrix2f* self, PyObject* args);
PyObject* Matrix2f_get_row(Matrix2f* self, PyObject* args);
PyObject* Matrix2f_set_row(Matrix2f* self, PyObject* args);

PyObject* Matrix2f_invert(Matrix2f* self, PyObject* noargs);

// Number methods
PyObject* Matrix2f_add(PyObject* o1, PyObject* o2);
PyObject* Matrix2f_subtract(PyObject* o1, PyObject* o2);
PyObject* Matrix2f_multiply(PyObject* o1, PyObject* o2);
PyObject* Matrix2f_divide(PyObject* o1, PyObject* o2);
PyObject* Matrix2f_negative(PyObject* o);
PyObject* Matrix2f_inplace_add(PyObject* o1, PyObject* o2);
PyObject* Matrix2f_inplace_subtract(PyObject* o1, PyObject* o2);
PyObject* Matrix2f_inplace_multiply(PyObject* o1, PyObject* o2);
PyObject* Matrix2f_inplace_divide(PyObject* o1, PyObject* o2);

// Mapping methods
Py_ssize_t Matrix2f_length(Matrix2f* self);
PyObject* Matrix2f_subscript(Matrix2f* self, PyObject* key);
int Matrix2f_ass_subscript(Matrix2f* self, PyObject* key, PyObject* value);

// Special methods
PyObject* Matrix2f_repr(Matrix2f* self);
PyObject* Matrix2f_richcompare(PyObject* a, PyObject* b, int op);

#endif
