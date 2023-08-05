// Copyright 2010 Jussi Lepisto

#include "matrix3f.h"

#include <Eigen/Array>
#include <Eigen/Geometry>
#include <Eigen/LU>

#include "util/macros.h"
#include "vector/rowvector3f.h"
#include "vector/vector3f.h"
#include "matrix2f.h"

// Structures
PyGetSetDef Matrix3f_getset[] = {
	{"inverse",		(getter)Matrix3f_get_inverse,	NULL,
	 "The matrix inverse of this matrix.\n\
Note: This matrix must be invertible, otherwise the result is undefined.",
	  NULL},
	{"transpose",	(getter)Matrix3f_get_transpose,
	 (setter)Matrix3f_set_transpose, "Transpose of this matrix.", NULL},

	{NULL}
};

PyMethodDef Matrix3f_methods[] = {
	{"zero",		(PyCFunction)Matrix3f_zero,		METH_CLASS | METH_NOARGS,
	 "Return a 3x3 zero matrix."},
	{"ones",		(PyCFunction)Matrix3f_ones,		METH_CLASS | METH_NOARGS,
	 "Return a 3x3 matrix where all coefficients equal one."},
	{"identity",	(PyCFunction)Matrix3f_identity,	METH_CLASS | METH_NOARGS,
	 "Return a 3x3 identity matrix."},
	{"constant",	(PyCFunction)Matrix3f_constant,	METH_CLASS | METH_VARARGS,
	 "Return a 3x3 constant matrix."},
	{"random",		(PyCFunction)Matrix3f_random,	METH_CLASS | METH_NOARGS,
	 "Return a 3x3 random matrix."},

	{"set",				(PyCFunction)Matrix3f_set,			METH_VARARGS,
	 "Set all coefficients of this matrix."},
	{"set_zero",		(PyCFunction)Matrix3f_set_zero,		METH_NOARGS,
	 "Set all coefficients of this matrix to zero."},
	{"set_ones",		(PyCFunction)Matrix3f_set_ones,		METH_NOARGS,
	 "Set all coefficients of this matrix to one."},
	{"set_identity",	(PyCFunction)Matrix3f_set_identity,	METH_NOARGS,
	 "Writes the identity expression into this matrix."},
	{"set_constant",	(PyCFunction)Matrix3f_set_constant,	METH_VARARGS,
	 "Set all coefficients of this matrix to a constant."},
	{"set_random",		(PyCFunction)Matrix3f_set_random,	METH_NOARGS,
	 "Set all coefficients of this matrix to random values."},

	{"get_block2",		(PyCFunction)Matrix3f_get_block2,	METH_VARARGS,
	 "Return a Matrix2f representing a block of this matrix."},
	{"set_block2",		(PyCFunction)Matrix3f_set_block2,	METH_VARARGS,
	 "Set a block of this matrix to a Matrix2f object."},
	{"get_col",			(PyCFunction)Matrix3f_get_col,		METH_VARARGS,
	 "Return a Vector3f representing a column of this matrix."},
	{"set_col",			(PyCFunction)Matrix3f_set_col,		METH_VARARGS,
	 "Set a column of this matrix to a Vector3f."},
	{"get_row",			(PyCFunction)Matrix3f_get_row,		METH_VARARGS,
	 "Return a RowVector3f representing a row of this matrix."},
	{"set_row",			(PyCFunction)Matrix3f_set_row,		METH_VARARGS,
	 "Set a row of this matrix to a RowVector3f."},

	{"invert",			(PyCFunction)Matrix3f_invert,		METH_NOARGS,
	 "Invert this matrix in place."},

	{NULL}
};

PyNumberMethods Matrix3f_numbermethods = {
	Matrix3f_add,				// nb_add
	Matrix3f_subtract,			// nb_subtract
	Matrix3f_multiply,			// nb_multiply
	Matrix3f_divide,			// nb_divide
	0,							// nb_remainder
	0,							// nb_divmod
	0,							// nb_power
	Matrix3f_negative,			// nb_negative
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
	Matrix3f_inplace_add,		// nb_inplace_add
	Matrix3f_inplace_subtract,	// nb_inplace_subtract
	Matrix3f_inplace_multiply,	// nb_inplace_multiply
	Matrix3f_inplace_divide,	// nb_inplace_divide
};

