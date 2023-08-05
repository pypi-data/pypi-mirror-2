// Copyright 2010 Jussi Lepisto

#include "matrix2f.h"

#include <Eigen/Array>
#include <Eigen/Geometry>
#include <Eigen/LU>

#include "util/macros.h"
#include "vector/rowvector2f.h"
#include "vector/vector2f.h"

// Structures
PyGetSetDef Matrix2f_getset[] = {
	{"inverse",		(getter)Matrix2f_get_inverse,	NULL,
	 "The matrix inverse of this matrix.\n\
Note: This matrix must be invertible, otherwise the result is undefined.",
	  NULL},
	{"transpose",	(getter)Matrix2f_get_transpose,
	 (setter)Matrix2f_set_transpose, "Transpose of this matrix.", NULL},

	{NULL}
};

PyMethodDef Matrix2f_methods[] = {
	{"zero",		(PyCFunction)Matrix2f_zero,		METH_CLASS | METH_NOARGS,
	 "Return a 2x2 zero matrix."},
	{"ones",		(PyCFunction)Matrix2f_ones,		METH_CLASS | METH_NOARGS,
	 "Return a 2x2 matrix where all coefficients equal one."},
	{"identity",	(PyCFunction)Matrix2f_identity,	METH_CLASS | METH_NOARGS,
	 "Return a 2x2 identity matrix."},
	{"constant",	(PyCFunction)Matrix2f_constant,	METH_CLASS | METH_VARARGS,
	 "Return a 2x2 constant matrix."},
	{"random",		(PyCFunction)Matrix2f_random,	METH_CLASS | METH_NOARGS,
	 "Return a 2x2 random matrix."},

	{"set",				(PyCFunction)Matrix2f_set,			METH_VARARGS,
	 "Set all coefficients of this matrix."},
	{"set_zero",		(PyCFunction)Matrix2f_set_zero,		METH_NOARGS,
	 "Set all coefficients of this matrix to zero."},
	{"set_ones",		(PyCFunction)Matrix2f_set_ones,		METH_NOARGS,
	 "Set all coefficients of this matrix to one."},
	{"set_identity",	(PyCFunction)Matrix2f_set_identity,	METH_NOARGS,
	 "Writes the identity expression into this matrix."},
	{"set_constant",	(PyCFunction)Matrix2f_set_constant,	METH_VARARGS,
	 "Set all coefficients of this matrix to a constant."},
	{"set_random",		(PyCFunction)Matrix2f_set_random,	METH_NOARGS,
	 "Set all coefficients of this matrix to random values."},

	{"get_col",			(PyCFunction)Matrix2f_get_col,		METH_VARARGS,
	 "Return a Vector2f representing a column of this matrix."},
	{"set_col",			(PyCFunction)Matrix2f_set_col,		METH_VARARGS,
	 "Set a column of this matrix to a Vector2f."},
	{"get_row",			(PyCFunction)Matrix2f_get_row,		METH_VARARGS,
	 "Return a RowVector2f representing a row of this matrix."},
	{"set_row",			(PyCFunction)Matrix2f_set_row,		METH_VARARGS,
	 "Set a row of this matrix to a RowVector2f."},

	{"invert",			(PyCFunction)Matrix2f_invert,		METH_NOARGS,
	 "Invert this matrix in place."},

	{NULL}
};

PyNumberMethods Matrix2f_numbermethods = {
	Matrix2f_add,				// nb_add
	Matrix2f_subtract,			// nb_subtract
	Matrix2f_multiply,			// nb_multiply
	Matrix2f_divide,			// nb_divide
	0,							// nb_remainder
	0,							// nb_divmod
	0,							// nb_power
	Matrix2f_negative,			// nb_negative
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
	Matrix2f_inplace_add,		// nb_inplace_add
	Matrix2f_inplace_subtract,	// nb_inplace_subtract
	Matrix2f_inplace_multiply,	// nb_inplace_multiply
	Matrix2f_inplace_divide,	// nb_inplace_divide
};

