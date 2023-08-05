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

//#include <slab/python/file.h>
//#include <slab/python/environment.h>
//#include <slab/python/sldict.h>
//#include <slab/python/error.h>
#include <slab/pyslab.h>


extern PyGetSetDef slfile_getseters[];
extern PyMethodDef slfile_methods[];
//extern PyMemberDef slfile_members[];

//PyObject *
//PySLdict_new( PyTypeObject *type, PyObject *args, PyObject *kwds );

extern int
PySLdict_update_pydict( Dict d, PyObject* pd );

//PyObject*
//PySLdict_update( PySLDict_Object *self, PyObject *args, PyObject *kwds );
//
//
//PyObject*
//SLDICT_items( Dict dict );
//
//PyObject*
//SLDICT_pair( Pair pair );
//
//PyObject*
//SLDICT_keys( Dict dict );
//
//PyObject*
//SLDICT_values( Dict dict );
//
PyObject*
SLDICT_getitem( Dict dict, const char* key );
//
//PyObject*
//SLDICT_haskey( Dict dict, char* key );
//
//void
//SLDICT_update( Dict dict, PyObject* obj );

void
slfile_dealloc( SLFILE_Object* self)
{
	if (!self)
		return;
    Py_XDECREF(self->header_stream);
    Py_XDECREF(self->binary_stream);
    Py_XDECREF(self->env);

    if (self->slfile)
    {
    	slab_dict_delete(self->slfile->header_values);
		slab_dict_delete(self->slfile->changed_header_values);
		free(self->slfile->history);
    }
    self->ob_type->tp_free((PyObject*)self);
}

PyObject *
slfile_new( PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	SLFILE_Object *self=NULL;

    self = (SLFILE_Object *)type->tp_alloc(type, 0);

    self->slfile = 0;


    Py_INCREF(Py_None);
    self->header_stream=Py_None;
    Py_INCREF(Py_None);
    self->binary_stream=Py_None;
    Py_INCREF(Py_None);
    self->env=Py_None;


    return (PyObject *) self;
}

int
slfile_input( SLFILE_Object *self, char* name, SLEnviron env )
{
	int success=0;
	self->slfile = slab_file_create(env);
	success = slab_read_header_file( self->slfile, name );

	if ( !success )
	{
		py_set_error_from_slab( );
		return 0;
	}

	success = sl_open_binary_file( self->slfile );

	if (!success)
	{
		py_set_error_from_slab();
		return 0;
	}

	return 1;
}

int
slfile_init( SLFILE_Object *self, PyObject *args, PyObject *kwds)
{
	PyObject *Oinput=NULL;
	PyObject *Oenv=NULL;
	SLEnviron env = NULL;
	char* name;

//	static char *kwlist2[] = { "input",  NULL };

    if (! PyArg_ParseTuple(args, "s|OO", &name, &Oinput, &Oenv ) )
    	return -1;

    if ( kwds && !Oinput)
    	Oinput = PyDict_GetItemString( kwds, "input" );

    if ( kwds && !Oenv)
    	Oenv = PyDict_GetItemString( kwds, "env" );

    if ( kwds )
    {
    	PyDict_DelItemString( kwds, "input");
    	PyDict_DelItemString( kwds, "env");

    }
    PyErr_Clear();


    struct SLFileStruct *input_file=0;
    int is_input=0;

    if ( Oinput==NULL )
    	is_input=1;

    else if (PyObject_TypeCheck( Oinput, (PyTypeObject *) &SLFile_Type) )
    {
    	input_file=( (SLFILE_Object*) Oinput)->slfile;
    	is_input=0;
    }
    else if (  Oinput == Py_None )
    {
    	is_input = 0;
//    	is_input = PyObject_IsTrue( Oinput );
    }

    if ( !Oenv )
    {
    	env = slab_env_create( );
    }
    else if (PyObject_TypeCheck( Oenv, (PyTypeObject *) &slab_EnvironmentType) )
    {
    	env = slab_env_copy(((SEO*) Oenv)->env);
    }
    else if ( PyDict_Check(Oenv) )
    {
    	env = slab_env_create( );
    	PySLdict_update_pydict( env->options, Oenv );
    }
    else
    {
    	PyErr_SetString( PyExc_ValueError, "argument 'env' to be an slab.Environment or dict" );
    	return 0;
    }

    if ( kwds )
    	PySLdict_update_pydict(env->options, kwds);

    if ( is_input )
    {
    	if ( !slfile_input( self, name , env) )
    		return -1;
    }
    else
    {

    	self->slfile = slab_output(  name, input_file, env );
	    if ( self->slfile == 0 )
	    {
	    	py_set_error_from_slab();
	    	return -1;
	    }
    }

    PyObject* tmp=0;

    tmp = self->header_stream;
    self->header_stream = PyFile_FromFile( self->slfile->header_stream,
    									   self->slfile->header_name,
    									   self->slfile->open_mode, 0  );

    Py_XDECREF(tmp);
    tmp = 0;

    tmp = self->binary_stream;
    self->binary_stream = PyFile_FromFile( self->slfile->binary_stream,
    									   self->slfile->binary_name,
    									   self->slfile->open_mode, 0 );
    Py_XDECREF(tmp);
    tmp = 0;

    tmp = self->env;
    self->env = PySlabEnv_FromEnv( self->slfile->env );
    Py_XDECREF(tmp);
    tmp = 0;

	return 0;
}

