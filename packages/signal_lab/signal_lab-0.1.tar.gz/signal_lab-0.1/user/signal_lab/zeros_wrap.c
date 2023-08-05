

#include<signal_lab.h>
#include<signal_lab/wrap.h>
#include<signal_lab/wrap.h>

#include<zeros.h>


#define SIGFUNC zeros_like
	#include <signal_lab/wrap_inline.h>
#undef SIGFUNC // sl_zeros


PyObject* write_zeros_wrap( PyObject* self, PyObject* args )
{
	PyObject* pfile;
	FILE*file;
	unsigned long size;
	int esize;
	if (!PyArg_ParseTuple( args, "O!ki" , PyFile_Type, &pfile, &size, &esize ) )
        return NULL;

	file = PyFile_AsFile( pfile );


	if (!write_zeros( file, size, esize))
	{
		if ( sl_get_error() )
		{
			PyErr_SetString( PyExc_Exception, sl_get_error() );
			sl_clear_error();
		}
		return NULL;
	}
	Py_RETURN_NONE;

}

METHODS

	SIGMETHOD(zeros_like)
	{ "write_zeros", write_zeros_wrap, METH_VARARGS,
	"write_zeros( file, size, esize ) -> None" },

END_METHODS


char doc[] = "";


INIT_USER_MODULE( zeros );


