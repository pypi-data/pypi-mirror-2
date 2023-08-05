
#include <string.h>

#include <slab/Dictionary.h>

#include "slab_test.h"


SLAB_TEST_METHOD( dict_create )
{
	Dict d = slab_dict_create( );

	sl_assert( d, "dictionary is null" );
	sl_assertfalse( d->flag, "dictionary is not empty" );
	sl_assertfalse( d->pair, "dictionary is not empty" );
	sl_assertfalse( d->dict_next, "dictionary is not empty" );

	slab_return;
}

SLAB_TEST_METHOD( dict_copy )
{
	Dict d;
	Dict d_copy;

	d = slab_dict_create( );

	slab_dict_set( d, "key", "value" );

	d_copy = slab_dict_copy( d );

	sl_assert( slab_dict_has_key( d_copy, "key" ), "dict does not have expeted key" );

	slab_return;
}

SLAB_TEST_METHOD( dict_delete )
{
	slab_return;
}

SLAB_TEST_METHOD( dict_has_key )
{
	Dict d = slab_dict_create( );
	slab_dict_set( d, "key", "value" );
	sl_assert( slab_dict_has_key(d, "key"), "dict does not have expeted key" );
	sl_assertfalse( slab_dict_has_key(d, "no" ), "dict does not have expeted key" );

	slab_return;
}

SLAB_TEST_METHOD( dict_get )
{
	char* val;
	Dict d;

	d = slab_dict_create( );
	slab_dict_set( d, "key", "value" );
	val = slab_dict_get( d, "key", 0 );

	sl_assert( val, "slab did not return value" );
	sl_assert( !strcmp(val,"value"), "slab did not return correct value" );

	// get non existing entry
	val = slab_dict_get( d, "e", 0 );
	sl_assertfalse( val, "slab did not return value" );

	// get non existing entry w default
	val = slab_dict_get( d, "e", "e" );
	sl_assert( val, "slab did not return value" );
	sl_assert( !strcmp(val,"e"), "slab did not return value" );

	// over write origonal
	slab_dict_set( d, "key", "new value" );
	val = slab_dict_get( d, "key", 0 );

	sl_assert( val, "slab did not return value" );
	sl_assert( !strcmp(val,"new value"), "slab did not return correct value" );

	slab_return;
}


SLAB_TEST_METHOD( dict_update )
{
	char* val;
	Dict d1, d2;

	d1 = slab_dict_create( );
	d2 = slab_dict_create( );

	slab_dict_set( d1, "key1", "value" );
	slab_dict_set( d2, "key2", "value" );

	slab_dict_update( d1, d2 );

	val = slab_dict_get( d1, "key1", 0 );
	sl_assert( val, "slab dict did not return correct value" );

	val = slab_dict_get( d1, "key2", 0 );
	sl_assert( val, "slab dict did not return correct value" );

//	val = slab_dict_get( d2, "key1", 0 );
//	sl_assertfalse( val, "slab dict did not return correct value" );

// ! dont understand error
//  python(611) malloc: *** error for object 0x1848200: incorrect checksum for freed object
	// - object was probably modified after being freed, break at szone_error to debug
//	python(611) malloc: *** set a breakpoint in szone_error to debug

	slab_return;
}
