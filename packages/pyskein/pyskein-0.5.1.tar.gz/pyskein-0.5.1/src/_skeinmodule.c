/*
   _skeinmodule.c
   Copyright 2008, 2009 Hagen Fürstenau <hfuerstenau@gmx.net>

   Wraps skein.c and threefish.c into a Python module.

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
#include "threefish.h"


/* objects */

static PyTypeObject skein256Type;
static PyTypeObject skein512Type;
static PyTypeObject skein1024Type;

#define SKEIN_OBJECTDEF(X, Y) typedef struct { \
    PyObject_HEAD \
    int blockBitLen; \
    int hashByteLen; \
    Skein ## Y ## _Ctxt_t ctx; \
} skein ## X ## Object;
SKEIN_OBJECTDEF(256, _256)
SKEIN_OBJECTDEF(512, _512)
SKEIN_OBJECTDEF(1024, 1024)


typedef struct {
    PyObject_HEAD
    size_t blockByteLen;
    u64b_t *kw;            /* precomputed key schedule */
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

static PyObject *
threefish_get_tweak(PyObject *self, void *closure)
{
    PyObject *rv;
    char *buf;

    if ((rv = PyBytes_FromStringAndSize(NULL, 16)) == NULL ||
            (buf = PyBytes_AsString(rv)) == NULL)
        return NULL;
    Skein_Put64_LSB_First(buf, ((threefishObject *)self)->kw, 16);
    return rv;
}

static int
threefish_set_tweak(PyObject *self, PyObject *value, void *closure)
{
    char *buf;
    Py_ssize_t len;
    PyObject *h=NULL;

    if (PyByteArray_Check(value))
        if ((h = value = PyBytes_FromObject(value)) == NULL)
            return -1;
    if (PyBytes_AsStringAndSize(value, &buf, &len) < 0)
        goto error;
    if (len != 16) {
        PyErr_SetString(PyExc_ValueError, "tweak value must have 16 bytes");
        goto error;
    }
    Skein_Get64_LSB_First(((threefishObject *)self)->kw, buf, 2);
    Py_CLEAR(h);
    return 0;
error:
    Py_CLEAR(h);
    return -1;
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
    {"tweak",
     (getter)threefish_get_tweak, (setter)threefish_set_tweak,
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

PyDoc_STRVAR(threefish_encrypt_block__doc__,
"Encrypt the given block.");

static PyObject *
threefish_encrypt_block(PyObject *self, PyObject *args)
{
    u64b_t *kw = ((threefishObject *)self)->kw;
    u64b_t w[16], out[16];
    size_t len = ((threefishObject *)self)->blockByteLen;
    char *q;
    Py_buffer buf;
    PyObject *rv;

    if (!PyArg_ParseTuple(args, "y*:encrypt", &buf))
        return NULL;
    if (buf.len != len) {
        PyErr_Format(PyExc_ValueError,
                     "block must have same length as key (%d bytes)", len);
        PyBuffer_Release(&buf);
        return NULL;
    }

    /* set up output buffer */
    if ((rv = PyBytes_FromStringAndSize(NULL, len)) == NULL)
        return NULL;
    if ((q = PyBytes_AsString(rv)) == NULL)
        return NULL;

    switch (len) {
        case 32:
            Skein_Get64_LSB_First(w, buf.buf, 4);
            Threefish_256_encrypt(kw, w, out, 0);
            Skein_Put64_LSB_First(q, out, 32);
            break;
        case 64:
            Skein_Get64_LSB_First(w, buf.buf, 8);
            Threefish_512_encrypt(kw, w, out, 0);
            Skein_Put64_LSB_First(q, out, 64);
            break;
        case 128:
            Skein_Get64_LSB_First(w, buf.buf, 16);
            Threefish1024_encrypt(kw, w, out, 0);
            Skein_Put64_LSB_First(q, out, 128);
    }
    PyBuffer_Release(&buf);
    return rv;
}


PyDoc_STRVAR(threefish_decrypt_block__doc__,
"Decrypt the given block.");

static PyObject *
threefish_decrypt_block(PyObject *self, PyObject *args)
{
    u64b_t *kw = ((threefishObject *)self)->kw;
    u64b_t w[16], out[16];
    size_t len = ((threefishObject *)self)->blockByteLen;
    char *q;
    Py_buffer buf;
    PyObject *rv;

    if (!PyArg_ParseTuple(args, "y*:decrypt", &buf))
        return NULL;
    if (buf.len != len) {
        PyErr_Format(PyExc_ValueError,
                     "block must have same length as key (%d bytes)", len);
        PyBuffer_Release(&buf);
        return NULL;
    }

    /* set up output buffer */
    if ((rv = PyBytes_FromStringAndSize(NULL, len)) == NULL)
        return NULL;
    if ((q = PyBytes_AsString(rv)) == NULL)
        return NULL;

    switch (len) {
        case 32:
            Skein_Get64_LSB_First(w, buf.buf, 4);
            Threefish_256_decrypt(kw, w, out);
            Skein_Put64_LSB_First(q, out, 32);
            break;
        case 64:
            Skein_Get64_LSB_First(w, buf.buf, 8);
            Threefish_512_decrypt(kw, w, out);
            Skein_Put64_LSB_First(q, out, 64);
            break;
        case 128:
            Skein_Get64_LSB_First(w, buf.buf, 16);
            Threefish1024_decrypt(kw, w, out);
            Skein_Put64_LSB_First(q, out, 128);
    }
    PyBuffer_Release(&buf);
    return rv;
}


static PyMethodDef threefish_methods[] = {
    {"encrypt_block", (PyCFunction)threefish_encrypt_block, METH_VARARGS,
        threefish_encrypt_block__doc__},
    {"decrypt_block", (PyCFunction)threefish_decrypt_block, METH_VARARGS,
        threefish_decrypt_block__doc__},
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
    PyMem_Free(((threefishObject *)self)->kw);
    PyObject_Del(self);
}

#define TYPEDEF(X) \
static PyTypeObject skein ## X ## Type = {                  \
    PyVarObject_HEAD_INIT(NULL, 0)                          \
    "_skein.skein" #X,             /* tp_name */            \
    sizeof(skein ## X ## Object),  /* tp_basicsize */       \
    0,                             /* tp_itemsize */        \
    skein_dealloc,                 /* tp_dealloc */         \
    0,                             /* tp_print */           \
    0,                             /* tp_getattr */         \
    0,                             /* tp_setattr */         \
    0,                             /* tp_compare */         \
    0,                             /* tp_repr */            \
    0,                             /* tp_as_number */       \
    0,                             /* tp_as_sequence */     \
    0,                             /* tp_as_mapping */      \
    0,                             /* tp_hash */            \
    0,                             /* tp_call */            \
    0,                             /* tp_str */             \
    0,                             /* tp_getattro */        \
    0,                             /* tp_setattro */        \
    0,                             /* tp_as_buffer */       \
    Py_TPFLAGS_DEFAULT,            /* tp_flags */           \
    0,                             /* tp_doc */             \
    0,                             /* tp_traverse */        \
    0,                             /* tp_clear */           \
    0,                             /* tp_richcompare */     \
    0,                             /* tp_weaklistoffset */  \
    0,                             /* tp_iter */            \
    0,                             /* tp_iternext */        \
    skein ## X ## _methods,        /* tp_methods */         \
    NULL,                          /* tp_members */         \
    skein_getseters                /* tp_getset */          \
}
TYPEDEF(256);
TYPEDEF(512);
TYPEDEF(1024);

static PyTypeObject threefishType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_skein.threefish",       /* tp_name */
    sizeof(threefishObject),  /* tp_basicsize */
    0,                        /* tp_itemsize */
    threefish_dealloc,        /* tp_dealloc */
    0,                        /* tp_print */
    0,                        /* tp_getattr */
    0,                        /* tp_setattr */
    0,                        /* tp_compare */
    0,                        /* tp_repr */
    0,                        /* tp_as_number */
    0,                        /* tp_as_sequence */
    0,                        /* tp_as_mapping */
    0,                        /* tp_hash */
    0,                        /* tp_call */
    0,                        /* tp_str */
    0,                        /* tp_getattro */
    0,                        /* tp_setattro */
    0,                        /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,       /* tp_flags */
    0,                        /* tp_doc */
    0,                        /* tp_traverse */
    0,                        /* tp_clear */
    0,                        /* tp_richcompare */
    0,                        /* tp_weaklistoffset */
    0,                        /* tp_iter */
    0,                        /* tp_iternext */
    threefish_methods,        /* tp_methods */
    NULL,                     /* tp_members */
    threefish_getseters       /* tp_getset */
};


/* factory functions */

#define FACTORYDEF(X, Y)  \
PyDoc_STRVAR(skein ## X ## _new__doc__,  \
"skein" #X "(init=b'', digest_bits=" #X ", mac=b'', pers=b'', nonce=b'')\n\n" \
"Return a new Skein-" #X " hash object.\n\n"); \
\
static PyObject * \
skein ## X ## _new(PyObject *self, PyObject *args, PyObject *kw) \
{ \
    skein ## X ## Object *new; \
    Py_buffer buf, mac, pers, nonce; \
    int hashBitLen = X; \
    static char *kwlist[] = {"init", "digest_bits", "mac", "pers", "nonce", \
                             NULL}; \
\
    buf.buf = mac.buf = pers.buf = nonce.buf = NULL; \
    if (!PyArg_ParseTupleAndKeywords(args, kw, "|y*iy*y*y*:skein" #X , kwlist,\
                                     &buf, &hashBitLen, &mac, &pers, &nonce)) \
        goto error; \
    if (hashBitLen <= 0 || hashBitLen%8 != 0) { \
        PyErr_SetString(PyExc_ValueError, "Invalid number of digest bits"); \
        goto error; \
    } \
\
    new = PyObject_New(skein ## X ## Object, &skein ## X ## Type); \
    if (new == NULL) \
        goto error; \
    if (mac.buf == NULL && pers.buf == NULL && nonce.buf == NULL) \
        Skein ## Y ## _Init(&new->ctx, hashBitLen); \
    else { \
        Skein ## Y ## _InitExt(&new->ctx, hashBitLen, \
                               mac.buf, mac.len, pers.buf, pers.len, \
                               nonce.buf, nonce.len); \
    } \
    if (mac.buf != NULL) \
        PyBuffer_Release(&mac); \
    if (pers.buf != NULL) \
        PyBuffer_Release(&pers); \
    if (nonce.buf != NULL) \
        PyBuffer_Release(&nonce); \
\
    new->blockBitLen = X; \
    new->hashByteLen = (hashBitLen+7)>>3; \
    if (buf.buf != NULL) { \
        Skein ## Y ## _Update(&new->ctx, buf.buf, buf.len); \
        PyBuffer_Release(&buf); \
    } \
    return (PyObject *)new; \
\
error:\
    if (buf.buf != NULL) \
        PyBuffer_Release(&buf); \
    if (mac.buf != NULL) \
        PyBuffer_Release(&mac); \
    if (nonce.buf != NULL) \
        PyBuffer_Release(&nonce); \
    return NULL;\
}
FACTORYDEF(256, _256)
FACTORYDEF(512, _512)
FACTORYDEF(1024, 1024)

PyDoc_STRVAR(threefish_new__doc__,
"threefish(key, tweak)\n\n"
"Return a new Threefish encryption object.");

static PyObject *
threefish_new(PyObject *self, PyObject *args)
{
    threefishObject *new;
    Py_buffer key, tweak;
    int i;

    if (!PyArg_ParseTuple(args, "y*y*:threefish", &key, &tweak))
        return NULL;
    /* check key and tweak lengths */
    if (key.len != 32 && key.len != 64 && key.len != 128) {
        PyErr_SetString(PyExc_ValueError,
                        "key must be 32, 64 or 128 bytes long");
        goto error;
    }
    if (tweak.len != 16) {
        PyErr_SetString(PyExc_ValueError, "tweak must be 16 bytes long");
        goto error;
    }

    /* create object */
    new = PyObject_New(threefishObject, &threefishType);
    if (new == NULL)
        goto error;
    new->blockByteLen = key.len;
    /* precompute key schedule */
    if ((new->kw = PyMem_Malloc(sizeof(u64b_t)*(key.len/8+4))) == NULL)
        return PyErr_NoMemory();
    Skein_Get64_LSB_First(new->kw, tweak.buf, 2);
    new->kw[2] = new->kw[0] ^ new->kw[1];
    Skein_Get64_LSB_First(new->kw+3, key.buf, key.len/8);
    new->kw[3+key.len/8] = SKEIN_KS_PARITY;
    for (i=3; i<3+key.len/8; i++)
        new->kw[3+key.len/8] ^= new->kw[i];

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
    "_skein",
    NULL,
    -1,
    skein_functions,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC
PyInit__skein(void)
{
    if (PyType_Ready(&skein256Type) < 0 ||
        PyType_Ready(&skein512Type) < 0 ||
        PyType_Ready(&skein1024Type) < 0 ||
        PyType_Ready(&threefishType) < 0)
        return NULL;
    return PyModule_Create(&skeinmodule);
}
