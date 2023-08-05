#include <string.h>

#include <slab/command_line_options.h>

#include "slab_test.h"



SLAB_TEST_METHOD( option_is_opt )
{
	slab_default_options();
	OptionsList curr = &DefaultOptions;

	Option o = slab_option_is_opt( curr, "--datapath" );

	sl_assertfalse( o==0 , "should return datapath option" );

	sl_assertfalse( strcmp(o->name, "datapath" ) ,"should return the datapath option");

	slab_return;
}

SLAB_TEST_METHOD( option_is_kw )
{
//	slab_default_options();

	sl_assert( slab_option_is_kw( "a=b") , "test if argument is a key=value pair");

	sl_assertfalse( slab_option_is_kw( "a"), "test that argument is not a key=value pair" );

	slab_return;
}

SLAB_TEST_METHOD( option_append )
{
	slab_default_options();

	slab_return;
}
