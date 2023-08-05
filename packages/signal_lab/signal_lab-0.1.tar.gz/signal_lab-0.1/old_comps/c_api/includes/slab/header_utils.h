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

#ifndef _SLAB_header_utils_h__
#define _SLAB_header_utils_h__

#include <slab/file.h>


#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */


//#######################################################
// getters
//#######################################################

//! the size of each element in the binary part of the file
int slab_file_esize( SLFile file );

//! data type of the file
char*  slab_file_dtype( SLFile file );

//! data form of the file
char*  slab_file_form( SLFile file );

//! list of the lenth of each dimention
unsigned long long int* slab_file_dims( SLFile file );

//! number of dimentions the data has
int slab_file_ndim( SLFile file );

//#######################################################
// setters
//#######################################################



//! set element size of data
int slab_file_set_esize( SLFile file, const int esize );

//! set type of data
int slab_file_set_dtype( SLFile file, const char* type );

//! set dimentions of data
int slab_file_set_dims( SLFile file, const unsigned long long int* dims );


//! test if the data is of a type
#define sl_is_type( FILE, TYPE ) slab_is_file_type( FILE, #TYPE, sizeof(TYPE) )


int slab_is_file_type( SLFile file, char* name, unsigned int size );

//! create a list of zeros
unsigned long long int*
slab_dims_create( unsigned int ndim );

//! copy list
unsigned long long int*
slab_dims_copy( const unsigned long long int* dims );

//! get number of consecutive non-zeroes in list
int slab_dims_ndim( const unsigned long long int* dims );

//! incrament a list
int
slab_dims_inc( unsigned long long int* dims, unsigned long long int* idx_dims );

//! foo
unsigned long long int
slab_dims_left_size( unsigned long long int* dims, int dim );

unsigned long long int
slab_dims_right_size( unsigned long long int* dims, int dim );

void
sl_sdimsprint( char* r, unsigned long long int* dims, unsigned int ndim );

unsigned long long int slab_file_size( SLFile file );
unsigned long long int slab_file_left_size( SLFile , int );
unsigned long long int slab_file_right_size( SLFile file , int dim );

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif // _SLAB_header_utils_h__


