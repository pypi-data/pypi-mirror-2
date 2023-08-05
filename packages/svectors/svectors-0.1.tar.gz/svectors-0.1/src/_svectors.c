/*
    _svectors.c
    Copyright 2008, 2009, 2010 Hagen Fürstenau <hfuerstenau@gmx.net>
    Some of this code evolved from an implementation by Doug Whiting,
    which was released to the public domain.

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

#define RESIZE_STEP_SIZE 1000000

#if !(defined HAVE_UINT64_T)
#error "svectors requires PY_UINT64_T"
#endif

typedef struct {
    PY_UINT64_T id;
    double v;
} entry_t;


int add_entry(entry_t **data, size_t *size, size_t *filled,
              PY_UINT64_T id, double v)
{
    if (*filled >= *size) {
        *size += RESIZE_STEP_SIZE;
        /* printf("resized data to %ld items\n", *size); */
        *data = PyMem_Realloc(*data, (*size)*sizeof(entry_t));
        if (*data == NULL)
            return 0;
    }
    ((*data)[*filled]).id = id;
    ((*data)[*filled]).v = v;
    ++*filled;
    return 1;
}

PyDoc_STRVAR(make_image_doc,
"make_image(iterator, file, snip_flag=False)\n\n"
"Take an iterator with items of the form (word, [(id1, v1), ..., (idn, vn)])\n"
"and a file object to which the resulting image is dumped.\n\n"
"The 'snip_flag' tells the Dataset methods to discard the last character of \n"
"each lemma before looking it up in the index. This is a cheap way of making \n"
"images aware of whether they contain POS tags while maintaining efficiency.");

static PyObject *
make_image(PyObject *self, PyObject *args, PyObject *kw)
{
    static char *kwlist[] = {"iterator", "file", "snip_flag", NULL};
    PyObject *iter, *file, *snip_flag=NULL;
    PyObject *entry=NULL, *entry2, *word, *l, *filledObj, *id, *v;
    Py_ssize_t pos, len;
    entry_t *data;
    PyObject *index=NULL, *bytes=NULL;
    size_t size, filled;
    PyObject *pickle=NULL, *dump=NULL, *tuple=NULL, *write=NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "OO|O:make_image",
                                     kwlist, &iter, &file, &snip_flag))
        return NULL;
    if (!PyIter_Check(iter)) {
        PyErr_SetString(PyExc_TypeError, "argument has to be an iterator");
        return NULL;
    }

    /* build index and data from iterator */
    if ((index=PyDict_New()) == NULL)
        return NULL;
    filled = 0;
    size = RESIZE_STEP_SIZE;
    if ((data=PyMem_Malloc(size*sizeof(entry_t))) == NULL)
        goto error;
    while ((entry=PyIter_Next(iter))) {
        word = PyTuple_GetItem(entry, 0);
        l = PyTuple_GetItem(entry, 1);
        if (!(word && l))
            goto error;
        filledObj = PyLong_FromSize_t(filled);
        PyDict_SetItem(index, word, filledObj);
        Py_CLEAR(filledObj);

        if ((len=PyList_Size(l)) == -1)
            goto error;
        for (pos=0; pos<len; pos++) {
            if (!(entry2 = PyList_GetItem(l, pos)))
                goto error;
            id = PyTuple_GetItem(entry2, 0);
            v = PyTuple_GetItem(entry2, 1);
            if (!(id && v))
                goto error;
            if (!add_entry(&data, &size, &filled,
                           PyLong_AsLongLong(id), PyFloat_AsDouble(v)))
                goto error;
        }
        if (!add_entry(&data, &size, &filled, -1, 0))
            goto error;
        Py_CLEAR(entry);
    }
    if (PyErr_Occurred())
        goto error;

    /* store snip_flag */
    if ((snip_flag != NULL) && (PyObject_IsTrue(snip_flag)))
        PyDict_SetItem(index, Py_None, Py_None);

    /* make bytes from data */
    bytes = PyBytes_FromStringAndSize((char *)data, filled*sizeof(entry_t));
    if (bytes == NULL)
        goto error;
    PyMem_Free(data);

    /* write pickle of index to file */
    if ((pickle=PyImport_ImportModule("pickle")) == NULL)
        goto error;
    if ((dump=PyObject_GetAttrString(pickle, "dump")) == NULL)
        goto error;
    if ((tuple=PyTuple_New(2)) == NULL)
        goto error;
    Py_INCREF(index);
    Py_INCREF(file);
    PyTuple_SET_ITEM(tuple, 0, index);
    PyTuple_SET_ITEM(tuple, 1, file);
    if (PyObject_Call(dump, tuple, NULL) == NULL)
        goto error;
    Py_CLEAR(pickle);
    Py_CLEAR(dump);
    Py_CLEAR(tuple);
    Py_CLEAR(index);

    /* write bytes to file */
    if ((write=PyObject_GetAttrString(file, "write")) == NULL)
        goto error;
    if ((tuple=PyTuple_New(1)) == NULL)
        goto error;
    Py_INCREF(bytes);
    PyTuple_SET_ITEM(tuple, 0, bytes);
    if (PyObject_Call(write, tuple, NULL) == NULL)
        goto error;
    Py_CLEAR(write);
    Py_CLEAR(tuple);
    Py_CLEAR(bytes);

    return Py_None;

