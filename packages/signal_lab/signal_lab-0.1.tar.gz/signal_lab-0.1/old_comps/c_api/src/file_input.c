
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <slab/environment.h>
#include <slab/file.h>
#include <slab/error.h>

// Read values from a header file
int
slab_read_header_file( SLFile file, const char* name )
{

//	SLFile file = CreateSLFile( );
	file->finalized=1;
	file->is_input=1;

	char* open_mode =  slab_dict_get( file->env->options, "read_mode", "r+" );
	strcpy(file->open_mode,open_mode);

	if ( strcmp( name, "in") == 0)
	{
		name = slab_dict_get( file->env->options, "stdin", "stdin" );
		strcpy(file->header_name, name );
		if (!strcmp( name, "stdin"))
			file->header_stream = stdin;
		else
			file->header_stream = fopen( file->header_name, file->open_mode );
	}
	else
	{
		strcpy( file->header_name, name );
		file->header_stream = fopen( file->header_name, file->open_mode );
	}

	if (file->header_stream == 0)
	{
		char r[1024]; sprintf(r,"trouble opening header file '%s'", file->header_name );
//		slab_error( -1 , r );
		slab_error( SLAB_FILE_ERROR | SLAB_IO_ERROR | SLAB_STD_ERROR, "slab_read_header_file",r );
		return 0;
	}

	char* end;
	int  accept_tty = strtol( slab_dict_get( file->env->options, "accept_tty", "0" ) , &end , 10);
	int is_atty = isatty( fileno(file->header_stream) );
	if ( is_atty && (!accept_tty) )
	{
		char r[1024]; sprintf(r,"header file '%s' is a tty", file->header_name );
		slab_error( SLAB_FILE_ERROR | SLAB_IO_ERROR, "slab_read_header_file", r );
//		slab_error( -1 , r );
		return 0;
	}

	int c = fgetc( file->header_stream );

	if ( ferror(file->header_stream) || feof(file->header_stream) )
	{
		// Error
		char r[1024]; sprintf(r,"trouble reading header file '%s'", file->header_name);
//		slab_error( -1 , r );
		slab_error( SLAB_FILE_ERROR | SLAB_IO_ERROR, "slab_read_header_file",r );
		return 0;
	}
	else
	{
		int err = ungetc( c, file->header_stream );
		if (err==EOF)
		{
			char r[1024]; sprintf(r,"trouble reading header file '%s'", file->header_name);
			slab_error( SLAB_FILE_ERROR | SLAB_IO_ERROR, "slab_read_header_file", r );
//			slab_error( -1 , r );
			return 0;
		}
	}


	if ( read_header_file( file ) != 0 )
	{
		char r[1024]; sprintf(r,"trouble reading header file '%s'", file->header_name);
//		slab_error( -1 , r );
		slab_error( SLAB_FILE_ERROR | SLAB_IO_ERROR,"slab_read_header_file", r );
		return 0;
	}

	return 1;
}

int sl_open_binary_file( SLFile file )
{
	char* in = slab_file_getdefault( file, "in" , 0 );
	if ( in==0 )
	{
		char r[1024]; sprintf(r,"trouble opening binary from header file '%s', no 'in=' ", file->header_name);
		slab_error( SLAB_FILE_ERROR | SLAB_KEY_ERROR, "sl_open_binary_file", r );
//		slab_error( -1 , r );

		return 0;
	}

	if ( strcmp( in, "stdin") == 0)
	{
		strcpy( file->binary_name, file->header_name );
		file->binary_stream = file->header_stream;
	}
	else
	{
		strcpy( file->binary_name, in );
		file->binary_stream = fopen( file->binary_name, "r" );
	}

	if (file->binary_stream == 0)
	{
		char r[1024]; sprintf(r,"trouble opening binary file '%s' from header '%s'",
								file->binary_name, file->header_name);
		slab_error( SLAB_FILE_ERROR | SLAB_IO_ERROR, "sl_open_binary_file",r );
//		slab_error( -1 , r );
		return 0;
	}

	int c = fgetc( file->binary_stream );

	if ( ferror(file->binary_stream) || feof(file->binary_stream) )
	{
		char r[1024]; sprintf(r,"trouble reading binary file '%s' from header '%s'", file->binary_name, file->header_name);
//		slab_error( -1 , r );
		slab_error( SLAB_FILE_ERROR | SLAB_IO_ERROR, "sl_open_binary_file", r );
		return 0;
	}
	else
	{
		int err = ungetc( c, file->binary_stream );
		if (err==EOF)
		{
			slab_error( 1 , "sl_open_binary_file", "weird error: don't know what happend here" );
			return 0;
		}
	}

	return 1;

}

SLFile sl_input( char* name, SLEnviron env )
{
	SLFile file = slab_file_create(env);

	if (!slab_read_header_file( file, name ))
		throw_error_already_set( );

	if (!sl_open_binary_file( file ))
		throw_error_already_set( );

	return file;
}

