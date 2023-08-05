/*
   skeinmodule.c   version 0.2
   Copyright 2008 Hagen Fürstenau <hfuerstenau@gmx.net>

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

/* External functions from skein_block.c for usage in Threefish */
void Skein_256_Process_Block(Skein_256_Ctxt_t *ctx, const u08b_t *blkPtr,
                             size_t blkCnt, size_t byteCntAdd);
void Skein_512_Process_Block(Skein_512_Ctxt_t *ctx, const u08b_t *blkPtr,
                             size_t blkCnt,size_t byteCntAdd);
void Skein1024_Process_Block(Skein1024_Ctxt_t *ctx, const u08b_t *blkPtr,
                             size_t blkCnt, size_t byteCntAdd);


/* objects */

static PyTypeObject skein256Type;
static PyTypeObject skein512Type;
static PyTypeObject skein1024Type;

#define OBJECTDEF(X, Y) typedef struct { \
    PyObject_HEAD \
    int blockBitLen; \
    int hashByteLen; \
    Skein ## Y ## _Ctxt_t ctx; \
} skein ## X ## Object;
OBJECTDEF(256, _256)
OBJECTDEF(512, _512)
OBJECTDEF(1024, 1024)

typedef struct {
    PyObject_HEAD \
    int blockByteLen;
    void *ctx;
} threefishObject;


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


/* threefish object attributes */
static PyObject *
threefish_get_block_size(PyObject *self, void *closure)
{
    return PyLong_FromLong(((threefishObject *)self)->blockByteLen);
}

static PyObject *
threefish_get_block_bits(PyObject *self, void *closure)
{
    return PyLong_FromLong(((threefishObject *)self)->blockByteLen * 8);
}

