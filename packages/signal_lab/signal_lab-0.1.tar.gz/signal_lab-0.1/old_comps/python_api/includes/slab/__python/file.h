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

#ifndef _SLAB_PYTHON_SL_FILE_H__
#define _SLAB_PYTHON_SL_FILE_H__

#include <Python.h>
#include "structmember.h"

#include <slab/file.h>

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    struct SLFileStruct *slfile;

	PyObject* header_stream;
	PyObject* binary_stream;
	PyObject* env;

} SLFILE_Object;


extern PyGetSetDef slfile_getseters[];
extern PyMethodDef slfile_methods[];
extern PyMemberDef slfile_members[];


PyAPI_DATA(PyTypeObject) SLFile_Type;


#endif // _SLAB_PYTHON_SL_FILE_H__
