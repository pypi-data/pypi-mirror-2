// Copyright 2010 Jussi Lepisto

#ifndef ROWVECTOR2F_H
#define ROWVECTOR2F_H

#include <Python.h>
#include <Eigen/Core>

#include "config.h"

typedef struct
{
	PyObject_HEAD
	Eigen::RowVector2f vector;
} RowVector2f;

extern PyTypeObject RowVector2fType;

// Helpers
int RowVector2f_Check(PyObject* p);

// Construction
PyObject* RowVector2f_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int RowVector2f_init(RowVector2f* self, PyObject* args, PyObject* kwds);
void RowVector2f_dealloc(RowVector2f* self);

// Properties
PyObject* RowVector2f_get_x(RowVector2f* self, void* closure);
int RowVector2f_set_x(RowVector2f* self, PyObject* value, void* closure);
PyObject* RowVector2f_get_y(RowVector2f* self, void* closure);
int RowVector2f_set_y(RowVector2f* self, PyObject* value, void* closure);

PyObject* RowVector2f_get_norm(RowVector2f* self, void* closure);
PyObject* RowVector2f_get_norm_sq(RowVector2f* self, void* closure);
PyObject* RowVector2f_get_normalized(RowVector2f* self, void* closure);
PyObject* RowVector2f_get_transpose(RowVector2f* self, void* closure);
int RowVector2f_set_transpose(RowVector2f* self, PyObject* value,
	void* closure);

// Methods
PyObject* RowVector2f_zero(PyTypeObject* cls, PyObject* args);
PyObject* RowVector2f_ones(PyTypeObject* cls, PyObject* args);
PyObject* RowVector2f_constant(PyTypeObject* cls, PyObject* args);
PyObject* RowVector2f_random(PyTypeObject* cls, PyObject* args);
PyObject* RowVector2f_unit_x(PyTypeObject* cls, PyObject* args);
PyObject* RowVector2f_unit_y(PyTypeObject* cls, PyObject* args);

PyObject* RowVector2f_set(RowVector2f* self, PyObject* args);
PyObject* RowVector2f_set_zero(RowVector2f* self, PyObject* noargs);
PyObject* RowVector2f_set_ones(RowVector2f* self, PyObject* noargs);
PyObject* RowVector2f_set_constant(RowVector2f* self, PyObject* args);
PyObject* RowVector2f_set_random(RowVector2f* self, PyObject* noargs);

PyObject* RowVector2f_dot(RowVector2f* self, PyObject* other);

PyObject* RowVector2f_normalize(RowVector2f* self, PyObject* noargs);

// Number methods
PyObject* RowVector2f_add(PyObject* o1, PyObject* o2);
PyObject* RowVector2f_subtract(PyObject* o1, PyObject* o2);
PyObject* RowVector2f_multiply(PyObject* o1, PyObject* o2);
PyObject* RowVector2f_divide(PyObject* o1, PyObject* o2);
PyObject* RowVector2f_negative(PyObject* o);
PyObject* RowVector2f_inplace_add(PyObject* o1, PyObject* o2);
PyObject* RowVector2f_inplace_subtract(PyObject* o1, PyObject* o2);
PyObject* RowVector2f_inplace_multiply(PyObject* o1, PyObject* o2);
PyObject* RowVector2f_inplace_divide(PyObject* o1, PyObject* o2);

// Sequence methods
Py_ssize_t RowVector2f_length(RowVector2f* self);
PyObject* RowVector2f_item(RowVector2f* self, Py_ssize_t index);
PyObject* RowVector2f_slice(RowVector2f* self, Py_ssize_t index1,
	Py_ssize_t index2);
int RowVector2f_ass_item(RowVector2f* self, Py_ssize_t index,
	PyObject* value);
int RowVector2f_ass_slice(RowVector2f* self, Py_ssize_t index1,
	Py_ssize_t index2, PyObject* value);

// Special methods
PyObject* RowVector2f_repr(RowVector2f* self);
PyObject* RowVector2f_richcompare(PyObject* a, PyObject* b, int op);

#endif
