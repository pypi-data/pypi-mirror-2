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

#include "slab_test.h"

void Sl_Assert( char* msg, int line, char* file )
{
	char r[500]; sprintf( r, "%s:%i, '%s'",  file, line,msg );
	PyErr_SetString( PyExc_AssertionError, r );
}



static PyMethodDef module_methods[] = {
	
	#define TEST_METHOD(METH) PYSLAB_TEST_METHOD(METH)
	#include "all_test_methods.h"
	#undef TEST_METHOD 

//	PYSLAB_TEST_METHOD( dict_create )
//	PYSLAB_TEST_METHOD( dict_copy )
//	PYSLAB_TEST_METHOD( dict_delete )
//	PYSLAB_TEST_METHOD( dict_has_key )
//	PYSLAB_TEST_METHOD( dict_get )
////	PYSLAB_TEST_METHOD( dict_set )
//	PYSLAB_TEST_METHOD( dict_update )

    {NULL}  /* Sentinel */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

PyMODINIT_FUNC
init_test_slab(void)
{
    PyObject* m;

    m = Py_InitModule3("_test_slab", module_methods,
                       "Example module that creates an extension type.");

    if (m == NULL)
      return;
}

