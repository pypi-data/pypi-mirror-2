
#ifndef __SLAB_RSF_ALT_API__
#define __SLAB_RSF_ALT_API__

#include <signal_lab.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>
#include <float.h>
#include <unistd.h>
#include <string.h>

#define sf_file sl_file
#define SF_MAX_DIM 9
void sf_init( int argc, char** argv );

sl_environ get_global_env( void );
sl_file get_first_file( void );

sf_file sf_input( char* tag );
sf_file sf_output( char* tag );

#define sf_error( MSG ) sl_error( MSG )

enum SF_FILETYPE { SF_FLOAT, SF_COMPLEX, SF_INT};


typedef enum SF_FILETYPE sf_datatype;

typedef struct {
	const char* name;
	enum SF_FILETYPE sftype;
	} sf_typedict;

const char* _sf_type_to_string( enum SF_FILETYPE type );
enum SF_FILETYPE _sf_string_to_type( char*  type );

enum SF_FILETYPE sf_gettype( sf_file file );

#define sf_settype( SLFILE, SFTYPE ) sl_settype( SLFILE, _sf_type_to_string(SFTYPE) )

#define sf_histint( SLFILE, KEY, VALUE ) SL_SAFECALL(sl_histint( SLFILE, KEY, VALUE ))
#define sf_leftsize( SLFILE, LEFT ) sl_leftsize( SLFILE, LEFT )

#define sf_getint( KEY, PTR ) SL_SAFECALL(  sl_getint( get_global_env() , KEY, PTR, 0 ))
#define sf_getbool( KEY, PTR ) SL_SAFECALL(  sl_getbool( get_global_env() , KEY, PTR, 0 ))
#define sf_getfloat( KEY, PTR ) SL_SAFECALL( sl_getfloat( get_global_env() , KEY, PTR, 0 ))
#define sf_getstring( KEY ) SL_SAFECALLPTR( char*, sl_getstring( get_global_env() , KEY,  0 ))


#define sf_close(  ) sl_close( get_first_file() )

#define sf_tempfile(  ARG1, ARG2 ) tmpfile(  )


//! TYPES
typedef float complex sf_complex;
typedef unsigned long int sf_ulargeint;
typedef unsigned short int bool;

#define false 0
#define true 1

#define sf_alloc( N ,SIZE) malloc( N* SIZE)
#define sf_floatalloc( SIZE ) ((float*) malloc(sizeof(float)* SIZE))
#define sf_complexalloc( SIZE ) ((sf_complex*) malloc(sizeof(sf_complex)* SIZE))
#define sf_warning( MSG ) fprintf( stderr, MSG );


int sf_floatread( float* data, int size, sf_file file );
int sf_floatwrite( float* data, int size, sf_file file );

int sf_complexread( sf_complex* data, int size, sf_file file );
int sf_complexwrite( sf_complex* data, int size, sf_file file );

#define sf_filesize( SLFILE ) sl_leftsize( SLFILE, 0 )

int sf_memsize( void);


//! complex stuff

#define sf_cdiv( CPX1, CPX2 ) ( CPX1 / CPX2 )
#define sf_csub( CPX1, CPX2 ) ( CPX1 - CPX2 )
#define sf_crmul( CPX, RE ) ( CPX * RE )
#define sf_cmul( CPX1, CPX2 ) ( CPX1 * CPX2 )
#define sf_cmplx( REAL, IMAG ) (REAL+ IMAG*I)

#endif // __SLAB_RSF_ALT_API__