PyMappingMethods Matrix3f_mappingmethods = {
	(lenfunc)Matrix3f_length,				// mp_length
	(binaryfunc)Matrix3f_subscript,			// mp_subscript
	(objobjargproc)Matrix3f_ass_subscript,	// mp_ass_subscript
};

PyTypeObject Matrix3fType = {
	PyObject_HEAD_INIT(NULL)

	0,								// ob_size
	"pyeigen.Matrix3f",				// tp_name
	sizeof(Matrix3f),				// tp_basicsize
	0,								// tp_itemsize
	0,								// tp_dealloc
	0,								// tp_print
	0,								// tp_getattr
	0,								// tp_setattr
	0,								// tp_compare
	(reprfunc)Matrix3f_repr,		// tp_repr
	&Matrix3f_numbermethods,		// tp_as_number
	0,								// tp_as_sequence
	&Matrix3f_mappingmethods,		// tp_as_mapping
	0,								// tp_hash
	0,								// tp_call
	0,								// tp_str
	0,								// tp_getattro
	0,								// tp_setattro
	0,								// tp_as_buffer
	Py_TPFLAGS_DEFAULT |			// tp_flags
	Py_TPFLAGS_BASETYPE |
	Py_TPFLAGS_CHECKTYPES,
	"3x3 fixed-size matrix with float elements",	// tp_doc
	0,								// tp_traverse
	0,								// tp_clear
	Matrix3f_richcompare,			// tp_richcompare
	0,								// tp_weaklistoffset
	0,								// tp_iter
	0,								// tp_iternext
	Matrix3f_methods,				// tp_methods
	0,								// tp_members
	Matrix3f_getset,				// tp_getset
	0,								// tp_base
	0,								// tp_dict
	0,								// tp_descr_get
	0,								// tp_descr_set
	0,								// tp_dictoffset
	(initproc)Matrix3f_init,		// tp_init
	0,								// tp_alloc
	Matrix3f_new,					// tp_new
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
int Matrix3f_Check(PyObject* p)
{
	return p->ob_type == &Matrix3fType;
}

int Matrix3f_ParseKey(PyObject* key, int& key1, int& key2)
{
	if(!PyArg_ParseTuple(key, "ii", &key1, &key2))
		return 0;

	if(key1 < 0)
		key1 += 3;
	if(key2 < 0)
		key2 += 3;

	if(key1 < 0 || key1 >= 3 || key2 < 0 || key2 >= 3)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return 0;
	}

	return 1;
}

// Construction
PyObject* Matrix3f_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
	return type->tp_alloc(type, 0);
}

int Matrix3f_init(Matrix3f* self, PyObject* args, PyObject* kwds)
{
	if(PySequence_Length(args) > 0)
		if(!Matrix3f_set(self, args))
			return -1;

	return 0;
}

// Properties
PyObject* Matrix3f_get_inverse(Matrix3f* self, void* closure)
{
	Matrix3f* result = PyObject_New(Matrix3f, &Matrix3fType);
	if(result != NULL)
		self->matrix.computeInverse(&result->matrix);

	return (PyObject*)result;
}

PyObject* Matrix3f_get_transpose(Matrix3f* self, void* closure)
{
	Matrix3f* result = PyObject_New(Matrix3f, &Matrix3fType);
	if(result != NULL)
		result->matrix = self->matrix.transpose();

	return (PyObject*)result;
}

int Matrix3f_set_transpose(Matrix3f* self, PyObject* value, void* closure)
{
	if(!Matrix3f_Check(value))
	{
		PyErr_SetString(PyExc_TypeError, "transpose must be Matrix3f");
		return -1;
	}

	Matrix3f* m = (Matrix3f*)value;
	self->matrix.transpose() = m->matrix;
	return 0;
}

// Methods
PyObject* Matrix3f_zero(PyTypeObject* cls, PyObject* noargs)
{
	Matrix3f* result = PyObject_New(Matrix3f, cls);
	if(result != NULL)
		result->matrix.setZero();

	return (PyObject*)result;
}

