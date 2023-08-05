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

#include <slab/SLIO.h>
#include <slab/error.h>

ulli slab_read( SLFile slfile, char* buffer, ulli count )
{
	size_t nrd = fread( (void *) buffer, (size_t) 1, (size_t) count , slfile->binary_stream );
	if ( ferror ( slfile->binary_stream ) != 0 )
	{
		char r[1024];
		sprintf( r, "trouble reading binary file %s", slfile->binary_name);
		slab_error( SLAB_FILE_ERROR | SLAB_IO_ERROR , "slab_read",r );
	}

	slfile->bytes_proccessed += nrd;

	return (ulli) nrd;

}

ulli slab_write( SLFile slfile, char* buffer, ulli count )
{
	if ( slfile->finalized == 0)
	{
		slab_error( SLAB_FILE_ERROR  , "slab_write",
			"header file was not finalized, need to call 'slab_file_finalize' before 'slab_write'" );
		return 0;
	}
	size_t nwt = fwrite( (void *) buffer, (size_t) 1, (size_t) count , slfile->binary_stream );

	if ( ferror( slfile->binary_stream )  )
	{
		char r[1024];
		sprintf(r, "trouble writing to binary file %s", slfile->binary_name);
		slab_error( SLAB_FILE_ERROR | SLAB_IO_ERROR , "slab_write", r );
	}

	slfile->bytes_proccessed += nwt;
	return (ulli) nwt;
}
