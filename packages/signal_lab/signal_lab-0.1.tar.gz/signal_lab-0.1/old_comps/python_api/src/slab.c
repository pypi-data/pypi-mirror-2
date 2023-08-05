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

#include <Python.h>

#include <slab/error.h>

#include <slab/pyslab.h>

#include <slab/python/xml.h>

static PyMethodDef module_methods[] = {
    {NULL}  /* Sentinel */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

static
void pyslab_exit( int err )
{
	PyErr_SetString( PyExc_SystemExit,  "slab exit" );
	return;
}

static
void pyslab_warn( char* msg )
{
	PyErr_WarnEx( PyExc_UserWarning, msg, 2 );
	return;
}

PyMODINIT_FUNC
initslab(void)
{

	slab_set_exit_function( pyslab_exit );
	slab_set_warnfunc( pyslab_warn );
    PyObject* m;

    if (PyType_Ready(&slab_EnvironmentType) < 0)
        return;

    if (PyType_Ready(&SLFile_Type) < 0)
        return;

    if (PyType_Ready(&PySLdict_Type) < 0)
        return;

    if (PyType_Ready(&Py_SLIterator_Type) < 0)
        return;

    if (PyType_Ready(&PyESLFile_Type) < 0)
        return;

    m = Py_InitModule3("slab", module_methods,
                       "Signal Lab Python API.");

    if (m == NULL)
      return;

    Py_INCREF(&slab_EnvironmentType);
    PyModule_AddObject(m, "Environment", (PyObject *)&slab_EnvironmentType);

    Py_INCREF(&SLFile_Type);
    PyModule_AddObject(m, "sl_file", (PyObject *)&SLFile_Type);

    Py_INCREF(&PySLdict_Type);
    PyModule_AddObject(m, "sldict", (PyObject *)&PySLdict_Type);

    Py_INCREF(&Py_SLIterator_Type);
    PyModule_AddObject(m, "sliter", (PyObject *)&Py_SLIterator_Type);



    Py_INCREF(&PyESLFile_Type);
    PyModule_AddObject(m, "eslfile", (PyObject *)&PyESLFile_Type);

}

