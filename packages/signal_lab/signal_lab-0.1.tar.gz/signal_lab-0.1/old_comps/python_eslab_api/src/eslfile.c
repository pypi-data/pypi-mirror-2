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

#include <slab/error.h>
#include <slab/pyslab.h>

//#include <slab/python/error.h>
//#include <slab/python/file.h>

#include <slab/xml/slabio.h>
#include <slab/xml/sub_header.h>
#include <slab/xml/meta_header.h>

#include <slab/python/xml/xmlfile.h>

void
PyESLFile_dealloc( PyESLFile_Object* self)
{
	scew_tree_free( self->tree );
	Py_XDECREF( self->slfile );

    self->ob_type->tp_free((PyObject*)self);
}

PyObject *
PyESLFile_new( PyTypeObject *type, PyObject *args, PyObject *kwds )
{
	PyESLFile_Object *self;

    self = (PyESLFile_Object *)type->tp_alloc(type, 0);

    self->tree = 0;
    self->file = 0;

    Py_INCREF(Py_None);
    self->slfile = Py_None;

    return (PyObject *) self;
}


int
PyESLFile_init( PyESLFile_Object *self, PyObject *args, PyObject *kwds )
{

	PyObject *Ofile=NULL,
			 *Oinfile=NULL;
    PyObject* tmpp;
    if (! PyArg_ParseTuple( args, "O!|O!", (PyTypeObject*) &SLFile_Type,    &Ofile,
    									   (PyTypeObject*) &PyESLFile_Type, &Oinfile ) )
    	return -1;

    Py_INCREF( Ofile );
    tmpp = self->slfile;
    Py_XDECREF( tmpp );
    self->slfile = Ofile;

    self->file = ((SLFILE_Object*) Ofile)->slfile;


    if (self->file->is_input)
    {
    	if (Oinfile)
    	{
    		PyErr_SetString( PyExc_Exception,  "slab.eslfile does not accept a second argument when the first is an input" );
    		return -1;
    	}

    	self->tree = eslab_file_read_xml( self->file );
    	if (!self->tree)
    	{
    		py_set_error_from_slab( );
    		return -1;
    	}
    	return 0;
    }
    else
    {
    	if (Oinfile)
    	{
    		self->tree = scew_tree_copy(((PyESLFile_Object*) Oinfile)->tree);
    	}
    	else
    		self->tree =eslab_new( );

    	return 0;
    }
}

PyObject*
PyESLFile_get_value( PyESLFile_Object *self, PyObject *args, PyObject *kwds )
{
	char* key=NULL, *def=NULL;
	int rank;

    if (! PyArg_ParseTuple( args, "is|s", &rank, &key, &def ) )
    	return 0;

    char* res  = eslab_sub_header_value( self->tree , rank , key );

    if (!res)
    {
    	if (!def)
    	{
    		py_set_error_from_slab( );
    		return 0;
    	}
    	else
    	{
    		slab_error_clear();
    		res = def;
    	}
    }

    PyObject* Ores = PyString_FromString( res );

    return Ores;
}

