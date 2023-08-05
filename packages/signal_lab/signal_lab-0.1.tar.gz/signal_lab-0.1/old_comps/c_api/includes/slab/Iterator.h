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

#ifndef _SLAB_ITERATOR_H__
#define _SLAB_ITERATOR_H__

#include <slab/file.h>

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

	
typedef unsigned long long int (*rwfunc)( SLFile, char* , unsigned long long int );

struct slab_dims_iterator_struct
{
	char read;
	unsigned int esize;
	SLFile file;
	rwfunc function;

	unsigned long long int buffer_size;
	unsigned long long int buffer_elements;
	void* buffer;
	void* buffer_end;
	unsigned int owns_buffer;

	unsigned int iter_ndim;
	unsigned int data_ndim;

	unsigned long long int *data_dims;

	unsigned long long int left_size;
	unsigned long long int *left_dims;
	unsigned long long int *left_pos;

	unsigned long long int  current_step;
	unsigned long long int  total_steps;

	char started;
	char error;
};



typedef struct slab_dims_iterator_struct slab_dims_iter;
typedef struct slab_dims_iterator_struct *sldi;

sldi
slab_iter_create( SLFile file, unsigned int dim );

void
slab_iter_delete( sldi iter );

int
slab_iter_read_init( sldi iter, void* buffer, unsigned long long int buff_size );

int
slab_iter_write_init( sldi iter, void* buffer, unsigned long long int buff_size );


sldi
slab_iter_read_create( SLFile, int );

sldi
slab_iter_write_create( SLFile, int );

sldi
slab_iter_write_create_from_iter( SLFile file, sldi other );


int slab_iter_has_next( sldi );

struct slab_multi_iterator_struct
{
	sldi iter;
	struct slab_multi_iterator_struct *next;
};


typedef struct slab_multi_iterator_struct slab_multi_iter;
typedef struct slab_multi_iterator_struct *slmi;

slmi
slab_multi_iterator_create( void );

void
slab_multi_iterator_delete( slmi );

int
slab_multi_iterator_append( slmi mit, sldi dit );

int
slab_multi_iterator_next( slmi );

slmi slab_simple_iterator( SLFile,SLFile,int );

#ifdef __cplusplus
}
#endif /* __cplusplus */


#endif //_SLAB_ITERATOR_H__


