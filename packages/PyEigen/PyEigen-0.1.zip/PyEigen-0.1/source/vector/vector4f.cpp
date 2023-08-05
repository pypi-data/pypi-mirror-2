// Copyright 2010 Jussi Lepisto

#include "vector4f.h"

#include <Eigen/Array>
#include <Eigen/Geometry>

#include "util/macros.h"
#include "vector/rowvector4f.h"


// Structures
PyGetSetDef Vector4f_getset[] = {
	{"x", (getter)Vector4f_get_x, (setter)Vector4f_set_x,
	 "The first coefficient of this vector.", NULL},
	{"y", (getter)Vector4f_get_y, (setter)Vector4f_set_y,
	 "The second coefficient of this vector.", NULL},
	{"z", (getter)Vector4f_get_z, (setter)Vector4f_set_z,
	 "The third coefficient of this vector.", NULL},
	{"w", (getter)Vector4f_get_w, (setter)Vector4f_set_w,
	 "The fourth coefficient of this vector.", NULL},

	{"norm",		(getter)Vector4f_get_norm,			NULL,
	 "Norm of this vector.", NULL},
	{"norm_sq",		(getter)Vector4f_get_norm_sq,		NULL,
	 "Squared norm of this vector.", NULL},
	{"normalized",	(getter)Vector4f_get_normalized,	NULL,
	 "This vector divided by its norm.", NULL},
	{"transpose",
	 (getter)Vector4f_get_transpose, (setter)Vector4f_set_transpose,
	 "Transpose of this vector.", NULL},

	{NULL}
};

