
#include <string.h>

#include <slab/list.h>

#include "slab_test.h"

SLAB_TEST_METHOD( list_create )
{
	StringList l = slab_list_create( );

	slab_list_append( l, "a");

	char* a = slab_list_get( l, 0 );

	sl_assertfalse( strcmp("a", a ) , "test list was created with default argument");

	slab_list_delete( l );
	slab_return;
}

SLAB_TEST_METHOD( list_copy)
{
	StringList l, l2;
	l = slab_list_create( );
	slab_list_append( l, "value");

	l2 = slab_list_copy( l );

	char* a = slab_list_get( l, 0 );
	char* b = slab_list_get( l2, 0 );

	sl_assertfalse( strcmp(b, a ) , "test list was created with default argument");

	slab_list_delete( l );
	slab_list_delete( l2 );
	slab_return;
}


//SLAB_TEST_METHOD( list_append)
//{
//	slab_return;
//}

SLAB_TEST_METHOD( list_len )
{
	StringList l = slab_list_create( );

	sl_assert( slab_list_len(l) == 0, "tst list length " );
//	slab_list_len( l )

	slab_list_append( l, "a");

	sl_assert( slab_list_len(l) == 1, "tst list length " );

	slab_list_append( l, "b");

	sl_assert( slab_list_len(l) == 2, "tst list length " );

	slab_return;
}

SLAB_TEST_METHOD( list_flatten)
{

	StringList l = slab_list_create( );

	slab_list_append( l, "a");
	slab_list_append( l, "b");

	int len;
	char** args = slab_list_flatten( l, &len );

	sl_assert( len == 2, "test list length" );

	sl_assertfalse( strcmp( args[0], "a" ) , "test flatten has the same vaules");
	sl_assertfalse( strcmp( args[1], "b" ) , "test flatten has the same vaules");




	slab_return;
}