static PyObject*
SLFILE_getitem( SLFILE_Object *self, PyObject* Okey )
{
	char* key;

	if (!PyString_Check( Okey) )
	{
    	PyErr_SetString( PyExc_ValueError,  "expected string as first argument" );
    	return 0;
	}

	key = PyString_AsString( Okey );

	PyObject* item = SLDICT_getitem( self->slfile->header_values, key );

	if (!item)
	{
		char r[1024]; sprintf( r, "no key '%s=' in header file '%s'",
				key, self->slfile->header_name );

    	PyErr_SetString( PyExc_KeyError,  r);
    	return 0;

	}

	return item;


}

static int
SLFILE_setitem( SLFILE_Object *self, PyObject *Okey, PyObject *Oval )
{
	if ( self->slfile->finalized != 0 )
	{
		char r[1024];
		sprintf( r,"SLAB header '%s' file is not writable ", self->slfile->header_name );
    	PyErr_SetString( PyExc_Exception,  r);
    	return -1;
	}

	if (!PyString_Check( Okey ) )
	{
		Okey = PyObject_Repr(Okey);
	}

	if (!PyString_Check( Oval ) )
	{
		Oval= PyObject_Repr(Oval);
	}

	char *key, *val;
	key = PyString_AsString( Okey );
	val = PyString_AsString( Oval );

	slab_dict_set( self->slfile->header_values, key, val);
	slab_dict_set( self->slfile->changed_header_values, key, val);

	return 0;
}

static PyMappingMethods slfile_as_mapping[] =
{
	{
				   0 , //lenfunc mp_length
	(binaryfunc)   SLFILE_getitem , //binaryfunc mp_subscript
	(objobjargproc)SLFILE_setitem , //objobjargproc mp_ass_subscript
		}
};

static PyMemberDef slfile_members[] = {
    {"header", T_OBJECT_EX, offsetof(SLFILE_Object, header_stream), 0,
     "header file"},
    {"binary", T_OBJECT_EX, offsetof(SLFILE_Object, binary_stream), 0,
     "binary file"},
    {"env", T_OBJECT_EX, offsetof(SLFILE_Object, env), 0,
     "environment" },
    {NULL}  /* Sentinel */
};

static char slfiledoc[] ="SLAB file object\n"
		"sl_file( name, input=True, env=sys.argv , **kw )\n"
		"\n"
		"name: is a path to a slab file\n"
		"input: may be True False or an sl_file instance\n"
		"  if input if an sl_file, then the header values \n"
		" and history are copied to the output\n"
		"env: may be a slab Environment or a dictionary\n"
		"kw: all other key word arguments are updated to the \n"
		"Environment options";


PyTypeObject SLFile_Type = {
	    PyObject_HEAD_INIT(NULL)
	    0,                         /*ob_size*/
	    "slab.sl_file",             /*tp_name*/
	    sizeof(SLFILE_Object),     /*tp_basicsize*/
	    0,                         /*tp_itemsize*/
	    (destructor)slfile_dealloc, /*tp_dealloc*/
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
	    slfile_as_mapping,                         /*tp_as_mapping*/

	    0,                         /*tp_hash */
	    0,                         /*tp_call*/
	    0,                         /*tp_str*/
	    0,                         /*tp_getattro*/
	    0,                         /*tp_setattro*/
	    0,                         /*tp_as_buffer*/
	    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
	    slfiledoc,           /* tp_doc */
	    0,		               /* tp_traverse */
	    0,		               /* tp_clear */
	    0,		               /* tp_richcompare */
	    0,		               /* tp_weaklistoffset */
	    0,		               /* tp_iter */
	    0,		               /* tp_iternext */

//	    0,             /* tp_methods */
	    slfile_methods,             /* tp_methods */

//	    0,                         /* tp_members */
	    slfile_members,                         /* tp_members */
	    slfile_getseters,           /* tp_getset */
	    0,                         /* tp_base */
	    0,                         /* tp_dict */
	    0,                         /* tp_descr_get */
	    0,                         /* tp_descr_set */
	    0,                         /* tp_dictoffset */
	    (initproc) slfile_init,      /* tp_init */
//	    0,      /* tp_init */
	    0,                         /* tp_alloc */
	    slfile_new,                 /* tp_new */
};
