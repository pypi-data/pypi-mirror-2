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
//#include<slab/python/sldict.h>

PyObject*
SLDICT_pair( Pair pair )
{
	if (pair==0)
		return 0;

	PyObject* t = PyTuple_New( 2 );
	PyTuple_SetItem(t, 0, PyString_FromString(pair->key) );
	PyTuple_SetItem(t, 1, PyString_FromString(pair->value) );

	return t;
}


PyObject*
SLDICT_items( Dict dict )
{

	PyObject* list = PyList_New( 0 );

	if (dict==0)
		return list;

	PyObject* pair;
	Dict curr = dict;
	while ( SLAB_DICT_HAS_PAIR(curr) )
	{
		pair = SLDICT_pair( curr->pair );
		if (pair)
			PyList_Append( list, pair );
		curr = SLAB_DICT_NEXT(curr);
	}

	return list;
}

PyObject*
SLDICT_keys( Dict dict )
{
	PyObject* list = PyList_New( 0 );

	if (dict==0)
		return list;

	Dict curr = dict;
	while ( SLAB_DICT_HAS_PAIR(curr) )
	{
		if (curr->pair && curr->pair->key)
			PyList_Append( list, PyString_FromString(curr->pair->key) );
		else
		{
			return 0;
		}
		curr = SLAB_DICT_NEXT(curr);
	}

	return list;

}

PyObject*
SLDICT_values( Dict dict )
{
	PyObject* list = PyList_New( 0 );

	if (dict==0)
		return list;

	Dict curr = dict;
	while ( SLAB_DICT_HAS_PAIR(curr) )
	{

		PyList_Append( list, PyString_FromString(curr->pair->value) );
		curr = SLAB_DICT_NEXT(curr);
	}

	return list;

}

PyObject*
SLDICT_getitem( Dict dict, const char* key )
{
	char* value = slab_dict_get( dict, key, 0 );
	if (!value)
		return 0;
	return PyString_FromString(value);
}


PyObject*
SLDICT_haskey( Dict dict, char* key )
{
	Dict hk = slab_dict_has_key( dict, key);
	PyObject* res = PyInt_FromLong( (long int) hk );
	return res;
}

