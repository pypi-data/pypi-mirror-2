// Copyright 2010 Jussi Lepisto

#ifndef VECTOR2F_H
#define VECTOR2F_H

#include <Python.h>
#include <Eigen/Core>

#include "config.h"

typedef struct
{
	PyObject_HEAD
	Eigen::Vector2f vector;
} Vector2f;

extern PyTypeObject Vector2fType;

// Helpers
int Vector2f_Check(PyObject* p);

// Construction
PyObject* Vector2f_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int Vector2f_init(Vector2f* self, PyObject* args, PyObject* kwds);
void Vector2f_dealloc(Vector2f* self);

// Properties
PyObject* Vector2f_get_x(Vector2f* self, void* closure);
int Vector2f_set_x(Vector2f* self, PyObject* value, void* closure);
PyObject* Vector2f_get_y(Vector2f* self, void* closure);
int Vector2f_set_y(Vector2f* self, PyObject* value, void* closure);

PyObject* Vector2f_get_norm(Vector2f* self, void* closure);
PyObject* Vector2f_get_norm_sq(Vector2f* self, void* closure);
PyObject* Vector2f_get_normalized(Vector2f* self, void* closure);
PyObject* Vector2f_get_transpose(Vector2f* self, void* closure);
int Vector2f_set_transpose(Vector2f* self, PyObject* value, void* closure);

// Methods
PyObject* Vector2f_zero(PyTypeObject* cls, PyObject* args);
PyObject* Vector2f_ones(PyTypeObject* cls, PyObject* args);
PyObject* Vector2f_constant(PyTypeObject* cls, PyObject* args);
PyObject* Vector2f_random(PyTypeObject* cls, PyObject* args);
PyObject* Vector2f_unit_x(PyTypeObject* cls, PyObject* args);
PyObject* Vector2f_unit_y(PyTypeObject* cls, PyObject* args);

PyObject* Vector2f_set(Vector2f* self, PyObject* args);
PyObject* Vector2f_set_zero(Vector2f* self, PyObject* noargs);
PyObject* Vector2f_set_ones(Vector2f* self, PyObject* noargs);
PyObject* Vector2f_set_constant(Vector2f* self, PyObject* args);
PyObject* Vector2f_set_random(Vector2f* self, PyObject* noargs);

PyObject* Vector2f_dot(Vector2f* self, PyObject* other);

PyObject* Vector2f_normalize(Vector2f* self, PyObject* noargs);

// Number methods
PyObject* Vector2f_add(PyObject* o1, PyObject* o2);
PyObject* Vector2f_subtract(PyObject* o1, PyObject* o2);
PyObject* Vector2f_multiply(PyObject* o1, PyObject* o2);
PyObject* Vector2f_divide(PyObject* o1, PyObject* o2);
PyObject* Vector2f_negative(PyObject* o);
PyObject* Vector2f_inplace_add(PyObject* o1, PyObject* o2);
PyObject* Vector2f_inplace_subtract(PyObject* o1, PyObject* o2);
PyObject* Vector2f_inplace_multiply(PyObject* o1, PyObject* o2);
PyObject* Vector2f_inplace_divide(PyObject* o1, PyObject* o2);

// Sequence methods
Py_ssize_t Vector2f_length(Vector2f* self);
PyObject* Vector2f_item(Vector2f* self, Py_ssize_t index);
PyObject* Vector2f_slice(Vector2f* self, Py_ssize_t index1,
	Py_ssize_t index2);
int Vector2f_ass_item(Vector2f* self, Py_ssize_t index, PyObject* value);
int Vector2f_ass_slice(Vector2f* self, Py_ssize_t index1, Py_ssize_t index2,
	PyObject* value);

// Special methods
PyObject* Vector2f_repr(Vector2f* self);
PyObject* Vector2f_richcompare(PyObject* a, PyObject* b, int op);

#endif
