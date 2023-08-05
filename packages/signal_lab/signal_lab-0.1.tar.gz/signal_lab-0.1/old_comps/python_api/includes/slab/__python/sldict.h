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

#ifndef _SLAB_PYTHON_SL_DICT_H__
#define _SLAB_PYTHON_SL_DICT_H__

#include <Python.h>
#include "structmember.h"

#include <slab/Dictionary.h>

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    Dict dict;

} PySLDict_Object;


PyAPI_DATA(PyTypeObject) PySLdict_Type;


int
PySlabDict_Check( PyObject * Od );

PyObject *
PySlabDict_FromDict( Dict d);

Dict
PySlabDict_AsDict( PyObject * Od);

//PyGetSetDef sldict_getseters[];
//
//PyMethodDef sldict_methods[];


PyObject *
PySLdict_new( PyTypeObject *type, PyObject *args, PyObject *kwds );

int
PySLdict_update_pydict( Dict d, PyObject* pd );

PyObject*
PySLdict_update( PySLDict_Object *self, PyObject *args, PyObject *kwds );


PyObject*
SLDICT_items( Dict dict );

PyObject*
SLDICT_pair( Pair pair );

PyObject*
SLDICT_keys( Dict dict );

PyObject*
SLDICT_values( Dict dict );

PyObject*
SLDICT_getitem( Dict dict, const char* key );

PyObject*
SLDICT_haskey( Dict dict, char* key );

void
SLDICT_update( Dict dict, PyObject* obj );

#endif //_SLAB_PYTHON_SL_DICT_H__