PyMethodDef Vector4f_methods[] = {
	{"zero",		(PyCFunction)Vector4f_zero,		METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional zero vector."},
	{"ones",		(PyCFunction)Vector4f_ones,		METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional vector where all coefficients equal one."},
	{"constant",	(PyCFunction)Vector4f_constant,	METH_CLASS | METH_VARARGS,
	 "Return a 4-dimensional constant vector."},
	{"random",		(PyCFunction)Vector4f_random,	METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional random vector."},
	{"unit_x",		(PyCFunction)Vector4f_unit_x,	METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional X axis unit vector."},
	{"unit_y",		(PyCFunction)Vector4f_unit_y,	METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional Y axis unit vector."},
	{"unit_z",		(PyCFunction)Vector4f_unit_z,	METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional Z axis unit vector."},
	{"unit_w",		(PyCFunction)Vector4f_unit_w,	METH_CLASS | METH_NOARGS,
	 "Return a 4-dimensional W axis unit vector."},

	{"set",				(PyCFunction)Vector4f_set,			METH_VARARGS,
	 "Set all coefficients of this vector."},
	{"set_zero",		(PyCFunction)Vector4f_set_zero,		METH_NOARGS,
	 "Set all coefficients of this vector to zero."},
	{"set_ones",		(PyCFunction)Vector4f_set_ones,		METH_NOARGS,
	 "Set all coefficients of this vector to one."},
	{"set_constant",	(PyCFunction)Vector4f_set_constant,	METH_VARARGS,
	 "Set all coefficients of this vector to a constant."},
	{"set_random",		(PyCFunction)Vector4f_set_random,	METH_NOARGS,
	 "Set all coefficients of this vector to random values."},

	{"dot",				(PyCFunction)Vector4f_dot,			METH_O,
	 "The dot product of this vector with the other vector."},

	{"normalize",		(PyCFunction)Vector4f_normalize,	METH_NOARGS,
	 "Normalizes this vector, i.e. divides it by its own norm."},

	{NULL}
};

PyNumberMethods Vector4f_numbermethods = {
	Vector4f_add,				// nb_add
	Vector4f_subtract,			// nb_subtract
	Vector4f_multiply,			// nb_multiply
	Vector4f_divide,			// nb_divide
	0,							// nb_remainder
	0,							// nb_divmod
	0,							// nb_power
	Vector4f_negative,			// nb_negative
	0,							// nb_positive
	0,							// nb_absolute
	0,							// nb_nonzero
	0,							// nb_invert
	0,							// nb_lshift
	0,							// nb_rshift
	0,							// nb_and
	0,							// nb_xor
	0,							// nb_or
	0,							// nb_coerce
	0,							// nb_int
	0,							// nb_long
	0,							// nb_float
	0,							// nb_oct
	0,							// nb_hex
	Vector4f_inplace_add,		// nb_inplace_add
	Vector4f_inplace_subtract,	// nb_inplace_subtract
	Vector4f_inplace_multiply,	// nb_inplace_multiply
	Vector4f_inplace_divide,	// nb_inplace_divide
};

PySequenceMethods Vector4f_sequencemethods = {
	(lenfunc)Vector4f_length,					// sq_length
	0,											// sq_concat
	0,											// sq_repeat
	(ssizeargfunc)Vector4f_item,				// sq_item
	(ssizessizeargfunc)Vector4f_slice,			// sq_slice
	(ssizeobjargproc)Vector4f_ass_item,			// sq_ass_item
	(ssizessizeobjargproc)Vector4f_ass_slice,	// sq_ass_slice
};

PyTypeObject Vector4fType = {
	PyObject_HEAD_INIT(NULL)

	0,								// ob_size
	"pyeigen.Vector4f",				// tp_name
	sizeof(Vector4f),				// tp_basicsize
	0,								// tp_itemsize
	0,								// tp_dealloc
	0,								// tp_print
	0,								// tp_getattr
	0,								// tp_setattr
	0,								// tp_compare
	(reprfunc)Vector4f_repr,		// tp_repr
	&Vector4f_numbermethods,		// tp_as_number
	&Vector4f_sequencemethods,		// tp_as_sequence
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
	Vector4f_richcompare,			// tp_richcompare
	0,								// tp_weaklistoffset
	0,								// tp_iter
	0,								// tp_iternext
	Vector4f_methods,				// tp_methods
	0,								// tp_members
	Vector4f_getset,				// tp_getset
	0,								// tp_base
	0,								// tp_dict
	0,								// tp_descr_get
	0,								// tp_descr_set
	0,								// tp_dictoffset
	(initproc)Vector4f_init,		// tp_init
	0,								// tp_alloc
	Vector4f_new,					// tp_new
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
int Vector4f_Check(PyObject* p)
{
	return p->ob_type == &Vector4fType;
}

// Construction
PyObject* Vector4f_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
	return type->tp_alloc(type, 0);
}

int Vector4f_init(Vector4f* self, PyObject* args, PyObject* kwds)
{
	if(PySequence_Length(args) > 0)
		if(!Vector4f_set(self, args))
			return -1;

	return 0;
}

// Properties
PyObject* Vector4f_get_x(Vector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.x());
}

int Vector4f_set_x(Vector4f* self, PyObject* value, void* closure)
{
	self->vector.x() = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

PyObject* Vector4f_get_y(Vector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.y());
}

int Vector4f_set_y(Vector4f* self, PyObject* value, void* closure)
{
	self->vector.y() = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

PyObject* Vector4f_get_z(Vector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.z());
}

int Vector4f_set_z(Vector4f* self, PyObject* value, void* closure)
{
	self->vector.z() = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

PyObject* Vector4f_get_w(Vector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.w());
}

int Vector4f_set_w(Vector4f* self, PyObject* value, void* closure)
{
	self->vector.w() = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

PyObject* Vector4f_get_norm(Vector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.norm());
}

PyObject* Vector4f_get_norm_sq(Vector4f* self, void* closure)
{
	return PyFloat_FromDouble(self->vector.squaredNorm());
}

PyObject* Vector4f_get_normalized(Vector4f* self, void* closure)
{
	Vector4f* result = PyObject_New(Vector4f, &Vector4fType);
	if(result != NULL)
		result->vector = self->vector.normalized();

	return (PyObject*)result;
}

PyObject* Vector4f_get_transpose(Vector4f* self, void* closure)
{
	RowVector4f* result = PyObject_New(RowVector4f, &RowVector4fType);
	if(result != NULL)
		result->vector = self->vector.transpose();

	return (PyObject*)result;
}

int Vector4f_set_transpose(Vector4f* self, PyObject* value, void* closure)
{
	if(!RowVector4f_Check(value))
	{
		PyErr_SetString(PyExc_TypeError, "transpose must be a RowVector4f");
		return -1;
	}

	RowVector4f* v = (RowVector4f*)value;
	self->vector.transpose() = v->vector;
	return 0;
}

// Methods
PyObject* Vector4f_zero(PyTypeObject* cls, PyObject* noargs)
{
	Vector4f* result = PyObject_New(Vector4f, cls);
	if(result != NULL)
		result->vector.setZero();

	return (PyObject*)result;
}

PyObject* Vector4f_ones(PyTypeObject* cls, PyObject* noargs)
{
	Vector4f* result = PyObject_New(Vector4f, cls);
	if(result != NULL)
		result->vector.setOnes();

	return (PyObject*)result;
}

PyObject* Vector4f_constant(PyTypeObject* cls, PyObject* args)
{
	float constant = 0.0f;
	if(!PyArg_ParseTuple(args, "f", &constant))
		return NULL;

	Vector4f* result = PyObject_New(Vector4f, cls);
	if(result != NULL)
		result->vector.setConstant(constant);

	return (PyObject*)result;
}

PyObject* Vector4f_random(PyTypeObject* cls, PyObject* noargs)
{
	Vector4f* result = PyObject_New(Vector4f, cls);
	if(result != NULL)
		result->vector.setRandom();

	return (PyObject*)result;
}

PyObject* Vector4f_unit_x(PyTypeObject* cls, PyObject* noargs)
{
	Vector4f* result = PyObject_New(Vector4f, cls);
	if(result != NULL)
		result->vector << 1.f, 0.f, 0.f, 0.f;

	return (PyObject*)result;
}

PyObject* Vector4f_unit_y(PyTypeObject* cls, PyObject* noargs)
{
	Vector4f* result = PyObject_New(Vector4f, cls);
	if(result != NULL)
		result->vector << 0.f, 1.f, 0.f, 0.f;

	return (PyObject*)result;
}

PyObject* Vector4f_unit_z(PyTypeObject* cls, PyObject* noargs)
{
	Vector4f* result = PyObject_New(Vector4f, cls);
	if(result != NULL)
		result->vector << 0.f, 0.f, 1.f, 0.f;

	return (PyObject*)result;
}

PyObject* Vector4f_unit_w(PyTypeObject* cls, PyObject* noargs)
{
	Vector4f* result = PyObject_New(Vector4f, cls);
	if(result != NULL)
		result->vector << 0.f, 0.f, 0.f, 1.f;

	return (PyObject*)result;
}

PyObject* Vector4f_set(Vector4f* self, PyObject* args)
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

PyObject* Vector4f_set_zero(Vector4f* self, PyObject* noargs)
{
	self->vector.setZero();
	Py_RETURN_NONE;
}

PyObject* Vector4f_set_ones(Vector4f* self, PyObject* noargs)
{
	self->vector.setOnes();
	Py_RETURN_NONE;
}

PyObject* Vector4f_set_constant(Vector4f* self, PyObject* args)
{
	float constant = 0.0f;
	if(!PyArg_ParseTuple(args, "f", &constant))
		return NULL;

	self->vector.setConstant(constant);
	Py_RETURN_NONE;
}

PyObject* Vector4f_set_random(Vector4f* self, PyObject* noargs)
{
	self->vector.setRandom();
	Py_RETURN_NONE;
}

PyObject* Vector4f_dot(Vector4f* self, PyObject* other)
{
	if(!Vector4f_Check(other))
	{
		PyErr_SetString(PyExc_ValueError, "Need Vector4f for dot product");
		return NULL;
	}

	Vector4f* otherv = (Vector4f*)other;
	return PyFloat_FromDouble(self->vector.dot(otherv->vector));
}

PyObject* Vector4f_normalize(Vector4f* self, PyObject* noargs)
{
	self->vector.normalize();
	Py_RETURN_NONE;
}

// Number methods
PyObject* Vector4f_add(PyObject* o1, PyObject* o2)
{
	if(!Vector4f_Check(o1) || !Vector4f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Vector4f* v1 = (Vector4f*)o1;
	Vector4f* v2 = (Vector4f*)o2;
	Vector4f* result = PyObject_New(Vector4f, &Vector4fType);
	if(result != NULL)
		result->vector = v1->vector + v2->vector;

	return (PyObject*)result;
}

PyObject* Vector4f_subtract(PyObject* o1, PyObject* o2)
{
	if(!Vector4f_Check(o1) || !Vector4f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Vector4f* v1 = (Vector4f*)o1;
	Vector4f* v2 = (Vector4f*)o2;
	Vector4f* result = PyObject_New(Vector4f, &Vector4fType);
	if(result != NULL)
		result->vector = v1->vector - v2->vector;

	return (PyObject*)result;
}

PyObject* Vector4f_multiply(PyObject* o1, PyObject* o2)
{
	if(Vector4f_Check(o1) && PyNumber_Check(o2))
	{
		Vector4f* v = (Vector4f*)o1;
		float scalar = (float)PyFloat_AsDouble(o2);
		if(PyErr_Occurred())
			return NULL;

		Vector4f* result = PyObject_New(Vector4f, &Vector4fType);
		if(result != NULL)
			result->vector = v->vector * scalar;
		return (PyObject*)result;
	}
	else if(PyNumber_Check(o1) && Vector4f_Check(o2))
	{
		float scalar = (float)PyFloat_AsDouble(o1);
		Vector4f* v = (Vector4f*)o2;
		if(PyErr_Occurred())
			return NULL;

		Vector4f* result = PyObject_New(Vector4f, &Vector4fType);
		if(result != NULL)
			result->vector = v->vector * scalar;
		return (PyObject*)result;
	}

	pyeigen_RETURN_NOTIMPLEMENTED;
}

PyObject* Vector4f_divide(PyObject* o1, PyObject* o2)
{
	if(!Vector4f_Check(o1) || !PyNumber_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Vector4f* v = (Vector4f*)o1;
	float scalar = (float)PyFloat_AsDouble(o2);
	if(PyErr_Occurred())
		return NULL;

	Vector4f* result = PyObject_New(Vector4f, &Vector4fType);
	if(result != NULL)
		result->vector = v->vector / scalar;

	return (PyObject*)result;
}

PyObject* Vector4f_negative(PyObject* o)
{
	if(!Vector4f_Check(o))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Vector4f* v = (Vector4f*)o;
	Vector4f* result = PyObject_New(Vector4f, &Vector4fType);
	if(result != NULL)
		result->vector = -v->vector;

	return (PyObject*)result;
}

PyObject* Vector4f_inplace_add(PyObject* o1, PyObject* o2)
{
	if(!Vector4f_Check(o1) || !Vector4f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Vector4f* v1 = (Vector4f*)o1;
	Vector4f* v2 = (Vector4f*)o2;
	v1->vector += v2->vector;

	Py_INCREF(v1);
	return (PyObject*)v1;
}

PyObject* Vector4f_inplace_subtract(PyObject* o1, PyObject* o2)
{
	if(!Vector4f_Check(o1) || !Vector4f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Vector4f* v1 = (Vector4f*)o1;
	Vector4f* v2 = (Vector4f*)o2;
	v1->vector -= v2->vector;

	Py_INCREF(v1);
	return (PyObject*)v1;
}

PyObject* Vector4f_inplace_multiply(PyObject* o1, PyObject* o2)
{
	if(Vector4f_Check(o1) && PyNumber_Check(o2))
	{
		Vector4f* v = (Vector4f*)o1;
		float scalar = (float)PyFloat_AsDouble(o2);
		if(PyErr_Occurred())
			return NULL;

		v->vector *= scalar;
		Py_INCREF(v);
		return (PyObject*)v;
	}
	else if(PyNumber_Check(o1) && Vector4f_Check(o2))
	{
		float scalar = (float)PyFloat_AsDouble(o1);
		Vector4f* v = (Vector4f*)o2;
		if(PyErr_Occurred())
			return NULL;

		v->vector *= scalar;
		Py_INCREF(v);
		return (PyObject*)v;
	}

	pyeigen_RETURN_NOTIMPLEMENTED;
}

PyObject* Vector4f_inplace_divide(PyObject* o1, PyObject* o2)
{
	if(!Vector4f_Check(o1) || !PyNumber_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Vector4f* v = (Vector4f*)o1;
	float scalar = (float)PyFloat_AsDouble(o2);
	if(PyErr_Occurred())
		return NULL;

	v->vector /= scalar;
	Py_INCREF(v);
	return (PyObject*)v;
}
// Sequence methods
Py_ssize_t Vector4f_length(Vector4f* self)
{
	return 4;
}

PyObject* Vector4f_item(Vector4f* self, Py_ssize_t index)
{
	if(index < 0 || index >= 4)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	return PyFloat_FromDouble(self->vector[(int)index]);
}

PyObject* Vector4f_slice(Vector4f* self, Py_ssize_t index1, Py_ssize_t index2)
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

int Vector4f_ass_item(Vector4f* self, Py_ssize_t index, PyObject* value)
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

int Vector4f_ass_slice(Vector4f* self, Py_ssize_t index1, Py_ssize_t index2,
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
		PyErr_SetString(PyExc_ValueError, "Can't change size of Vector4f");
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
PyObject* Vector4f_repr(Vector4f* self)
{
	char buffer[1024];
	snprintf(buffer, 1024, "Vector4f(%f, %f, %f, %f)", self->vector.x(),
		self->vector.y(), self->vector.z(), self->vector.w());
	return PyString_FromString(buffer);
}

PyObject* Vector4f_richcompare(PyObject* a, PyObject* b, int op)
{
	if(!Vector4f_Check(a) || !Vector4f_Check(b))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Vector4f* v1 = (Vector4f*)a;
	Vector4f* v2 = (Vector4f*)b;

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
