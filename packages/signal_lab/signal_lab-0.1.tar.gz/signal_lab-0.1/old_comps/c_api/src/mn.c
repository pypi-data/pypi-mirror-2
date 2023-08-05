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

#include <stdio.h>
#include <stdlib.h>

#include <sys/types.h>
#include <sys/stat.h>

#include <string.h>


#include <signal_lab.h>

static float clip=0;
static int par=0;
static int dpar=22;
/*! @page sfclip
 *  this is clip
 */

static kwarglist kwargs[] = {
//      |  NAME  |   TYPE  |   VALUE  |  DEFAULT |   HELP
		{ "clip" ,  "float",  &clip   ,  NULL    ,  "clip data with this parameter"},
//      |        |         |          |          |
		{ "par"  ,  "int"  ,  &par    ,  &dpar   ,  "example parameter with a default value"},

		{0} // END OF LIST
};


static char help[] = "clip data. \n"
		  		     "example usage:     \n"
	                 "sfclip clip=0.5 < input.rsf > output.rsf"
;


int main(int argc, char** argv)
{
	
	SLEnviron env = slab_env_init(argc,argv);

	SLFile dd = slab_file_create(env);
	sl_env_help(env,kwargs,help);

	if (slab_error_occured())
		throw_error_already_set();
	printf( "clipx = %f\n", clip );
	printf( "par = %i\n", par );
//	float clip = slab_env_get_float( env, "clip");

	SLFile in = sl_input( "in" ,env);
	SLFile out = sl_output(  "out", in , env );

//	char* zz = sl_file_get( out,"zz" );
//	printf( "zz = %s", zz );
	sl_file_set( out,"foo","bar");
	sl_file_finalize( out );

	slmi miter = slab_simple_iterator(in,out,0);

	float *elements;
	elements = (float*) miter->iter->buffer;


	unsigned long long int i;
	while( slab_multi_iterator_next(miter) )
	{
		for( i=0; i<miter->iter->buffer_elements; i++)
		{
		    if      (elements[i] >  clip) elements[i]= clip;
		    else if (elements[i] < -clip) elements[i]=-clip;
		}
	}


	slab_multi_iterator_delete(miter);
	slab_file_close( in );
	slab_file_close( out );

	return 0;
}