PyMappingMethods Matrix2f_mappingmethods = {
	(lenfunc)Matrix2f_length,				// mp_length
	(binaryfunc)Matrix2f_subscript,			// mp_subscript
	(objobjargproc)Matrix2f_ass_subscript,	// mp_ass_subscript
};

PyTypeObject Matrix2fType = {
	PyObject_HEAD_INIT(NULL)

	0,								// ob_size
	"pyeigen.Matrix2f",				// tp_name
	sizeof(Matrix2f),				// tp_basicsize
	0,								// tp_itemsize
	0,								// tp_dealloc
	0,								// tp_print
	0,								// tp_getattr
	0,								// tp_setattr
	0,								// tp_compare
	(reprfunc)Matrix2f_repr,		// tp_repr
	&Matrix2f_numbermethods,		// tp_as_number
	0,								// tp_as_sequence
	&Matrix2f_mappingmethods,		// tp_as_mapping
	0,								// tp_hash
	0,								// tp_call
	0,								// tp_str
	0,								// tp_getattro
	0,								// tp_setattro
	0,								// tp_as_buffer
	Py_TPFLAGS_DEFAULT |			// tp_flags
	Py_TPFLAGS_BASETYPE |
	Py_TPFLAGS_CHECKTYPES,
	"2x2 fixed-size matrix with float elements",	// tp_doc
	0,								// tp_traverse
	0,								// tp_clear
	Matrix2f_richcompare,			// tp_richcompare
	0,								// tp_weaklistoffset
	0,								// tp_iter
	0,								// tp_iternext
	Matrix2f_methods,				// tp_methods
	0,								// tp_members
	Matrix2f_getset,				// tp_getset
	0,								// tp_base
	0,								// tp_dict
	0,								// tp_descr_get
	0,								// tp_descr_set
	0,								// tp_dictoffset
	(initproc)Matrix2f_init,		// tp_init
	0,								// tp_alloc
	Matrix2f_new,					// tp_new
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
int Matrix2f_Check(PyObject* p)
{
	return p->ob_type == &Matrix2fType;
}

int Matrix2f_ParseKey(PyObject* key, int& key1, int& key2)
{
	if(!PyArg_ParseTuple(key, "ii", &key1, &key2))
		return 0;

	if(key1 < 0)
		key1 += 2;
	if(key2 < 0)
		key2 += 2;

	if(key1 < 0 || key1 >= 2 || key2 < 0 || key2 >= 2)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return 0;
	}

	return 1;
}

// Construction
PyObject* Matrix2f_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
	return type->tp_alloc(type, 0);
}

int Matrix2f_init(Matrix2f* self, PyObject* args, PyObject* kwds)
{
	if(PySequence_Length(args) > 0)
		if(!Matrix2f_set(self, args))
			return -1;

	return 0;
}

// Properties
PyObject* Matrix2f_get_inverse(Matrix2f* self, void* closure)
{
	Matrix2f* result = PyObject_New(Matrix2f, &Matrix2fType);
	if(result != NULL)
		self->matrix.computeInverse(&result->matrix);

	return (PyObject*)result;
}

PyObject* Matrix2f_get_transpose(Matrix2f* self, void* closure)
{
	Matrix2f* result = PyObject_New(Matrix2f, &Matrix2fType);
	if(result != NULL)
		result->matrix = self->matrix.transpose();

	return (PyObject*)result;
}

int Matrix2f_set_transpose(Matrix2f* self, PyObject* value, void* closure)
{
	if(!Matrix2f_Check(value))
	{
		PyErr_SetString(PyExc_TypeError, "transpose must be Matrix2f");
		return -1;
	}

	Matrix2f* m = (Matrix2f*)value;
	self->matrix.transpose() = m->matrix;
	return 0;
}

// Methods
PyObject* Matrix2f_zero(PyTypeObject* cls, PyObject* noargs)
{
	Matrix2f* result = PyObject_New(Matrix2f, cls);
	if(result != NULL)
		result->matrix.setZero();

	return (PyObject*)result;
}

