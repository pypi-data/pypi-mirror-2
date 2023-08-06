/*
 * vim: tabstop=4 shiftwidth=4 softtabstop=4
 *
 * Copyright (c) 2011 Chris Behrens <cbehrens@codestud.com>
 * All Rights Reserved.
 *
 *    Licensed under the Apache License, Version 2.0 (the "License"); you may
 *    not use this file except in compliance with the License. You may obtain
 *    a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 *    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 *    License for the specific language governing permissions and limitations
 *    under the License.
 */


#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include <sys/types.h>
#include <errno.h>
#include <xs.h>
#undef _POSIX_C_SOURCE
#include <Python.h>
#include "pyxenstore.h"

#define PYXENSTORE_MODULE_NAME "pyxenstore"
#define PYXENSTORE_HANDLE_CLASS_NAME "Handle"


typedef struct _pyxs_handle pyxs_handle_t;

struct _pyxs_handle
{   
    PyObject_HEAD
    struct xs_handle *handle;
    xs_transaction_t txn;
};

static PyTypeObject _XenStoreHandle =
{   
    PyVarObject_HEAD_INIT(NULL, 0)
    PYXENSTORE_MODULE_NAME "." PYXENSTORE_HANDLE_CLASS_NAME, /* tp_name */
    sizeof(pyxs_handle_t),                      /* tp_basicsize */
    0,                                          /* tp_itemsize */
    0,                                          /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_compare */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   /* tp_flags */
    0,                                          /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    0,                                          /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    &PyBaseObject_Type,                         /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    0,                                          /* tp_init */
    PyType_GenericAlloc,                        /* tp_alloc */
    PyType_GenericNew,                          /* tp_new */
    0,                                          /* tp_free */
};

static PyObject *_PyXenStoreError;
static PyObject *_InvalidArgError;
static PyObject *_NotFoundError;
static PyObject *_TransactionStartedError;
static PyObject *_TransactionNotStartedError;
static PyObject *_NoPermissionError;

/* Static functions */

static int _handle_init(pyxs_handle_t *xsi, PyObject *args, PyObject *kwargs)
{   
    errno = 0;

    xsi->handle = xs_domain_open();
    if (xsi->handle == NULL)
    {
        int err = errno;

        /* We'll use this errno below, as xs_daemon_open() is really just a
         * last ditch effort
         */

        xsi->handle = xs_daemon_open();
        if (xsi->handle == NULL)
        {
            switch(err)
            {
                case ENOMEM:
                    PyErr_NoMemory();
                    return -1;
                case EACCES:
                    PyErr_Format(_NoPermissionError,
                            "No permission to open connection to the xenstore");
                    return -1;
                default:
                    break;
            }

            PyErr_Format(_PyXenStoreError,
                    "Couldn't open connection to the xenstore: %s",
                    strerror(err));
            return -1;
        }
    }

    xsi->txn = XBT_NULL;

    return 0;
}

static void _handle_dealloc(pyxs_handle_t *xsi)
{
    if (xsi->txn != XBT_NULL)
    {
        /* 
         * Happens if somehow object is deleted without ending the transaction.
         * Let's abort the transaction in this case...
         */
        xs_transaction_end(xsi->handle, xsi->txn, true);
    }

    if (xsi->handle != NULL)
    {
        xs_daemon_close(xsi->handle);
    }

    Py_TYPE(xsi)->tp_free((PyObject *)xsi);
}

static PyObject *_handle_transaction_start(pyxs_handle_t *xsi, PyObject *args)
{
    if (xsi->txn != XBT_NULL)
    {
        return PyErr_Format(_TransactionStartedError,
                "Transaction has already been started");
    }

    xsi->txn = xs_transaction_start(xsi->handle);
    if (xsi->txn == XBT_NULL)
    {
        int err = errno;

        switch(err)
        {
            case ENOMEM:
                return PyErr_NoMemory();
            default:
                break;
        }

        return PyErr_Format(_PyXenStoreError, "Failed to start transaction: %s",
                strerror(err));
    }

    Py_RETURN_NONE;
}

static PyObject *_handle_transaction_end(pyxs_handle_t *xsi, PyObject *args, PyObject *kwds)
{
    static char *keywords[] = { "abort", NULL };
    bool do_abort;
    PyObject *abort_obj = Py_False;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O!", keywords,
                &PyBool_Type,
                &abort_obj))
    {
        return NULL;
    }

    if (xsi->txn == XBT_NULL)
    {
        return PyErr_Format(_TransactionNotStartedError,
                "Transaction hasn't been started");
    }

    do_abort = (abort_obj == Py_True);

    xs_transaction_end(xsi->handle, xsi->txn, do_abort);

    xsi->txn = XBT_NULL;

    Py_RETURN_NONE;
}

