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

#include <slab/error.h>
#include <slab/pyslab.h>
//#include <slab/python/file.h>
//#include <slab/python/error.h>


PyObject*
get_isinput( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}

	return PyBool_FromLong((long) self->slfile->is_input );
}

PyObject*
get_fifo( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}

	return PyBool_FromLong( (long) self->slfile->fifo );
}
PyObject*
get_pack( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}

	return PyBool_FromLong( (long) self->slfile->pack );
}
PyObject*
get_finalized( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}

	return PyBool_FromLong( (long) self->slfile->finalized );
}

PyObject*
get_header_name( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}

	return PyString_FromString( self->slfile->header_name) ;
}

PyObject*
get_binary_name( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}

	return PyString_FromString( self->slfile->binary_name) ;
}

PyObject*
get_history( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}

	return PyString_FromString( self->slfile->history) ;
}

PyObject*
get_ndim( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}

	int ndim = slab_file_ndim(self->slfile);
	if (!ndim)
	{
		py_set_error_from_slab();
		return 0;
	}

	return PyInt_FromLong( ndim ) ;
}

PyObject*
get_esize( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}

	int esize = slab_file_esize(self->slfile);
	if (!esize)
	{
		py_set_error_from_slab();
		return 0;
	}


	return PyInt_FromLong( esize ) ;
}

int
set_esize( SLFILE_Object *self, PyObject* Oval, void *closure )
{
	if (!PyInt_Check( Oval ))
	{
		PyErr_SetString( PyExc_ValueError, "expected argument to be of type int" );
		return -1;
	}
	int val = (int) PyInt_AsLong(Oval);
	if (!slab_file_set_esize( self->slfile, val))
	{
		py_set_error_from_slab();
		return -1;
	}
	return 0;
}


PyObject*
get_size( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}

	unsigned long long int size = slab_file_size(self->slfile);
	if (slab_error_occured())
	{
		py_set_error_from_slab();
		return 0;
	}
	
	return PyInt_FromLong( (long int) size ) ;
}

PyObject*
get_type( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_RETURN_NONE;
	}

	char* type = slab_file_dtype( self->slfile );
	if (!type)
	{
		py_set_error_from_slab();
		return 0;
	}

	return PyString_FromString( type ) ;
}

PyObject*
get_form( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_RETURN_NONE;
	}

	char* form= slab_file_form( self->slfile );
	if (!form)
	{
		py_set_error_from_slab();
		return 0;
	}

	return PyString_FromString( form ) ;
}

int
set_type( SLFILE_Object *self, PyObject* Oval, void *closure )
{
	if (!PyString_Check(Oval))
	{
		PyErr_SetString( PyExc_ValueError, "expected argument to be of type str" );
		return -1;
	}

	char* val = PyString_AsString(Oval);
	if (!slab_file_set_dtype( self->slfile, val ))
	{
		py_set_error_from_slab( );
		return -1;
	}

	return 0;
}

PyObject*
get_shape( SLFILE_Object *self, void *closure )
{
	if (!self->slfile)
	{
		Py_RETURN_NONE;
	}

	int ndim = slab_file_ndim( self->slfile );
	unsigned long long int  *shape = slab_file_dims(self->slfile);

	if (!shape)
	{
		py_set_error_from_slab();
		return 0;
	}

	PyObject *tuple = PyTuple_New(ndim);

	int i;
	for (i=0;i<ndim;i++)
	{
		PyTuple_SetItem(tuple,i, PyLong_FromUnsignedLongLong( shape[i] ) );
	}

	return tuple ;
}


int
set_shape( SLFILE_Object *self, PyObject* Oval, void *closure )
{
	if (!PySequence_Check(Oval) )
	{
		PyErr_SetString( PyExc_ValueError, "expected argument to be a sequence" );
		return -1;
	}

	PyObject* item;
	unsigned long long litem;
	long i, n;
	unsigned long long *dims;
	n = PySequence_Size(Oval);
	dims = slab_dims_create( n );
	for ( i=0; i<n; i++ )
	{
		item = PySequence_GetItem( Oval, i);
		if (item == NULL)
			return -1; /* Not a sequence, or other failure */

		litem = PyInt_AsUnsignedLongLongMask( item );

		if (PyErr_Occurred())
			return -1;

		dims[i] = litem;
	}

	if (!slab_file_set_dims(self->slfile, dims))
	{
		py_set_error_from_slab();
		return -1;
	}
	return 0;
}


PyGetSetDef slfile_getseters[] = {
    {"fifo",
     (getter)get_fifo, NULL,
     "file is a fifo",
     NULL},
    {"is_input",
     (getter)get_isinput, NULL,
     "file is input",
     NULL},

     {"pack",
     (getter)get_pack, NULL,
     "header a and binary are packed",
     NULL},

     {"finalized",
     (getter)get_finalized, NULL,
     "header has been written",
     NULL},

     {"header_name",
     (getter)get_header_name, NULL,
     "name of header file",
     NULL},

     {"binary_name",
     (getter)get_binary_name, NULL,
     "name of binary file",
     NULL},

     {"history",
     (getter)get_history, NULL,
     "history from header file",
     NULL},

     {"ndim",
     (getter)get_ndim, NULL,
     "number of dimentions",
     NULL},

     {"esize",
     (getter)get_esize, (setter)set_esize,
     "element size",
     NULL},

     {"size",
     (getter)get_size, NULL,
     "data size",
     NULL},
     {"shape",
     (getter)get_shape, (setter)set_shape,
     "data size",
     NULL},

     {"type",
     (getter)get_type, (setter)set_type,
     "data type",
     NULL},

     {"form",
     (getter)get_form, NULL,
     "data form",
     NULL},

    {NULL}  /* Sentinel */
};
