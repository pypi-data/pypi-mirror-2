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

#include <slab/Dictionary.h>

#include <slab/pyslab.h>
//#include <slab/python/sldict.h>
//#include <slab/python/error.h>


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


void
PySLdict_dealloc( PySLDict_Object* self)
{
	slab_dict_delete( self->dict );
    self->ob_type->tp_free((PyObject*)self);
}

PyObject *
PySLdict_new( PyTypeObject *type, PyObject *args, PyObject *kwds )
{
	PySLDict_Object *self;

    self = (PySLDict_Object *)type->tp_alloc(type, 0);
    self->dict = 0;
    self->dict = slab_dict_allocate( );

    return (PyObject *) self;
}


int
PySLdict_init( PySLDict_Object *self, PyObject *args, PyObject *kwds)
{
	slab_dict_init(self->dict);
	PyObject* Odict=NULL;
    if (! PyArg_ParseTuple( args, "|O", &Odict ) )
    	return -1;

    if (Odict)
    {
	    if( PyObject_TypeCheck( Odict, (PyTypeObject *) &PySLdict_Type) )
	    {
	    	slab_dict_update( self->dict, ((PySLDict_Object*)Odict)->dict );
	    }
	    else if (  PyDict_Check( Odict ))
	    {
	    	if( !PySLdict_update_pydict( self->dict, Odict))
	    		return -1;
	    }
	    else
	    {
	    	PyErr_SetString( PyExc_ValueError,  "expected a dict or slab.sldict object as first argument" );
	    	return -1;
	    }
    }

    if ( kwds)
    {
    	if( !PySLdict_update_pydict( self->dict, kwds))
    		return -1;

    }
    return 0;
}


PyObject*
PySLdict_getitem( PySLDict_Object *self, PyObject* Okey )
{
	char* key;

	if (!PyString_Check( Okey) )
	{
    	PyErr_SetString( PyExc_ValueError,  "expected string as first argument" );
    	return 0;
	}

	key = PyString_AsString( Okey );

	PyObject* item = SLDICT_getitem( self->dict, key );

	if (!item)
	{
		char r[1024]; sprintf( r, "no key '%s=' in dict",
				key );

    	PyErr_SetString( PyExc_KeyError,  r);
    	return 0;

	}

	return item;

}

int
PySLdict_setitem( PySLDict_Object *self, PyObject *Okey, PyObject *Oval )
{

//	if ( !PyString_Check( Okey ) )
//	{
//		Okey = PyObject_Repr(Okey);
//	}
//
//	if (!PyString_Check( Oval ) )
//	{
//		Oval= PyObject_Repr(Oval);
//	}

	char *key, *val;
	key = PyString_AsString( Okey );
	val = PyString_AsString( Oval );

	slab_dict_set( self->dict, key, val);
//	slab_dict_set( self->slfile->changed_header_values, key, val);
	return 0;
}

static PyMappingMethods PySLdict_as_mapping[] =
{
	{
				   0 , //lenfunc mp_length
	(binaryfunc)   PySLdict_getitem , //binaryfunc mp_subscript
	(objobjargproc)PySLdict_setitem, //objobjargproc mp_ass_subscript
		}
};

PyObject*
PySLdict_clear( PySLDict_Object* self )
{
	slab_dict_delete( self->dict );
	self->dict = slab_dict_create( );
	Py_INCREF(Py_None);
	return Py_None;
}

PyObject*
PySLdict_copy( PySLDict_Object* self )
{
	Dict new = slab_dict_copy( self->dict );

	PySLDict_Object* Onew = (PySLDict_Object*)_PyObject_New( (PyTypeObject*)&PySLdict_Type);
	Onew->dict = new;
	return (PyObject*)Onew;
}

PyObject*
PySLdict_get( PySLDict_Object* self, PyObject *args, PyObject *kwds  )
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

	PyObject* item = SLDICT_getitem( self->dict, key );

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
PySLdict_items( PySLDict_Object *self )
{
	PyObject* items = SLDICT_items( self->dict );
	return items;
}

static PyObject*
PySLdict_keys( PySLDict_Object *self )
{
	PyObject* items = SLDICT_keys( self->dict );
	return items;
}

static PyObject*
PySLdict_values( PySLDict_Object *self )
{
	PyObject* items = SLDICT_values( self->dict );
	return items;
}

static PyObject*
SLFILE_haskey( PySLDict_Object *self, PyObject* Okey )
{
	char* key;

	if (!PyString_Check( Okey) )
	{
    	PyErr_SetString( PyExc_ValueError,  "expected string as first argument" );
    	return 0;
	}

	key = PyString_AsString( Okey );
	return SLDICT_haskey( self->dict, key );
}

int
PySLdict_update_pydict( Dict d, PyObject* pd )
{
	long int ppos=0;
	char *key,*value;

	PyObject *pkey;
	PyObject *pvalue;

	while ( PyDict_Next( pd, &ppos, &pkey, &pvalue) )
	{
		key = PyString_AsString( pkey );
		if (!key)
			return 0;
		value = PyString_AsString( pvalue );
		if (!value)
			return 0;

		slab_dict_set( d, key,value);
	}
	return 1;

}