PyObject* Matrix3f_ones(PyTypeObject* cls, PyObject* noargs)
{
	Matrix3f* result = PyObject_New(Matrix3f, cls);
	if(result != NULL)
		result->matrix.setOnes();

	return (PyObject*)result;
}

PyObject* Matrix3f_identity(PyTypeObject* cls, PyObject* noargs)
{
	Matrix3f* result = PyObject_New(Matrix3f, cls);
	if(result != NULL)
		result->matrix.setIdentity();

	return (PyObject*)result;
}

PyObject* Matrix3f_constant(PyTypeObject* cls, PyObject* args)
{
	float constant = 0.0f;
	if(!PyArg_ParseTuple(args, "f", &constant))
		return NULL;

	Matrix3f* result = PyObject_New(Matrix3f, cls);
	if(result != NULL)
		result->matrix.setConstant(constant);

	return (PyObject*)result;
}

PyObject* Matrix3f_random(PyTypeObject* cls, PyObject* noargs)
{
	Matrix3f* result = PyObject_New(Matrix3f, cls);
	if(result != NULL)
		result->matrix.setRandom();

	return (PyObject*)result;
}

PyObject* Matrix3f_set(Matrix3f* self, PyObject* args)
{
	float m11 = 0.0f, m12 = 0.0f, m13 = 0.0f;
	float m21 = 0.0f, m22 = 0.0f, m23 = 0.0f;
	float m31 = 0.0f, m32 = 0.0f, m33 = 0.0f;
	if(!PyArg_ParseTuple(args, "fffffffff",
		&m11, &m12, &m13,
		&m21, &m22, &m23,
		&m31, &m32, &m33))
		return NULL;

	self->matrix << m11, m12, m13, m21, m22, m23, m31, m32, m33;
	Py_RETURN_NONE;
}

PyObject* Matrix3f_set_zero(Matrix3f* self, PyObject* noargs)
{
	self->matrix.setZero();
	Py_RETURN_NONE;
}

PyObject* Matrix3f_set_ones(Matrix3f* self, PyObject* noargs)
{
	self->matrix.setOnes();
	Py_RETURN_NONE;
}

PyObject* Matrix3f_set_identity(Matrix3f* self, PyObject* noargs)
{
	self->matrix.setIdentity();
	Py_RETURN_NONE;
}

PyObject* Matrix3f_set_constant(Matrix3f* self, PyObject* args)
{
	float constant = 0.0f;
	if(!PyArg_ParseTuple(args, "f", &constant))
		return NULL;

	self->matrix.setConstant(constant);
	Py_RETURN_NONE;
}

PyObject* Matrix3f_set_random(Matrix3f* self, PyObject* noargs)
{
	self->matrix.setRandom();
	Py_RETURN_NONE;
}

PyObject* Matrix3f_get_block2(Matrix3f* self, PyObject* args)
{
	int i = 0, j = 0;
	if(!PyArg_ParseTuple(args, "ii", &i, &j))
		return NULL;

	if(i < 0)
		i += 3;
	if(j < 0)
		j += 3;

	if(i < 0 || i > 1 || j < 0 || j > 1)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	Matrix2f* result = PyObject_New(Matrix2f, &Matrix2fType);
	if(result != NULL)
		result->matrix = self->matrix.block<2, 2>(i, j);

	return (PyObject*)result;
}

PyObject* Matrix3f_set_block2(Matrix3f* self, PyObject* args)
{
	int i = 0, j = 0;
	Matrix2f* value = NULL;
	if(!PyArg_ParseTuple(args, "iiO!", &i, &j, &Matrix2fType, &value))
		return NULL;

	if(i < 0)
		i += 3;
	if(j < 0)
		j += 3;

	if(i < 0 || i > 1 || j < 0 || j > 1)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	self->matrix.block<2, 2>(i, j) = value->matrix;
	Py_RETURN_NONE;
}

PyObject* Matrix3f_get_col(Matrix3f* self, PyObject* args)
{
	int index;
	if(!PyArg_ParseTuple(args, "i", &index))
		return NULL;

	if(index < 0 || index >= 3)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	Vector3f* result = PyObject_New(Vector3f, &Vector3fType);
	if(result != NULL)
		result->vector = self->matrix.col(index);

	return (PyObject*)result;
}