error:
    Py_CLEAR(index);
    Py_CLEAR(bytes);
    Py_CLEAR(entry);
    Py_CLEAR(pickle);
    Py_CLEAR(dump);
    Py_CLEAR(write);
    Py_CLEAR(tuple);
    PyMem_Free(data);
    return NULL;
}


typedef struct {
    PyObject_HEAD
    PyObject *index;
    PyObject *bytes;
    int snip_flag;
} DatasetObject;


static int
Dataset_init(DatasetObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *file;
    PyObject *pickle=NULL, *load=NULL;
    PyObject *tuple=NULL, *read=NULL;

    self->index = NULL;
    self->bytes = NULL;

    if (!PyArg_ParseTuple(args, "O:Dataset", &file))
        return -1;

    /* unpickle the index */
    if ((pickle=PyImport_ImportModule("pickle")) == NULL)
        return -1;
    if ((load=PyObject_GetAttrString(pickle, "load")) == NULL)
        goto error;
    if ((tuple=PyTuple_New(1)) == NULL)
        goto error;
    Py_INCREF(file);
    PyTuple_SET_ITEM(tuple, 0, file);
    if ((self->index=PyObject_Call(load, tuple, NULL)) == NULL)
        goto error;
    Py_CLEAR(pickle);
    Py_CLEAR(load);
    Py_CLEAR(tuple);

    /* read snip_flag */
    self->snip_flag = (PyDict_GetItem(self->index, Py_None) != NULL);

    /* read the bytes object */
    read = PyObject_GetAttrString(file, "read");
    if (read == NULL)
        goto error;
    if ((tuple=PyTuple_New(0)) == NULL)
        goto error;
    if ((self->bytes=PyObject_Call(read, tuple, NULL)) == NULL)
        goto error;
    Py_CLEAR(read);
    Py_CLEAR(tuple);

    return 0;

error:
    Py_CLEAR(pickle);
    Py_CLEAR(load);
    Py_CLEAR(read);
    Py_CLEAR(tuple);
    return -1;
}

static void
Dataset_dealloc(DatasetObject* self)
{
    Py_CLEAR(self->index);
    Py_CLEAR(self->bytes);
}

static PyObject *
Dataset_dot(DatasetObject *self, PyObject *args)
{
    PyObject *w1, *w2, *index1, *index2;
    size_t i, j;
    PY_UINT64_T id1, id2;
    double res=0;
    entry_t *data;

    if (!PyArg_ParseTuple(args, "OO:dot", &w1, &w2))
        return NULL;
    if (self->snip_flag) {
        w1 = PySequence_GetSlice(w1, 0, -1);
        w2 = PySequence_GetSlice(w2, 0, -1);
    }
    if (PyUnicode_Compare(w1, w2) == 0)
        return PyFloat_FromDouble(1);
    if (!((index1=PyDict_GetItem(self->index, w1)) &&
          (index2=PyDict_GetItem(self->index, w2))))
        return PyFloat_FromDouble(0);
    i = PyLong_AsSize_t(index1);
    j = PyLong_AsSize_t(index2);
    data = (entry_t *)PyBytes_AS_STRING(self->bytes);

    while (1) {
        id1 = data[i].id;
        id2 = data[j].id;
        if ((id1 == -1) || (id2 == -1))
            break;
        if (id1 == id2) {
            res += data[i].v * data[j].v;
            ++i, ++j;
        }
        else if (id1 < id2)
            ++i;
        else
            ++j;
    }

    if (self->snip_flag) {
        Py_CLEAR(w1);
        Py_CLEAR(w2);
    }
    return PyFloat_FromDouble(res);
}