static PyGetSetDef threefish_getseters[] = {
    {"block_size",
     (getter)threefish_get_block_size, NULL,
     NULL,
     NULL},
    {"block_bits",
     (getter)threefish_get_block_bits, NULL,
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
    char nib; \
    PyObject *rv; \
    u08b_t *hashVal; \
    char *hex; \
\
    if ((hashVal = PyMem_Malloc(len)) == NULL) \
	return PyErr_NoMemory(); \
    if ((hex = PyMem_Malloc(hexlen)) == NULL) { \
        PyMem_Free(hashVal); \
	return PyErr_NoMemory(); \
    } \
\
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


/* threefish object methods */
PyDoc_STRVAR(threefish_encrypt__doc__,
"Encrypt the given bytes block.");

static PyObject *
threefish_encrypt_block(PyObject *self, PyObject *args)
{
    Py_buffer buf;
    PyObject *rv;
    u08b_t *encrypted;
    u64b_t T[2];
    u64b_t X[16];
    int i;
    int len = ((threefishObject *)self)->blockByteLen;
    void *ctx = ((threefishObject *)self)->ctx;

    if (!PyArg_ParseTuple(args, "y*:encrypt", &buf))
	return NULL;
    if (buf.len != len) {
        char msg[47];
        sprintf(msg, "block must have same length as key (%d bytes)", len);
	PyErr_SetString(PyExc_ValueError, msg);
        PyBuffer_Release(&buf);
        return NULL;
    }

    if ((encrypted = PyMem_Malloc(len)) == NULL)
	return PyErr_NoMemory();

    switch (len) {
        case 32:
            memcpy(T, ((Skein_256_Ctxt_t *)ctx)->h.T, sizeof(T));
            memcpy(X, ((Skein_256_Ctxt_t *)ctx)->X, len);
            Skein_256_Process_Block((Skein_256_Ctxt_t *)ctx, buf.buf, 1, 0);
            Skein_Put64_LSB_First(encrypted, ((Skein_256_Ctxt_t *)ctx)->X, len);
            memcpy(((Skein_256_Ctxt_t *)ctx)->h.T, T, sizeof(T));
            memcpy(((Skein_256_Ctxt_t *)ctx)->X, X, len);
            break;
        case 64:
            memcpy(T, ((Skein_512_Ctxt_t *)ctx)->h.T, sizeof(T));
            memcpy(X, ((Skein_512_Ctxt_t *)ctx)->X, len);
            Skein_512_Process_Block((Skein_512_Ctxt_t *)ctx, buf.buf, 1, 0);
            Skein_Put64_LSB_First(encrypted, ((Skein_512_Ctxt_t *)ctx)->X, len);
            memcpy(((Skein_512_Ctxt_t *)ctx)->h.T, T, sizeof(T));
            memcpy(((Skein_512_Ctxt_t *)ctx)->X, X, len);
            break;
        case 128:
            memcpy(T, ((Skein1024_Ctxt_t *)ctx)->h.T, sizeof(T));
            memcpy(X, ((Skein1024_Ctxt_t *)ctx)->X, len);
            Skein1024_Process_Block((Skein1024_Ctxt_t *)ctx, buf.buf, 1, 0);
            Skein_Put64_LSB_First(encrypted, ((Skein1024_Ctxt_t *)ctx)->X, len);
            memcpy(((Skein1024_Ctxt_t *)ctx)->h.T, T, sizeof(T));
            memcpy(((Skein1024_Ctxt_t *)ctx)->X, X, len);
            break;
    }
    for (i=0; i<len; i++)
        encrypted[i] ^= ((u08b_t *)buf.buf)[i];

    rv = PyBytes_FromStringAndSize((const char *)encrypted, len);
    PyBuffer_Release(&buf);
    PyMem_Free(encrypted);
    return rv;
}

static PyMethodDef threefish_methods[] = {
    {"encrypt_block", (PyCFunction)threefish_encrypt_block, METH_VARARGS,
	threefish_encrypt__doc__},
    {NULL, NULL}
};


/* types */

static void
skein_dealloc(PyObject *self)
{
    PyObject_Del(self);
}

static void
threefish_dealloc(PyObject *self)
{
    PyMem_Free(((threefishObject *)self)->ctx);
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
    skein_getseters	        	/* tp_getset */			  \
}
TYPEDEF(256);
TYPEDEF(512);
TYPEDEF(1024);

static PyTypeObject threefishType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "skein.threefish",			/* tp_name */
    sizeof(threefishObject),	        /* tp_basicsize */
    0,					/* tp_itemsize */
    threefish_dealloc,			/* tp_dealloc */
    0,					/* tp_print */
    0,					/* tp_getattr */
    0,					/* tp_setattr */
    0,					/* tp_compare */
    0,	    				/* tp_repr */
    0,					/* tp_as_number */
    0,					/* tp_as_sequence */
    0,					/* tp_as_mapping */
    0,					/* tp_hash */
    0,	    				/* tp_call */
    0,					/* tp_str */
    0,					/* tp_getattro */
    0,					/* tp_setattro */
    0,					/* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,			/* tp_flags */
    0,					/* tp_doc */
    0,					/* tp_traverse */
    0,					/* tp_clear */
    0,					/* tp_richcompare */
    0,					/* tp_weaklistoffset */
    0,					/* tp_iter */
    0,					/* tp_iternext */
    threefish_methods,      		/* tp_methods */
    NULL,				/* tp_members */
    threefish_getseters		        /* tp_getset */
};


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
    Py_buffer buf, mac; \
    int hashBitLen = X; \
    static char *kwlist[] = {"init", "digest_bits", "mac", NULL}; \
\
    buf.buf = NULL; \
    mac.buf = NULL; \
    if (!PyArg_ParseTupleAndKeywords(args, kw, "|y*iy*:skein" #X , kwlist, \
				     &buf, &hashBitLen, &mac)) \
	goto error; \
    if (hashBitLen <= 0 || hashBitLen%8 != 0) { \
	PyErr_SetString(PyExc_ValueError, "Invalid number of digest bits"); \
	goto error; \
    } \
\
    new = PyObject_New(skein ## X ## Object, &skein ## X ## Type); \
    if (new == NULL) \
	goto error; \
    if (mac.buf == NULL) \
        Skein ## Y ## _Init(&new->ctx, hashBitLen); \
    else { \
        Skein ## Y ## _InitExt(&new->ctx, hashBitLen, \
                SKEIN_CFG_TREE_INFO_SEQUENTIAL, mac.buf, mac.len); \
        PyBuffer_Release(&mac); \
    } \
    new->blockBitLen = X; \
    new->hashByteLen = (hashBitLen+7)>>3; \
    if (buf.buf != NULL) { \
	Skein ## Y ## _Update(&new->ctx, buf.buf, buf.len); \
        PyBuffer_Release(&buf); \
    } \
    return (PyObject *)new; \
\
error:\
    if (buf.buf != NULL) { \
        PyBuffer_Release(&buf); \
    } \
    if (mac.buf != NULL) { \
        PyBuffer_Release(&mac); \
    } \
    return NULL;\
}
FACTORYDEF(256, _256)
FACTORYDEF(512, _512)
FACTORYDEF(1024, 1024)

