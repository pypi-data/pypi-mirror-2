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

#include <stdlib.h>
#include <string.h>

#include <slab/stringtype.h>

#include <slab/header_utils.h>
#include <slab/error.h>


int slab_file_esize( SLFile file )
{
	char* result = slab_file_get( file, "esize" );
	if (!result)
	{
		push_error( "slab_file_esize");
		return 0;
	}

	char* endptr[100];
	return (int) strtol( result, endptr, 10 );
}

char*  slab_file_form( SLFile file )
{
	char *form_type = slab_file_get( file, "data_format" );
	if (!form_type)
	{
		push_error( "slab_file_dtype");
		return 0;
	}
	char* pch = strtok ( form_type, "_" );
//    pch = strtok ( NULL, "_" );
	return pch;

}

char*  slab_file_dtype( SLFile file )
{
//	char *type;
	char *form_type = slab_file_get( file, "data_format" );
	if (!form_type)
	{
		push_error( "slab_file_dtype");
		return 0;
	}

	char* pch = strtok ( form_type, "_" );
    pch = strtok ( NULL, "_" );

	return pch;

}


unsigned long long int* slab_file_dims( SLFile file )
{
	char key[10];
	char* nX;
	char* endptr[100];

	int ndim = slab_file_ndim(file);

	if (!ndim)
	{
		slab_error( 1, "slab_file_dims", "file has 0 dimentions");
		return 0;
	}

	unsigned long long int* dims = slab_dims_create( ndim );
	unsigned long long int dim;

	int i;
	for (i=0;i<ndim;i++)
	{
		sprintf(key,"n%i", i+1);
		nX = slab_dict_get(file->header_values,key,0);
		if (!nX)
		{
			push_error( "slab_file_dims");
			return 0;
		}
		dim = strtoul( nX, endptr, 10);
		dims[i] = dim;
	}

	dims[ndim]=0;
	return dims;
}

//#######################################################
// setters
//#######################################################

//! set element size of data
int slab_file_set_esize( SLFile file, const int esize )
{
	return slab_file_set( file,"esize", slab_str_int(esize) );
}

//! set type of data
int slab_file_set_dtype( SLFile file, const char* type )
{
	char r[100];
	sprintf(r,"native_%s",type);
	return slab_file_set( file,"esize", r );
}

//! set dimentions of data
int slab_file_set_dims( SLFile file, const unsigned long long int* dims )
{
	int ndim;
	int i;
	char key[100];

	ndim = slab_file_ndim(file);
	for (i=0;i<ndim;i++)
	{
		sprintf(key,"n%i", i+1);
		if (!slab_file_set(file, key, "1" ))
			return 0;
	}

	ndim = slab_dims_ndim( dims );
	for (i=0;i<ndim;i++)
	{
		sprintf(key,"n%i", i+1);
		if (!slab_file_set(file, key, slab_str_ulli(dims[i]) ))
			return 0;
	}

	return 1;
}


int slab_file_ndim( SLFile file )
{
	char key[10] = "n1";


	int i = 1;
	while( slab_dict_has_key(file->header_values,key) )
	{
		i++;
		sprintf(key,"n%i", i);
	}
	return i-1;
}


int slab_is_file_type( SLFile file, char* name, unsigned int size )
{
	int istype = 1;
	int esize = slab_file_esize( file );
	char * dtype = slab_file_dtype( file );
	if (!(dtype && esize) )
		return -1;

	istype = ( (esize == size ) && (strcmp(dtype,name) == 0  ) );

	return istype;
}


unsigned long long int slab_file_size( SLFile file)
{
	return slab_file_left_size( file , 0 );
}


int slab_dims_ndim( const unsigned long long int* dims )
{
	if (!dims)
		return 0;

	int ndim = 0;
	while ( *dims )
	{
		ndim++;
		dims++;
	}
	return ndim;
}


unsigned long long int* slab_dims_create( unsigned int ndim )
{
	int size = sizeof(unsigned long long int)*(ndim+1);
	unsigned long long int* dimscpy = malloc( size  );
	memset( dimscpy, 0, size );
	return dimscpy;
}

unsigned long long int* slab_dims_copy( const unsigned long long int* dims )
{
	int i;
	int ndim = slab_dims_ndim(dims);
	unsigned long long int* dimscpy = slab_dims_create( ndim );

	for (i=0;i<=ndim;i++)
	{
		dimscpy[i] = dims[i];
	}
	return dimscpy;
}

int slab_dims_inc( unsigned long long int* dims, unsigned long long int* idx_dims )
{
	if ( !(dims && idx_dims) )
		return 0;

	while( *dims )
	{
		if ( *idx_dims == ((*dims)-1) )
		{
			(*idx_dims)=0;
			idx_dims++;
			dims++;
		}
		else
		{
			(*idx_dims)++;
			break;
		}
	}

	return 1;

}

unsigned long long int slab_dims_left_size( unsigned long long int* dims, int dim )
{
	unsigned long long int* curdim = dims;
	if (!dims)
		return 0;

	curdim += dim;

	unsigned long long int size =1;

	while ( *curdim )
	{
		size *= *curdim;
		curdim++;
	}

	return size;

}

unsigned long long int slab_dims_right_size( unsigned long long int* dims, int dim )
{
	if (!dims)
		return 0;

	unsigned long long int size =1;
	int i;
	for( i=0; i<dim; i++ )
	{
		if (!dims[i])
			break;
		size *= dims[i];
	}
	return size;
}

void
sl_sdimsprint( char* r, unsigned long long int* dims, unsigned int ndim )
{
	if (!dims)
	{
		sprintf( r, "(null)");
		return;
	}

	char x[20];
	sprintf( r, "[");
	int i;
	for (i=0;i<ndim;i++)
	{
		sprintf(x,"%i", (int)dims[i] );
		strcat( r, x );
		if ( i<(ndim-1) )
			strcat( r, ", " );
	}

	strcat( r, "]" );

}

unsigned long long int slab_file_right_size( SLFile file , int dim )
{
	unsigned long long int* dims = slab_file_dims( file );

	unsigned long long int size = slab_dims_right_size(dims,dim);

	free(dims);

	return size;
}


unsigned long long int slab_file_left_size( SLFile file , int dim )
{
	unsigned long long int* dims = slab_file_dims(file);
	if (!dims)
		return 0;

	unsigned long long int size = slab_dims_left_size(dims,dim);

	free(dims);

	return size;

}

