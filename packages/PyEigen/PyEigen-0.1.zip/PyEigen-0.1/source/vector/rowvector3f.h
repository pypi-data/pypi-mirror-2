// Copyright 2010 Jussi Lepisto

#ifndef ROWVECTOR3F_H
#define ROWVECTOR3F_H

#include <Python.h>
#include <Eigen/Core>

#include "config.h"

typedef struct
{
	PyObject_HEAD
	Eigen::RowVector3f vector;
} RowVector3f;

extern PyTypeObject RowVector3fType;

// Helpers
int RowVector3f_Check(PyObject* p);

// Construction
PyObject* RowVector3f_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int RowVector3f_init(RowVector3f* self, PyObject* args, PyObject* kwds);
void RowVector3f_dealloc(RowVector3f* self);

// Properties
PyObject* RowVector3f_get_x(RowVector3f* self, void* closure);
int RowVector3f_set_x(RowVector3f* self, PyObject* value, void* closure);
PyObject* RowVector3f_get_y(RowVector3f* self, void* closure);
int RowVector3f_set_y(RowVector3f* self, PyObject* value, void* closure);
PyObject* RowVector3f_get_z(RowVector3f* self, void* closure);
int RowVector3f_set_z(RowVector3f* self, PyObject* value, void* closure);

PyObject* RowVector3f_get_norm(RowVector3f* self, void* closure);
PyObject* RowVector3f_get_norm_sq(RowVector3f* self, void* closure);
PyObject* RowVector3f_get_normalized(RowVector3f* self, void* closure);
PyObject* RowVector3f_get_transpose(RowVector3f* self, void* closure);
int RowVector3f_set_transpose(RowVector3f* self, PyObject* value,
	void* closure);

// Methods
PyObject* RowVector3f_zero(PyTypeObject* cls, PyObject* args);
PyObject* RowVector3f_ones(PyTypeObject* cls, PyObject* args);
PyObject* RowVector3f_constant(PyTypeObject* cls, PyObject* args);
PyObject* RowVector3f_random(PyTypeObject* cls, PyObject* args);
PyObject* RowVector3f_unit_x(PyTypeObject* cls, PyObject* args);
PyObject* RowVector3f_unit_y(PyTypeObject* cls, PyObject* args);
PyObject* RowVector3f_unit_z(PyTypeObject* cls, PyObject* args);

PyObject* RowVector3f_set(RowVector3f* self, PyObject* args);
PyObject* RowVector3f_set_zero(RowVector3f* self, PyObject* noargs);
PyObject* RowVector3f_set_ones(RowVector3f* self, PyObject* noargs);
PyObject* RowVector3f_set_constant(RowVector3f* self, PyObject* args);
PyObject* RowVector3f_set_random(RowVector3f* self, PyObject* noargs);

PyObject* RowVector3f_dot(RowVector3f* self, PyObject* other);
PyObject* RowVector3f_cross(RowVector3f* self, PyObject* other);

PyObject* RowVector3f_normalize(RowVector3f* self, PyObject* noargs);

// Number methods
PyObject* RowVector3f_add(PyObject* o1, PyObject* o2);
PyObject* RowVector3f_subtract(PyObject* o1, PyObject* o2);
PyObject* RowVector3f_multiply(PyObject* o1, PyObject* o2);
PyObject* RowVector3f_divide(PyObject* o1, PyObject* o2);
PyObject* RowVector3f_negative(PyObject* o);
PyObject* RowVector3f_inplace_add(PyObject* o1, PyObject* o2);
PyObject* RowVector3f_inplace_subtract(PyObject* o1, PyObject* o2);
PyObject* RowVector3f_inplace_multiply(PyObject* o1, PyObject* o2);
PyObject* RowVector3f_inplace_divide(PyObject* o1, PyObject* o2);

// Sequence methods
Py_ssize_t RowVector3f_length(RowVector3f* self);
PyObject* RowVector3f_item(RowVector3f* self, Py_ssize_t index);
PyObject* RowVector3f_slice(RowVector3f* self, Py_ssize_t index1,
	Py_ssize_t index2);
int RowVector3f_ass_item(RowVector3f* self, Py_ssize_t index,
	PyObject* value);
int RowVector3f_ass_slice(RowVector3f* self, Py_ssize_t index1,
	Py_ssize_t index2, PyObject* value);

// Special methods
PyObject* RowVector3f_repr(RowVector3f* self);
PyObject* RowVector3f_richcompare(PyObject* a, PyObject* b, int op);

#endif
