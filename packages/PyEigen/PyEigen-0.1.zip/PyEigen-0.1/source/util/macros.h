#ifndef MACROS_H
#define MACROS_H

#define pyeigen_RETURN_NOTIMPLEMENTED return Py_INCREF(Py_NotImplemented), Py_NotImplemented
#define pyeigen_RETURN_TRUE return Py_INCREF(Py_True), Py_True
#define pyeigen_RETURN_FALSE return Py_INCREF(Py_False), Py_False

#endif
