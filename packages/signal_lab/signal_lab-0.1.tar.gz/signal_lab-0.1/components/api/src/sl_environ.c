
#include <Python.h>

#include <signal_lab/slab_utils.h>
#include <signal_lab.h>


struct _sl_environ
{
	PyObject* penv;
};


PyObject* _sl_from_env( sl_environ env)
{
	return env->penv;
}

sl_environ _sl_to_env( PyObject* penv )
{
	sl_environ env = (sl_environ) malloc( sizeof( struct _sl_environ ) );
	env->penv = penv;
	return env;
}


PyObject* _get_module( )
{
	PyObject  *signal_lab_module = PyImport_ImportModule( "signal_lab" );
	sl_pycheck( signal_lab_module );
	return signal_lab_module;
}

PyObject* _get_env_object( )
{
	PyObject *signal_lab_module = _get_module( );
	PyObject *pEnvironment = PyObject_GetAttrString(_get_module(), "Environment" );

	sl_pycheck(pEnvironment );
	Py_DECREF( signal_lab_module );

	return pEnvironment;
}



sl_environ sl_init( int argc , char** argv )
{


	Py_Initialize( );
	PySys_SetArgv( argc, argv );

	sl_environ env = sl_environ_init( argc, argv );
	return env;

}

sl_environ sl_environ_init( int argc , char** argv )
{
	PyObject* pEnvironment, *penv, *pArgs,*pargv;

	if (!_get_module())
		return 0;

	pEnvironment = _get_env_object( );

	sl_pycheck(pEnvironment );

	pArgs = PyTuple_New(1);
	pargv = sl_to_py_tuple( argc, argv);

	PyTuple_SetItem(pArgs, 0, pargv);


	penv = PyObject_CallObject( pEnvironment, pArgs );

	Py_DECREF(pArgs);
	Py_DECREF(pargv);
	Py_DECREF(pEnvironment);

	sl_pycheck( penv );

	sl_environ env = (sl_environ) malloc( sizeof( struct _sl_environ ) );

	env->penv = penv;

	return env;
}


int sl_getfloat( sl_environ env, char* item , float* value,float* _default )
{
	PyObject *penv, *pres;

	penv = env->penv;

	pres = PyObject_CallMethod( penv, "_sl_getfloat", "s", item );

	if (pres==NULL)
	{
		if (_default)
		{
			PyErr_Clear();
			*value=*_default;
			return 1;
		}
		return 0;
	}

	*value = (float) PyFloat_AsDouble( pres );

	Py_DECREF(pres);

	if (PyErr_Occurred())
	{
		if (_default)
		{
			PyErr_Clear();
			*value=*_default;
			return 1;
		}
		return 0;
	}

	return 1;

}

int sl_getint( sl_environ env, char* item , int* value, int* _default )
{
	PyObject *penv, *pres;

	penv = env->penv;

	pres = PyObject_CallMethod( penv, "_sl_getint", "s", item );

	if (pres==NULL)
	{
		if (_default)
		{
			PyErr_Clear();
			*value=*_default;
			return 1;
		}
		return 0;
	}

	*value = (int) PyInt_AsLong( pres );


	if (PyErr_Occurred())
	{
		if (_default)
		{
			PyErr_Clear();
			*value=*_default;
			return 1;
		}
		return 0;
	}
	Py_DECREF(pres);

	return 1;

}

int sl_getbool( sl_environ env, char* item , unsigned short int* value, unsigned short int* _default )
{
	PyObject *penv, *pres;

	penv = env->penv;

	pres = PyObject_CallMethod( penv, "_sl_getbool", "s", item );


	if (pres==NULL)
	{
		if (_default)
		{
			PyErr_Clear();
			*value=*_default;
			return 1;
		}
		return 0;
	}

	*value = (unsigned short int) PyInt_AsLong( pres );


	if (PyErr_Occurred())
	{
		if (_default)
		{
			PyErr_Clear();
			*value=*_default;
			return 1;
		}
		return 0;
	}
	Py_DECREF(pres);

	if (pres == Py_True)
		*value = 1;
	else
		*value = 0;

	return 1;

}

char* sl_getstring( sl_environ env, char* item , char* _default )
{

	char* value;
	PyObject *pres;


	pres = PyObject_CallMethod( env->penv, "_sl_getstring", "s", item );


	if (pres==NULL)
	{
		if (_default)
		{
			PyErr_Clear();
			return _default;
		}
		return 0;
	}

	value = PyString_AsString( pres );

	if (!value)
	{
		if (_default)
		{
			PyErr_Clear();
			return _default;
		}
		return 0;
	}

	Py_DECREF(pres);

	return value;


}

void sl_exit( )
{
	Py_Finalize();
}