PyObject*
PyESLFile_set_value( PyESLFile_Object *self, PyObject *args, PyObject *kwds )
{
	char* key=NULL, *val=NULL;
	int rank;

    if (! PyArg_ParseTuple( args, "iss", &rank, &key, &val ) )
    	return 0;

    if (!eslab_sub_header_set_value( self->tree , rank , key, val ))
    {
		py_set_error_from_slab( );
		return 0;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject*
PyESLFile_get( PyESLFile_Object *self, PyObject *args, PyObject *kwds )
{
	char* key=NULL, *def=NULL;
	int rank;

    if (! PyArg_ParseTuple( args, "is|s", &rank, &key, &def ) )
    	return 0;

    char* res  = eslab_sub_header_get( self->tree , rank , key );

    if (!res)
    {
    	if (!def)
    	{
    		py_set_error_from_slab( );
    		return 0;
    	}
    	else
    	{
    		slab_error_clear();
    		res = def;
    	}
    }

    PyObject* Ores = PyString_FromString( res );

    return Ores;
}

PyObject*
PyESLFile_set( PyESLFile_Object *self, PyObject *args, PyObject *kwds )
{
	char* key=NULL, *val=NULL;
	int rank;

    if (! PyArg_ParseTuple( args, "iss", &rank, &key, &val ) )
    	return 0;

    if (!eslab_sub_header_set( self->tree , rank , key, val ))
    {
		py_set_error_from_slab( );
		return 0;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject*
PyESLFile_finalize( PyESLFile_Object *self )
{

	if ( ! eslab_file_write_xml( self->file, self->tree ) )
	{
		py_set_error_from_slab( );
		return 0;
	}

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject*
PyESLFile_append_subheader( PyESLFile_Object *self, PyObject *args, PyObject *kwds )
{
	int rank;

    if (! PyArg_ParseTuple( args, "i", &rank ) )
    	return 0;

    eslab_append_sub_header( self->tree, rank );

    Py_INCREF(Py_None);
    return Py_None;
}



PyMethodDef PyESLFile_methods[] = {
    {"get_value", (PyCFunction)PyESLFile_get_value, METH_VARARGS,
     "efile.get_value( rank, key [,default] ) -> value \n"
     "get meta-key from xml subheader\n"
     "rank is an int, key and default must be strings"
    },
    {"set_value", (PyCFunction)PyESLFile_set_value, METH_VARARGS,
	 "efile.set_value( rank, key, value )\n"
     "set meta-key from xml subheader\n"
     "rank is an int, key and value must be strings"
    },

    {"get", (PyCFunction)PyESLFile_get, METH_VARARGS,
     "efile.get( rank, key [,default] ) -> value \n"
     "get key from xml subheader"
    },
    {"set", (PyCFunction)PyESLFile_set, METH_VARARGS,
   	 "efile.set( rank, key, value )\n"
     "set key from xml subheader"
    },

    {"finalize", (PyCFunction)PyESLFile_finalize, METH_NOARGS,
     "efile.finalize()\n"
     "write header file and xml data"
    },

    {"append", (PyCFunction)PyESLFile_append_subheader, METH_VARARGS,
     "efile.append( rank )\n"
     "append a new sub-header with global rank "
    },
//
//    {"get", (PyCFunction)PyESLFile_get, METH_VARARGS,
//     "get an item"
//    },
//
//    {"update", (PyCFunction)PyESLFile_update, METH_VARARGS,
//     "get an item"
//    },
//    {"items", (PyCFunction)PyESLFile_items, METH_NOARGS,
//     "get an item"
//    },
//    {"keys", (PyCFunction)PyESLFile_keys, METH_NOARGS,
//     "get an item"
//    },
//    {"values", (PyCFunction)PyESLFile_values, METH_NOARGS,
//     "get an item"
//    },
//
//    {"has_key", (PyCFunction)SLFILE_haskey, METH_O,
//     "check if dict has an item"
//    },
		{NULL}  /* Sentinel */

};



PyMemberDef eslfile_members[] = {
    {"slfile", T_OBJECT_EX, offsetof(PyESLFile_Object, slfile), 0,
     "slab.sl_file"},
    {NULL}  /* Sentinel */
};

PyGetSetDef eslfile_getseters[] = {
//	    {"fifo",
//	     (getter)get_fifo,
//		 (setter) NULL,
//	     "file is a fifo",
//	     NULL},

		{NULL}
};

char eslfiledoc[] = "SLAB parallel file format \n"
		"eslfile( intput ) -> new distributed input file\n"
		"enlfile( output [,input] ) -> new distributed output file\n";

PyTypeObject PyESLFile_Type = {
	    PyObject_HEAD_INIT(NULL)
	    0,                         /*ob_size*/
	    "slab.eslfile",             /*tp_name*/
	    sizeof(PyESLFile_Object),     /*tp_basicsize*/
	    0,                         /*tp_itemsize*/
	    (destructor)PyESLFile_dealloc, /*tp_dealloc*/
//	    0, /*tp_dealloc*/
	    0,                         /*tp_print*/
	    0,                         /*tp_getattr*/
	    0,                         /*tp_setattr*/
	    0,                         /*tp_compare*/
	    0,                         /*tp_repr*/
	    0,                         /*tp_as_number*/

	    0,                         /*tp_as_sequence*/
//	    slfile_as_sequence, 		/*tp_as_sequence*/

	    0,                         /*tp_as_mapping*/
//	    PyESLFile_as_mapping,                         /*tp_as_mapping*/

	    0,                         /*tp_hash */
	    0,                         /*tp_call*/
	    0,                         /*tp_str*/
	    0,                         /*tp_getattro*/
	    0,                         /*tp_setattro*/
	    0,                         /*tp_as_buffer*/
	    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
	    eslfiledoc,           /* tp_doc */
	    0,		               /* tp_traverse */
	    0,		               /* tp_clear */
	    0,		               /* tp_richcompare */
	    0,		               /* tp_weaklistoffset */
	    0,		               /* tp_iter */
	    0,		               /* tp_iternext */

//	    0,             /* tp_methods */
	    PyESLFile_methods,             /* tp_methods */

	    eslfile_members,       /* tp_members */
	    eslfile_getseters,           /* tp_getset */
	    0,                         /* tp_base */
	    0,                         /* tp_dict */
	    0,                         /* tp_descr_get */
	    0,                         /* tp_descr_set */
	    0,                         /* tp_dictoffset */
	    (initproc) PyESLFile_init,      /* tp_init */
//	    0,      /* tp_init */
	    0,                         /* tp_alloc */
	    PyESLFile_new,                 /* tp_new */
};

int
PyESLFile_Check( PyObject * Od )
{
	return PyObject_TypeCheck( Od, (PyTypeObject *) &PyESLFile_Type);
}

scew_tree *
PyESLFile_AsTree( PyObject * Od)
{
	if (!PyESLFile_Check(Od))
	{
		PyErr_SetString( PyExc_ValueError,  "expected a dict or slab.elsfile object" );
		return 0;
	}

	return ((PyESLFile_Object*) Od )->tree;
}
