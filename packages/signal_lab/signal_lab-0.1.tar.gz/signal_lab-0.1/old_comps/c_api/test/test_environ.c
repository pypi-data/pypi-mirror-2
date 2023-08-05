#include <string.h>

#include <slab/environment.h>

#include "slab_test.h"



SLAB_TEST_METHOD(env_init_)
{
	slab_return;
}

SLAB_TEST_METHOD(env_create)
{
	slab_return;
}

SLAB_TEST_METHOD(environ_init)
{
	int c = 5;
	char *args[] = {"hi","there","a=kw","xx","--datapath"};


	SLEnviron env = slab_env_create( );

	slab_default_options();
	OptionsList curr = &DefaultOptions;

	slab_environ_init( env, c,args, curr );

//	SLEnviron env = slab_env_init( c, args );

	char* a = slab_env_get( env, "a" );

//	sl_assert( env ,"env");
//	Dict hk = env->kw;

	sl_assert( a , "test that a is in the environment" );
	sl_assertfalse( strcmp(a,"kw") , "test that a is 'kw'" );

	slab_env_delete( env );

	slab_return;
}

SLAB_TEST_METHOD(env_delete)
{
	slab_return;

}

SLAB_TEST_METHOD(env_copy)
{
	int c = 5;
	char *args[] = {"hi","there","a=kw","xx","--datapath"};


	SLEnviron env = slab_env_create( );

	slab_default_options();
	OptionsList curr = &DefaultOptions;

	slab_environ_init( env, c,args, curr );

	SLEnviron envcp = slab_env_copy( env );


	slab_return;
}

SLAB_TEST_METHOD(env_get)
{
	slab_return;
}

SLAB_TEST_METHOD(env_getdefault)
{
	slab_return;
}

SLAB_TEST_METHOD(env_get_opt)
{
	slab_return;
}

SLAB_TEST_METHOD(env_getdefault_opt)
{
	slab_return;
}

SLAB_TEST_METHOD(env_init)
{
	slab_return;
}

SLAB_TEST_METHOD(init_default_options)
{
	slab_return;
}

SLAB_TEST_METHOD(sl_env_get)
{
	slab_return;
}
SLAB_TEST_METHOD(sl_env_getdefault)
{
	slab_return;
}

SLAB_TEST_METHOD(sl_env_get_opt)
{
	slab_return;
}
SLAB_TEST_METHOD(sl_env_getdefault_opt)
{
	slab_return;
}

SLAB_TEST_METHOD(sl_env_init)
{
	slab_return;
}

SLAB_TEST_METHOD(env_help)
{
	slab_return;
}

