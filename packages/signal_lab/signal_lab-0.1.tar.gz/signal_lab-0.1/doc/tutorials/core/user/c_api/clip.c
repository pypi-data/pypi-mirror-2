/*
  Copyright (C) 2008 The University of British Columbia

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

#include <string.h>

#include <signal_lab.h>


// For doxygen manpage

/*! @page sfclip
 @section NAME
        sfclip
 @section DESCRIPTION
        Clip the data. 
 @section SYNOPSIS
        sfclip < in.rsf > out.rsf clip= [par=22]
 @section PARAMETERS
        float   clip=   clip value 
 @section SOURCE
        clip.c
 
 */

static float clip=0;
static int par=0;
static int dpar=22;


// Optional way to get Command line arguments
// used for -h command help
static kwarglist kwargs[] = { 
//      |  NAME  |   TYPE  |   VALUE  |  DEFAULT |   HELP
		{ "clip" ,  "float",  &clip   ,  NULL    ,  "clip data with this parameter"},
//      |        |         |          |          |  
		{ "par"  ,  "int"  ,  &par    ,  &dpar   ,  "example parameter with a default value"},
		
		0 // END OF LIST
}; 

// '-h' command help
static char help[] = "clip data. \n"
		  		     "example usage:     \n"
	                 "sfclip clip=0.5 < input.rsf > output.rsf"
;

int main(int argc, char** argv)
{
	// initialize the environment from command line options
	SLEnviron env = slab_env_init(argc,argv);
	
	// tell slab to get the parameters in kwarglist from the command line
	// aslo will print -h command options
	// this is an alternative to the command
	//	float clip = slab_env_get_float( env, "clip");
	sl_env_help(env,kwargs,help);
	
	// create an input file from stdin
	SLFile in = sl_input( "in" ,env);
	
	// create an output file from stdout
	// passing slfile 'in' tells out to use the history of in 
	SLFile out = sl_output(  "out", in , env );
	
	// set an item on the output header file
	sl_file_set( out,"foo","bar");
	
	// Write the header file and allow binary writes
	sl_finalize( out );
	
	// Create an element wise iterator 
	slmi miter = slab_simple_iterator(in,out,0);	
	
	// Get the buffer allocated by the iterator 
	float *elements;
	elements = (float*) miter->iter->buffer;
	
	
	// loop over read/write bufer sized chunks of data
	unsigned long int i;
	while( slab_multi_iterator_next(miter) )
	{
		// loop over the elements in the buffer
		for( i=0; i<miter->iter->buffer_elements; i++)
		{
			// clip the data
		    if      (elements[i] >  clip) elements[i]= clip;
		    else if (elements[i] < -clip) elements[i]=-clip;
		}
	}
	
	// free the memory in the iterator
	slab_multi_iterator_delete(miter);
	
	// close the files
	slab_file_close( in );
	slab_file_close( out );
	
	return 0;
}












