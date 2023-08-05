
#ifndef _SLAB_ENV_UTILS_HPP__
#define _SLAB_ENV_UTILS_HPP__

#include <slab/environment.h>


int slab_env_have_stdin( SLEnviron env );

int
slab_env_have_stdout( SLEnviron env );

char*
slab_env_prog( SLEnviron env );

char*
slab_env_time( SLEnviron env );

char*
slab_env_user( SLEnviron env );


#endif // _SLAB_ENV_UTILS_HPP__


