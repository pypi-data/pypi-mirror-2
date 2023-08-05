/*
   skeinmodule.c   version 0.1 (November 2008)
   Author: Hagen Fürstenau <hfuerstenau@gmx.net>

   Wraps skein.c into a Python module.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "Python.h"
#include "skein.h"

static PyTypeObject skein256Type;
static PyTypeObject skein512Type;
static PyTypeObject skein1024Type;

/* hash objects */

#define OBJECTDEF(X, Y) typedef struct { \
    PyObject_HEAD \
    int blockBitLen; \
    int hashByteLen; \
    Skein ## Y ## _Ctxt_t ctx; \
} skein ## X ## Object;
OBJECTDEF(256, _256)
OBJECTDEF(512, _512)
OBJECTDEF(1024, 1024)


/* hash object attributes */

static PyObject *
skein_get_name(PyObject *self, void *closure)
{
    char name[sizeof(int)*3+7];
    int bits = ((skein256Object *)self)->blockBitLen;

    sprintf(name, "Skein-%d", bits);
    return PyUnicode_FromString(name);
}

static PyObject *
skein_get_block_size(PyObject *self, void *closure)
{
    return PyLong_FromLong(((skein256Object *)self)->blockBitLen / 8);
}

static PyObject *
skein_get_block_bits(PyObject *self, void *closure)
{
    return PyLong_FromLong(((skein256Object *)self)->blockBitLen);
}

static PyObject *
skein_get_digest_size(PyObject *self, void *closure)
{
    return PyLong_FromLong(((skein256Object *)self)->hashByteLen);
}

static PyObject *
skein_get_digest_bits(PyObject *self, void *closure)
{
    return PyLong_FromLong(((skein256Object *)self)->ctx.h.hashBitLen);
}

static PyGetSetDef skein_getseters[] = {
    {"name",
     (getter)skein_get_name, NULL,
     NULL,
     NULL},
    {"block_size",
     (getter)skein_get_block_size, NULL,
     NULL,
     NULL},
    {"block_bits",
     (getter)skein_get_block_bits, NULL,
     NULL,
     NULL},
    {"digest_size",
     (getter)skein_get_digest_size, NULL,
     NULL,
     NULL},
    {"digest_bits",
     (getter)skein_get_digest_bits, NULL,
     NULL,
     NULL},
    {NULL}
};


/* hash object methods */

