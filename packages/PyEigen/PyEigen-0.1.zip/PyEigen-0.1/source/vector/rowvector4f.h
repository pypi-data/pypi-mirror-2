// Copyright 2010 Jussi Lepisto

#ifndef ROWVECTOR4F_H
#define ROWVECTOR4F_H

#include <Python.h>
#include <Eigen/Core>

#include "config.h"

typedef struct
{
	PyObject_HEAD
	Eigen::RowVector4f vector;
} RowVector4f;

extern PyTypeObject RowVector4fType;

// Helpers
int RowVector4f_Check(PyObject* p);

// Construction
PyObject* RowVector4f_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int RowVector4f_init(RowVector4f* self, PyObject* args, PyObject* kwds);
void RowVector4f_dealloc(RowVector4f* self);

// Properties
PyObject* RowVector4f_get_x(RowVector4f* self, void* closure);
int RowVector4f_set_x(RowVector4f* self, PyObject* value, void* closure);
PyObject* RowVector4f_get_y(RowVector4f* self, void* closure);
int RowVector4f_set_y(RowVector4f* self, PyObject* value, void* closure);
PyObject* RowVector4f_get_z(RowVector4f* self, void* closure);
int RowVector4f_set_z(RowVector4f* self, PyObject* value, void* closure);
PyObject* RowVector4f_get_w(RowVector4f* self, void* closure);
int RowVector4f_set_w(RowVector4f* self, PyObject* value, void* closure);

PyObject* RowVector4f_get_norm(RowVector4f* self, void* closure);
PyObject* RowVector4f_get_norm_sq(RowVector4f* self, void* closure);
PyObject* RowVector4f_get_normalized(RowVector4f* self, void* closure);
PyObject* RowVector4f_get_transpose(RowVector4f* self, void* closure);
int RowVector4f_set_transpose(RowVector4f* self, PyObject* value,
	void* closure);

// Methods
PyObject* RowVector4f_zero(PyTypeObject* cls, PyObject* args);
PyObject* RowVector4f_ones(PyTypeObject* cls, PyObject* args);
PyObject* RowVector4f_constant(PyTypeObject* cls, PyObject* args);
PyObject* RowVector4f_random(PyTypeObject* cls, PyObject* args);
PyObject* RowVector4f_unit_x(PyTypeObject* cls, PyObject* args);
PyObject* RowVector4f_unit_y(PyTypeObject* cls, PyObject* args);
PyObject* RowVector4f_unit_z(PyTypeObject* cls, PyObject* args);
PyObject* RowVector4f_unit_w(PyTypeObject* cls, PyObject* args);

PyObject* RowVector4f_set(RowVector4f* self, PyObject* args);
PyObject* RowVector4f_set_zero(RowVector4f* self, PyObject* noargs);
PyObject* RowVector4f_set_ones(RowVector4f* self, PyObject* noargs);
PyObject* RowVector4f_set_constant(RowVector4f* self, PyObject* args);
PyObject* RowVector4f_set_random(RowVector4f* self, PyObject* noargs);

PyObject* RowVector4f_dot(RowVector4f* self, PyObject* other);

PyObject* RowVector4f_normalize(RowVector4f* self, PyObject* noargs);

// Number methods
PyObject* RowVector4f_add(PyObject* o1, PyObject* o2);
PyObject* RowVector4f_subtract(PyObject* o1, PyObject* o2);
PyObject* RowVector4f_multiply(PyObject* o1, PyObject* o2);
PyObject* RowVector4f_divide(PyObject* o1, PyObject* o2);
PyObject* RowVector4f_negative(PyObject* o);
PyObject* RowVector4f_inplace_add(PyObject* o1, PyObject* o2);
PyObject* RowVector4f_inplace_subtract(PyObject* o1, PyObject* o2);
PyObject* RowVector4f_inplace_multiply(PyObject* o1, PyObject* o2);
PyObject* RowVector4f_inplace_divide(PyObject* o1, PyObject* o2);

// Sequence methods
Py_ssize_t RowVector4f_length(RowVector4f* self);
PyObject* RowVector4f_item(RowVector4f* self, Py_ssize_t index);
PyObject* RowVector4f_slice(RowVector4f* self, Py_ssize_t index1,
	Py_ssize_t index2);
int RowVector4f_ass_item(RowVector4f* self, Py_ssize_t index,
	PyObject* value);
int RowVector4f_ass_slice(RowVector4f* self, Py_ssize_t index1,
	Py_ssize_t index2, PyObject* value);

// Special methods
PyObject* RowVector4f_repr(RowVector4f* self);
PyObject* RowVector4f_richcompare(PyObject* a, PyObject* b, int op);

#endif
