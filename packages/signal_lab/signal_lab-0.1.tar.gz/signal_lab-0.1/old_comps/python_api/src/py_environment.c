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

#include <slab/pyslab.h>

//#include <slab/python/error.h>
//#include <slab/python/environment.h>
//#include <slab/python/sldict.h>


void
Environment_dealloc(SEO* self)
{
    Py_XDECREF(self->kw);
//    Py_XDECREF(self->list);
    Py_XDECREF(self->options);

    free( self->env );

    self->ob_type->tp_free((PyObject*)self);
}

PyObject *
Environ_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	SEO *self;

    self = (SEO *)type->tp_alloc(type, 0);
//    self->env = slab_env_create( );
    self->env = 0;
    if (self != NULL) {
        self->kw = PyDict_New( );
//        if (self->kw == NULL)
//          {
//            Py_DECREF(self);
//            return NULL;
//          }

        Py_INCREF(Py_None);
        self->options = Py_None;

//        Py_INCREF(Py_None);
//        self->list = Py_None;

        Py_INCREF(Py_None);
        self->kw = Py_None;

    }

    self->env = slab_env_allocate( );
//
//	((PySLDict_Object*)self->options)->dict = self->env->options;
//	((PySLDict_Object*)self->kw)->dict = self->env->kw;

    return (PyObject *)self;
}

//static int have_default_options =0;
int
Environ_init(SEO *self, PyObject *args, PyObject *kwds)
{
	PyObject *sys_module;
    PyObject *sys_argv=NULL;
//    char* name;

    static char *kwlist[] = {"argc", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "|O", kwlist, &sys_argv) )
        return -1;

    if (sys_argv==NULL)
    {
    	sys_module = PyImport_ImportModule( "sys" );
    	if (sys_module == NULL)
    		return -1;

    	sys_argv = PyObject_GetAttrString( sys_module, "argv" );
        if (sys_argv==NULL)
        {
    		return -1;
        }
    }

	if (!PyList_Check(sys_argv) )
	{
		PyErr_SetString( PyExc_ValueError, "expected a list");
		return -1;
	}

	int argc = PyObject_Length(sys_argv);

	char** argv = malloc( argc );
	char *string;
	int i;
	PyObject* arg;
	for (i=0; i<argc; i++)
	{
		arg = PyList_GetItem(sys_argv, i );
		if (!arg)
			return -1;

		if ( !PyString_Check(arg) )
		{
			PyErr_SetString( PyExc_ValueError, "Expected a list of strings" );
			return 0;
		}

		string = PyString_AS_STRING( arg );
		if (string==0)
			return 0;
		argv[i] = (char*) malloc( strlen(string) +1);
		strcpy( argv[i], string);
	}

	slab_env_init_( self->env );
	slab_init_default_options( self->env );
	slab_environ_init( self->env, argc, argv , &DefaultOptions );

	PyObject* tmp;

	tmp = self->kw;
	self->kw = PySlabDict_FromDict( self->env->kw );
	Py_XDECREF(tmp);

	tmp = self->options;
	self->options = PySlabDict_FromDict( self->env->options );
	Py_XDECREF(tmp);

	return 0;

}

static PyObject *
Environ_getkw(SEO *self, void *closure)
{
    Py_INCREF(self->kw);
    return self->kw;
}

static PyObject *
Environ_getoptions(SEO *self, void *closure)
{
    Py_INCREF(self->options);
    return self->options;
}

static PyObject *
Environ_getargs(SEO *self, void *closure)
{

	int ln = slab_list_len(self->env->par);
	if(!ln)
		return PyTuple_New( 0 );

	PyObject* t = PyTuple_New( ln );

	if (!t)
		return 0;

	unsigned int i;
	char* s;
	PyObject* S;
	for (i=0;i<ln;i++)
	{
		s = slab_list_get( self->env->par, i );
		S = PyString_FromString( s );
		PyTuple_SetItem(t, i, S );
	}
    return t;
}


