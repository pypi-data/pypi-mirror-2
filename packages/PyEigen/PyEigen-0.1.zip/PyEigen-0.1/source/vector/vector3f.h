// Copyright 2010 Jussi Lepisto

#ifndef VECTOR3F_H
#define VECTOR3F_H

#include <Python.h>
#include <Eigen/Core>

#include "config.h"

typedef struct
{
	PyObject_HEAD
	Eigen::Vector3f vector;
} Vector3f;

extern PyTypeObject Vector3fType;

// Helpers
int Vector3f_Check(PyObject* p);

// Construction
PyObject* Vector3f_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int Vector3f_init(Vector3f* self, PyObject* args, PyObject* kwds);
void Vector3f_dealloc(Vector3f* self);

// Properties
PyObject* Vector3f_get_x(Vector3f* self, void* closure);
int Vector3f_set_x(Vector3f* self, PyObject* value, void* closure);
PyObject* Vector3f_get_y(Vector3f* self, void* closure);
int Vector3f_set_y(Vector3f* self, PyObject* value, void* closure);
PyObject* Vector3f_get_z(Vector3f* self, void* closure);
int Vector3f_set_z(Vector3f* self, PyObject* value, void* closure);

PyObject* Vector3f_get_norm(Vector3f* self, void* closure);
PyObject* Vector3f_get_norm_sq(Vector3f* self, void* closure);
PyObject* Vector3f_get_normalized(Vector3f* self, void* closure);
PyObject* Vector3f_get_transpose(Vector3f* self, void* closure);
int Vector3f_set_transpose(Vector3f* self, PyObject* value, void* closure);

// Methods
PyObject* Vector3f_zero(PyTypeObject* cls, PyObject* args);
PyObject* Vector3f_ones(PyTypeObject* cls, PyObject* args);
PyObject* Vector3f_constant(PyTypeObject* cls, PyObject* args);
PyObject* Vector3f_random(PyTypeObject* cls, PyObject* args);
PyObject* Vector3f_unit_x(PyTypeObject* cls, PyObject* args);
PyObject* Vector3f_unit_y(PyTypeObject* cls, PyObject* args);
PyObject* Vector3f_unit_z(PyTypeObject* cls, PyObject* args);

PyObject* Vector3f_set(Vector3f* self, PyObject* args);
PyObject* Vector3f_set_zero(Vector3f* self, PyObject* noargs);
PyObject* Vector3f_set_ones(Vector3f* self, PyObject* noargs);
PyObject* Vector3f_set_constant(Vector3f* self, PyObject* args);
PyObject* Vector3f_set_random(Vector3f* self, PyObject* noargs);

PyObject* Vector3f_dot(Vector3f* self, PyObject* other);
PyObject* Vector3f_cross(Vector3f* self, PyObject* other);

PyObject* Vector3f_normalize(Vector3f* self, PyObject* noargs);

// Number methods
PyObject* Vector3f_add(PyObject* o1, PyObject* o2);
PyObject* Vector3f_subtract(PyObject* o1, PyObject* o2);
PyObject* Vector3f_multiply(PyObject* o1, PyObject* o2);
PyObject* Vector3f_divide(PyObject* o1, PyObject* o2);
PyObject* Vector3f_negative(PyObject* o);
PyObject* Vector3f_inplace_add(PyObject* o1, PyObject* o2);
PyObject* Vector3f_inplace_subtract(PyObject* o1, PyObject* o2);
PyObject* Vector3f_inplace_multiply(PyObject* o1, PyObject* o2);
PyObject* Vector3f_inplace_divide(PyObject* o1, PyObject* o2);

// Sequence methods
Py_ssize_t Vector3f_length(Vector3f* self);
PyObject* Vector3f_item(Vector3f* self, Py_ssize_t index);
PyObject* Vector3f_slice(Vector3f* self, Py_ssize_t index1,
	Py_ssize_t index2);
int Vector3f_ass_item(Vector3f* self, Py_ssize_t index, PyObject* value);
int Vector3f_ass_slice(Vector3f* self, Py_ssize_t index1, Py_ssize_t index2,
	PyObject* value);

// Special methods
PyObject* Vector3f_repr(Vector3f* self);
PyObject* Vector3f_richcompare(PyObject* a, PyObject* b, int op);

#endif
