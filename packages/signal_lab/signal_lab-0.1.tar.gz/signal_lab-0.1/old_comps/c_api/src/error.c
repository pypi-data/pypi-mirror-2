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

#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>

#include <slab/error.h>

char* slab_error_class( int etype )
{
	return 0;
}

char* slab_error_type( int etype )
{
	switch (etype & SLAB_ERROR_TYPES)
	{
	case SLAB_NULL_POINTER:
		return "SLAB NULL POINTER";
	case SLAB_KEY_ERROR:
		return "SLAB Key Error";
	case SLAB_INDEX_ERROR:
		return "SLAB_Index Error";
	case SLAB_IO_ERROR:
		return "SLAB IO Error";
	default:
		return "SLAB Error";
	}
}


struct slab_error_struct *SLAB_ERROR_STACK=0;
struct slab_error_struct *SLAB_ERROR_STACK_CURR=0;

static slab_exit_function _slab_exit = exit;

void slab_exit( int e )
{
	_slab_exit( e );
}

slab_exit_function slab_set_exit_function( slab_exit_function f)
{
	slab_exit_function old = exit;
	_slab_exit = f;
	return old;
}
void slab_error_sdelete( struct slab_error_struct* sl_errors )
{
	if (!sl_errors)
		return;

	if (sl_errors->next)
		slab_error_sdelete(sl_errors->next);

	free( sl_errors );
	return;
}

int slab_error_occured( )
{
	return (int) SLAB_ERROR_STACK;
}

int slab_error_clear( )
{
	slab_error_sdelete(SLAB_ERROR_STACK);
	SLAB_ERROR_STACK = 0;
	SLAB_ERROR_STACK_CURR = 0;
	return 1;
}


typedef struct slab_error_struct slab_exc;
struct slab_error_struct* slab_error_create( int slerrno, char* funcname , char* msg , int line, char* file )
{
	slab_exc* err = malloc( sizeof(slab_exc) );

	err->slab_err = slerrno;
	err->slab_err_line = line;

	err->slab_err_file = malloc( 200 );
	err->slab_err_msg = malloc( 200 );
	if (file)
		strcpy( err->slab_err_file, file );
	else
		strcpy( err->slab_err_file, "???" );
	if (msg)
		strcpy( err->slab_err_msg, msg );
	else
		strcpy( err->slab_err_msg, "???" );

	if (funcname)
		strcpy( err->function_name, funcname );
	else
		strcpy( err->function_name, "???" );

	err->next = 0;

	return err;
}

void _slab_error( int serrno, char* funcname, char* msg , int line, char* file )
{
	slab_error_clear( );
//	slab_error_sdelete(ERROR_BASE);
//	slab_error_sdelete(ERROR_CURR);

	SLAB_ERROR_STACK = slab_error_create(serrno, funcname,  msg, line, file);
	SLAB_ERROR_STACK_CURR = SLAB_ERROR_STACK;
}


void
_slab_error_push( char* fname, int line, char* file )
{

	if (SLAB_ERROR_STACK_CURR)
	{
		struct slab_error_struct * ERROR_PREV = SLAB_ERROR_STACK_CURR;
		SLAB_ERROR_STACK_CURR = slab_error_create( 0, fname, "" , line, file );
		ERROR_PREV->next = SLAB_ERROR_STACK_CURR;
	}

}

void print_err( struct slab_error_struct* SLERR )
{
	if (!SLERR)
		return;

	char* setype = slab_error_type(SLERR->slab_err);
//	char setype[] = "SLAB Error";
	if (SLERR->slab_err)
	{
		fprintf( stderr, "%s [%d]: %s", setype, SLERR->slab_err, SLERR->slab_err_msg );
		if ( SLAB_STD_ERROR & SLERR->slab_err )
			fprintf( stderr, " (<errno.h> '%s')",strerror(errno));
		fprintf( stderr, "\n" );
	}

	fprintf( stderr, "  From file \"%s\", line %i, in %s\n", SLERR->slab_err_file,SLERR->slab_err_line,SLERR->function_name);

//	char filepath[FILENAME_MAX];
//	char* srcdir = getenv("SLABSRC");
//	if (! srcdir )
//		srcdir = ".";
//	sprintf(filepath,"%s/%s", srcdir, SLERR->slab_err_file );
//	FILE* scrfile = 0;
//
//	char fline[1024];
//	scrfile = fopen( filepath ,"r");
//	if ( !  scrfile )
//		fprintf( stderr, "    [no source]");
//	else
//	{
//		int i;
//		size_t nrd;
//		for (i=0; i< SLERR->slab_err_line; i++ )
//		{
//			nrd = fgets( fline, 1024, scrfile);
//			if (!nrd)
//				strcpy(fline,"[EOF]");
//		}
//
//		fprintf( stderr, "    %s\n" , fline );
//	}

	print_err( SLERR->next );
	return;
}
void throw_error_already_set( )
{
	if (!SLAB_ERROR_STACK)
		fprintf( stderr, "SLAB: throw_error_already_set called but no error was set\n");
	else
		print_err( SLAB_ERROR_STACK );

	fflush(stderr);
	slab_exit(-1);
}



void slab_warnf( char* msg )
{
	fprintf( stderr, "SLAB warning: %s", msg );
}


static slab_warn_function _slab_warning=slab_warnf;

slab_warn_function slab_set_warnfunc( slab_warn_function f )
{
	slab_warn_function old = _slab_warning;
	_slab_warning=f;
	return old;
}


void slab_warn( char* msg)
{
	_slab_warning( msg );

}

