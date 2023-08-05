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

#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include <slab/error.h>

#include <slab/Dictionary.h>


//! Concatonate two strings into a third
char* SCat( char* str1, char* str2 )
{
	char* str3;
	int len=0;
	if (str1>0)
		len += strlen(str1);
	if (str2>0)
		len += strlen(str2);

	len ++;
	len ++;

	str3 = malloc( len );

	if (str1>0)
	{
		strcpy( str3, str1);
		if (str2>0)
			str3 = strcat( str3, "\n");
			str3 = strcat( str3, str2);
		free(str1);
	}
	else if (str2>0)
	{
		strcpy( str3, str2 );
	}

	return str3;

}

//! create a Pair struct from a key and value string
Pair slab_pair_create( char* key, char* value )
{
	void* p = malloc(sizeof(struct PairStruct) );
	Pair pair = (Pair) p;

	int keylen = strlen(key)+1;
	int vallen = strlen(value)+1;

	pair->key = malloc( keylen );
	pair->value = malloc( vallen );


	strcpy(pair->key ,key );
	strcpy(pair->value ,value );

	return pair;
}

//! free a pair and its memory
void slab_pair_delete( Pair p )
{
	if (!p)
		return;
	free( p->key);
	free( p->value);

	p->key = 0;
	p->value = 0;

	free( p );

}

//! perform a deep copy on a pair
Pair slab_pair_copy( Pair p )
{
	if ( p ==0 )
	{
		slab_error( SLAB_PAIR_ERROR | SLAB_NULL_POINTER , "pair_copy", "got null pointer" );
		return 0;
	}
	return slab_pair_create( p->key, p->value );
}

//! allocate memory for a dict object
Dict slab_dict_allocate( void )
{
	return (Dict) malloc(sizeof(struct Dictionary) );
}
//! initialize the dict to default values
void slab_dict_init( Dict d )
{
	d->flag  =0;
	d->pair = 0;
	d->dict_next = 0;
}
//! create and initialize a Dict struct
Dict slab_dict_create( void )
{
	Dict d = slab_dict_allocate();
	slab_dict_init(d);
	return d;
}


//! free a dict and all of its refrences
int
slab_dict_delete( Dict d )
{
	if (d==0)
	{
//		slab_error( SLAB_DICT_ERROR | SLAB_NULL_POINTER , "slab_dict_delete", "got null pointer");
		return 0;
	}

//	int err=0;
	if ( SLAB_DICT_HAS_PAIR( d ) )
	{
		free( d->pair );
		d->pair=0;
		slab_dict_delete( SLAB_DICT_NEXT( d ) );
		SLAB_DICT_NEXT( d ) = 0;
//			return 0;
		free( d );
	}

	return 1;
}

//! deep copy of a Dict
Dict slab_dict_copy( Dict d )
{
	if (d==0)
	{
		slab_error( SLAB_DICT_ERROR | SLAB_NULL_POINTER , "slab_dict_copy", "got null pointer");
		return 0;
	}

	Dict new = slab_dict_create();

	if ( SLAB_DICT_HAS_PAIR( d ) )
	{
		new->flag=1;
		new->pair = slab_pair_copy( d->pair );
		new->dict_next = slab_dict_copy( SLAB_DICT_NEXT( d ) );
	}

	return new;
}

//! swap the pair associated with the current dictionary
Pair slab_pair_swap( Dict d, Pair p )
{
	if ( !d )
	{
//		slab_error( -55 , "SLAB: slab_pair_swap - got null Dict pointer");
		slab_error( SLAB_PAIR_ERROR | SLAB_NULL_POINTER , "slab_pair_swap", "got null pointer");
		return 0;
	}

	if ( SLAB_DICT_HAS_NEXT(d) && (p==0) )
	{
//		slab_error( -52 , "SLAB: slab_pair_swap - Dict has next but is setting pair to NULL");
		slab_error( SLAB_PAIR_ERROR | SLAB_NULL_POINTER , "slab_pair_swap"," Dict has next but is setting pair to NULL");
		return 0;
	}

	Pair pair = d->pair;
	d->pair = p;

//	if ( !p )
//		d->flag=0;
//	else
	d->flag=1;

	return pair;
}