PyObject* Matrix3f_set_col(Matrix3f* self, PyObject* args)
{
	int index;
	Vector3f* value = NULL;
	if(!PyArg_ParseTuple(args, "iO!", &index, &Vector3fType, &value))
		return NULL;

	if(index < 0 || index >= 3)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	self->matrix.col(index) = value->vector;
	Py_RETURN_NONE;
}

PyObject* Matrix3f_get_row(Matrix3f* self, PyObject* args)
{
	int index;
	if(!PyArg_ParseTuple(args, "i", &index))
		return NULL;

	if(index < 0 || index >= 3)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	RowVector3f* result = PyObject_New(RowVector3f, &RowVector3fType);
	if(result != NULL)
		result->vector = self->matrix.row(index);

	return (PyObject*)result;
}

PyObject* Matrix3f_set_row(Matrix3f* self, PyObject* args)
{
	int index;
	RowVector3f* value = NULL;
	if(!PyArg_ParseTuple(args, "iO!", &index, &RowVector3fType, &value))
		return NULL;

	if(index < 0 || index >= 3)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	self->matrix.row(index) = value->vector;
	Py_RETURN_NONE;
}

PyObject* Matrix3f_invert(Matrix3f* self, PyObject* noargs)
{
	Eigen::Matrix3f temp;
	self->matrix.computeInverse(&temp);
	self->matrix = temp;
	Py_RETURN_NONE;
}

