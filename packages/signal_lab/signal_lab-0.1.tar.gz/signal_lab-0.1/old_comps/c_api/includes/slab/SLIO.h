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


#ifndef _SLAB_SLIO_H__
#define _SLAB_SLIO_H__

#include <slab/file.h>

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

typedef unsigned long long int ulli;

#define SLRead( TYPE, FILE, buffer, size ) sl_read( FILE , (char*) buffer , size * sizeof( TYPE ) );
#define SLWrite( TYPE, FILE, buffer, size ) sl_write( FILE , (char*) buffer , size * sizeof( TYPE ) );

ulli slab_read( SLFile slfile, char* buffer, ulli size );

ulli slab_write( SLFile slfile, char* buffer, ulli size );


struct SLIterator
{
	void* buffer;
	void* curr;

};

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* _SLAB_SLIO_H__ */


