// Copyright 2010 Jussi Lepisto

#ifndef MATRIX3F_H
#define MATRIX3F_H

#include <Python.h>
#include <Eigen/Core>

#include "config.h"

typedef struct
{
	PyObject_HEAD
	Eigen::Matrix3f matrix;
} Matrix3f;

extern PyTypeObject Matrix3fType;

// Helpers
int Matrix3f_Check(PyObject* p);
int Matrix3f_ParseKey(PyObject* key, int& key1, int& key2);

// Construction
PyObject* Matrix3f_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int Matrix3f_init(Matrix3f* self, PyObject* args, PyObject* kwds);
void Matrix3f_dealloc(Matrix3f* self);

// Properties
PyObject* Matrix3f_get_inverse(Matrix3f* self, void* closure);
PyObject* Matrix3f_get_transpose(Matrix3f* self, void* closure);
int Matrix3f_set_transpose(Matrix3f* self, PyObject* value, void* closure);

// Methods
PyObject* Matrix3f_zero(PyTypeObject* cls, PyObject* args);
PyObject* Matrix3f_ones(PyTypeObject* cls, PyObject* args);
PyObject* Matrix3f_constant(PyTypeObject* cls, PyObject* args);
PyObject* Matrix3f_identity(PyTypeObject* cls, PyObject* args);
PyObject* Matrix3f_random(PyTypeObject* cls, PyObject* args);

PyObject* Matrix3f_set(Matrix3f* self, PyObject* args);
PyObject* Matrix3f_set_zero(Matrix3f* self, PyObject* noargs);
PyObject* Matrix3f_set_ones(Matrix3f* self, PyObject* noargs);
PyObject* Matrix3f_set_identity(Matrix3f* self, PyObject* noargs);
PyObject* Matrix3f_set_constant(Matrix3f* self, PyObject* args);
PyObject* Matrix3f_set_random(Matrix3f* self, PyObject* noargs);

PyObject* Matrix3f_get_block2(Matrix3f* self, PyObject* args);
PyObject* Matrix3f_set_block2(Matrix3f* self, PyObject* args);
PyObject* Matrix3f_get_col(Matrix3f* self, PyObject* args);
PyObject* Matrix3f_set_col(Matrix3f* self, PyObject* args);
PyObject* Matrix3f_get_row(Matrix3f* self, PyObject* args);
PyObject* Matrix3f_set_row(Matrix3f* self, PyObject* args);

PyObject* Matrix3f_invert(Matrix3f* self, PyObject* noargs);

// Number methods
PyObject* Matrix3f_add(PyObject* o1, PyObject* o2);
PyObject* Matrix3f_subtract(PyObject* o1, PyObject* o2);
PyObject* Matrix3f_multiply(PyObject* o1, PyObject* o2);
PyObject* Matrix3f_divide(PyObject* o1, PyObject* o2);
PyObject* Matrix3f_negative(PyObject* o);
PyObject* Matrix3f_inplace_add(PyObject* o1, PyObject* o2);
PyObject* Matrix3f_inplace_subtract(PyObject* o1, PyObject* o2);
PyObject* Matrix3f_inplace_multiply(PyObject* o1, PyObject* o2);
PyObject* Matrix3f_inplace_divide(PyObject* o1, PyObject* o2);

// Mapping methods
Py_ssize_t Matrix3f_length(Matrix3f* self);
PyObject* Matrix3f_subscript(Matrix3f* self, PyObject* key);
int Matrix3f_ass_subscript(Matrix3f* self, PyObject* key, PyObject* value);

// Special methods
PyObject* Matrix3f_repr(Matrix3f* self);
PyObject* Matrix3f_richcompare(PyObject* a, PyObject* b, int op);

#endif