//returns the a Dict if true otherwise 0
Dict
slab_dict_has_key( Dict dict, const char* key )
{
	if ( !dict )
	{
//		slab_error( -55 , "SLAB: slab_dict_has_key - got null Dict pointer");
		slab_error( SLAB_DICT_ERROR | SLAB_NULL_POINTER , "slab_dict_has_key","");

		return 0;
	}

	Dict curr = dict;

	while ( SLAB_DICT_HAS_PAIR( curr ) )
	{
		if ( strcmp( key, curr->pair->key ) == 0 )
			return curr;
		else
			curr = SLAB_DICT_NEXT( curr );
	}

	return 0;
}

//! set a pair in the dict. will overwrite any pair with the same key
int slab_dict_set_pair( Dict dict, Pair p )
{
	if ( !( dict || p ) )
	{
//		slab_error( -55 , "SLAB: slab_dict_set - got null pointer");
		slab_error( SLAB_DICT_ERROR | SLAB_NULL_POINTER , "slab_dict_set","");
		return 0;
	}

	Dict item;
	item = slab_dict_has_key( dict, p->key );
	if ( item )
	{
		p = slab_pair_swap(item , p );
		slab_pair_delete( p );
	}
	else
	{
		slab_dict_append( dict, p );
	}

	return 1;

}

//! set a key in the dict to value
int slab_dict_set( Dict dict, char* key, char * value )
{
	Pair p = slab_pair_create( key, value );
	return slab_dict_set_pair(dict,p);

}

//! append a pair to a dictionary
int slab_dict_append( Dict d, const Pair p )
{
	if ( ! d  )
	{
		slab_error( SLAB_DICT_ERROR | SLAB_NULL_POINTER , "slab_dict_append","");
		return 0;
	}

	if ( ! p  )
	{
		slab_error( SLAB_DICT_ERROR | SLAB_NULL_POINTER , "slab_dict_append","");
		return 0;
	}

	Dict curr = d;
	Dict last = slab_dict_create( );
//	Pair old;

	while ( SLAB_DICT_HAS_PAIR(curr) )
	{
		curr = SLAB_DICT_NEXT(curr);
	}

	curr->flag=1;
	curr->pair = p;
	curr->dict_next = last;

	return 1;
}

// get a key from the dict
char*
slab_dict_get( Dict dict, const char* key, char * def )
{

	if ( ! dict  )
	{
//		slab_error( -55 , "SLAB: slab_dict_get - got null Dict pointer");
		slab_error( SLAB_DICT_ERROR | SLAB_NULL_POINTER , "slab_dict_get","");
		return 0;
	}

	if ( ! key  )
	{
//		slab_error( -55 , "SLAB: slab_dict_get - got null char pointer");
		slab_error( SLAB_DICT_ERROR | SLAB_NULL_POINTER , "slab_dict_get","");
		return 0;
	}


	Dict curr = dict;
	while ( SLAB_DICT_HAS_PAIR(curr) )
	{
		if ( strcmp( key, curr->pair->key)==0 )
		{
			char* value = malloc( strlen(curr->pair->value)+1 );
			strcpy( value ,curr->pair->value );
			return value;
		}

		curr = SLAB_DICT_NEXT(curr);
	}

	if (!def)
	{
		char r[1024];
		sprintf(r, "no key %s", key );
		slab_error( SLAB_DICT_ERROR | SLAB_KEY_ERROR , "slab_dict_get",r );
	}

	return def;
}


Pair slab_pair_split_kw( const char* kwarg2 )
{
	char* kwarg = malloc( strlen(kwarg2) + 1);

	strcpy( kwarg, kwarg2 );

	char *key, *value;
	char *eq;

	eq = strchr( kwarg, '=' );

	*eq = 0;
	key  = kwarg;
	value = eq+1;

	Pair p = slab_pair_create( key, value);

	free(kwarg);
	return p;

}

//! update a dictionary with values from another
void
slab_dict_update( Dict dict, Dict other )
{
	while ( SLAB_DICT_HAS_PAIR(other) )
	{
		slab_dict_set(dict,other->pair->key,other->pair->value);
		other = SLAB_DICT_NEXT(other);
	}

	return ;
}
