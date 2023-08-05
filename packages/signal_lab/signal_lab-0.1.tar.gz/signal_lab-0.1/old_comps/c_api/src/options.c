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

#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include <slab/command_line_options.h>

#define OPTION_STR_LEN 1024

Option CreateOption( char* name )
{

	void* ptr = malloc(sizeof(struct OptionStruct) );

	Option opt = (Option) ptr;

	strcpy (opt->name, name );

//	char* longname;
//	char* shortname;
//	char* default_value;
//	char* value;
//	char* seen_value;


	return opt;

}

Option slab_option_create( char* name ,
		char* longname ,
		char* shortname ,
		char* default_value,
		char* seen_value,
		char* help
)
{
	Option opt = malloc(sizeof(struct OptionStruct) );

	strcpy (opt->name, name );
	strcpy (opt->longname, longname );
	strcpy (opt->shortname, shortname );
	strcpy (opt->default_value, default_value );
	strcpy (opt->seen_value, seen_value );
	strcpy (opt->help, help );
	return opt;

}




int CmpOption( const Option opt, const char* arg )
{
	char *shortname, *longname;
	int nshort, nlong;

	shortname = opt->shortname;
	longname = opt->longname;

	nshort = strlen( opt->shortname );
	nlong  = strlen( opt->longname );

	if ( nshort != 0 && strncmp( shortname, arg, nshort) == 0 )
		return 1;

	if ( nlong != 0 && strncmp( longname, arg, nlong ) == 0 )
	{
		return 1;
	}

	return 0;

}

Option slab_option_is_opt( OptionsList lopt, char* arg )
{
//	printf("IsOption\n");
	OptionsList curr = lopt;

//	char *shortname, *longname;

	while ( curr->opt && curr->next )
	{

		if ( curr->opt != 0 && CmpOption( curr->opt ,arg ) )
		{
//			printf("found option");
			return curr->opt;
		}
		curr = curr->next;
	}

	return 0;

}

int slab_option_is_kw( char* arg)
{
	if ( 0 == strpbrk( arg, "=") )
		return 0;
	else
		return 1;
}

struct OptionsListStruct DefaultOptions =
{
	0,
	0
};

void slab_option_append( OptionsList olist, Option opt)
{
	while ( olist->opt && olist->next)
	{
		olist = olist->next;
	}

	olist->opt = opt;
	olist->next = malloc(sizeof(struct OptionsListStruct) );
	olist->next->opt = 0;
	olist->next->next = 0;
	return;
}

static int SLAB_HAVE_DEFAULT_OPTIONS=0;


static Option datapath = 0;
static Option pack = 0;
static Option accept_tty = 0;
static Option stdinopt = 0;
static Option stdoutopt = 0;
static Option fifo = 0;
static Option buffer_size = 0;
static Option overwrite = 0;
static Option helpopt = 0;

void slab_default_options( void )
{
	OptionsList curr = &DefaultOptions;
	if (!SLAB_HAVE_DEFAULT_OPTIONS)
	{
		SLAB_HAVE_DEFAULT_OPTIONS=1;

		char* dp = getenv( "DATAPATH");

		if (!dp)
			dp=".";

		datapath = slab_option_create( "datapath" ,
				 "--datapath", // long name
				 "",// short name
				 dp, // default value
				 "", // value when seen on the command line
				"path to put binary data to" );


		pack = slab_option_create( "pack",
				 "--pack", // long name
				 "-p",// short name
				 "0", // default value
				 "1", // value when seen on the command line
				 "pack header with binary data"
				 );

		accept_tty = slab_option_create( "accept_tty",
				 "--accept-tty", // long name
				 "",// short name
				 "0", // default value
				 "1", // value when seen on the command line
				 "accept a tty device from stdin/out"
				 );

		stdinopt = slab_option_create( "stdin",
				 "--stdin", // long name
				 "",// short name
				 "stdin", // default value
				 "", // value when seen on the command line
				 "..."
				 );

		stdoutopt = slab_option_create( "stdout",
				 "--stdout", // long name
				 "",// short name
				 "stdout", // default value
				 "", // value when seen on the command line
				 "..."
				 );

		fifo = slab_option_create( "fifo",
				 "--fifo", // long name
				 "-f",// short name
				 "0", // default value
				 "1", // value when seen on the command line
				 "create a fifo device for output"
				 );

		buffer_size = slab_option_create( "buffer_size",
				 "--buffer-size", // long name
				 "-b",// short name
				 SLAB_QUOTEME(BUFSIZ), // default value
				 "", // value when seen on the command line
				 "buffer size"
				 );

		overwrite = slab_option_create( "unique_binary",
				 "--unique-binary", // long name
				 "-u",// short name
				 "0", // default value
				 "1", // value when seen on the command line
				 "if true do not overwrite binary file"
				 );

		helpopt = slab_option_create( "help",
				 "--help", // long name
				 "-h",// short name
				 "0", // default value
				 "1", // value when seen on the command line
				 "print this help message"
				 );

		slab_option_append(curr,datapath);
		slab_option_append(curr,pack);
		slab_option_append(curr,accept_tty);

		slab_option_append(curr,stdinopt);
		slab_option_append(curr,stdoutopt);
		slab_option_append(curr,fifo);
		slab_option_append(curr,buffer_size);
		slab_option_append(curr,overwrite);
		slab_option_append(curr,helpopt);
	}

}

