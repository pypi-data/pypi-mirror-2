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

#include <signal_lab.h>

#define SLAB_assert( cond ) if ( !(cond) ) { printf("SLAB Assertion error: Condition '%s' is not true.\n\t%s:%d\n", #cond,__FILE__,__LINE__ ); failures++;num_tests++;}


static int failures =0;
static int num_tests=0;
void test_dictionary( )
{

	printf("testing slab pair ... ");

	Pair p = slab_pair_create(  "a", "b" );

	SLAB_assert( strcmp(p->key,"a")==0 );
	printf("testing slab dictionary ... ");
	// test creator


	Dict d = slab_dict_create();

	SLAB_assert( d!=0 );
//	SLAB_assert( DictLen(d)==0 );

	printf("\n" );

}

int main(int argc, char** argv)
{
	printf("============================\n");
	test_dictionary( );


	if (failures!=0)
	{
		printf("============================\n");
		printf("SLAB TESTS FAIL: %d failures, %d tests\n" , failures,num_tests);
	}
	else
	{
		printf("============================\n");
		printf("SLAB TESTS ALL OK\n" );
	}

	return 0;

}
