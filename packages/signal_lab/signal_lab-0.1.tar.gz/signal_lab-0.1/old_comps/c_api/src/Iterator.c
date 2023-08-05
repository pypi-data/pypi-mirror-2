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

#include<stdlib.h>

#include<slab/SLIO.h>
#include<slab/header_utils.h>
#include<slab/error.h>

#include<slab/Iterator.h>

//#ifndef SLAB_BUFFER_SIZE
//#define SLAB_BUFFER_SIZE 16
//#endif // SLAB_BUFFER_SIZE

sldi slab_iter_create( SLFile file, unsigned int dim )
{

	sldi iter = malloc( sizeof(slab_dims_iter) );
	iter->read=-1;
	iter->file = file;

	iter->esize = slab_file_esize( file );
	if (!iter->esize)
		return 0;

	iter->iter_ndim = dim;

	iter->data_ndim = slab_file_ndim( file );

		return_if_error_0( iter->data_ndim, "slab_iter_create" );


	iter->data_dims = slab_file_dims( file );

		return_if_error_0( iter->data_dims, "slab_iter_create" );

	if (dim)
	{

		iter->left_size = slab_dims_left_size( iter->data_dims, dim );

		iter->left_dims = slab_dims_copy( iter->data_dims+dim );

		iter->left_pos  = slab_dims_create( iter->data_ndim-dim );

		iter->buffer_elements = slab_dims_right_size( iter->data_dims, dim );
	}
	else
	{
//		iter->data_dims = 0;
		iter->left_dims = 0;
		iter->left_pos  = 0;
		char* cbs = slab_dict_get(iter->file->env->options,"buffer_size","1024");

		unsigned long int buff_size =strtoul(cbs,0,10);

		iter->buffer_elements = buff_size / iter->esize;
		unsigned long long int ls = slab_dims_left_size( iter->data_dims, 0 );
		iter->left_size = ls / iter->buffer_elements;
		(ls % iter->buffer_elements) ? iter->left_size++ : 0;
	}

	iter->buffer_size = iter->esize*iter->buffer_elements;

	iter->buffer = 0;
	iter->buffer_end = 0;
	iter->owns_buffer=0;

	iter->current_step= 0;
	iter->started=0;
	iter->error=0;
	return iter;
}

int
slab_iter_read_init( sldi iter, void* buffer, unsigned long long int buff_size )
{
	iter->read=1;
	iter->function = slab_read;
	if (!buffer)
	{
		iter->buffer = malloc( iter->buffer_size );
		iter->owns_buffer=1;
	}
	else
	{
		if (buff_size < iter->buffer_size)
		{
			slab_error(-1,"slab_iter_read_init"," size of buffer is less than needed" );
			return 0;
		}
		iter->buffer= buffer;
		iter->owns_buffer=0;
	}

	iter->buffer_end = iter->buffer + iter->buffer_size;

//	iter->function( iter->file, iter->buffer, iter->buffer_size);

	return 1;
}

sldi
slab_iter_read_create( SLFile file, int dim )
{
	sldi iter = slab_iter_create( file, dim );
		return_if_error_0( iter, "slab_iter_read_create" );
	int err = slab_iter_read_init( iter, 0, 0 );
		return_if_error_I0( err, "slab_iter_read_create" );

	return iter;
}

int
slab_iter_write_init( sldi iter, void* buffer, unsigned long long int buff_size )
{
	iter->read=0;
	iter->function = slab_write;
	if (!buffer)
	{
		iter->buffer = malloc( iter->buffer_size );
		iter->owns_buffer=1;
	}
	else
	{
		if (buff_size < iter->buffer_size)
		{
			slab_error(-1,"slab_iter_read_init"," size of buffer is less than needed" );
			return 0;
		}
		iter->buffer= buffer;
		iter->owns_buffer=0;
	}

	iter->buffer_end = iter->buffer + iter->buffer_size;

	return 1;

}

sldi
slab_iter_write_create( SLFile file, int dim)
{
	sldi iter = slab_iter_create( file, dim );
		return_if_error_0( iter, "slab_iter_write_create" );
	int err = slab_iter_write_init( iter, 0, 0 );
		return_if_error_0( err, "slab_iter_write_create" );

	return iter;

}