PyObject* Matrix2f_ones(PyTypeObject* cls, PyObject* noargs)
{
	Matrix2f* result = PyObject_New(Matrix2f, cls);
	if(result != NULL)
		result->matrix.setOnes();

	return (PyObject*)result;
}

PyObject* Matrix2f_identity(PyTypeObject* cls, PyObject* noargs)
{
	Matrix2f* result = PyObject_New(Matrix2f, cls);
	if(result != NULL)
		result->matrix.setIdentity();

	return (PyObject*)result;
}

PyObject* Matrix2f_constant(PyTypeObject* cls, PyObject* args)
{
	float constant = 0.0f;
	if(!PyArg_ParseTuple(args, "f", &constant))
		return NULL;

	Matrix2f* result = PyObject_New(Matrix2f, cls);
	if(result != NULL)
		result->matrix.setConstant(constant);

	return (PyObject*)result;
}

PyObject* Matrix2f_random(PyTypeObject* cls, PyObject* noargs)
{
	Matrix2f* result = PyObject_New(Matrix2f, cls);
	if(result != NULL)
		result->matrix.setRandom();

	return (PyObject*)result;
}

PyObject* Matrix2f_set(Matrix2f* self, PyObject* args)
{
	float m11 = 0.0f, m12 = 0.0f;
	float m21 = 0.0f, m22 = 0.0f;
	if(!PyArg_ParseTuple(args, "ffff", &m11, &m12, &m21, &m22))
		return NULL;

	self->matrix << m11, m12, m21, m22;
	Py_RETURN_NONE;
}

PyObject* Matrix2f_set_zero(Matrix2f* self, PyObject* noargs)
{
	self->matrix.setZero();
	Py_RETURN_NONE;
}

PyObject* Matrix2f_set_ones(Matrix2f* self, PyObject* noargs)
{
	self->matrix.setOnes();
	Py_RETURN_NONE;
}

PyObject* Matrix2f_set_identity(Matrix2f* self, PyObject* noargs)
{
	self->matrix.setIdentity();
	Py_RETURN_NONE;
}

PyObject* Matrix2f_set_constant(Matrix2f* self, PyObject* args)
{
	float constant = 0.0f;
	if(!PyArg_ParseTuple(args, "f", &constant))
		return NULL;

	self->matrix.setConstant(constant);
	Py_RETURN_NONE;
}

PyObject* Matrix2f_set_random(Matrix2f* self, PyObject* noargs)
{
	self->matrix.setRandom();
	Py_RETURN_NONE;
}

PyObject* Matrix2f_get_col(Matrix2f* self, PyObject* args)
{
	int index;
	if(!PyArg_ParseTuple(args, "i", &index))
		return NULL;

	if(index < 0 || index >= 2)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	Vector2f* result = PyObject_New(Vector2f, &Vector2fType);
	if(result != NULL)
		result->vector = self->matrix.col(index);

	return (PyObject*)result;
}

PyObject* Matrix2f_set_col(Matrix2f* self, PyObject* args)
{
	int index;
	Vector2f* value = NULL;
	if(!PyArg_ParseTuple(args, "iO!", &index, &Vector2fType, &value))
		return NULL;

	if(index < 0 || index >= 2)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	self->matrix.col(index) = value->vector;
	Py_RETURN_NONE;
}

PyObject* Matrix2f_get_row(Matrix2f* self, PyObject* args)
{
	int index;
	if(!PyArg_ParseTuple(args, "i", &index))
		return NULL;

	if(index < 0 || index >= 2)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	RowVector2f* result = PyObject_New(RowVector2f, &RowVector2fType);
	if(result != NULL)
		result->vector = self->matrix.row(index);

	return (PyObject*)result;
}

PyObject* Matrix2f_set_row(Matrix2f* self, PyObject* args)
{
	int index;
	RowVector2f* value = NULL;
	if(!PyArg_ParseTuple(args, "iO!", &index, &RowVector2fType, &value))
		return NULL;

	if(index < 0 || index >= 2)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	self->matrix.row(index) = value->vector;
	Py_RETURN_NONE;
}

