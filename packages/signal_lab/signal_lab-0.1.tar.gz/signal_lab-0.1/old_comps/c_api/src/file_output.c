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
#include <slab/filesys.h>
#include <slab/stringtype.h>


int slab_file_output( SLFile output, const char* name )
{
	char* header_path, *binary_name, *datapath, *binary_path;
	char* open_mode;
//	long dot;
	char* end;
	int hfifo =0;
	int  accept_tty, is_atty;

	struct stat stats;

	open_mode =  slab_dict_get( output->env->options, "write_mode", "w+" );
	strcpy(output->open_mode,open_mode);

	if ( strcmp( name, "out" ) ==0 )
	{
		name = slab_dict_get( output->env->options, "stdout", "stdout" );

//		if ( !strcm )
//		{
//
//		}

		strcpy(output->header_name, name );
		if (! strcmp( name, "stdout") )
			output->header_stream = stdout;
		else
			output->header_stream = fopen( output->header_name, output->open_mode );

	}
	else
	{
		strcpy( output->header_name, name );
		hfifo = slab_int ( slab_dict_get( output->env->options, "fifo", "0" ));

		if (hfifo)
		{
			if ( mkfifo( name , 0666 ) )
			{
				char r[1024]; sprintf(r,"trouble creating fifo file '%s' to write to. ",
										output->header_name);

				slab_error( SLAB_FILE_ERROR | SLAB_STD_ERROR, "slab_output" , r );

				return 0;
			}
		}


		output->header_stream = fopen( output->header_name, output->open_mode );
	}

	if (output->header_stream==0)
	{
		char r[1024]; sprintf(r,"trouble opening header file '%s' to write to",
								output->header_name);
		slab_error( SLAB_FILE_ERROR | SLAB_STD_ERROR, "slab_output" , r );
		return 0;
	}


	accept_tty = strtol( slab_dict_get( output->env->options, "accept_tty", "0" ) , &end , 10);
	is_atty = isatty( fileno(output->header_stream) );

	if ( is_atty && (!accept_tty) )

	{
		char r[1024]; sprintf(r,"header file '%s' is a tty", output->header_name );
		slab_error( SLAB_FILE_ERROR, "slab_output" , r );
		return 0;
	}


	fstat( fileno(output->header_stream), &stats );

	int isreg = S_ISREG(stats.st_mode);

	if (isreg)
		output->pack =0;
	else
		output->pack =1;

	if (!output->pack)
	{
		output->pack = strtol( slab_dict_get( output->env->options, "pack", "0" ) , &end , 10);
	}

	if ( !output->pack )
	{

		datapath = slab_dict_get( output->env->options, "datapath", ".");

		// unpack
		if ( !strcmp( name, "stdout" ) )
		{
			header_path = slab_getfilename( fileno(output->header_stream) );
//			fprintf(stderr, "header path = '''%s'''", header_path);
			if (header_path==0)
			{
				header_path = malloc( L_tmpnam );
				header_path = tmpnam( header_path );
			}
			binary_name = strrchr( header_path, '/' );
		}
		else
		{
			binary_name = malloc( strlen(name)+1);
			strcpy(binary_name , name);
		}

		binary_path = malloc( strlen(datapath)+ strlen(binary_name)+5  );
		sprintf(binary_path,"%s/%s@", datapath, binary_name);

		int unique_binary;
		unique_binary = slab_int( slab_dict_get( output->env->options, "unique_binary", "0" ) );
		
		if ( unique_binary && stat(binary_path, &stats) == 0 )
		{
			int i=1;
			binary_name[strlen(binary_name)-4] =0;
			sprintf(binary_path,"%s/%s-%i.rsf@", datapath, binary_name,i );
			while ( stat(binary_path, &stats) == 0 )
			{
				i++;
				sprintf(binary_path,"%s/%s-%i.rsf@", datapath, binary_name,i );
			}
		}


		strcpy(output->binary_name, binary_path);
		output->binary_stream = fopen( output->binary_name, "wb" );

		slab_file_set( output, "in", output->binary_name );
	}
	else
	{
		// pack data
		output->binary_stream = output->header_stream;
		strcpy(output->binary_name, output->header_name);
		slab_file_set( output, "in", "stdin" );

	}

	if ( output->binary_stream == 0 )
	{
		perror( "SLAB--");
		char r[1024]; sprintf(r,"trouble opening binary file '%s' from header '%s' for writing",
				output->binary_name, output->header_name );
		slab_error( SLAB_FILE_ERROR, "slab_output" , r );
		return 0;
	}


	return 1;

}


SLFile slab_output( char* name, SLFile input, SLEnviron env )
{
	SLFile output;
	if (input!=0)
		 output = slab_file_copy( input, env );
	else
		 output = slab_file_create( env );

	output->finalized = 0;
	output->is_input=0;

	if ( !slab_file_output(output,name) )
	{
		push_error( "slab_output");
		return 0;
	}

	return output;

}

SLFile sl_output( char* name, SLFile input, SLEnviron env )
{
	SLFile result = slab_output( name, input, env );
	if(!result)
		throw_error_already_set( );
	return result;


}

int
slab_finalize_output( SLFile output )
{
	if (output->finalized != 0 )
	{
		slab_error( SLAB_FILE_ERROR, "slab_finalize_output", "header file not writable" );
		return 0;
	}

	FILE* stream = output->header_stream;

	fprintf(stream,"%s\nThis is the new part of the header file\n", output->history );

	Dict chv = output->changed_header_values;
	while (chv)
	{
		if ( chv->pair != 0 )
			fprintf(stream, "\t%s=%s\n", chv->pair->key, chv->pair->value );

		chv = chv->dict_next;
	}

	fprintf(stream, "\n\n" );
	if ( output->pack )
	{
		fputc( 12, stream );
		fputc( 12, stream );
		fputc( '\004',stream  );
	}
	fflush( stream );
	output->finalized = 1;
	return 1;

}

void
sl_finalize( SLFile output )
{
	if (!slab_finalize_output( output ))
		throw_error_already_set( );
	return;
}

