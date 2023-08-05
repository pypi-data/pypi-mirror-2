// Copyright 2010 Jussi Lepisto

#include "rowvector4f.h"

#include <Eigen/Array>
#include <Eigen/Geometry>

#include "util/macros.h"
#include "vector/vector4f.h"


// Structures
PyGetSetDef RowVector4f_getset[] = {
	{"x", (getter)RowVector4f_get_x, (setter)RowVector4f_set_x,
	 "The first coefficient of this vector.", NULL},
	{"y", (getter)RowVector4f_get_y, (setter)RowVector4f_set_y,
	 "The second coefficient of this vector.", NULL},
	{"z", (getter)RowVector4f_get_z, (setter)RowVector4f_set_z,
	 "The third coefficient of this vector.", NULL},
	{"w", (getter)RowVector4f_get_w, (setter)RowVector4f_set_w,
	 "The fourth coefficient of this vector.", NULL},

	{"norm",		(getter)RowVector4f_get_norm,			NULL,
	 "Norm of this vector.", NULL},
	{"norm_sq",		(getter)RowVector4f_get_norm_sq,		NULL,
	 "Squared norm of this vector.", NULL},
	{"normalized",	(getter)RowVector4f_get_normalized,		NULL,
	 "This vector divided by its norm.", NULL},
	{"transpose",
	 (getter)RowVector4f_get_transpose, (setter)RowVector4f_set_transpose,
	 "Transpose of this vector.", NULL},

	{NULL}
};

