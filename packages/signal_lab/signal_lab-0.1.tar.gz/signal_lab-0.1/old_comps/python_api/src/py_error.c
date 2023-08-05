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

#include <stdio.h>
#include <Python.h>

#include <slab/error.h>


PyObject* Py_slab_error_type( int etype )
{

	switch (etype & SLAB_ERROR_TYPES)
	{
	case SLAB_NULL_POINTER:
		return PyExc_SystemError;
	case SLAB_KEY_ERROR:
		return PyExc_KeyError;
	case SLAB_INDEX_ERROR:
		return PyExc_IndexError;
	case SLAB_IO_ERROR:
		return PyExc_IOError;
	default:
		return PyExc_Exception;
	}

}


void py_set_error_from_slab(void)
{
	char r[1024];

//	if (! slab_error_occured() )
//	{
//		fprintf( stderr, "Warning: py_set_error_from_slab called without error in slab\n" );
//		return;
//	}
//
//	if (SLAB_ERROR_STACK->slab_err == 0)
//	{
//		PyErr_SetString( PyExc_Exception, "'py_set_error_from_slab' called, but slab error was set to 0." );
//		return;
//	}

	if (SLAB_ERROR_STACK)
	{
		sprintf( r, "[%d]: %s From file \"%s\", line %i, in %s\n",
				SLAB_ERROR_STACK->slab_err, SLAB_ERROR_STACK->slab_err_msg,
				SLAB_ERROR_STACK->slab_err_file,SLAB_ERROR_STACK->slab_err_line,SLAB_ERROR_STACK->function_name
				);

		PyErr_SetString( Py_slab_error_type(SLAB_ERROR_STACK->slab_err), r );
		slab_error_clear();
	}
	else
	{
		if ( PyErr_Occurred() )
			return;

		PyErr_SetString( PyExc_Exception, "'py_set_error_from_slab' called, but no slab error was set." );
	}

	return;

}
