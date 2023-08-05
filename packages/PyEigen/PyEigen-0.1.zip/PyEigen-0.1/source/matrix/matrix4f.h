// Copyright 2010 Jussi Lepisto

#ifndef MATRIX4F_H
#define MATRIX4F_H

#include <Python.h>
#include <Eigen/Core>

#include "config.h"

typedef struct
{
	PyObject_HEAD
	Eigen::Matrix4f matrix;
} Matrix4f;

extern PyTypeObject Matrix4fType;

// Helpers
int Matrix4f_Check(PyObject* p);
int Matrix4f_ParseKey(PyObject* key, int& key1, int& key2);

// Construction
PyObject* Matrix4f_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int Matrix4f_init(Matrix4f* self, PyObject* args, PyObject* kwds);
void Matrix4f_dealloc(Matrix4f* self);

// Properties
PyObject* Matrix4f_get_inverse(Matrix4f* self, void* closure);
PyObject* Matrix4f_get_transpose(Matrix4f* self, void* closure);
int Matrix4f_set_transpose(Matrix4f* self, PyObject* value, void* closure);

// Methods
PyObject* Matrix4f_zero(PyTypeObject* cls, PyObject* args);
PyObject* Matrix4f_ones(PyTypeObject* cls, PyObject* args);
PyObject* Matrix4f_constant(PyTypeObject* cls, PyObject* args);
PyObject* Matrix4f_identity(PyTypeObject* cls, PyObject* args);
PyObject* Matrix4f_random(PyTypeObject* cls, PyObject* args);

PyObject* Matrix4f_set(Matrix4f* self, PyObject* args);
PyObject* Matrix4f_set_zero(Matrix4f* self, PyObject* noargs);
PyObject* Matrix4f_set_ones(Matrix4f* self, PyObject* noargs);
PyObject* Matrix4f_set_identity(Matrix4f* self, PyObject* noargs);
PyObject* Matrix4f_set_constant(Matrix4f* self, PyObject* args);
PyObject* Matrix4f_set_random(Matrix4f* self, PyObject* noargs);

PyObject* Matrix4f_get_block2(Matrix4f* self, PyObject* args);
PyObject* Matrix4f_set_block2(Matrix4f* self, PyObject* args);
PyObject* Matrix4f_get_block3(Matrix4f* self, PyObject* args);
PyObject* Matrix4f_set_block3(Matrix4f* self, PyObject* args);
PyObject* Matrix4f_get_col(Matrix4f* self, PyObject* args);
PyObject* Matrix4f_set_col(Matrix4f* self, PyObject* args);
PyObject* Matrix4f_get_row(Matrix4f* self, PyObject* args);
PyObject* Matrix4f_set_row(Matrix4f* self, PyObject* args);

PyObject* Matrix4f_invert(Matrix4f* self, PyObject* noargs);

// Number methods
PyObject* Matrix4f_add(PyObject* o1, PyObject* o2);
PyObject* Matrix4f_subtract(PyObject* o1, PyObject* o2);
PyObject* Matrix4f_multiply(PyObject* o1, PyObject* o2);
PyObject* Matrix4f_divide(PyObject* o1, PyObject* o2);
PyObject* Matrix4f_negative(PyObject* o);
PyObject* Matrix4f_inplace_add(PyObject* o1, PyObject* o2);
PyObject* Matrix4f_inplace_subtract(PyObject* o1, PyObject* o2);
PyObject* Matrix4f_inplace_multiply(PyObject* o1, PyObject* o2);
PyObject* Matrix4f_inplace_divide(PyObject* o1, PyObject* o2);

// Mapping methods
Py_ssize_t Matrix4f_length(Matrix4f* self);
PyObject* Matrix4f_subscript(Matrix4f* self, PyObject* key);
int Matrix4f_ass_subscript(Matrix4f* self, PyObject* key, PyObject* value);

// Special methods
PyObject* Matrix4f_repr(Matrix4f* self);
PyObject* Matrix4f_richcompare(PyObject* a, PyObject* b, int op);

#endif