static PyGetSetDef Environ_getseters[] = {
    {"kw",
     (getter)Environ_getkw, NULL,
     "key word arguments",
     NULL},
    {"options",
     (getter)Environ_getoptions, NULL,
     "key word arguments",
     NULL},
     {"args",
     (getter)Environ_getargs, NULL,
     "non-key word arguments",
     NULL},

    {NULL}  /* Sentinel */
};


PyObject* Environ_help( SEO *self, PyObject *args, PyObject *kwds )
{
	char* help=0;
	PyObject* dct;
    if (! PyArg_ParseTuple(args,"Os", &dct, &help ) )
        return 0;


    int exit = slab_env_help(self->env,0,help);

    if (!exit)
    {
    	py_set_error_from_slab();
    	return 0;

    }
	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef Environ_methods[] = {
    {"help", (PyCFunction)Environ_help, METH_VARARGS,
     "Generate Help message if the -h option is detected\n"
     "env.help( parameters, help_text )\n"
     ""
    },
//    {"get_kw", (PyCFunction) Environ_getKW, METH_NOARGS,
//     "Return the name, combining the first and last name"
//    },
    {NULL}  /* Sentinel */
};

char envdoc[] = "Environment( [argv,]  **kw )\n"
		"argv must be a list of strings\n"
		"if argv is not given then sys.argv is used\n"
		"all keyword arguments update the dict member env.opts \n";


PyTypeObject slab_EnvironmentType = {
	    PyObject_HEAD_INIT(NULL)
	    0,                         /*ob_size*/
	    "slab.Environment",             /*tp_name*/
	    sizeof(SEO),             /*tp_basicsize*/
	    0,                         /*tp_itemsize*/
	    (destructor)Environment_dealloc, /*tp_dealloc*/
	    0,                         /*tp_print*/
	    0,                         /*tp_getattr*/
	    0,                         /*tp_setattr*/
	    0,                         /*tp_compare*/
	    0,                         /*tp_repr*/
	    0,                         /*tp_as_number*/
	    0,                         /*tp_as_sequence*/
	    0,                         /*tp_as_mapping*/
	    0,                         /*tp_hash */
	    0,                         /*tp_call*/
	    0,                         /*tp_str*/
	    0,                         /*tp_getattro*/
	    0,                         /*tp_setattro*/
	    0,                         /*tp_as_buffer*/
	    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
	    envdoc,           /* tp_doc */
	    0,		               /* tp_traverse */
	    0,		               /* tp_clear */
	    0,		               /* tp_richcompare */
	    0,		               /* tp_weaklistoffset */
	    0,		               /* tp_iter */
	    0,		               /* tp_iternext */
	    Environ_methods,             /* tp_methods */
	    0,                         /* tp_members */
	    Environ_getseters,           /* tp_getset */
	    0,                         /* tp_base */
	    0,                         /* tp_dict */
	    0,                         /* tp_descr_get */
	    0,                         /* tp_descr_set */
	    0,                         /* tp_dictoffset */
	    (initproc)Environ_init,      /* tp_init */
	    0,                         /* tp_alloc */
	    Environ_new,                 /* tp_new */
};


int PySlabEnv_Check( PyObject* Oenv )
{
	return PyObject_TypeCheck( Oenv, (PyTypeObject *) &slab_EnvironmentType );
}


struct SLEnvironment* PySlabEnv_AsEnv( PyObject* Oenv )
{
	if (! PySlabEnv_Check(Oenv) )
	{
		PyErr_SetString( PyExc_TypeError,  "expected a dict or slab.Environment object " );
		return 0;
	}

	return ((SEO*) Oenv)->env;
}


PyObject* PySlabEnv_FromEnv( struct SLEnvironment *env )
{
	if (!env)
		return 0;

	SEO* Oenv = (SEO*) Environ_new( (PyTypeObject *) &slab_EnvironmentType, 0,0 );

	if (!Oenv)
		return 0;

	Oenv->env = env;

	PyObject* tmp;

	tmp = Oenv->kw;
	Oenv->kw = PySlabDict_FromDict( env->kw );
	Py_XDECREF(tmp);

	tmp = Oenv->options;
	Oenv->options = PySlabDict_FromDict( env->options );
	Py_XDECREF(tmp);

	return (PyObject*) Oenv;
}

