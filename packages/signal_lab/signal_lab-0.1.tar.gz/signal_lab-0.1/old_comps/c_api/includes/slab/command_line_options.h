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

#ifndef __SLAB_COMMAND_LINE_OPTS__
#define __SLAB_COMMAND_LINE_OPTS__

#ifndef _SLAB_QUOTEME
#define _SLAB_QUOTEME(x) #x
#define SLAB_QUOTEME(x) _SLAB_QUOTEME(x)
#endif // _SLAB_QUOTEME

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */


//! This is the maximum string length for options
#define OPT_STRING_LEN 1024

//! Structure to hold command line options options
struct OptionStruct
{
	//! name of the option
	char name[OPT_STRING_LEN];

	//! long command line name (i.e. '--datapath' )
	char longname[OPT_STRING_LEN];

	//! short command line name (i.e. '-p' )
	char shortname[OPT_STRING_LEN];

	//! default value if option not present on the command line
	char default_value[OPT_STRING_LEN];

	//! depricated options are stored in an SLEnviron struct
	char value[OPT_STRING_LEN];

	//! value given in option is seen, but no value is given
	char seen_value[OPT_STRING_LEN];

	//! help for '-h' print-out
	char help[OPT_STRING_LEN];
};


typedef struct OptionStruct* Option;

//! create a new option with only a name
Option CreateOption( char* name );

//! create a new option with all values
Option slab_option_create( char* name ,
		char* longname ,
		char* shortname ,
		char* default_value,
		char* seen_value,
		char* help
);

//! forward linked list of option types
struct OptionsListStruct
{
	//! current option
	Option opt;
	//! next in the lest
	struct OptionsListStruct* next;
};

typedef struct OptionsListStruct* OptionsList;

//! default slab options
extern struct OptionsListStruct DefaultOptions;

//! check if a given string is an option in the options list
//! @param arg string to test
//  @param lopt is a list of valid options
//  @return the coresponding option from lopt or NULL
Option slab_option_is_opt( OptionsList lopt, char* arg );

//! check if string \e arg is of the form 'x=y'
int slab_option_is_kw( char* arg);

//! append an option to the end of an options list
void slab_option_append( OptionsList olist, Option opt);

//static int SLAB_HAVE_DEFAULT_OPTIONS;

//! add default options to the static options list
void slab_default_options( void );

#ifdef __cplusplus
}
#endif /* __cplusplus */


#endif // __SLAB_COMMAND_LINE_OPTS__

