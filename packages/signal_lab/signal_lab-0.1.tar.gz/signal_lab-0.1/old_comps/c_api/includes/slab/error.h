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

#ifndef _SLAB_ERROR_H__
#define _SLAB_ERROR_H__

//! slab error types
#define SLAB_ERROR_TYPES    31

#define SLAB_UNKNOWN_ERROR   0
#define SLAB_NULL_POINTER    1
#define SLAB_KEY_ERROR       2
#define SLAB_INDEX_ERROR     3
#define SLAB_IO_ERROR        4
// ...
// #define    SLAB_..._ERROR  30
// up to 31 error types

#define SLAB_STD_ERROR      32  //  1 << 5

//! error codes for structs
#define SLAB_ERROR_STRUCTS    1984

#define SLAB_PAIR_ERROR       64 // 1 << 6
#define SLAB_DICT_ERROR      128 // 2 << 6
#define SLAB_ENVIRON_ERROR   192 // 3 << 6
#define SLAB_FILE_ERROR      256 // 4 << 6
#define SLAB_ITERATOR_ERROR	 320 // 5 << 6

char* slab_error_class( int etype );
char* slab_error_type( int etype );


#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */


//! information about last error that occurred
struct slab_error_struct
{
	int  slab_err;
	int  slab_err_line;
	char* slab_err_file;
	char* slab_err_msg;
	char function_name[100];
	struct slab_error_struct *next;
};
//! test if an error occured
int slab_error_occured( void );

//! clear the current error
int slab_error_clear( void );

typedef void (*slab_exit_function)( int);


//! exit fuction for throw_error_already_set to call
//extern slab_exit_function slab_exit;
void slab_exit( int e );

slab_exit_function slab_set_exit_function( slab_exit_function );

extern struct slab_error_struct *SLAB_ERROR_STACK;
extern struct slab_error_struct *SLAB_ERROR_STACK_CURR;

//! set slab error
void _slab_error( int eno, char* funcname, char* msg, int line, char* file);

//! push file and line info to error stack
void _slab_error_push( char* fname, int , char* );

#define slab_error( ERRNO, FUNC, MSG ) _slab_error( ERRNO, FUNC, MSG , __LINE__, __FILE__ )

#define return_if_error_0( cond, FUNCNAME ) if ((cond)==0) {_slab_error_push( FUNCNAME, __LINE__, __FILE__  ); return 0;}
#define return_if_error_I( cond, FUNCNAME ) if ((cond)==-1) {_slab_error_push( FUNCNAME, __LINE__, __FILE__  ); return -1;}
#define return_if_error_I0( cond, FUNCNAME ) if ((cond)==-1) {_slab_error_push(  FUNCNAME, __LINE__, __FILE__  ); return 0;}
#define push_error( FUNCNAME ) _slab_error_push( FUNCNAME, __LINE__, __FILE__  )

// Print error and exit
void throw_error_already_set( void );

typedef void (*slab_warn_function)( char* );

void slab_warn( char* msg );

slab_warn_function
slab_set_warnfunc( slab_warn_function f );

//! warning fuction for throw_error_already_set to call
//extern slab_warn_function slab_warning;

void slab_warn( char* );

#ifdef __cplusplus
}
#endif /* __cplusplus */


#endif // _SLAB_ERROR_H__
