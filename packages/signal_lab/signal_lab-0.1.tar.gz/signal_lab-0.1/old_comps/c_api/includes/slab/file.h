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

#ifndef _SLAB_FILE_H__
#define _SLAB_FILE_H__

#include <stdio.h>
#include <slab/Dictionary.h>
#include <slab/environment.h>

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */


#define FS_STRLEN 1024

//! represent rsf file
struct SLFileStruct
{
	//! true if file is input. false if output.
	int is_input;

	//! file io is attached to a fifo device
	int fifo;
	//! pack binary with header (output only)
	int pack;
	//! header has been written
	// must be true to write binary
	int finalized;
	//! environment used to create struct
	// get global options from env->options
	SLEnviron env;
	//! header part of the file
	FILE* header_stream;

	//! mode to open header and binary
	char open_mode[10];

	//! binary part of the file
	FILE* binary_stream;
	//! dictionary of header keys
	Dict header_values;
	//! dictionary of  header keys changed sine file creation (output only)
	Dict changed_header_values;

	//! history of previous file
	char *history;

	//! name of header file on disk
	char header_name[FS_STRLEN];

	//! name of binary file on disk
	char binary_name[FS_STRLEN];

	unsigned long long int bytes_proccessed;
};


typedef struct SLFileStruct *SLFile;

//! open a SLFile from disk, reads header but not binary
//  @param name is the name of the file to open
//  @param env environment containing global options to use
//    when opening the file.
//    may be an existing SLEnviron struct or 0
//  @return an opened SLFile instance or NULL on error
//  @throw slab_error is set
SLFile sl_input( char* name, SLEnviron env );

//! deep copy of the file
SLFile slab_file_copy( SLFile , SLEnviron );

SLFile slab_file_allocate( void );

void slab_file_delete( SLFile );

void slab_file_init( SLFile file, const SLEnviron env );

//! allocate memory and copy \e env parameter into
// return a new SLFile refrence
SLFile slab_file_create( const SLEnviron );


//! open and read a the header file
/*  places the header keys in file->header_values
 *  @param file a valid file refrence created by slab_file_create
 *  @param name path name of a file on disk.
 *  @return 0 on success and -1 on failure
 *  @throw slab_error
 */
int
slab_read_header_file( SLFile file, const char* name );

//! internal helper function
int read_header_file( SLFile input );


//! open the binary file associated with \e file
/*  @return 0 on success and -1 on failure
 */
int sl_open_binary_file( SLFile file );


//! close the header and binary parts associated with \e file
void slab_file_close( SLFile file );

//! get a key from header_values dictionary of file
/*  @param file opened file refrence.
 *  @key string ofheader key to get
 *  @return the header value corresponding to the header key \e key.
 *   or 0 if the key does not exist
 *  @throw slab_error
 */
char*
slab_file_get( SLFile file, const char* key );

//! get a key from header_values dictionary of file
/*  @param file opened file refrence.
 *  @return the header value corresponding to the header key \e key.
 *   or \e def if the key does not exist
 */
char*
slab_file_getdefault( SLFile file, char* key, char* def );

//! set a key/value pair in header file (output only)
int
slab_file_set( SLFile file, char* key, char* value );


char* sl_file_get( SLFile file, char* key );
void sl_file_set( SLFile file, char* key, char* value );
#define sl_file_getdefault( FILE,KEY,DEF) slab_file_getdefault( FILE, KEY, DEF );


//############################
// Output

int slab_file_output( SLFile output, const char* name );

SLFile slab_output( char* name, SLFile input, SLEnviron env );

SLFile sl_output( char* name, SLFile input, SLEnviron env );

int slab_finalize_output( SLFile output );
void sl_finalize( SLFile output );
#define sl_file_finalize( OUTPUT ) if (!slab_finalize_output( OUTPUT )) { push_error("sl_file_finalize"); throw_error_already_set( ); }


//slab_file_test( SLFile, file );


#ifdef __cplusplus
}
#endif /* __cplusplus */


#endif // _SLAB_FILE_H__