static PyObject *_handle_entries(pyxs_handle_t *xsi, PyObject *args,
        PyObject *kwds)
{
    static char *keywords[] = { "path", NULL };
    char *path;
    unsigned int dir_list_num;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s", keywords,
                &path))
    {
        return NULL;
    }

    char **dir_list = xs_directory(xsi->handle, xsi->txn, path, &dir_list_num);
    if (dir_list == NULL)
    {
        int err = errno;

        switch(err)
        {
            case ENOMEM:
                return PyErr_NoMemory();
            case EINVAL:
                return PyErr_Format(_InvalidArgError,
                        "Invalid argument specified");
            case ENOENT:
                return PyErr_Format(_NotFoundError,
                        "Directory path '%s' doesn't exist", path);
            case EACCES:
                return PyErr_Format(_NoPermissionError,
                        "No permission to read '%s'", path);
            default:
                break;
        }

        return PyErr_Format(_PyXenStoreError,
                "Couldn't read entries from '%s': %s",
                path, strerror(err));
    }

    PyObject *list = PyList_New(dir_list_num);

    if (list == NULL)
    {
        free(dir_list);

        return NULL;
    }

    unsigned int i;

    for(i=0;i < dir_list_num;i++)
    {
        PyList_SetItem(list, i, PyString_FromString(dir_list[i]));
    }

    free(dir_list);

    return list;
}

static PyObject *_handle_read(pyxs_handle_t *xsi, PyObject *args, PyObject *kwds)
{
    static char *keywords[] = { "path", NULL };
    char *path;
    unsigned int len;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s", keywords,
                &path))
    {
        return NULL;
    }

    void *data = xs_read(xsi->handle, xsi->txn, path, &len);
    if (data == NULL)
    {
        int err = errno;

        switch(err)
        {
            case ENOMEM:
                return PyErr_NoMemory();
            case EINVAL:
                return PyErr_Format(_InvalidArgError,
                        "Invalid argument specified");
            case ENOENT:
                return PyErr_Format(_NotFoundError,
                        "Directory path '%s' doesn't exist", path);
            case EACCES:
                return PyErr_Format(_NoPermissionError,
                        "No permission to read from '%s'", path);
            default:
                break;
        }

        return PyErr_Format(_PyXenStoreError, "Couldn't read from '%s': %s",
                path, strerror(err));
    }

    PyObject *obj = PyString_FromStringAndSize(data, len);

    free(data);

    return obj;
}

static PyObject *_handle_write(pyxs_handle_t *xsi, PyObject *args, PyObject *kwds)
{
    static char *keywords[] = { "path", "data", NULL };
    char *path;
    void *data;
    Py_ssize_t data_len;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "ss#", keywords,
                &path,
                &data,
                &data_len))
    {
        return NULL;
    }

    if (!xs_write(xsi->handle, xsi->txn, path, data, data_len))
    {
        int err = errno;

        switch(err)
        {
            case ENOMEM:
                return PyErr_NoMemory();
            case EINVAL:
                return PyErr_Format(_InvalidArgError,
                        "Invalid argument specified");
            case EACCES:
                return PyErr_Format(_NoPermissionError,
                        "No permission to write to '%s'",
                        path);
            default:
                break;
        }

        return PyErr_Format(_PyXenStoreError, "Couldn't write to '%s': %s",
                path, strerror(err));
    }

    Py_RETURN_NONE;
}

static PyObject *_handle_mkdir(pyxs_handle_t *xsi, PyObject *args, PyObject *kwds)
{
    static char *keywords[] = { "path", NULL };
    char *path;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s", keywords,
                &path))
    {
        return NULL;
    }

    if (!xs_mkdir(xsi->handle, xsi->txn, path))
    {
        int err = errno;

        switch(err)
        {
            case ENOMEM:
                return PyErr_NoMemory();
            case EINVAL:
                return PyErr_Format(_InvalidArgError,
                        "Invalid argument specified");
            case EACCES:
                return PyErr_Format(_NoPermissionError,
                        "No permission to create '%s'",
                        path);
            default:
                break;
        }

        return PyErr_Format(_PyXenStoreError, "Couldn't create '%s': %s",
                path, strerror(err));
    }

    Py_RETURN_NONE;
}

