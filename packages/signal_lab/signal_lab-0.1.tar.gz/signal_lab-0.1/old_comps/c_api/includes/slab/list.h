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
#ifndef _SLAB_LIST_H_
#define _SLAB_LIST_H_

//! linked list of strings
struct StringListStruct
{
	char** lst;
	unsigned int mem_len;
	unsigned int len;
//	char str[1024];
};

typedef struct StringListStruct* StringList;

StringList slab_list_allocate( void );

void slab_list_init( StringList l );
void slab_list_init1( StringList l , int size );

StringList slab_list_create( void );
StringList slab_list_copy( StringList );

void slab_list_delete( StringList );

void slab_list_append( StringList sl, const char* value );

int slab_list_len( StringList sl );

//int StringListLen( StringList sl );

//las
char** slab_list_flatten( StringList sl, int* len );


//! get a value from the string list
char* slab_list_get( StringList sl, unsigned int idx );




#endif  // _SLAB_LIST_H_
