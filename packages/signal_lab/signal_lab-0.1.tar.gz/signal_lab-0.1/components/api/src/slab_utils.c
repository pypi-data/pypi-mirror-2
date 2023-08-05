

#include <signal_lab/slab_utils.h>


void sl_pycheck( PyObject* obj )
{
	if ( obj == NULL )
	{
		PyErr_Print();
		PyErr_Clear( );
		sl_exit( );
		exit(-1);
	}

}

int _sl_safecall( int no_err )
{
	if (no_err==0)
	{
		PyErr_Print();
		PyErr_Clear( );
		sl_exit( );
		exit(-1);
	}
	return no_err;
}

void* _sl_safecallptr( void* no_err )
{
	if (no_err==0)
	{
		PyErr_Print();
		PyErr_Clear( );
		sl_exit( );
		exit(-1);
	}
	return no_err;
}


PyObject* sl_to_py_tuple( int argc , char** argv )
{
	PyObject * ptuple, *pstring;
	unsigned int i;

	ptuple = PyTuple_New( argc );

	for (i=0; i<argc; i++)
	{
		pstring = PyString_FromString( argv[i] );
		PyTuple_SetItem( ptuple, i, pstring );
	}

	return ptuple;
}


sl_file * _sl_to_files( PyObject* pfiles )
{

	int nb_files = PySequence_Length( pfiles );

	sl_file*  files = (sl_file*) malloc( sizeof(sl_file) *nb_files );

	int i;
	sl_file file;
	PyObject* pfile;
	for (i=0;i<nb_files;i++)
	{
		pfile = PySequence_GetItem( pfiles, i );
		if ( !pfile ) return NULL;

		file = _sl_to_file( pfile );
		if (!file) return NULL;

		files[i]=file;
	}


	return files ;

}
PyObject* _sl_from_files( sl_file* files, int nb_files )
{
	PyObject* pfiles = PyTuple_New(nb_files);

	int i;
	for (i=0;i<nb_files;i++)
	{
		PyTuple_SetItem( pfiles, i, _sl_from_file(files[i] ) );
	}

	return pfiles ;

}
