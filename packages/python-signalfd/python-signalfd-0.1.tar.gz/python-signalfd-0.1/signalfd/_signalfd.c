/*
 * Copyright (c) 2010 Jean-Paul Calderone.
 * See LICENSE file for details.
 *
 * sigprocmask and signalfd wrapper module.
 */

#include "Python.h"

#include <signal.h>
#include <sys/signalfd.h>

#if (PY_VERSION_HEX >= 0x03000000)
#define PY3
#endif

static int
_iterable_to_mask(PyObject *iterable, sigset_t *mask)
{
    static const char* range_format = "signal number %d out of range";
    int result = 0;

    PyObject *item, *iterator = NULL;

    sigemptyset(mask);

    iterator = PyObject_GetIter(iterable);
    if (iterator == NULL) {
        result = -1;
        goto error;
    }

    while ((item = PyIter_Next(iterator))) {
#ifdef PY3
        int signum = PyLong_AsLong(item);
#else
        int signum = PyInt_AsLong(item);
#endif
        Py_DECREF(item);
        if (signum == -1 && PyErr_Occurred()) {
	    result = -1;
	    goto error;
        }
        if (sigaddset(mask, signum) == -1) {
            PyErr_Format(PyExc_ValueError, range_format, signum);
            result = -1;
            goto error;
        }
    }

error:
    Py_XDECREF(iterator);
    return result;
}

#define PY_SIGMASK pthread_sigmask

static PyObject *
signal_sigprocmask(PyObject *self, PyObject *args)
{
    static const char* how_format = "value specified for how (%d) invalid";

    int how, sig;
    PyObject *signals, *result, *signum;
    sigset_t mask, previous;

    if (!PyArg_ParseTuple(args, "iO:sigprocmask", &how, &signals)) {
        return NULL;
    }

    if (_iterable_to_mask(signals, &mask) == -1) {
        return NULL;
    }

    if (PY_SIGMASK(how, &mask, &previous) != 0) {
        PyErr_Format(PyExc_ValueError, how_format, how);
        return NULL;
    }

    result = PyList_New(0);
    if (result == NULL) {
        return NULL;
    }

    for (sig = 1; sig < NSIG; ++sig) {
        if (sigismember(&previous, sig) == 1) {
            /* Handle the case where it is a member by adding the signal to
               the result list.  Ignore the other cases because they mean the
               signal isn't a member of the mask or the signal was invalid,
               and an invalid signal must have been our fault in constructing
               the loop boundaries. */
            signum = PyLong_FromLong(sig);
            if (signum == NULL) {
                Py_DECREF(result);
                return NULL;
            }
            if (PyList_Append(result, signum) == -1) {
                Py_DECREF(signum);
                Py_DECREF(result);
                return NULL;
            }
            Py_DECREF(signum);
        }
    }
    return result;
}

PyDoc_STRVAR(sigprocmask_doc,
"sigprocmask(how, mask) -> old mask\n\
\n\
Examine and change blocked signals.");

static PyObject *
signal_signalfd(PyObject *self, PyObject *args)
{
    int result, flags = 0;
    sigset_t mask;

    int fd;
    PyObject *signals;

    if (!PyArg_ParseTuple(args, "iO|i:signalfd", &fd, &signals, &flags)) {
        return NULL;
    }

    if (_iterable_to_mask(signals, &mask) == -1) {
        return NULL;
    }

    result = signalfd(-1, &mask, flags);

    if (result == -1) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return PyLong_FromLong(result);
}

PyDoc_STRVAR(signalfd_doc,
"signalfd(fd, mask, flags)\n\
\n\
Create a file descriptor for accepting signals.");


PyDoc_STRVAR(_signalfd_doc,
             "This module wraps sigprocmask(2) and signalfd(2).\n");


static PyMethodDef _signalfd_methods[] = {
    {"sigprocmask", signal_sigprocmask, METH_VARARGS, sigprocmask_doc},
    {"signalfd", signal_signalfd, METH_VARARGS, signalfd_doc},
    {NULL, NULL}
};

#ifdef PY3
static struct PyModuleDef _signalfdmodule = {
    PyModuleDef_HEAD_INIT,
    "signalfd._signalfd",
    _signalfd_doc,
    -1,
    _signalfd_methods,
    NULL,
    NULL,
    NULL,
    NULL
};
#endif

PyMODINIT_FUNC
#ifdef PY3
PyInit__signalfd(void) {
#else
init_signalfd(void) {
#endif
    PyObject *m, *x;

#ifdef PY3
    m = PyModule_Create(&_signalfdmodule);
#else
    m = Py_InitModule3(
        "signalfd._signalfd", _signalfd_methods, _signalfd_doc);
#endif

#ifdef SIG_BLOCK
    x = PyLong_FromLong(SIG_BLOCK);
    PyModule_AddObject(m, "SIG_BLOCK", x);
#endif

#ifdef SIG_UNBLOCK
    x = PyLong_FromLong(SIG_UNBLOCK);
    PyModule_AddObject(m, "SIG_UNBLOCK", x);
#endif

#ifdef SIG_SETMASK
    x = PyLong_FromLong(SIG_SETMASK);
    PyModule_AddObject(m, "SIG_SETMASK", x);
#endif

#ifdef SFD_CLOEXEC
    x = PyLong_FromLong(SFD_CLOEXEC);
    PyModule_AddObject(m, "SFD_CLOEXEC", x);
#endif

#ifdef SFD_NONBLOCK
    x = PyLong_FromLong(SFD_NONBLOCK);
    PyModule_AddObject(m, "SFD_NONBLOCK", x);
#endif

#ifdef PY3
    return m;
#endif
}

#ifdef PY3
#undef PY3
#endif