PyObject*
PySLdict_update( PySLDict_Object *self, PyObject *args, PyObject *kwds )
{
	PyObject* Odict=NULL;
    if (! PyArg_ParseTuple( args, "|O", &Odict ) )
    	return NULL;

    if (Odict)
    {
	    if( PyObject_TypeCheck( Odict, (PyTypeObject *) &PySLdict_Type) )
	    {
	    	slab_dict_update( self->dict, ((PySLDict_Object*)Odict)->dict );
	    }
	    else if (  PyDict_Check( Odict ))
	    {
	    	if( !PySLdict_update_pydict( self->dict, Odict))
	    		return 0;
	    }
	    else
	    {
	    	PyErr_SetString( PyExc_ValueError,  "expected a dict or slab.sldict object as first argument" );
	    	return 0;
	    }
    }

    if ( kwds)
    {
    	if( !PySLdict_update_pydict( self->dict, kwds))
    		return 0;

    }

    Py_INCREF(Py_None);

    return Py_None;
}


static
PyMethodDef PySLdict_methods[] = {
    {"clear", (PyCFunction)PySLdict_clear, METH_NOARGS,
     "clear all items"
    },

    {"copy", (PyCFunction)PySLdict_copy, METH_NOARGS,
     "copy sldict"
    },

    {"get", (PyCFunction)PySLdict_get, METH_VARARGS,
     "get an item"
    },

    {"update", (PyCFunction)PySLdict_update, METH_VARARGS,
     "get an item"
    },
    {"items", (PyCFunction)PySLdict_items, METH_NOARGS,
     "get an item"
    },
    {"keys", (PyCFunction)PySLdict_keys, METH_NOARGS,
     "get an item"
    },
    {"values", (PyCFunction)PySLdict_values, METH_NOARGS,
     "get an item"
    },

    {"has_key", (PyCFunction)SLFILE_haskey, METH_O,
     "check if dict has an item"
    },
    {NULL}  /* Sentinel */
};

PyTypeObject PySLdict_Type = {
	    PyObject_HEAD_INIT(NULL)
	    0,                         /*ob_size*/
	    "slab.sldict",             /*tp_name*/
	    sizeof(PySLDict_Object),     /*tp_basicsize*/
	    0,                         /*tp_itemsize*/
	    (destructor)PySLdict_dealloc, /*tp_dealloc*/
//	    0, /*tp_dealloc*/
	    0,                         /*tp_print*/
	    0,                         /*tp_getattr*/
	    0,                         /*tp_setattr*/
	    0,                         /*tp_compare*/
	    0,                         /*tp_repr*/
	    0,                         /*tp_as_number*/

	    0,                         /*tp_as_sequence*/
//	    slfile_as_sequence, 		/*tp_as_sequence*/

//	    0,                         /*tp_as_mapping*/
	    PySLdict_as_mapping,                         /*tp_as_mapping*/

	    0,                         /*tp_hash */
	    0,                         /*tp_call*/
	    0,                         /*tp_str*/
	    0,                         /*tp_getattro*/
	    0,                         /*tp_setattro*/
	    0,                         /*tp_as_buffer*/
	    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
	    "SLAB dictionary",           /* tp_doc */
	    0,		               /* tp_traverse */
	    0,		               /* tp_clear */
	    0,		               /* tp_richcompare */
	    0,		               /* tp_weaklistoffset */
	    0,		               /* tp_iter */
	    0,		               /* tp_iternext */

//	    0,             /* tp_methods */
	    PySLdict_methods,             /* tp_methods */

	    0,                         /* tp_members */
	    0,           /* tp_getset */
	    0,                         /* tp_base */
	    0,                         /* tp_dict */
	    0,                         /* tp_descr_get */
	    0,                         /* tp_descr_set */
	    0,                         /* tp_dictoffset */
	    (initproc) PySLdict_init,      /* tp_init */
//	    0,      /* tp_init */
	    0,                         /* tp_alloc */
	    PySLdict_new,                 /* tp_new */
};

int
PySlabDict_Check( PyObject * Od )
{
	return PyObject_TypeCheck( Od, (PyTypeObject *) &PySLdict_Type);
}

PyObject *
PySlabDict_FromDict( Dict d)
{
	PySLDict_Object* Od = (PySLDict_Object*) PySLdict_new( (PyTypeObject *) &PySLdict_Type, 0, 0 );

	if (!Od)
		return 0;

	if (!d)
		return 0;

	Py_INCREF(Od);

	Od->dict = d;
	return (PyObject*) Od;

}

Dict
PySlabDict_AsDict( PyObject * Od)
{
	if (!PySlabDict_Check(Od))
	{
		PyErr_SetString( PyExc_ValueError,  "expected a dict or slab.sldict object" );
		return 0;
	}

	return ((PySLDict_Object*) Od )->dict;
}