static PyObject *_handle_rm(pyxs_handle_t *xsi, PyObject *args, PyObject *kwds)
{
    static char *keywords[] = { "path", NULL };
    char *path;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s", keywords,
                &path))
    {
        return NULL;
    }

    if (!xs_rm(xsi->handle, xsi->txn, path))
    {
        int err = errno;

        switch(err)
        {
            case ENOMEM:
                return PyErr_NoMemory();
            case EINVAL:
                return PyErr_Format(_InvalidArgError,
                        "Invalid argument specified");
            case EACCES:
                return PyErr_Format(_NoPermissionError,
                        "No permission to remove '%s'",
                        path);
            default:
                break;
        }

        return PyErr_Format(_PyXenStoreError, "Couldn't remove '%s': %s",
                path, strerror(err));
    }

    Py_RETURN_NONE;
}

static PyObject *_handle_permissions_get(pyxs_handle_t *xsi, PyObject *args, PyObject *kwds)
{
    static char *keywords[] = { "path", NULL };
    char *path;
    struct xs_permissions *perms;
    unsigned int i;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s", keywords,
                &path))
    {
        return NULL;
    }

    unsigned int num;

    perms = xs_get_permissions(xsi->handle, xsi->txn, path, &num);
    if (perms == NULL)
    {
        int err = errno;

        switch(err)
        {
            case ENOMEM:
                return PyErr_NoMemory();
            case EINVAL:
                return PyErr_Format(_InvalidArgError,
                        "Invalid argument specified");
            case ENOENT:
                return PyErr_Format(_NotFoundError,
                        "Directory path '%s' doesn't exist",
                        path);
            case EACCES:
                return PyErr_Format(_NoPermissionError,
                        "No permission to get permissions for '%s'",
                        path);
            default:
                break;
        }

        return PyErr_Format(_PyXenStoreError, "Couldn't get permissions for '%s': %s",
                path, strerror(err));
    }

    PyObject *tuple;
    PyObject *list = PyList_New(num);

    if (list == NULL)
    {
        free(perms);
        return NULL;
    }

    for(i=0;i < num;i++)
    {
        char buffer[40];

        if (!xs_perm_to_string(perms + i, buffer, sizeof(buffer)))
        {
            snprintf(buffer, sizeof(buffer), "%i", perms[i].perms);
        }
        else
        {
            buffer[1] = '\0'; /* don't want the ID */
        }

        tuple = PyTuple_New(2);
        if (tuple == NULL)
        {
            free(perms);
            Py_DECREF(list);
            return NULL;
        }

        PyTuple_SetItem(tuple, 0, PyInt_FromLong(perms[i].id));
        PyTuple_SetItem(tuple, 1, PyString_FromString(buffer));

        PyList_SetItem(list, i, tuple);
    }

    free(perms);

    return list;
}

static PyObject *_handle_permissions_set(pyxs_handle_t *xsi, PyObject *args, PyObject *kwds)
{
    static char *keywords[] = { "path", "perms", NULL };
    char *path;
    struct xs_permissions *perms;
    unsigned int i;
    PyObject *tuple;
    PyObject *list;
    char buffer[40];

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "sO!", keywords,
                &path,
                &PyList_Type,
                &list))
    {
        return NULL;
    }

    Py_ssize_t list_sz = PyList_Size(list);

    perms = malloc(list_sz * sizeof(struct xs_permissions));
    if (perms == NULL)
    {
        return PyErr_NoMemory();
    }

    for(i=0;i < list_sz;i++)
    {
        tuple = PyList_GetItem(list, i);
        if (!PyTuple_Check(tuple))
        {
            free(perms);
            return PyErr_Format(_InvalidArgError,
                    "List element #%d is not a tuple", i + 1);
        }

        if (PyTuple_Size(tuple) != 2)
        {
            free(perms);
            return PyErr_Format(_InvalidArgError,
                    "Tuple #%d does not contain 2 elements", i + 1);
        }

        PyObject *item1 = PyTuple_GetItem(tuple, 0);
        PyObject *item2 = PyTuple_GetItem(tuple, 1);

        if (!PyInt_Check(item1))
        {
            free(perms);
            return PyErr_Format(_InvalidArgError,
                    "Tuple #%d's first element is not an integer", i + 1);
        }

        if (!PyString_Check(item2))
        {
            free(perms);
            return PyErr_Format(_InvalidArgError,
                    "Tuple #%d's second element is not a string", i + 1);
        }

        snprintf(buffer, sizeof(buffer), "%s%ld",
                PyString_AsString(item2), PyInt_AsLong(item1));

        if (!xs_strings_to_perms(perms + i, 1, buffer))
        {
            free(perms);
            return PyErr_Format(_InvalidArgError,
                    "Tuple #%d contains invalid permissions", i + 1);
        }
    }

    if (!xs_set_permissions(xsi->handle, xsi->txn, path, perms, list_sz))
    {
        int err = errno;

        free(perms);

        switch(err)
        {
            case ENOMEM:
                return PyErr_NoMemory();
            case EINVAL:
                return PyErr_Format(_InvalidArgError,
                        "Invalid argument specified");
            case ENOENT:
                return PyErr_Format(_NotFoundError,
                        "Directory path '%s' doesn't exist",
                        path);
            case EACCES:
                return PyErr_Format(_NoPermissionError,
                        "No permission to set permissions on '%s'",
                        path);
            default:
                break;
        }

        return PyErr_Format(_PyXenStoreError,
                "Couldn't set permissions on '%s': %s",
                path, strerror(err));
    }

    free(perms);

    Py_RETURN_NONE;
}

