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

#ifndef __SLAB_ENVIRON_H_
#define __SLAB_ENVIRON_H_


#include <slab/list.h>
#include <slab/Dictionary.h>
#include <slab/command_line_options.h>

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */


//! This is an environment for a main program to use
struct SLEnvironment
{

	int global_optsc;
	char ** global_opts;

	char prog_name[1024];

	//! dictionary of global options
	Dict options;
	//! dictionary of local parameters
	Dict kw;
	//! list of local parameters
	StringList par;

};

//! This struct is for initialization
typedef struct
{
	char* name;
	char* type;
	void* value;
	void* def;
	char* help;
} kwarglist;


typedef struct SLEnvironment* SLEnviron;

//! allocate memory for environment
SLEnviron slab_env_allocate( void );

//! allocate memory for environment
void slab_env_init_( SLEnviron env );

SLEnviron slab_env_create( void );

//! initialize an environment with command line arguments
//
void slab_environ_init( SLEnviron, int , char **, OptionsList );

//! free all information
void slab_env_delete( SLEnviron );

//! copy an environment
SLEnviron slab_env_copy( SLEnviron );

//! get a value from the local parameters part of the
//  @param env slab environment
//  @param key to get from local parameter dictionary
//  @throw slab_error sets error if the key is not in the parameters
char* slab_env_get( SLEnviron env,const char* key);

#define slab_env_get_double( ENV, NAME ) strtod( sl_env_get( ENV, NAME) , 0 )
#define slab_env_get_float( ENV, NAME ) (float) strtod( sl_env_get( ENV, NAME) , 0 )
#define slab_env_get_int( ENV, NAME ) (int) strtol( sl_env_get( ENV, NAME) , 0, 10 )
#define slab_env_get_longint( ENV, NAME ) strtol( sl_env_get( ENV, NAME) , 0, 10 )
#define slab_env_get_uli( ENV, NAME ) strtoul( sl_env_get( ENV, NAME) , 0, 10 )

//! same as slab_env_get but retuns \e def instead of setting error
char* slab_env_getdefault( SLEnviron env, const char* key, char* def );

//! get a global option from the environment
//  @throw slab_error sets error if the key is not in the parameters
char* slab_env_get_opt( SLEnviron env,const char* key);

//! get a global option from the environment
char* slab_env_getdefault_opt( SLEnviron env, const char* key, char* def );


//! Create a SLEnvironment instance from command line arguments
SLEnviron slab_env_init( int argc, char **argv);

//! initializes environment options from defaults from static
//  variable DefaultOptions
void slab_init_default_options( SLEnviron );

char* sl_env_get( SLEnviron env,const char* key);
char* sl_env_getdefault( SLEnviron env, const char* key, char* def );

char* sl_env_get_opt( SLEnviron env,const char* key);
char* sl_env_getdefault_opt( SLEnviron env, const char* key, char* def );


//! Create a SLEnvironment instance from command line arguments
SLEnviron sl_env_init( int argc, char **argv );

//! set local parameters and add '-h/--help' option
int
slab_env_help( SLEnviron, kwarglist* , char* );

#define sl_env_help( env, kws, msg ) if ( !slab_env_help( env, kws, msg ) ) { push_error( "main" ); throw_error_already_set(); }

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif // __SLAB_ENVIRON_H_

