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
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>


#include <slab/environment.h>
#include <slab/file.h>
#include <slab/error.h>
#include <slab/header_utils.h>

SLFile slab_file_allocate( )
{
	return (SLFile) malloc(sizeof(struct SLFileStruct) );
}

void slab_file_init( SLFile file, const SLEnviron env )
{
	file->pack=0;
	file->finalized=0;
	file->history =0;
	file->header_stream=0;
	file->binary_stream=0;
	file->bytes_proccessed=0;

	file->changed_header_values = slab_dict_create();
	file->header_values = slab_dict_create();

	if (!env)
	{
		file->env = slab_env_create();
	}
	else
	{
		file->env = slab_env_copy( env );
	}
//	return file;

}

SLFile slab_file_create( SLEnviron env )
{
	SLFile file = slab_file_allocate( );
	slab_file_init( file, env );

	return file;
}


void slab_file_delete( SLFile file )
{
	slab_env_delete( file->env );

	slab_dict_delete( file->header_values );
	slab_dict_delete( file->changed_header_values );

	if (file->history)
		free(file->history);

	file->env =0 ;
	file->header_values =0;
	file->changed_header_values =0;
	file->history=0;
}


char* Strip( char* str )
{
	while( *str == ' ' || *str == '\t' || *str == '\'' || *str == '"' )
		str++;

	char* end = str;
	while(*end!=0) end++;

	end--;

	while(*end == ' ' || *end == '\t' || *end == '\'' || *end == '"' || *end== '\n' )
	{
		end--;
	}

	*(end+1) = 0;
	return str;
}
void  process_line(  SLFile input, char* line )
{

	input->history = SCat( input->history, line );

	size_t span = strcspn( line, "#" );

	if (span)
		line[span]=0;

	char* eq = strpbrk( line, "=" );
	if ( !eq )
		return;

	line = Strip(line);
	Pair p = slab_pair_split_kw( line );

	slab_dict_set( input->header_values, Strip(p->key), Strip(p->value) );

}

int
slab_get_line( char*line, int num, FILE* st  )
{
	char c;
	c = fgetc( st );
	if (c==12)
	{
		c = fgetc( st );
		if (c==12)
		{
			c = fgetc( st );
			return 0;
		}
		else
			ungetc( c, st );
	}
	else
		ungetc( c, st );

	char* err = fgets( line, num, st  );

	if (!err)
		return 0;
	line[strlen(line)-1] = 0;

	return (int)err;

}
int read_header_file( SLFile input )
{
//	int c;
//	int err;
	char line[2048];

	FILE* st = input->header_stream;
//	int ll=0;
//	int breaks=0;
	while ( slab_get_line( line, 2048, st) )
	{
		process_line( input, line );
		memset(line,0,2048);
	}
	return 0;


}



SLFile slab_file_copy( SLFile file, SLEnviron env )
{
	SLFile new = malloc(sizeof(struct SLFileStruct) );

	new->fifo = file->fifo;
	new->header_stream = file->header_stream;
	new->binary_stream = file->binary_stream;

	new->header_values = slab_dict_copy( file->header_values );
	new->changed_header_values = slab_dict_copy(file->changed_header_values);

	new->history = malloc ( strlen(file->history)+1 );
	strcpy( new->history ,file->history );

	strcpy( new->header_name, file->header_name );
	strcpy( new->binary_name, file->binary_name );

	if (env)
		new->env = slab_env_copy( env);
	else
		new->env = slab_env_copy( file->env );

	return new;

}


char*
slab_file_get( SLFile file, const char* key )
{
	if ( !slab_dict_has_key( file->header_values, key) )
	{
		char r[1024];
		sprintf(r,"no key \"%s=\" in header file \"%s\" ", key, file->header_name );
//		slab_error( -61, r );Ö
		slab_error( SLAB_FILE_ERROR | SLAB_KEY_ERROR, "slab_file_get", r );
		return 0;
	}
	else
		return slab_dict_get( file->header_values, key, 0 );

}

char* slab_file_getdefault( SLFile file, char* key, char* def )
{
	return slab_dict_get( file->header_values, key, def );
}


int
slab_file_set( SLFile file, char* key, char* value )
{
	if (file->is_input)
	{
		char r[200]; sprintf(r,"could not set header '%s' with tag '%s' because header is an input",file->header_name,key);
//		slab_error( -33 , r );
		slab_error( SLAB_FILE_ERROR | SLAB_KEY_ERROR, "slab_file_set",r );
		return 0;
	}

	if (file->finalized)
	{
		char r[200]; sprintf(r,"could not set header '%s' with tag '%s' because header already written",file->header_name,key);
//		slab_error( -34 , r );
		slab_error( SLAB_FILE_ERROR | SLAB_KEY_ERROR, "slab_file_set", r );
		return 0;
	}

//	int err=0;
	if (!slab_dict_set( file->header_values, key, value ))
		return 0;

	if (!slab_dict_set( file->changed_header_values, key, value ))
		return 0;

	return 1;
}

char* sl_file_get( SLFile file, char* key )
{
	char* result = slab_file_get( file, key );
	if (!result)
		throw_error_already_set();
	return result;
}

void
sl_file_set( SLFile file, char* key, char* value )
{
	if (!slab_file_set( file, key, value ))
		throw_error_already_set();
	return;
}


void slab_file_close( SLFile file )
{
//	slab_file_esize
	unsigned long long int bytes_proccessed=1;
	bytes_proccessed *= slab_file_esize(file);
	bytes_proccessed *= slab_file_size(file);

	if (bytes_proccessed != file->bytes_proccessed )
	{
		char r[256];
		char msg[] = "slab_file_close: the number of bytes %s is not the same "
				     "as the number of bytes in the file '%s'. Processed %lu, expected %lu";

		if (file->is_input)
			sprintf( r , msg, "read",  file->header_name, file->bytes_proccessed,bytes_proccessed);
		else
			sprintf( r , msg, "written",  file->header_name, file->bytes_proccessed,bytes_proccessed);

		slab_warn( r );
	}

	fclose( file->header_stream );

	if (file->header_stream != file->binary_stream)
	{
		fclose( file->binary_stream );
	}

	return;

}