static PyObject *_create_exception(PyObject *pymod, char *name, PyObject *base)
{
    PyObject *obj;
    char buf[128];

    snprintf(buf, sizeof(buf), "%s.%s", PYXENSTORE_MODULE_NAME, name);

    obj = PyErr_NewException(buf, base, NULL);
    if (obj == NULL)
        return NULL;

    PyModule_AddObject(pymod, name, obj);

    return obj;
}

PyMODINIT_FUNC PYXENSTORE_PUBLIC_API initpyxenstore(void)
{
    static PyMethodDef _mod_methods[] =
    {
        { NULL, NULL, METH_NOARGS, NULL }
    };

    static PyMethodDef _handle_methods[] =
    {
        { "transaction_start", (PyCFunction)_handle_transaction_start,
                METH_NOARGS, "Start a transaction" },
        { "transaction_end", (PyCFunction)_handle_transaction_end,
                METH_VARARGS|METH_KEYWORDS, "End a transaction" },
        { "entries", (PyCFunction)_handle_entries,
                METH_VARARGS|METH_KEYWORDS, "Get entries in a xenstore path" },
        { "read", (PyCFunction)_handle_read,
                METH_VARARGS|METH_KEYWORDS, "Read from a xenstore path" },
        { "write", (PyCFunction)_handle_write,
                METH_VARARGS|METH_KEYWORDS, "Write to a xenstore path" },
        { "mkdir", (PyCFunction)_handle_mkdir,
                METH_VARARGS|METH_KEYWORDS, "Create a xenstore path" },
        { "rm", (PyCFunction)_handle_rm,
                METH_VARARGS|METH_KEYWORDS, "Remove a xenstore path" },
        { "permissions_get", (PyCFunction)_handle_permissions_get,
                METH_VARARGS|METH_KEYWORDS, "Get permissions for a xenstore path" },
        { "permissions_set", (PyCFunction)_handle_permissions_set,
                METH_VARARGS|METH_KEYWORDS, "Set permissions for a xenstore path" },
        { NULL, NULL, METH_NOARGS, NULL }
    };

    _XenStoreHandle.tp_methods = _handle_methods;
    _XenStoreHandle.tp_init = (initproc)_handle_init;
    _XenStoreHandle.tp_dealloc = (destructor)_handle_dealloc;

    PyObject *pymod = Py_InitModule(PYXENSTORE_MODULE_NAME, _mod_methods);

    if (PyType_Ready(&_XenStoreHandle) < 0)
    {
        PyErr_Format(PyExc_SystemError, "Couldn't init %s.%s",
                PYXENSTORE_MODULE_NAME, PYXENSTORE_HANDLE_CLASS_NAME);
        return;
    }

    /* TODO(cbehrens) -- error checking for NULLs */
    _PyXenStoreError = _create_exception(pymod, "PyXenStoreError", NULL);
    _InvalidArgError = _create_exception(pymod, "InvalidArgError",
            _PyXenStoreError);
    _NotFoundError = _create_exception(pymod, "NotFoundError",
            _PyXenStoreError);
    _TransactionStartedError = _create_exception(pymod,
            "TransactionStartedError",
            _PyXenStoreError);
    _TransactionNotStartedError = _create_exception(pymod,
            "TransactionNotStartedError",
            _PyXenStoreError);
    _NoPermissionError = _create_exception(pymod, "NoPermissionError",
            _PyXenStoreError);

    PyModule_AddObject(pymod, PYXENSTORE_HANDLE_CLASS_NAME,
        (PyObject *)&_XenStoreHandle);
}

