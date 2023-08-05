/*
  Copyright (C) 2008 Gilles Hennenfent and Sean Ross-Ross

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

#include <slab/header_utils.h>
#include <slab/SLIO.h>


#include <slab/pyslab.h>

//#include <slab/python/file.h>
//#include <slab/python/error.h>
//#include <slab/python/environment.h>
//#include <slab/python/sldict.h>

extern PyObject * PySLdict_new( PyTypeObject *type, PyObject *args, PyObject *kwds );
extern int PySLdict_update_pydict( Dict d, PyObject* pd );
extern PyObject* PySLdict_update( PySLDict_Object *self, PyObject *args, PyObject *kwds );
extern PyObject* SLDICT_items( Dict dict );
extern PyObject* SLDICT_pair( Pair pair );
extern PyObject* SLDICT_keys( Dict dict );
extern PyObject* SLDICT_values( Dict dict );
extern PyObject* SLDICT_getitem( Dict dict, const char* key );
extern PyObject* SLDICT_haskey( Dict dict, char* key );
extern void SLDICT_update( Dict dict, PyObject* obj );


static PyObject*
SLFILE_finalize( SLFILE_Object *self )
{
	SLFile file = self->slfile;

//	char * name = file->header_name;
//	printf("%s\n", name);
//	int f = ff( file );
//	if ( file ==0 )
//	{
//		PyErr_SetString( PyExc_Exception, "file is NULL" );
//		return NULL;
//	}
	slab_finalize_output( file );

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject*
SLFILE_items( SLFILE_Object *self )
{
	SLFile file = self->slfile;

	PyObject* items = SLDICT_items( file->header_values );

	return items;
}

static PyObject*
SLFILE_close( SLFILE_Object *self )
{
	slab_file_close( self->slfile);

	Py_INCREF(Py_None);
	return Py_None;

}

static PyObject*
SLFILE_keys( SLFILE_Object *self )
{
	SLFile file = self->slfile;

	PyObject* items = SLDICT_keys( file->header_values );

	return items;
}

static PyObject*
SLFILE_values( SLFILE_Object *self )
{
	SLFile file = self->slfile;

	PyObject* items = SLDICT_values( file->header_values );

	return items;

}



static PyObject*
SLFILE_set( SLFILE_Object *self, PyObject *args, PyObject *kwds )
{
	if ( self->slfile->finalized != 0 )
	{
		char r[1024];
		sprintf( r,"SLAB header '%s' file is not writable ", self->slfile->header_name );
    	PyErr_SetString( PyExc_Exception,  r);
    	return 0;
	}

	static char *kwlist2[] = { "key", "value",  NULL };

	PyObject *Okey=NULL, *Oval=NULL;

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "OO", kwlist2,
                                      &Okey, &Oval ) )
    	return 0;


	if (!PyString_Check( Okey ) )
	{
    	PyErr_SetString( PyExc_ValueError,  "expected string as first argument" );
    	return 0;
	}

	if (!PyString_Check( Oval ) )
	{
		Oval = PyObject_Repr( Oval );
	}

	char *key, *val;
	key = PyString_AsString( Okey );
	val = PyString_AsString( Oval );

	slab_dict_set( self->slfile->header_values, key, val);
	slab_dict_set( self->slfile->changed_header_values, key, val);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject*
SLFILE_get( SLFILE_Object *self, PyObject *args, PyObject *kwds )
{
	char* key;

	static char *kwlist2[] = { "key", "default",  NULL };
//
	PyObject *Okey=NULL, *Odef=NULL;

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "O|O", kwlist2,
                                      &Okey, &Odef ) )
    	return 0;


	if (!PyString_Check( Okey ) )
	{
    	PyErr_SetString( PyExc_ValueError,  "expected string as first argument" );
    	return 0;
	}

	key = PyString_AsString( Okey );

	PyObject* item = SLDICT_getitem( self->slfile->header_values, key );

	if ( (item==0) )
	{
		if ( Odef == 0 )
		{
			Py_INCREF(Py_None);
			item = Py_None;
		}
		else
			item = Odef;
	}

	return item;


}

static PyObject*
SLFILE_haskey( SLFILE_Object *self, PyObject* Okey )
{
	char* key;

	if (!PyString_Check( Okey) )
	{
    	PyErr_SetString( PyExc_ValueError,  "expected string as first argument" );
    	return 0;
	}

	key = PyString_AsString( Okey );
	return SLDICT_haskey( self->slfile->header_values, key );
}

static PyObject*
PySLFile_Read( SLFILE_Object *self, PyObject *args, PyObject *kwds )
{
	PyObject* Obuff=NULL;
	unsigned long int nrd=0, count=0;

	static char *kwlist2[] = { "size",  NULL };

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "|k", kwlist2,
                                       &count ) )
    	return NULL;

    if (!count)
    {
    	count = slab_file_size( self->slfile ) * slab_file_esize( self->slfile );
    }

	if (!count)
	{
		py_set_error_from_slab();
    	return NULL;
	}

	void *buffer = malloc( count );

    nrd = slab_read( self->slfile, buffer, count );

    if (!nrd)
    {
    	PyErr_SetString( PyExc_IOError,  "could not read from file" );
    	return NULL;
    }

    if (nrd!=count)
    {
    	free(buffer+nrd);
    }



    Obuff = PyBuffer_FromReadWriteMemory( buffer, nrd );

//    if (nrd!=count)
//    {
//
//    }

    return Obuff;
}


static PyObject*
PySLFile_ReadInto( SLFILE_Object *self, PyObject *Obuff )
{
//	PyObject *Obuff=NULL;

	long int nrd, count=0;

    if (!PyBuffer_Check(Obuff) )
    {
    	PyErr_SetString( PyExc_ValueError,  "expected buffer object" );
    	return NULL;
    }

	count = PySequence_Length(Obuff);

	if (!count)
	{
    	PyErr_SetString( PyExc_ValueError,  "invalid buffer: could not determine size" );
    	return NULL;
	}

	void *buffer;
//    PyObject* buff = PyBuffer_FromReadWriteObject( Obuff, 0, count );
    if (-1==PyObject_AsWriteBuffer( Obuff, &buffer, &count ))
    	return NULL;

    nrd = slab_read( self->slfile, buffer, count );

    if (nrd!=count)
    {
    	void *last_buff = buffer+nrd;
    	memset(last_buff,0,(count-nrd));
    }
    return PyInt_FromLong((long int) nrd);

}
static PyObject*
PySLFile_Write( SLFILE_Object *self, PyObject *Obuff )
{
//	PyObject *Obuff=NULL;

	long int nrd, count=0;

    if (!PyBuffer_Check(Obuff) )
    {
    	PyErr_SetString( PyExc_ValueError,  "expected buffer object" );
    	return NULL;
    }

	count = PySequence_Length(Obuff);

	if (!count)
	{
    	PyErr_SetString( PyExc_ValueError,  "invalid buffer: could not determine size" );
    	return NULL;
	}

	void *buffer;
//    PyObject* buff = PyBuffer_FromReadWriteObject( Obuff, 0, count );
    if (-1==PyObject_AsWriteBuffer( Obuff, &buffer, &count ))
    {
    	PyErr_SetString( PyExc_ValueError,  "invalid buffer: can't create read write buffer from argument" );
    	return NULL;
    }

    nrd = slab_write( self->slfile, buffer, count );
    if(!nrd)
    {
		py_set_error_from_slab();
    	return 0;
    }
    if (nrd!=count)
    {
    	void *last_buff = buffer+nrd;
    	memset(last_buff,0,(count-nrd));
    }
    return PyInt_FromLong((long int) nrd);

}

PyMethodDef slfile_methods[] = {
//    { "finalize", (PyCFunction)SLFILE_finalize, METH_NOARGS,
//      "write header to file"
//    },
//

    {"finalize", (PyCFunction)SLFILE_finalize, METH_NOARGS,
     "Return the name, combining the first and last name\n"
     "file.finalize() -> None"
    },

    {"set", (PyCFunction)SLFILE_set, METH_VARARGS,
     "set a value in the header dictionary\n"
     "file must not be output or finalized.\n"
     "file.set( key, value )"
    },
	{"get",         (PyCFunction)SLFILE_get,          METH_VARARGS,
	 "get an item from the header\n"
	 "file.get( key [,default] )"},

    {"items", (PyCFunction)SLFILE_items, METH_NOARGS,
     "Return (key,value) pairs from header file\n"
     "file.items( ) -> list of file's (key, value) pairs, as 2-tuples"
    },
    {"keys", (PyCFunction)SLFILE_keys, METH_NOARGS,
     "Return keys from header file\n"
     "file.keys() -> list"
    },
    {"values", (PyCFunction)SLFILE_values, METH_NOARGS,
     "Return values from header file\n"
     "file.values( ) -> list"
    },
    {"close", (PyCFunction)SLFILE_close, METH_NOARGS,
     "close both header and binary files\n"
     "file.close( ) -> None"
    },

    {"has_key", (PyCFunction)SLFILE_haskey, METH_O,
     "Check if header file has key\n"
     "file.has_key( key ) -> bool"
    },

	{"read",         (PyCFunction)PySLFile_Read,          METH_VARARGS,
	 "file.read( [size]) -> buffer\n"
	 "read at most size bytes\n"
	 "If the size argument is omitted, read until EOF is reached"
	 ""
	 ""},
	{"readinto",         (PyCFunction)PySLFile_ReadInto,          METH_O,
	 "file.readinto( buffer ) -> int\n"
	 " read binary data into a writeable python buffer object\n"
	 "returns the number of bytes read"},

	{"write",         (PyCFunction)PySLFile_Write,          METH_O,
	 "file.write( buffer ) -> int\n"
	 "write binary data\n"
	 "returns the number of bytes written"},

    {NULL}  /* Sentinel */
};
