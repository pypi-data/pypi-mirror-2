

#include <Python.h>

#include <signal_lab/slab_utils.h>
#include <signal_lab.h>

#include <string.h>


PyObject* _sl_from_env( sl_environ env);
PyObject* _get_module( );

//static PyObject* signal_lab_module;

struct _sl_file
{
	PyObject* pfile;
	int finalized;
	FILE* bin;
};


PyObject* _sl_from_file( sl_file file )
{
	return file->pfile;
}
sl_file _sl_to_file( PyObject* pfile )
{

	sl_file file = (sl_file) malloc( sizeof( struct _sl_file ) );

	file->pfile = pfile;

	return file;

}



PyObject* _get_file_object( )
{
	PyObject *signal_lab_module = _get_module( );
	PyObject *pFile = PyObject_GetAttrString(_get_module(), "File" );

	sl_pycheck(pFile );
	Py_DECREF( signal_lab_module );

	return pFile;
}


sl_file sl_input( char* tag, sl_environ env )
{
	PyObject *pstring, *pFile, *pArgs, *pKW, *pinput;

	pstring = PyString_FromString( tag );

	pFile = _get_file_object( );

	sl_pycheck(pFile );

	pArgs = PyTuple_New(1);
	pKW = PyDict_New( );

	PyTuple_SetItem(pArgs, 0, pstring);

	PyDict_SetItemString( pKW , "env", _sl_from_env(env) );

	pinput = PyObject_Call( pFile, pArgs, pKW );

	Py_DECREF(pArgs);
	Py_DECREF(pKW);
	Py_DECREF(pFile);

	sl_pycheck(pinput );

	sl_file file = (sl_file) malloc( sizeof( struct _sl_file ) );
	file->pfile = pinput;
	file->bin = 0;
	file->finalized=1;
	return file;

}

sl_file sl_output( char* tag, sl_file input, sl_environ env )
{
	PyObject *pstring, *pFile, *pArgs, *pKW, *poutput;

	pstring = PyString_FromString( tag );

	PyObject* mod = _get_module();


	pFile = PyObject_GetAttrString(mod, "File" );

	if (!pFile)
		return 0;

	pArgs = PyTuple_New(1);
	pKW = PyDict_New( );

	PyTuple_SetItem(pArgs, 0, pstring);

	PyDict_SetItemString( pKW , "env", _sl_from_env(env) );
	if ( !input )
	{
		PyDict_SetItemString( pKW , "input", Py_False );
	}
	else
	{
		PyDict_SetItemString( pKW , "input", input->pfile );
	}

	poutput = PyObject_Call( pFile, pArgs, pKW );
	Py_DECREF(pArgs);
	Py_DECREF(pKW);

	if (!poutput) return 0;

	sl_file file = (sl_file) malloc( sizeof( struct _sl_file ) );
	file->pfile = poutput;
	file->bin = 0;
	file->finalized= 0;
	return file;

}


sl_file* create_outputs( int nb_outputs )
{
	sl_file*  outputs = (sl_file*) malloc( sizeof(sl_file) *nb_outputs );
	return outputs;
}


int sl_histint( sl_file file, char* item, int* value )
{
	PyObject *pfile, *pres;

	pfile = file->pfile;

	pres = PyObject_CallMethod( pfile, "_sl_getint", "s", item );

	if (pres==NULL)
	{
		PyErr_Clear();
		return 0;
	}

	*value = (int) PyInt_AsLong( pres );

	Py_DECREF(pres);

	if (PyErr_Occurred())
	{
		PyErr_Clear();
		return 0;
	}

	return 1;
}

int sl_setint( sl_file file, char* item, const int value )
{
	int err = PyObject_SetItem( file->pfile, PyString_FromString(item), PyInt_FromLong(value) );

	if (err==-1)
		return 0;

	return 1;

}


int sl_settype( sl_file file, const char* value )
{
	int err = PyObject_SetAttrString( file->pfile, "type", PyString_FromString(value) );

	if (err==-1)
		return 0;

	return 1;

}





size_t sl_esize( sl_file file )
{
	PyObject* pesize =  PyObject_GetAttrString( file->pfile, "esize" );

	size_t value = (size_t) PyInt_AsLong( pesize  );

	Py_DECREF(pesize);

	return value;
}

void sl_finalize( sl_file file )
{
	file->finalized = 1;
	PyObject* pres = PyObject_CallMethod( file->pfile, "finalize", 0 );

	sl_pycheck( pres );

	Py_DECREF(pres);


	return;
}

FILE* sl_get_binary_FILE( sl_file file )
{
	if (!file->bin)
	{
		PyObject* pfile =  PyObject_GetAttrString( file->pfile, "binary_file" );
		sl_pycheck( pfile );
		file->bin = PyFile_AsFile(pfile);

		if (PyErr_Occurred())
		{
			PyErr_Print();
			exit(-1);
		}
	}


	return file->bin;
}




unsigned long int sl_leftsize( sl_file file , int left )
{

	PyObject *pfile, *pres;

	pfile = file->pfile;

	pres = PyObject_CallMethod( pfile, "leftsize", "i", left );

	sl_pycheck( pres );

	unsigned long int value = (unsigned long int) PyInt_AsLong( pres  );

	Py_DECREF( pres );

	if (PyErr_Occurred())
	{
		PyErr_Print();
		exit(-1);
	}

	return value;
}

char* sl_filetype( sl_file file )
{
	PyObject* ptype =  PyObject_GetAttrString( file->pfile, "type" );

	sl_pycheck( ptype );


	char* value = PyString_AsString( ptype );

	if (PyErr_Occurred())
		{
			PyErr_Print();
			exit(-1);
		}

	return value;

}

void sl_error( char * msg )
{
	fprintf( stderr, "SLAB Error: ");
	fprintf( stderr, msg );
	fprintf( stderr, "\n");
	exit(-1);
}

char* _sl_error_msg = 0;
void sl_set_error( char * msg )
{
	int len = strlen( msg );
	_sl_error_msg = malloc( (len+1)* sizeof(char) );
	strcpy( _sl_error_msg, msg);
}

char* sl_get_error( void )
{
	return _sl_error_msg;
}

void sl_clear_error( void )
{
	if (!_sl_error_msg)
		return;
	else
	{
		free(_sl_error_msg);
		_sl_error_msg=0;
	}
}



int _sl_is_finalized( sl_file file )
{

	PyObject* pfinalized =  PyObject_GetAttrString( file->pfile, "finalized" );
	int finalized;

	sl_pycheck( pfinalized );


	finalized = PyObject_IsTrue( pfinalized );

	if (PyErr_Occurred())
		{
			PyErr_Print();
			exit(-1);
		}

	return finalized;

}



int sl_is_finalized( sl_file file )
{
	return file->finalized;
}

void sl_close( sl_file file )
{

	PyObject* pres = PyObject_CallMethod( file->pfile, "close", 0 );
	sl_pycheck( pres );
	Py_DECREF(pres);



}
