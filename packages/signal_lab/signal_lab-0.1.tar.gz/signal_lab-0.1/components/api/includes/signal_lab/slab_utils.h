

#ifndef __ALT_SLAB_UTILS_H__
#define __ALT_SLAB_UTILS_H__


#include <Python.h>
#include <signal_lab.h>

void sl_pycheck( PyObject* obj );

PyObject* sl_to_py_tuple( int argc , char** argv );

PyObject* _sl_from_env( sl_environ env);
sl_environ _sl_to_env( PyObject* penv );

PyObject* _sl_from_file( sl_file file );
sl_file _sl_to_file( PyObject* penv );


sl_file * _sl_to_files( PyObject* inputs );
PyObject* _sl_from_files( sl_file* files, int nb_files );

void _set_module(PyObject*);

#endif //__ALT_SLAB_UTILS_H__
