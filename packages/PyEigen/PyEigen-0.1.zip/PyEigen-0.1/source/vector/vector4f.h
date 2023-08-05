// Copyright 2010 Jussi Lepisto

#ifndef VECTOR4F_H
#define VECTOR4F_H

#include <Python.h>
#include <Eigen/Core>

#include "config.h"

typedef struct
{
	PyObject_HEAD
	Eigen::Vector4f vector;
} Vector4f;

extern PyTypeObject Vector4fType;

// Helpers
int Vector4f_Check(PyObject* p);

// Construction
PyObject* Vector4f_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int Vector4f_init(Vector4f* self, PyObject* args, PyObject* kwds);
void Vector4f_dealloc(Vector4f* self);

// Properties
PyObject* Vector4f_get_x(Vector4f* self, void* closure);
int Vector4f_set_x(Vector4f* self, PyObject* value, void* closure);
PyObject* Vector4f_get_y(Vector4f* self, void* closure);
int Vector4f_set_y(Vector4f* self, PyObject* value, void* closure);
PyObject* Vector4f_get_z(Vector4f* self, void* closure);
int Vector4f_set_z(Vector4f* self, PyObject* value, void* closure);
PyObject* Vector4f_get_w(Vector4f* self, void* closure);
int Vector4f_set_w(Vector4f* self, PyObject* value, void* closure);

PyObject* Vector4f_get_norm(Vector4f* self, void* closure);
PyObject* Vector4f_get_norm_sq(Vector4f* self, void* closure);
PyObject* Vector4f_get_normalized(Vector4f* self, void* closure);
PyObject* Vector4f_get_transpose(Vector4f* self, void* closure);
int Vector4f_set_transpose(Vector4f* self, PyObject* value, void* closure);

// Methods
PyObject* Vector4f_zero(PyTypeObject* cls, PyObject* args);
PyObject* Vector4f_ones(PyTypeObject* cls, PyObject* args);
PyObject* Vector4f_constant(PyTypeObject* cls, PyObject* args);
PyObject* Vector4f_random(PyTypeObject* cls, PyObject* args);
PyObject* Vector4f_unit_x(PyTypeObject* cls, PyObject* args);
PyObject* Vector4f_unit_y(PyTypeObject* cls, PyObject* args);
PyObject* Vector4f_unit_z(PyTypeObject* cls, PyObject* args);
PyObject* Vector4f_unit_w(PyTypeObject* cls, PyObject* args);

PyObject* Vector4f_set(Vector4f* self, PyObject* args);
PyObject* Vector4f_set_zero(Vector4f* self, PyObject* noargs);
PyObject* Vector4f_set_ones(Vector4f* self, PyObject* noargs);
PyObject* Vector4f_set_constant(Vector4f* self, PyObject* args);
PyObject* Vector4f_set_random(Vector4f* self, PyObject* noargs);

PyObject* Vector4f_dot(Vector4f* self, PyObject* other);

PyObject* Vector4f_normalize(Vector4f* self, PyObject* noargs);

// Number methods
PyObject* Vector4f_add(PyObject* o1, PyObject* o2);
PyObject* Vector4f_subtract(PyObject* o1, PyObject* o2);
PyObject* Vector4f_multiply(PyObject* o1, PyObject* o2);
PyObject* Vector4f_divide(PyObject* o1, PyObject* o2);
PyObject* Vector4f_negative(PyObject* o);
PyObject* Vector4f_inplace_add(PyObject* o1, PyObject* o2);
PyObject* Vector4f_inplace_subtract(PyObject* o1, PyObject* o2);
PyObject* Vector4f_inplace_multiply(PyObject* o1, PyObject* o2);
PyObject* Vector4f_inplace_divide(PyObject* o1, PyObject* o2);

// Sequence methods
Py_ssize_t Vector4f_length(Vector4f* self);
PyObject* Vector4f_item(Vector4f* self, Py_ssize_t index);
PyObject* Vector4f_slice(Vector4f* self, Py_ssize_t index1,
	Py_ssize_t index2);
int Vector4f_ass_item(Vector4f* self, Py_ssize_t index, PyObject* value);
int Vector4f_ass_slice(Vector4f* self, Py_ssize_t index1, Py_ssize_t index2,
	PyObject* value);

// Special methods
PyObject* Vector4f_repr(Vector4f* self);
PyObject* Vector4f_richcompare(PyObject* a, PyObject* b, int op);

#endif
