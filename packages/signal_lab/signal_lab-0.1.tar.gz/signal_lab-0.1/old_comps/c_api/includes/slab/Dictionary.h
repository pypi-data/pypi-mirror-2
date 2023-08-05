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

#ifndef __SLAB_DICT_H_
#define __SLAB_DICT_H_

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#define PAIR_STRING_LEN 1024

//! Pair is a key/value entry in a dictionary
struct PairStruct
{
	char* key;
	char* value;
};

typedef struct PairStruct* Pair;


//! concatonate two strings
//!
//
char* SCat( char* str1, char* str2 );


//! Class containing key value pairs
struct Dictionary
{
	int flag;
	Pair pair;
	struct Dictionary* dict_next;
};


typedef struct Dictionary* Dict;

#define SLAB_DICT_NEXT( d ) (d)->dict_next
#define SLAB_DICT_HAS_NEXT( d ) ( d->flag && (d)->dict_next && (d)->dict_next->flag )
#define SLAB_DICT_HAS_PAIR( d ) ( d->flag )

//! allocate memory for a dict object
Dict slab_dict_allocate( void );
//! initialize the dict to default values
void slab_dict_init( Dict d );

//! Create an empty dict
Dict slab_dict_create(  void );

//! Copy a dictionary
Dict slab_dict_copy( Dict );

//! free all memory used by Dict
int
slab_dict_delete( Dict );


//! get a value from the dict
Dict
slab_dict_has_key( Dict dict, const char* key );

//! get a value from the dict
char*
slab_dict_get( Dict dict, const char* key, char * def );

//! set a vlaue from the dict
int slab_dict_set( Dict dict, char* key, char * value);

//! set a vlaue from the dict
int slab_dict_set_pair( Dict dict, Pair p );

//! update the entries in a dictionary with anithor
void
slab_dict_update( Dict dict, Dict other );

//! Swap a pair
Pair slab_pair_swap( Dict, Pair );


//! create a key value pair
Pair slab_pair_create( char* key, char* value );

//! delete a pair
void slab_pair_delete( Pair );

//! append a pair to the end of a dictionaly
int  slab_dict_append( Dict d, const Pair p );



////! Get a key value pair from dict
//Pair Get_Pair( Dict dict, const char* key );
//

//! split a "key=value" string into a Pair struct
Pair slab_pair_split_kw( const char* kwarg2  );



#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif // __SLAB_DICT_H_
