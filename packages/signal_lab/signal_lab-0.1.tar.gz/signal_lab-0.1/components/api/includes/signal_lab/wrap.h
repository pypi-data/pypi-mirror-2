
#ifndef _SIGNAL_LAB_WRAP_H_
#define _SIGNAL_LAB_WRAP_H_

#include<Python.h>
#include<signal_lab/slab_utils.h>

#define SIGFUNCDEF( SIGFUNC ) int SIGFUNC( sl_environ env, sl_file* inputs, int nb_inputs , sl_file* outputs, int nb_outputs )

#define _WRAP_NAME( SIGNALFUNC ) wrap_##SIGNALFUNC
#define WRAP_NAME( SIGNALFUNC ) _WRAP_NAME( SIGNALFUNC )

#define _WRAP_MAP_NAME( SIGNALFUNC ) wrap_##SIGNALFUNC##_map
#define WRAP_MAP_NAME( SIGNALFUNC ) _WRAP_MAP_NAME( SIGNALFUNC )

#define _MAP_NAME( SIGNALFUNC ) SIGNALFUNC##_map
#define MAP_NAME( SIGNALFUNC ) _MAP_NAME( SIGNALFUNC )

#define _PY_NAME( SIGNALFUNC ) #SIGNALFUNC
#define PY_NAME( SIGNALFUNC ) _PY_NAME( SIGNALFUNC )

#define _PY_MAP_NAME( SIGNALFUNC ) PY_NAME(SIGNALFUNC##_map)
#define PY_MAP_NAME( SIGNALFUNC ) _PY_MAP_NAME( SIGNALFUNC )

#define _PY_DOC_NAME( SIGNALFUNC ) PY_NAME(SIGNALFUNC##_doc)
#define PY_DOC_NAME( SIGNALFUNC ) _PY_DOC_NAME( SIGNALFUNC )

#define METHODS static PyMethodDef ModuleMethods[] = {
#define END_METHODS {NULL, NULL, 0, NULL} /* Sentinel */ };

#define SIGMETHOD( SIGFUNC ) { PY_NAME(SIGFUNC) ,  WRAP_NAME( SIGFUNC ) , METH_VARARGS, PY_DOC_NAME( SIGFUNC ) }, \
	{ PY_MAP_NAME(SIGFUNC) ,  WRAP_MAP_NAME( SIGFUNC ) , METH_VARARGS, PY_DOC_NAME( SIGFUNC ) },


#define INIT_USER_MODULE( NAME ) PyMODINIT_FUNC init##NAME(void){ PyObject *m; m = Py_InitModule3( #NAME, ModuleMethods, doc ); if (m == NULL) return; \
		PyObject  *pName = PyImport_ImportModule( "signal_lab" ); \
		PyObject_Print(pName,stdout,0);\
		_set_module( pName ); \
		}



#endif // _SIGNAL_LAB_WRAP_H_
