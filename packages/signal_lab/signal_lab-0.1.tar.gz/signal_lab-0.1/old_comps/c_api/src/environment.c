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

#include <slab/command_line_options.h>
#include <slab/stringtype.h>
#include <slab/environment.h>
#include <slab/Dictionary.h>
#include <slab/error.h>

//static int slab_have_init_default_options =0;

void slab_init_default_options( SLEnviron env )
{

	slab_default_options();

	OptionsList curr = &DefaultOptions;

	char* name;
	char* def;
	while ( curr->opt && curr->next )
	{
		name = curr->opt->name;
		def = curr->opt->default_value;
		if (strlen(def))
		{
			slab_dict_set( env->options, name, def );
		}
		curr=curr->next;
	}

	return;
}



//! allocate memory for environment
SLEnviron slab_env_allocate( void )
{
	return malloc(sizeof(struct SLEnvironment) );
}

//! allocate memory for environment
void slab_env_init_( SLEnviron env )
{
	env->options = slab_dict_create();
	env->kw  = slab_dict_create();
	env->par = slab_list_create();
}

SLEnviron slab_env_create( )
{
	SLEnviron env = slab_env_allocate( );
	slab_env_init_( env );

	return env;
}

void slab_env_delete( SLEnviron env )
{
	if (env<=0)
		return;

	slab_dict_delete( env->kw );
	env->kw = 0;
	slab_dict_delete( env->options );
	env->options = 0;

	slab_list_delete( env->par );
	env->par=0;

	free( env );
	return;
}

SLEnviron slab_env_copy( SLEnviron env )
{

	SLEnviron new = slab_env_create( );

	new->kw = slab_dict_copy( env->kw );
	new->options = slab_dict_copy( env->options );
	new->par = slab_list_copy( env->par );
	return new;
}



void AddKeywordArg( SLEnviron env, char* arg)
{
	Pair p = slab_pair_split_kw( arg );
	slab_dict_set_pair( env->kw,  p );
}

void AddOption( SLEnviron env, Option opt, char* arg )
{
//	printf("AddOption %s, %s\n", opt->name, arg );
//	char* value;
	int iskw = slab_option_is_kw( arg );

	if (iskw)
	{
		Pair p = slab_pair_split_kw( arg );
		slab_dict_set( env->options, opt->name, p->value);
		slab_pair_delete( p );
		return;
	}
	else if ( strlen(opt->seen_value) )
	{
		slab_dict_set( env->options, opt->name, opt->seen_value);
	}
	else
	{
		slab_dict_set( env->options, opt->name, opt->default_value);
	}
}

void AddArg( SLEnviron env, char* arg )
{
	if ( env->par == 0 )
	{
		env->par = slab_list_create();
	}
	slab_list_append(env->par, arg);

}

char* slab_env_get( SLEnviron env, const char* key)
{
	char* val= slab_dict_get( env->kw, key , 0);
	if ( val == 0 )
	{
		char r[100];
		sprintf(r, "sl_error: Need '%s=' on command line\n", key );
		slab_error( SLAB_ENVIRON_ERROR | SLAB_KEY_ERROR, "slab_env_get", r );
		return 0;
	}
	else

		return val;
}

char* slab_env_getdefault( SLEnviron env, const char* key, char* def )
{
	return slab_dict_get( env->kw, key , def );

}

char* slab_env_get_opt( SLEnviron env, const char* key)
{
	if (!env)
	{
		slab_error( SLAB_ENVIRON_ERROR | SLAB_NULL_POINTER, "slab_env_get_opt"," null pointer to env" );
		return 0;
	}

	char* val= slab_dict_get( env->options, key , 0);
	if ( val == 0 )
	{
		char r[100];
		sprintf(r, "sl_error: Need '%s=' on command line\n", key );
		slab_error( SLAB_ENVIRON_ERROR | SLAB_KEY_ERROR, "slab_env_get_opt", r );
//		slab_error(-1,r);
		return 0;
	}
	else

		return val;
}

char* slab_env_getdefault_opt( SLEnviron env, const char* key, char* def )
{
	if (!env)
		return def;

	return  slab_dict_get( env->options, key , def );

}

void slab_environ_init( SLEnviron env, int argc, char **argv, OptionsList opts )
{
	int i=0;

	char *curr;
	Option opt;

	strcpy(env->prog_name,argv[0]);


	for (i=1; i<argc; i++)
	{
		curr = argv[i];


		if (opts)
			opt = slab_option_is_opt( opts, curr);
		else
			opt =0;

		if (  opt  )
		{
			AddOption(env, opt, curr);
		}
		else if ( slab_option_is_kw( curr) )
		{

			AddKeywordArg(env,curr);
		}
		else
		{
			AddArg(env,curr);
		}
	}
	return;

}

SLEnviron slab_env_init( int argc, char **argv)
{
	SLEnviron env = slab_env_create();
	slab_init_default_options( env );

	slab_environ_init( env, argc, argv, &DefaultOptions );

	return env;
}

#define SLOPT_HAS( NAME ) opt->NAME &&  strlen(opt->NAME)

void
print_option( Option opt )
{
	printf("    " );
	if  (SLOPT_HAS(shortname))
		printf("%s " , opt->shortname);
	if  (SLOPT_HAS(longname))
	{
		printf("%s" , opt->longname);
		if (SLOPT_HAS(seen_value))
		{
			printf(" ");
		}
		else
		{
			printf("=[%s]", opt->default_value );
		}
	}

	if ( SLOPT_HAS(help) )
		printf(": %s\n", opt->help );
	else
		printf("\n");

}


int
slab_env_help( SLEnviron env, kwarglist* args, char* help )
{

	int dohelp = slab_int( slab_dict_get( env->options,"help","0") );
	kwarglist* curr= args;

	if (dohelp)
	{
		printf("[prog] [OPTIONS] [PARAMETERS]\n");
		printf("%s\n\nLocal Parameters:\n",help);
		char *help;
		while (curr && curr->name)
		{

			if(!curr->help)
				help = "no help";
			else
				help  = curr->help;

			if(!curr->type)
				printf("    %s=ARG , %s\n", curr->name, help );
			else
				printf("    %s=[%s] , %s\n", curr->name,curr->type, help );

			curr++;
		}

		printf("\nGlobal Options:\n");
		OptionsList curro = &DefaultOptions;

		while(curro&& curro->opt)
		{
			print_option(curro->opt);
			curro = curro->next;
		}
		slab_exit(0);
		return 0;
	}

	curr = args;
	while (curr && curr->name)
	{
		if ( curr->type && curr->value )
		{
			char* val = slab_dict_get( env->kw, curr->name, 0 );

			if (!type_convert( curr->name, curr->type, val, curr->value, curr->def ))
			{
				push_error( "slab_env_help" );
				return 0;
			}
		}
		curr++;
	}

	return 1;

}


//! Function wrappers that Throw errors

char* sl_env_get( SLEnviron env,const char* key)
{
	char* val = slab_env_get( env, key);
	if (!val)
	{
		throw_error_already_set();
		return 0;
	}
	return val;
}

char* sl_env_get_opt( SLEnviron env,const char* key)
{
	char* val = slab_env_get_opt( env, key);
	if (!val)
	{
		throw_error_already_set();
		return 0;
	}
	return val;
}
