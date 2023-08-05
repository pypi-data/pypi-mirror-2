
#include <signal_lab.h>

#include <rsf.h>

static sl_environ __env__=0;

sl_environ get_global_env( void )
{
	return __env__;
}

static sl_file __first_input__=0;

sl_file get_first_file( void )
{
	return __first_input__;
}

void sf_init( int argc, char** argv )
{
	__env__ = sl_init( argc, argv );
}



sf_file sf_input( char* tag )
{


	sl_file file = SL_SAFECALLPTR( sl_file, sl_input( tag, __env__ ) );
	if (!__first_input__)
		__first_input__ = file;
	return file;
}

sf_file sf_output( char* tag )
{
	sl_file file = SL_SAFECALLPTR( sl_file, sl_output( tag, __first_input__, __env__  ));
	return file;
}


static sf_typedict __typedict__[] = { {"int", SF_INT},
		{"float", SF_FLOAT},
		{"complex", SF_COMPLEX},
		{0,0}
};

const char* _sf_type_to_string( enum SF_FILETYPE type )
{
	sf_typedict* td = __typedict__;

	while( td->name != 0 )
	{
		if ( td->sftype ==type )
			return td->name;
	}
	return 0;
}

enum SF_FILETYPE _sf_string_to_type( char*  type )
{
	sf_typedict* td = __typedict__;

	while( td->name != 0)
	{
		if ( strcmp( td->name, type )==0)
			return td->sftype;
	}
	return 0;
}


enum SF_FILETYPE sf_gettype( sf_file file )
{
	char* type = SL_SAFECALLPTR( char*, sl_filetype( file ));
	return _sf_string_to_type( type );
}




int sf_floatread( float* data, int size, sf_file file )
{
	int nb_read = SL_FREAD( file, data, sizeof(float)*size );
	if (nb_read!= size)
		sf_error( "could not read file" );
}
int sf_floatwrite( float* data, int size, sf_file file )
{
	if ( !sl_is_finalized(file) )
	{
		sl_finalize( file );
	}
	int nb_wrote = SL_FWRITE( file, data, sizeof(float)*size );
	if (nb_wrote!= size)
		sf_error( "could not write to file" );

}

int sf_complexread( sf_complex* data, int size, sf_file file )
{
	int nb_read = SL_FREAD( file, data, sizeof(sf_complex)*size );
}
int sf_complexwrite( sf_complex* data, int size, sf_file file )
{
	if ( !sl_is_finalized(file) )
	{
		sl_finalize( file );
	}
	SL_FWRITE( file, data, sizeof(sf_complex)*size );

}


int sf_memsize( void)
{
	int memsize=100;
	SL_SAFECALL(sl_getint( get_global_env() , "memsize", &memsize, &memsize ));
	return memsize;
}

