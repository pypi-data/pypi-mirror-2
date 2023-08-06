#ifndef FAULTHANDLER_HEADER
#define FAULTHANDLER_HEADER

#include "Python.h"
#include <signal.h>

#define MAX_FRAME_DEPTH 100

#define PUTS(fd, str) write(fd, str, strlen(str))

extern int faulthandler_enabled;

void faulthandler_init(void);

void faulthandler_enable(void);
PyObject* faulthandler_enable_py(PyObject *self);
PyObject* faulthandler_disable(PyObject *self);
PyObject* faulthandler_isenabled(PyObject *self);

void faulthandler_dump_backtrace(int fd);
PyObject* faulthandler_dump_backtrace_py(PyObject *self);
PyObject* faulthandler_dump_backtrace_threads(PyObject *self);

PyObject* faulthandler_sigsegv(PyObject *self, PyObject *args);
PyObject* faulthandler_sigfpe(PyObject *self, PyObject *args);

#if defined(SIGBUS)
PyObject* faulthandler_sigbus(PyObject *self, PyObject *args);
#endif

#if defined(SIGILL)
PyObject* faulthandler_sigill(PyObject *self, PyObject *args);
#endif

#endif