// Number methods
PyObject* Matrix3f_add(PyObject* o1, PyObject* o2)
{
	if(!Matrix3f_Check(o1) || !Matrix3f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix3f* m1 = (Matrix3f*)o1;
	Matrix3f* m2 = (Matrix3f*)o2;
	Matrix3f* result = PyObject_New(Matrix3f, &Matrix3fType);
	if(result != NULL)
		result->matrix = m1->matrix + m2->matrix;

	return (PyObject*)result;
}

PyObject* Matrix3f_subtract(PyObject* o1, PyObject* o2)
{
	if(!Matrix3f_Check(o1) || !Matrix3f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix3f* m1 = (Matrix3f*)o1;
	Matrix3f* m2 = (Matrix3f*)o2;
	Matrix3f* result = PyObject_New(Matrix3f, &Matrix3fType);
	if(result != NULL)
		result->matrix = m1->matrix - m2->matrix;

	return (PyObject*)result;
}

PyObject* Matrix3f_multiply(PyObject* o1, PyObject* o2)
{
	// Matrix multiply
	if(Matrix3f_Check(o1) && Matrix3f_Check(o2))
	{
		Matrix3f* m1 = (Matrix3f*)o1;
		Matrix3f* m2 = (Matrix3f*)o2;
		Matrix3f* result = PyObject_New(Matrix3f, &Matrix3fType);
		if(result != NULL)
			result->matrix = m1->matrix * m2->matrix;

		return (PyObject*)result;
	}
	// Vector multiply
	else if(Matrix3f_Check(o1) && Vector3f_Check(o2))
	{
		Matrix3f* m = (Matrix3f*)o1;
		Vector3f* v = (Vector3f*)o2;
		if(PyErr_Occurred())
			return NULL;

		Vector3f* result = PyObject_New(Vector3f, &Vector3fType);
		if(result != NULL)
			result->vector = m->matrix * v->vector;

		return (PyObject*)result;
	}
	// Scalar multiply
	else if(Matrix3f_Check(o1) && PyNumber_Check(o2))
	{
		Matrix3f* m = (Matrix3f*)o1;
		float scalar = (float)PyFloat_AsDouble(o2);
		if(PyErr_Occurred())
			return NULL;

		Matrix3f* result = PyObject_New(Matrix3f, &Matrix3fType);
		if(result != NULL)
			result->matrix = m->matrix * scalar;

		return (PyObject*)result;
	}
	else if(PyNumber_Check(o1) && Matrix3f_Check(o2))
	{
		float scalar = (float)PyFloat_AsDouble(o1);
		Matrix3f* m = (Matrix3f*)o2;
		if(PyErr_Occurred())
			return NULL;

		Matrix3f* result = PyObject_New(Matrix3f, &Matrix3fType);
		if(result != NULL)
			result->matrix = m->matrix * scalar;

		return (PyObject*)result;
	}

	pyeigen_RETURN_NOTIMPLEMENTED;
}

PyObject* Matrix3f_divide(PyObject* o1, PyObject* o2)
{
	if(!Matrix3f_Check(o1) || !PyNumber_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix3f* m = (Matrix3f*)o1;
	float scalar = (float)PyFloat_AsDouble(o2);
	if(PyErr_Occurred())
		return NULL;

	Matrix3f* result = PyObject_New(Matrix3f, &Matrix3fType);
	if(result != NULL)
		result->matrix = m->matrix / scalar;

	return (PyObject*)result;
}

PyObject* Matrix3f_negative(PyObject* o)
{
	if(!Matrix3f_Check(o))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix3f* m = (Matrix3f*)o;
	Matrix3f* result = PyObject_New(Matrix3f, &Matrix3fType);
	if(result != NULL)
		result->matrix = -m->matrix;

	return (PyObject*)result;
}

PyObject* Matrix3f_inplace_add(PyObject* o1, PyObject* o2)
{
	if(!Matrix3f_Check(o1) || !Matrix3f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix3f* m1 = (Matrix3f*)o1;
	Matrix3f* m2 = (Matrix3f*)o2;
	m1->matrix += m2->matrix;

	Py_INCREF(m1);
	return (PyObject*)m1;
}

PyObject* Matrix3f_inplace_subtract(PyObject* o1, PyObject* o2)
{
	if(!Matrix3f_Check(o1) || !Matrix3f_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix3f* m1 = (Matrix3f*)o1;
	Matrix3f* m2 = (Matrix3f*)o2;
	m1->matrix -= m2->matrix;

	Py_INCREF(m1);
	return (PyObject*)m1;
}

PyObject* Matrix3f_inplace_multiply(PyObject* o1, PyObject* o2)
{
	if(!Matrix3f_Check(o1))
		pyeigen_RETURN_NOTIMPLEMENTED;
	Matrix3f* m1 = (Matrix3f*)o1;

	// Matrix multiply
	if(Matrix3f_Check(o2))
	{
		Matrix3f* m2 = (Matrix3f*)o2;
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

PyObject* Matrix3f_inplace_divide(PyObject* o1, PyObject* o2)
{
	if(!Matrix3f_Check(o1) || !PyNumber_Check(o2))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix3f* m = (Matrix3f*)o1;
	float scalar = (float)PyFloat_AsDouble(o2);
	if(PyErr_Occurred())
		return NULL;

	m->matrix /= scalar;

	Py_INCREF(m);
	return (PyObject*)m;
}

// Mapping methods
Py_ssize_t Matrix3f_length(Matrix3f* self)
{
	return 9;
}

PyObject* Matrix3f_subscript(Matrix3f* self, PyObject* key)
{
	int key1, key2;
	if(!Matrix3f_ParseKey(key, key1, key2))
		return NULL;

	return PyFloat_FromDouble(self->matrix(key1, key2));
}

int Matrix3f_ass_subscript(Matrix3f* self, PyObject* key, PyObject* value)
{
	int key1, key2;
	if(!Matrix3f_ParseKey(key, key1, key2))
		return -1;

	self->matrix(key1, key2) = (float)PyFloat_AsDouble(value);
	if(PyErr_Occurred())
		return -1;

	return 0;
}

// Special methods
PyObject* Matrix3f_repr(Matrix3f* self)
{
	char buffer[1024];
	snprintf(buffer, 1024, "Matrix3f(%f, %f, %f,\n         %f, %f, %f,\n         %f, %f, %f)",
		self->matrix[0], self->matrix[1], self->matrix[2],
		self->matrix[3], self->matrix[4], self->matrix[5],
		self->matrix[6], self->matrix[7], self->matrix[8]);
	return PyString_FromString(buffer);
}

PyObject* Matrix3f_richcompare(PyObject* a, PyObject* b, int op)
{
	if(!Matrix3f_Check(a) || !Matrix3f_Check(b))
		pyeigen_RETURN_NOTIMPLEMENTED;

	Matrix3f* m1 = (Matrix3f*)a;
	Matrix3f* m2 = (Matrix3f*)b;

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