PyMethodDef RowVector4f_methods[] = {
	{"zero",		(PyCFunction)RowVector4f_zero,
	 METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional zero row vector."},
	{"ones",		(PyCFunction)RowVector4f_ones,
	 METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional row vector where all coefficients equal one."},
	{"constant",	(PyCFunction)RowVector4f_constant,
	 METH_CLASS | METH_VARARGS,
	 "Return a 4-dimensional constant row vector."},
	{"random",		(PyCFunction)RowVector4f_random,
	 METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional random row vector."},
	{"unit_x",		(PyCFunction)RowVector4f_unit_x,
	 METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional X axis unit row vector."},
	{"unit_y",		(PyCFunction)RowVector4f_unit_y,
	 METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional Y axis unit row vector."},
	{"unit_z",		(PyCFunction)RowVector4f_unit_z,
	 METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional Z axis unit row vector."},
	{"unit_w",		(PyCFunction)RowVector4f_unit_w,
	 METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional W axis unit row vector."},

	{"set",				(PyCFunction)RowVector4f_set,			METH_VARARGS,
	 "Set all coefficients of this vector."},
	{"set_zero",		(PyCFunction)RowVector4f_set_zero,		METH_NOARGS,
	 "Set all coefficients of this vector to zero."},
	{"set_ones",		(PyCFunction)RowVector4f_set_ones,		METH_NOARGS,
	 "Set all coefficients of this vector to one."},
	{"set_constant",	(PyCFunction)RowVector4f_set_constant,	METH_VARARGS,
	 "Set all coefficients of this vector to a constant."},
	{"set_random",		(PyCFunction)RowVector4f_set_random,	METH_NOARGS,
	 "Set all coefficients of this vector to random values."},

	{"dot",				(PyCFunction)RowVector4f_dot,			METH_O,
	 "The dot product of this vector with the other vector."},

	{"normalize",		(PyCFunction)RowVector4f_normalize,		METH_NOARGS,
	 "Normalizes this vector, i.e. divides it by its own norm."},

	{NULL}
};

PyNumberMethods RowVector4f_numbermethods = {
	RowVector4f_add,				// nb_add
	RowVector4f_subtract,			// nb_subtract
	RowVector4f_multiply,			// nb_multiply
	RowVector4f_divide,				// nb_divide
	0,								// nb_remainder
	0,								// nb_divmod
	0,								// nb_power
	RowVector4f_negative,			// nb_negative
	0,								// nb_positive
	0,								// nb_absolute
	0,								// nb_nonzero
	0,								// nb_invert
	0,								// nb_lshift
	0,								// nb_rshift
	0,								// nb_and
	0,								// nb_xor
	0,								// nb_or
	0,								// nb_coerce
	0,								// nb_int
	0,								// nb_long
	0,								// nb_float
	0,								// nb_oct
	0,								// nb_hex
	RowVector4f_inplace_add,		// nb_inplace_add
	RowVector4f_inplace_subtract,	// nb_inplace_subtract
	RowVector4f_inplace_multiply,	// nb_inplace_multiply
	RowVector4f_inplace_divide,		// nb_inplace_divide
};

PySequenceMethods RowVector4f_sequencemethods = {
	(lenfunc)RowVector4f_length,					// sq_length
	0,												// sq_concat
	0,												// sq_repeat
	(ssizeargfunc)RowVector4f_item,					// sq_item
	(ssizessizeargfunc)RowVector4f_slice,			// sq_slice
	(ssizeobjargproc)RowVector4f_ass_item,			// sq_ass_item
	(ssizessizeobjargproc)RowVector4f_ass_slice,	// sq_ass_slice
};

PyTypeObject RowVector4fType = {
	PyObject_HEAD_INIT(NULL)

	0,								// ob_size
	"pyeigen.RowVector4f",			// tp_name
	sizeof(RowVector4f),			// tp_basicsize
	0,								// tp_itemsize
	0,								// tp_dealloc
	0,								// tp_print
	0,								// tp_getattr
	0,								// tp_setattr
	0,								// tp_compare
	(reprfunc)RowVector4f_repr,		// tp_repr
	&RowVector4f_numbermethods,		// tp_as_number
	&RowVector4f_sequencemethods,	// tp_as_sequence
	0,								// tp_as_mapping
	0,								// tp_hash
	0,								// tp_call
	0,								// tp_str
	0,								// tp_getattro
	0,								// tp_setattro
	0,								// tp_as_buffer
	Py_TPFLAGS_DEFAULT |			// tp_flags
	Py_TPFLAGS_BASETYPE |
	Py_TPFLAGS_CHECKTYPES,
	"4-dimensional vector with float elements",	// tp_doc
	0,								// tp_traverse
	0,								// tp_clear
	RowVector4f_richcompare,		// tp_richcompare
	0,								// tp_weaklistoffset
	0,								// tp_iter
	0,								// tp_iternext
	RowVector4f_methods,			// tp_methods
	0,								// tp_members
	RowVector4f_getset,				// tp_getset
	0,								// tp_base
	0,								// tp_dict
	0,								// tp_descr_get
	0,								// tp_descr_set
	0,								// tp_dictoffset
	(initproc)RowVector4f_init,		// tp_init
	0,								// tp_alloc
	RowVector4f_new,				// tp_new
	0,								// tp_free
	0,								// tp_is_gc
	0,								// tp_bases
	0,								// tp_mro
	0,								// tp_cache
	0,								// tp_subclasses
	0,								// tp_weaklist
	0,								// tp_del
};

// Helpers
int RowVector4f_Check(PyObject* p)
{
	return p->ob_type == &RowVector4fType;
}

// Construction
PyObject* RowVector4f_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
	return type->tp_alloc(type, 0);
}

int RowVector4f_init(RowVector4f* self, PyObject* args, PyObject* kwds)
{
	if(PySequence_Length(args) > 0)
		if(!RowVector4f_set(self, args))
			return -1;

	return 0;
}

// Properties
PyObject* RowVector4f_get_x(RowVector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.x());
}

int RowVector4f_set_x(RowVector4f* self, PyObject* value, void* closure)
{
	self->vector.x() = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

PyObject* RowVector4f_get_y(RowVector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.y());
}

int RowVector4f_set_y(RowVector4f* self, PyObject* value, void* closure)
{
	self->vector.y() = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

PyObject* RowVector4f_get_z(RowVector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.z());
}

int RowVector4f_set_z(RowVector4f* self, PyObject* value, void* closure)
{
	self->vector.z() = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

PyObject* RowVector4f_get_w(RowVector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.w());
}

int RowVector4f_set_w(RowVector4f* self, PyObject* value, void* closure)
{
	self->vector.w() = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

PyObject* RowVector4f_get_norm(RowVector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.norm());
}

PyObject* RowVector4f_get_norm_sq(RowVector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.squaredNorm());
}

PyObject* RowVector4f_get_normalized(RowVector4f* self, void* closure)
{
	RowVector4f* result = PyObject_New(RowVector4f, &RowVector4fType);
	if(result != NULL)
		result->vector = self->vector.normalized();

	return (PyObject*)result;
}

PyObject* RowVector4f_get_transpose(RowVector4f* self, void* closure)
{
	Vector4f* result = PyObject_New(Vector4f, &Vector4fType);
	if(result != NULL)
		result->vector = self->vector.transpose();

	return (PyObject*)result;
}

int RowVector4f_set_transpose(RowVector4f* self, PyObject* value,
	void* closure)
{
	if(!Vector4f_Check(value))
	{
		PyErr_SetString(PyExc_TypeError, "transpose must be a Vector4f");
		return -1;
	}

	Vector4f* v = (Vector4f*)value;
	self->vector.transpose() = v->vector;
	return 0;
}

// Methods
PyObject* RowVector4f_zero(PyTypeObject* cls, PyObject* noargs)
{
	RowVector4f* result = PyObject_New(RowVector4f, cls);
	if(result != NULL)
		result->vector.setZero();

	return (PyObject*)result;
}

PyObject* RowVector4f_ones(PyTypeObject* cls, PyObject* noargs)
{
	RowVector4f* result = PyObject_New(RowVector4f, cls);
	if(result != NULL)
		result->vector.setOnes();

	return (PyObject*)result;
}

PyObject* RowVector4f_constant(PyTypeObject* cls, PyObject* args)
{
	float constant = 0.0f;
	if(!PyArg_ParseTuple(args, "f", &constant))
		return NULL;

	RowVector4f* result = PyObject_New(RowVector4f, cls);
	if(result != NULL)
		result->vector.setConstant(constant);

	return (PyObject*)result;
}

PyObject* RowVector4f_random(PyTypeObject* cls, PyObject* noargs)
{
	RowVector4f* result = PyObject_New(RowVector4f, cls);
	if(result != NULL)
		result->vector.setRandom();

	return (PyObject*)result;
}

PyObject* RowVector4f_unit_x(PyTypeObject* cls, PyObject* noargs)
{
	RowVector4f* result = PyObject_New(RowVector4f, cls);
	if(result != NULL)
		result->vector << 1.f, 0.f, 0.f, 0.f;

	return (PyObject*)result;
}

PyObject* RowVector4f_unit_y(PyTypeObject* cls, PyObject* noargs)
{
	RowVector4f* result = PyObject_New(RowVector4f, cls);
	if(result != NULL)
		result->vector << 0.f, 1.f, 0.f, 0.f;

	return (PyObject*)result;
}

PyObject* RowVector4f_unit_z(PyTypeObject* cls, PyObject* noargs)
{
	RowVector4f* result = PyObject_New(RowVector4f, cls);
	if(result != NULL)
		result->vector << 0.f, 0.f, 1.f, 0.f;

	return (PyObject*)result;
}

PyObject* RowVector4f_unit_w(PyTypeObject* cls, PyObject* noargs)
{
	RowVector4f* result = PyObject_New(RowVector4f, cls);
	if(result != NULL)
		result->vector << 0.f, 0.f, 0.f, 1.f;

	return (PyObject*)result;
}

PyObject* RowVector4f_set(RowVector4f* self, PyObject* args)
{
	float x = 0.0f;
	float y = 0.0f;
	float z = 0.0f;
	float w = 0.0f;
	if(!PyArg_ParseTuple(args, "ffff", &x, &y, &z, &w))
		return NULL;

	self->vector << x, y, z, w;
	Py_RETURN_NONE;
}

PyObject* RowVector4f_set_zero(RowVector4f* self, PyObject* noargs)
{
	self->vector.setZero();
	Py_RETURN_NONE;
}

PyObject* RowVector4f_set_ones(RowVector4f* self, PyObject* noargs)
{
	self->vector.setOnes();
	Py_RETURN_NONE;
}

PyObject* RowVector4f_set_constant(RowVector4f* self, PyObject* args)
{
	float constant = 0.0f;
	if(!PyArg_ParseTuple(args, "f", &constant))
		return NULL;

	self->vector.setConstant(constant);
	Py_RETURN_NONE;
}

PyObject* RowVector4f_set_random(RowVector4f* self, PyObject* noargs)
{
	self->vector.setRandom();
	Py_RETURN_NONE;
}

PyObject* RowVector4f_dot(RowVector4f* self, PyObject* other)
{
	if(!RowVector4f_Check(other))
	{
		PyErr_SetString(PyExc_ValueError, "Need RowVector4f for dot product");
		return NULL;
	}

	RowVector4f* otherv = (RowVector4f*)other;
	return PyFloat_FromDouble(self->vector.dot(otherv->vector));
}

PyObject* RowVector4f_normalize(RowVector4f* self, PyObject* noargs)
{
	self->vector.normalize();
	Py_RETURN_NONE;
}

// Number methods
PyObject* RowVector4f_add(PyObject* o1, PyObject* o2)
{
	if(!RowVector4f_Check(o1) || !RowVector4f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	RowVector4f* v1 = (RowVector4f*)o1;
	RowVector4f* v2 = (RowVector4f*)o2;
	RowVector4f* result = PyObject_New(RowVector4f, &RowVector4fType);
	if(result != NULL)
		result->vector = v1->vector + v2->vector;

	return (PyObject*)result;
}

PyObject* RowVector4f_subtract(PyObject* o1, PyObject* o2)
{
	if(!RowVector4f_Check(o1) || !RowVector4f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	RowVector4f* v1 = (RowVector4f*)o1;
	RowVector4f* v2 = (RowVector4f*)o2;
	RowVector4f* result = PyObject_New(RowVector4f, &RowVector4fType);
	if(result != NULL)
		result->vector = v1->vector - v2->vector;

	return (PyObject*)result;
}

PyObject* RowVector4f_multiply(PyObject* o1, PyObject* o2)
{
	if(RowVector4f_Check(o1) && PyNumber_Check(o2))
	{
		RowVector4f* v = (RowVector4f*)o1;
		float scalar = (float)PyFloat_AsDouble(o2);
		if(PyErr_Occurred())
			return NULL;

		RowVector4f* result = PyObject_New(RowVector4f, &RowVector4fType);
		if(result != NULL)
			result->vector = v->vector * scalar;
		return (PyObject*)result;
	}
	else if(PyNumber_Check(o1) && RowVector4f_Check(o2))
	{
		float scalar = (float)PyFloat_AsDouble(o1);
		RowVector4f* v = (RowVector4f*)o2;
		if(PyErr_Occurred())
			return NULL;

		RowVector4f* result = PyObject_New(RowVector4f, &RowVector4fType);
		if(result != NULL)
			result->vector = v->vector * scalar;
		return (PyObject*)result;
	}

	pyeigen_RETURN_NOTIMPLEMENTED;
}

PyObject* RowVector4f_divide(PyObject* o1, PyObject* o2)
{
	if(!RowVector4f_Check(o1) || !PyNumber_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	RowVector4f* v = (RowVector4f*)o1;
	float scalar = (float)PyFloat_AsDouble(o2);
	if(PyErr_Occurred())
		return NULL;

	RowVector4f* result = PyObject_New(RowVector4f, &RowVector4fType);
	if(result != NULL)
		result->vector = v->vector / scalar;

	return (PyObject*)result;
}

PyObject* RowVector4f_negative(PyObject* o)
{
	if(!RowVector4f_Check(o))
		pyeigen_RETURN_NOTIMPLEMENTED;

	RowVector4f* v = (RowVector4f*)o;
	RowVector4f* result = PyObject_New(RowVector4f, &RowVector4fType);
	if(result != NULL)
		result->vector = -v->vector;

	return (PyObject*)result;
}

PyObject* RowVector4f_inplace_add(PyObject* o1, PyObject* o2)
{
	if(!RowVector4f_Check(o1) || !RowVector4f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	RowVector4f* v1 = (RowVector4f*)o1;
	RowVector4f* v2 = (RowVector4f*)o2;
	v1->vector += v2->vector;

	Py_INCREF(v1);
	return (PyObject*)v1;
}

PyObject* RowVector4f_inplace_subtract(PyObject* o1, PyObject* o2)
{
	if(!RowVector4f_Check(o1) || !RowVector4f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	RowVector4f* v1 = (RowVector4f*)o1;
	RowVector4f* v2 = (RowVector4f*)o2;
	v1->vector -= v2->vector;

	Py_INCREF(v1);
	return (PyObject*)v1;
}

PyObject* RowVector4f_inplace_multiply(PyObject* o1, PyObject* o2)
{
	if(RowVector4f_Check(o1) && PyNumber_Check(o2))
	{
		RowVector4f* v = (RowVector4f*)o1;
		float scalar = (float)PyFloat_AsDouble(o2);
		if(PyErr_Occurred())
			return NULL;

		v->vector *= scalar;
		Py_INCREF(v);
		return (PyObject*)v;
	}
	else if(PyNumber_Check(o1) && RowVector4f_Check(o2))
	{
		float scalar = (float)PyFloat_AsDouble(o1);
		RowVector4f* v = (RowVector4f*)o2;
		if(PyErr_Occurred())
			return NULL;

		v->vector *= scalar;
		Py_INCREF(v);
		return (PyObject*)v;
	}

	pyeigen_RETURN_NOTIMPLEMENTED;
}

PyObject* RowVector4f_inplace_divide(PyObject* o1, PyObject* o2)
{
	if(!RowVector4f_Check(o1) || !PyNumber_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	RowVector4f* v = (RowVector4f*)o1;
	float scalar = (float)PyFloat_AsDouble(o2);
	if(PyErr_Occurred())
		return NULL;

	v->vector /= scalar;
	Py_INCREF(v);
	return (PyObject*)v;
}
// Sequence methods
Py_ssize_t RowVector4f_length(RowVector4f* self)
{
	return 4;
}

PyObject* RowVector4f_item(RowVector4f* self, Py_ssize_t index)
{
	if(index < 0 || index >= 4)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	return PyFloat_FromDouble(self->vector[(int)index]);
}

PyObject* RowVector4f_slice(RowVector4f* self, Py_ssize_t index1, Py_ssize_t index2)
{
	if(index1 > 4)
		index1 = 4;
	if(index2 > 4)
		index2 = 4;
	if(index1 > index2)
		index1 = index2;

	Py_ssize_t length = index2 - index1;
	PyObject* tuple = PyTuple_New(length);
	if(tuple != NULL)
		for(Py_ssize_t index = 0; index < length; ++index)
		{
			float value = self->vector[(int)(index1 + index)];
			PyObject* item = PyFloat_FromDouble(value);
			if(item == NULL)
			{
				Py_DECREF(tuple);
				return NULL;
			}

			PyTuple_SetItem(tuple, index, item);
		}

	return tuple;
}

int RowVector4f_ass_item(RowVector4f* self, Py_ssize_t index, PyObject* value)
{
	if(index < 0 || index >= 4)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	self->vector[(int)index] = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

int RowVector4f_ass_slice(RowVector4f* self, Py_ssize_t index1, Py_ssize_t index2,
	PyObject* value)
{
	if(index1 > 4)
		index1 = 4;
	if(index2 > 4)
		index2 = 4;
	if(index1 > index2)
		index1 = index2;

	Py_ssize_t length = index2 - index1;

	if(value == NULL || PySequence_Length(value) != length)
	{
		PyErr_SetString(PyExc_ValueError, "Can't change size of RowVector4f");
		return -1;
	}

	for(Py_ssize_t index = index1; index < index2; ++index)
	{
		self->vector[(int)index] =
			(float)PyFloat_AsDouble(PySequence_GetItem(value, index));
		if(PyErr_Occurred())
			return -1;
	}

	return 0;
}

// Special methods
PyObject* RowVector4f_repr(RowVector4f* self)
{
	char buffer[1024];
	snprintf(buffer, 1024, "RowVector4f(%f, %f, %f, %f)", self->vector.x(),
		self->vector.y(), self->vector.z(), self->vector.w());
	return PyString_FromString(buffer);
}

PyObject* RowVector4f_richcompare(PyObject* a, PyObject* b, int op)
{
	if(!RowVector4f_Check(a) || !RowVector4f_Check(b))
		pyeigen_RETURN_NOTIMPLEMENTED;

	RowVector4f* v1 = (RowVector4f*)a;
	RowVector4f* v2 = (RowVector4f*)b;

	switch(op)
	{
	case Py_EQ:
		if(v1->vector == v2->vector)
			pyeigen_RETURN_TRUE;
		else
			pyeigen_RETURN_FALSE;

	case Py_NE:
		if(v1->vector != v2->vector)
			pyeigen_RETURN_TRUE;
		else
			pyeigen_RETURN_FALSE;
	};

	PyErr_SetString(PyExc_TypeError, "Comparison not supported");
	return NULL;
}