sldi
slab_iter_write_create_from_iter( SLFile file, sldi other )
{
	sldi iter = slab_iter_create( file, other->iter_ndim );
		return_if_error_0( iter,"slab_iter_write_create_from_iter" );
	int err = slab_iter_write_init( iter, other->buffer, other->buffer_size );
		return_if_error_I0( err,"slab_iter_write_create_from_iter" );
	return iter;

}


int slab_iter_has_next( sldi iter )
{
	return (iter->current_step < iter->left_size);
}

int slab_iter_next( sldi iter )
{
	// Special for first step
	if ( !iter->started )
	{
		// Dont want to write if just starting
		if (iter->read)
		{
//			printf("initial read %i \n",iter->buffer );
			iter->function( iter->file, iter->buffer, iter->buffer_size);
		}
		iter->started=1;
	}
	else
	{
		// End condition
		if ( (iter->current_step+1) >= iter->left_size )
		{
			if ( !iter->read )
			{
//				printf("last write %i\n",iter->buffer);
				iter->function( iter->file, iter->buffer, iter->buffer_size);
			}
			return 0;
		}

//		if ( iter->read )
//			printf("read some%i\n",iter->buffer);
//		else
//			printf("write some %i\n",iter->buffer);

		iter->function( iter->file, iter->buffer, iter->buffer_size);

		if (iter->iter_ndim)
			slab_dims_inc( iter->left_dims , iter->left_pos );

//		printf("curr step = %i\n", (int) iter->current_step );
		iter->current_step++;
	}

//	if (((iter->current_step+1) >= iter->left_size) && (iter->started) )
//	{
//		if (!iter->read)
//			iter->function( iter->file, iter->buffer, iter->buffer_size);
//		return 0;
//	}
//
//	if (iter->started)
//	{
//		iter->function( iter->file, iter->buffer, iter->buffer_size);
//		if (iter->iter_ndim)
//			slab_dims_inc( iter->left_dims , iter->left_pos );
//		iter->current_step++;
//	}
//	else
//		iter->started=1;

	return 1;
}


void slab_iter_delete( sldi iter )
{
	if (!iter)
		return;

	if (iter->owns_buffer)
		free(iter->buffer);

	if (iter->data_dims)
		free(iter->data_dims);

	if (iter->left_dims)
		free(iter->left_dims);

	if (iter->left_pos)
		free(iter->left_pos);

	free(iter);
	return;
}

slmi
slab_multi_iterator_create( )
{
	slmi iter = malloc( sizeof(slab_multi_iter) );
	iter->iter=0;
	iter->next=0;
	return iter;
}

int
slab_multi_iterator_append( slmi mit, sldi dit )
{
	if (mit->iter)
	{
		if (dit->left_size != mit->iter->left_size)
		{
			slab_error( -1, "slab_multi_iterator_append","iterators are not the same size");
			return 0;
		}

	}


	while(mit->next && mit->iter)
		mit = mit->next;

	mit->iter=dit;
	mit->next=slab_multi_iterator_create( );
	return 1;
}


int
slab_multi_iterator_next( slmi mit )
{
	int hn, has_next=2;
	slmi curr = mit;

	while(curr->next && curr->iter)
	{
		hn = slab_iter_next(curr->iter);

		if (hn==-1)
			return -1;
		if (has_next!=2 && has_next!=hn)
		{
			slab_error( -1, "slab_multi_iterator_next"," iterators are not the same size");
			return -1;
		}
		else
			has_next = has_next && hn;

		curr = curr->next;
	}
	return has_next;
}

slmi slab_simple_iterator( SLFile in ,SLFile out,int ndim)
{
	sldi iiter = slab_iter_read_create( in, 0 );
	sldi oiter = slab_iter_write_create_from_iter( out, iiter );

	slmi miter = slab_multi_iterator_create( );
	slab_multi_iterator_append(miter,oiter);
	slab_multi_iterator_append(miter,iiter);

	return miter;
}

void
slab_multi_iterator_delete( slmi mit )
{
	if (!mit)
		return;

	slab_multi_iterator_delete( mit->next );
	slab_iter_delete( mit->iter );

	free(mit);
}