PyObject* Matrix2f_invert(Matrix2f* self, PyObject* noargs)
{
	Eigen::Matrix2f temp;
	self->matrix.computeInverse(&temp);
	self->matrix = temp;
	Py_RETURN_NONE;
}

// Number methods
PyObject* Matrix2f_add(PyObject* o1, PyObject* o2)
{
	if(!Matrix2f_Check(o1) || !Matrix2f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix2f* m1 = (Matrix2f*)o1;
	Matrix2f* m2 = (Matrix2f*)o2;
	Matrix2f* result = PyObject_New(Matrix2f, &Matrix2fType);
	if(result != NULL)
		result->matrix = m1->matrix + m2->matrix;

	return (PyObject*)result;
}

PyObject* Matrix2f_subtract(PyObject* o1, PyObject* o2)
{
	if(!Matrix2f_Check(o1) || !Matrix2f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix2f* m1 = (Matrix2f*)o1;
	Matrix2f* m2 = (Matrix2f*)o2;
	Matrix2f* result = PyObject_New(Matrix2f, &Matrix2fType);
	if(result != NULL)
		result->matrix = m1->matrix - m2->matrix;

	return (PyObject*)result;
}

PyObject* Matrix2f_multiply(PyObject* o1, PyObject* o2)
{
	// Matrix multiply
	if(Matrix2f_Check(o1) && Matrix2f_Check(o2))
	{
		Matrix2f* m1 = (Matrix2f*)o1;
		Matrix2f* m2 = (Matrix2f*)o2;
		Matrix2f* result = PyObject_New(Matrix2f, &Matrix2fType);
		if(result != NULL)
			result->matrix = m1->matrix * m2->matrix;

		return (PyObject*)result;
	}
	// Vector multiply
	else if(Matrix2f_Check(o1) && Vector2f_Check(o2))
	{
		Matrix2f* m = (Matrix2f*)o1;
		Vector2f* v = (Vector2f*)o2;
		if(PyErr_Occurred())
			return NULL;

		Vector2f* result = PyObject_New(Vector2f, &Vector2fType);
		if(result != NULL)
			result->vector = m->matrix * v->vector;

		return (PyObject*)result;
	}
	// Scalar multiply
	else if(Matrix2f_Check(o1) && PyNumber_Check(o2))
	{
		Matrix2f* m = (Matrix2f*)o1;
		float scalar = (float)PyFloat_AsDouble(o2);
		if(PyErr_Occurred())
			return NULL;

		Matrix2f* result = PyObject_New(Matrix2f, &Matrix2fType);
		if(result != NULL)
			result->matrix = m->matrix * scalar;

		return (PyObject*)result;
	}
	else if(PyNumber_Check(o1) && Matrix2f_Check(o2))
	{
		float scalar = (float)PyFloat_AsDouble(o1);
		Matrix2f* m = (Matrix2f*)o2;
		if(PyErr_Occurred())
			return NULL;

		Matrix2f* result = PyObject_New(Matrix2f, &Matrix2fType);
		if(result != NULL)
			result->matrix = m->matrix * scalar;

		return (PyObject*)result;
	}

	pyeigen_RETURN_NOTIMPLEMENTED;
}

PyObject* Matrix2f_divide(PyObject* o1, PyObject* o2)
{
	if(!Matrix2f_Check(o1) || !PyNumber_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix2f* m = (Matrix2f*)o1;
	float scalar = (float)PyFloat_AsDouble(o2);
	if(PyErr_Occurred())
		return NULL;

	Matrix2f* result = PyObject_New(Matrix2f, &Matrix2fType);
	if(result != NULL)
		result->matrix = m->matrix / scalar;

	return (PyObject*)result;
}

PyObject* Matrix2f_negative(PyObject* o)
{
	if(!Matrix2f_Check(o))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix2f* m = (Matrix2f*)o;
	Matrix2f* result = PyObject_New(Matrix2f, &Matrix2fType);
	if(result != NULL)
		result->matrix = -m->matrix;

	return (PyObject*)result;
}

PyObject* Matrix2f_inplace_add(PyObject* o1, PyObject* o2)
{
	if(!Matrix2f_Check(o1) || !Matrix2f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix2f* m1 = (Matrix2f*)o1;
	Matrix2f* m2 = (Matrix2f*)o2;
	m1->matrix += m2->matrix;

	Py_INCREF(m1);
	return (PyObject*)m1;
}

PyObject* Matrix2f_inplace_subtract(PyObject* o1, PyObject* o2)
{
	if(!Matrix2f_Check(o1) || !Matrix2f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix2f* m1 = (Matrix2f*)o1;
	Matrix2f* m2 = (Matrix2f*)o2;
	m1->matrix -= m2->matrix;

	Py_INCREF(m1);
	return (PyObject*)m1;
}

PyObject* Matrix2f_inplace_multiply(PyObject* o1, PyObject* o2)
{
	if(!Matrix2f_Check(o1))
		pyeigen_RETURN_NOTIMPLEMENTED;
	Matrix2f* m1 = (Matrix2f*)o1;

	// Matrix multiply
	if(Matrix2f_Check(o2))
	{
		Matrix2f* m2 = (Matrix2f*)o2;
		m1->matrix *= m2->matrix;
	}
	// Scalar multiply
	else if(PyNumber_Check(o2))
	{
		float scalar = (float)PyFloat_AsDouble(o2);
		if(PyErr_Occurred())
			return NULL;

		m1->matrix *= scalar;
	}
	else
		pyeigen_RETURN_NOTIMPLEMENTED;

	Py_INCREF(m1);
	return (PyObject*)m1;
}

PyObject* Matrix2f_inplace_divide(PyObject* o1, PyObject* o2)
{
	if(!Matrix2f_Check(o1) || !PyNumber_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix2f* m = (Matrix2f*)o1;
	float scalar = (float)PyFloat_AsDouble(o2);
	if(PyErr_Occurred())
		return NULL;

	m->matrix /= scalar;

	Py_INCREF(m);
	return (PyObject*)m;
}

// Mapping methods
Py_ssize_t Matrix2f_length(Matrix2f* self)
{
	return 4;
}

PyObject* Matrix2f_subscript(Matrix2f* self, PyObject* key)
{
	int key1, key2;
	if(!Matrix2f_ParseKey(key, key1, key2))
		return NULL;

	return PyFloat_FromDouble(self->matrix(key1, key2));
}

int Matrix2f_ass_subscript(Matrix2f* self, PyObject* key, PyObject* value)
{
	int key1, key2;
	if(!Matrix2f_ParseKey(key, key1, key2))
		return -1;

	self->matrix(key1, key2) = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

// Special methods
PyObject* Matrix2f_repr(Matrix2f* self)
{
	char buffer[1024];
	snprintf(buffer, 1024, "Matrix2f(%f, %f,\n         %f, %f)",
		self->matrix[0], self->matrix[1], self->matrix[2], self->matrix[3]);
	return PyString_FromString(buffer);
}

PyObject* Matrix2f_richcompare(PyObject* a, PyObject* b, int op)
{
	if(!Matrix2f_Check(a) || !Matrix2f_Check(b))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix2f* m1 = (Matrix2f*)a;
	Matrix2f* m2 = (Matrix2f*)b;

	switch(op)
	{
	case Py_EQ:
		if(m1->matrix == m2->matrix)
			pyeigen_RETURN_TRUE;
		else
			pyeigen_RETURN_FALSE;

	case Py_NE:
		if(m1->matrix != m2->matrix)
			pyeigen_RETURN_TRUE;
		else
			pyeigen_RETURN_FALSE;
	};

	PyErr_SetString(PyExc_TypeError, "Comparison not supported");
	return NULL;
}