PyDoc_STRVAR(threefish_new__doc__,
"Return a new Threefish encryption object.\n\n"
"Takes key and tweak as bytes parameters.");

static PyObject *
threefish_new(PyObject *self, PyObject *args)
{
    threefishObject *new;
    Py_buffer key, tweak;

    if (!PyArg_ParseTuple(args, "y*y*:threefish", &key, &tweak))
	return NULL;
    if (key.len != 32 && key.len != 64 && key.len != 128) {
	PyErr_SetString(PyExc_ValueError,
                        "key must be 32, 64 or 128 bytes long");
	goto error;
    }
    if (tweak.len != 16) {
	PyErr_SetString(PyExc_ValueError, "tweak must be 16 bytes long");
	goto error;
    }

    new = PyObject_New(threefishObject, &threefishType);
    if (new == NULL)
	goto error;
    new->blockByteLen = key.len;

    /* make ctx and set key and tweak */
    switch (key.len) {
        case 32:
            if((new->ctx = PyMem_Malloc(sizeof(Skein_256_Ctxt_t))) == NULL)
	        return PyErr_NoMemory();
            Skein_Get64_LSB_First(((Skein_256_Ctxt_t *)(new->ctx))->X,
                                  key.buf, 4);
            Skein_Get64_LSB_First(((Skein_256_Ctxt_t *)(new->ctx))->h.T,
                                  tweak.buf, 2);
            break;
        case 64:
            if((new->ctx = PyMem_Malloc(sizeof(Skein_512_Ctxt_t))) == NULL)
	        return PyErr_NoMemory();
            Skein_Get64_LSB_First(((Skein_512_Ctxt_t *)(new->ctx))->X,
                                  key.buf, 8);
            Skein_Get64_LSB_First(((Skein_512_Ctxt_t *)(new->ctx))->h.T,
                                  tweak.buf, 2);
            break;
        case 128:
            if((new->ctx = PyMem_Malloc(sizeof(Skein1024_Ctxt_t))) == NULL)
	        return PyErr_NoMemory();
            Skein_Get64_LSB_First(((Skein1024_Ctxt_t *)(new->ctx))->X,
                                  key.buf, 16);
            Skein_Get64_LSB_First(((Skein1024_Ctxt_t *)(new->ctx))->h.T,
                                  tweak.buf, 2);
            break;
    }

    PyBuffer_Release(&key);
    PyBuffer_Release(&tweak);
    return (PyObject *)new;

error:
    PyBuffer_Release(&key);
    PyBuffer_Release(&tweak);
    return NULL;
}


#define METHODDEFLINE(X) \
{"skein" #X , (PyCFunction)skein ## X ## _new, METH_VARARGS|METH_KEYWORDS, \
skein ## X ## _new__doc__}

static struct PyMethodDef skein_functions[] = {
    METHODDEFLINE(256),
    METHODDEFLINE(512),
    METHODDEFLINE(1024),
    {"threefish", (PyCFunction)threefish_new, METH_VARARGS,
        threefish_new__doc__},
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
    if (PyType_Ready(&skein256Type) < 0 ||
	PyType_Ready(&skein512Type) < 0 ||
	PyType_Ready(&skein1024Type) < 0 ||
        PyType_Ready(&threefishType) < 0)
	return NULL;
    return PyModule_Create(&skeinmodule);
}