#define METHODSDEF(X, Y) \
PyDoc_STRVAR(skein ## X ## _update__doc__, \
"Update this hash object's state with the provided bytes object."); \
\
static PyObject * \
skein ## X ## _update(PyObject *self, PyObject *args) \
{ \
    Py_buffer buf; \
\
    if (!PyArg_ParseTuple(args, "y*:update", &buf)) \
	return NULL; \
\
    Skein ## Y ## _Update(&((skein ## X ## Object *)self)->ctx, \
			  buf.buf, buf.len); \
    PyBuffer_Release(&buf); \
    Py_RETURN_NONE; \
} \
\
PyDoc_STRVAR(skein ## X ## _digest__doc__, \
"Return the digest value as a bytes object."); \
\
static PyObject * \
skein ## X ## _digest(skein ## X ## Object *self, PyObject *nothing) \
{ \
    Skein ## Y ## _Ctxt_t ctx_copy; \
    size_t len = self->hashByteLen; \
    u08b_t *hashVal = PyMem_Malloc(len); \
    PyObject *rv; \
\
    if (hashVal == NULL) \
	return PyErr_NoMemory(); \
    memcpy(&ctx_copy, &self->ctx, sizeof(ctx_copy)); \
    Skein ## Y ## _Final(&ctx_copy, hashVal); \
    rv = PyBytes_FromStringAndSize((const char *)hashVal, len); \
    PyMem_Free(hashVal); \
    return rv; \
} \
\
PyDoc_STRVAR(skein ## X ## _hexdigest__doc__, \
"Return the digest value as a string of hexadecimal digits."); \
\
static PyObject * \
skein ## X ## _hexdigest(skein ## X ## Object *self, PyObject *nothing) \
{ \
    Skein ## Y ## _Ctxt_t ctx_copy; \
    size_t len = self->hashByteLen; \
    size_t hexlen = 2*len; \
    size_t i, j; \
    u08b_t *hashVal = PyMem_Malloc(len); \
    char *hex = PyMem_Malloc(hexlen); \
    char nib; \
    PyObject *rv; \
\
    if (hashVal == NULL || hex == NULL) \
	return PyErr_NoMemory(); \
    memcpy(&ctx_copy, &self->ctx, sizeof(ctx_copy)); \
    Skein ## Y ## _Final(&ctx_copy, hashVal); \
    for (i=j=0; i<len; i++) { \
	nib = (hashVal[i] >> 4) & 0x0F; \
	hex[j++] = (nib<10) ? '0'+nib : 'a'-10+nib; \
	nib = hashVal[i] & 0x0F; \
	hex[j++] = (nib<10) ? '0'+nib : 'a'-10+nib; \
    } \
    rv = PyUnicode_FromStringAndSize(hex, hexlen); \
    PyMem_Free(hashVal); \
    PyMem_Free(hex); \
    return rv; \
} \
\
PyDoc_STRVAR(skein ## X ## _copy__doc__, "Return a copy of the hash object."); \
\
static PyObject * \
skein ## X ## _copy(PyObject *self, PyObject *nothing) \
{ \
    skein ## X ## Object *new; \
\
    new = (skein ## X ## Object *)PyObject_New(skein ## X ## Object, \
					       &skein ## X ## Type); \
    if (new == NULL) \
	return NULL; \
    new->ctx = ((skein ## X ## Object *)self)->ctx; \
    new->hashByteLen = ((skein ## X ## Object *)self)->hashByteLen; \
    return (PyObject *)new; \
} \
\
static PyMethodDef skein ## X ## _methods[] = { \
    {"digest", (PyCFunction)skein ## X ## _digest, METH_NOARGS, \
	skein ## X ## _digest__doc__}, \
    {"hexdigest", (PyCFunction)skein ## X ## _hexdigest, METH_NOARGS, \
	skein ## X ## _hexdigest__doc__}, \
    {"update", (PyCFunction)skein ## X ## _update, METH_VARARGS, \
	skein ## X ## _update__doc__}, \
    {"copy", (PyCFunction)skein ## X ## _copy, METH_VARARGS, \
	skein ## X ## _copy__doc__}, \
    {NULL, NULL} \
};
METHODSDEF(256, _256)
METHODSDEF(512, _512)
METHODSDEF(1024, 1024)


/* hash object types */

static void
skein_dealloc(PyObject *self)
{
    PyObject_Del(self);
}

#define TYPEDEF(X) \
static PyTypeObject skein ## X ## Type = {  \
    PyVarObject_HEAD_INIT(NULL, 0)                                   \
    "skein.skein" #X,			/* tp_name */                     \
    sizeof(skein ## X ## Object),	/* tp_basicsize */                \
    0,					/* tp_itemsize */                 \
    skein_dealloc,			/* tp_dealloc */                  \
    0,					/* tp_print */                    \
    0,					/* tp_getattr */                  \
    0,					/* tp_setattr */                  \
    0,					/* tp_compare */                  \
    0,	    				/* tp_repr */                     \
    0,					/* tp_as_number */                \
    0,					/* tp_as_sequence */              \
    0,					/* tp_as_mapping */               \
    0,					/* tp_hash */                     \
    0,	    				/* tp_call */			  \
    0,					/* tp_str */			  \
    0,					/* tp_getattro */                 \
    0,					/* tp_setattro */                 \
    0,					/* tp_as_buffer */		  \
    Py_TPFLAGS_DEFAULT,			/* tp_flags */			  \
    0,					/* tp_doc */			  \
    0,					/* tp_traverse */		  \
    0,					/* tp_clear */			  \
    0,					/* tp_richcompare */		  \
    0,					/* tp_weaklistoffset */		  \
    0,					/* tp_iter */			  \
    0,					/* tp_iternext */		  \
    skein ## X ## _methods,		/* tp_methods */		  \
    NULL,				/* tp_members */		  \
    skein_getseters		/* tp_getset */			  \
}
TYPEDEF(256);
TYPEDEF(512);
TYPEDEF(1024);


/* factory functions */

#define FACTORYDEF(X, Y)  \
PyDoc_STRVAR(skein ## X ## _new__doc__,  \
"Return a new Skein-" #X " hash object.\n\n" \
"Optionally initialize with bytes object and set digest length in bits\n" \
"(default: " #X ")."); \
\
static PyObject * \
skein ## X ## _new(PyObject *self, PyObject *args, PyObject *kw) \
{ \
    skein ## X ## Object *new; \
    Py_buffer buf; \
    int hashBitLen = X; \
    static char *kwlist[] = {"init", "digest_bits", NULL}; \
\
    buf.buf = NULL; \
    if (!PyArg_ParseTupleAndKeywords(args, kw, "|y*i:skein" #X , kwlist, \
				     &buf, &hashBitLen)) \
	return NULL; \
    if (hashBitLen <= 0 || hashBitLen%8 != 0) { \
	PyErr_SetString(PyExc_ValueError, "Invalid number of digest bits"); \
	return NULL; \
    } \
\
    new = PyObject_New(skein ## X ## Object, &skein ## X ## Type); \
    if (new == NULL) \
	return NULL; \
    Skein ## Y ## _InitExt(&new->ctx, hashBitLen, \
			   SKEIN_CFG_TREE_INFO_SEQUENTIAL, 0, 0); \
    new->blockBitLen = X; \
    new->hashByteLen = (hashBitLen+7)>>3; \
    if (buf.buf != NULL) { \
	Skein ## Y ## _Update(&new->ctx, buf.buf, buf.len); \
        PyBuffer_Release(&buf); \
    } \
    return (PyObject *)new; \
}
FACTORYDEF(256, _256)
FACTORYDEF(512, _512)
FACTORYDEF(1024, 1024)

#define METHODDEFLINE(X) \
{"skein" #X , (PyCFunction)skein ## X ## _new, METH_VARARGS|METH_KEYWORDS, \
skein ## X ## _new__doc__}

static struct PyMethodDef skein_functions[] = {
    METHODDEFLINE(256),
    METHODDEFLINE(512),
    METHODDEFLINE(1024),
    {NULL, NULL}
};


/* module init */

static struct PyModuleDef skeinmodule = {
    PyModuleDef_HEAD_INIT,
    "skein",
    NULL,
    -1,
    skein_functions,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC
PyInit_skein(void)
{
    if (PyType_Ready(&skein256Type) < 0 || \
	PyType_Ready(&skein512Type) < 0 || \
	PyType_Ready(&skein1024Type) < 0)
	return NULL;
    return PyModule_Create(&skeinmodule);
}

