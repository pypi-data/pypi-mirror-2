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

#include<slab/pyslab.h>


void
sliter_dealloc( Py_SLIterator_Object* self)
{
    self->ob_type->tp_free((PyObject*)self);
}

PyObject *
sliter_new( PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	Py_SLIterator_Object *self;
    self = (Py_SLIterator_Object *)type->tp_alloc(type, 0);


    return (PyObject *) self;
}



int
sliter_init( Py_SLIterator_Object *self, PyObject *args, PyObject *kwds)
{
	return 0;
}

PyObject*
sl_iter_iter( Py_SLIterator_Object* self )
{
	return 0;
}

PyObject*
sl_iter_next( Py_SLIterator_Object* self )
{
	return 0;
}

PyTypeObject Py_SLIterator_Type = {
	    PyObject_HEAD_INIT(NULL)
	    0,                         /*ob_size*/
	    "slab.sliter",             /*tp_name*/
	    sizeof(Py_SLIterator_Type),     /*tp_basicsize*/
	    0,                         /*tp_itemsize*/
	    (destructor)sliter_dealloc, /*tp_dealloc*/
//	    0, /*t/p_dealloc*/
	    0,                         /*tp_print*/
	    0,                         /*tp_getattr*/
	    0,                         /*tp_setattr*/
	    0,                         /*tp_compare*/
	    0,                         /*tp_repr*/
	    0,                         /*tp_as_number*/

	    0,                         /*tp_as_sequence*/
//	    slfile_as_sequence, 		/*tp_as_sequence*/

	    0,                         /*tp_as_mapping*/

	    0,                         /*tp_hash */
	    0,                         /*tp_call*/
	    0,                         /*tp_str*/
	    0,                         /*tp_getattro*/
	    0,                         /*tp_setattro*/
	    0,                         /*tp_as_buffer*/
	    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_ITER, /*tp_flags*/
	    "SLAB objects",           /* tp_doc */
	    0,		               /* tp_traverse */
	    0,		               /* tp_clear */
	    0,		               /* tp_richcompare */
	    0,		               /* tp_weaklistoffset */
	    (getiterfunc) sl_iter_iter,		               /* tp_iter */
	    (iternextfunc)sl_iter_next,		               /* tp_iternext */

	    0,             /* tp_methods */
//	    slfile_methods,             /* tp_methods */

	    0,                         /* tp_members */
//	    slfile_members,                         /* tp_members */
	    0,           /* tp_getset */
	    0,                         /* tp_base */
	    0,                         /* tp_dict */
	    0,                         /* tp_descr_get */
	    0,                         /* tp_descr_set */
	    0,                         /* tp_dictoffset */
	    (initproc) sliter_init,      /* tp_init */
//	    0,      /* tp_init */
	    0,                         /* tp_alloc */
	    sliter_new,                 /* tp_new */
};