static PyObject *
Dataset_bjc(DatasetObject *self, PyObject *args)
{
    PyObject *w1, *w2;
    PyObject *index1, *index2;
    size_t i0, j0, i, j;
    PY_UINT64_T id1, id2, hyp1, hyp2, syn1, syn2;
    double v1, v2;
    entry_t *data;

    if (!PyArg_ParseTuple(args, "OO:bjc", &w1, &w2))
        return NULL;
    if (PyUnicode_Compare(w1, w2) == 0)
        return PyFloat_FromDouble(1);
    if (!((index1=PyDict_GetItem(self->index, w1)) &&
          (index2=PyDict_GetItem(self->index, w2)))) {
        return PyFloat_FromDouble(0);
    }
    i0 = i = PyLong_AsSize_t(index1);
    j0 = j = PyLong_AsSize_t(index2);
    data = (entry_t *)PyBytes_AS_STRING(self->bytes);

    /* find common ancestor with maximum information content */
    while (1) {
        id1 = data[i].id;
        id2 = data[j].id;
        if ((id1 == -1) || (id2 == -1))
            return PyFloat_FromDouble(0);
        hyp1 = id1 & 0xffffffff;
        hyp2 = id2 & 0xffffffff;
        v1 = data[i].v;
        v2 = data[j].v;
        if (hyp1 == hyp2) {
            syn1 = id1 >> 32;
            syn2 = id2 >> 32;
            break;
        }
        else if (v1 < v2)
            ++j;
        else if (v1 > v2)
            ++i;
        else if (hyp1 < hyp2)  /* conventional order for v1 == v2 */
            ++j;
        else
            ++i;
    }

    /* find information content of the two synsets */
    assert(v1 == v2);
    while (((id1=data[i0].id)&0xffffffff) != syn1) {
        if (id1 == -1) {
            PyErr_SetString(PyExc_RuntimeError, "Dataset inconsistent");
            return NULL;
        }
        ++i0;
    }
    while (((id2=data[j0].id)&0xffffffff) != syn2) {
        if (id2 == -1) {
            PyErr_SetString(PyExc_RuntimeError, "Dataset inconsistent");
            return NULL;
        }
        ++j0;
    }

    /* compute Jiang/Conrath similarity */
    return PyFloat_FromDouble(1 / (1+data[i0].v+data[j0].v-2*v1));
}

static PyMethodDef Dataset_methods[] = {
    {"dot", (PyCFunction)Dataset_dot, METH_VARARGS, NULL},
    {"bjc", (PyCFunction)Dataset_bjc, METH_VARARGS, NULL},
    {NULL, NULL}
};


static PyTypeObject DatasetType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "Dataset",                      /* tp_name */
    sizeof(DatasetObject),          /* tp_basicsize */
    0,                              /* tp_itemsize */
    (destructor)Dataset_dealloc,    /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_compare */
    0,                              /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    0,                              /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,             /* tp_flags */
    0,                              /* tp_doc */
    0,                              /* tp_traverse */
    0,                              /* tp_clear */
    0,                              /* tp_richcompare */
    0,                              /* tp_weaklistoffset */
    0,                              /* tp_iter */
    0,                              /* tp_iternext */
    Dataset_methods,                /* tp_methods */
    NULL,                           /* tp_members */
    0,                              /* tp_getset */
    0,                              /* tp_base */
    0,                              /* tp_dict */
    0,                              /* tp_descr_get */
    0,                              /* tp_descr_set */
    0,                              /* tp_dict_offset */
    (initproc)Dataset_init,         /* tp_init */
};



static struct PyMethodDef svectors_functions[] = {
    {"make_image", (PyCFunction)make_image, METH_VARARGS|METH_KEYWORDS,
                   make_image_doc},
    {NULL, NULL}
};

static struct PyModuleDef svectors_module = {
    PyModuleDef_HEAD_INIT,
    "_svectors",
    NULL,
    -1,
    svectors_functions
};

PyMODINIT_FUNC
PyInit__svectors(void)
{
    PyObject *m;

    /* init DatasetType */
    DatasetType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&DatasetType) < 0)
        return NULL;

    /* init module */
    if ((m=PyModule_Create(&svectors_module)) == NULL)
        return NULL;
    Py_INCREF(&DatasetType);
    if (PyModule_AddObject(m, "Dataset", (PyObject *)&DatasetType) < 0)
        return NULL;
    return m;
}
