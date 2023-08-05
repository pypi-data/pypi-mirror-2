
#ifndef __ALT_SIGNAL_LAB_H__
#define __ALT_SIGNAL_LAB_H__



#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>



struct _sl_environ;
typedef struct _sl_environ* sl_environ;

struct _sl_file;
typedef struct _sl_file* sl_file;


int _sl_safecall( int err );
void* _sl_safecallptr( void* err );

#define SL_SAFECALL( EXPR ) _sl_safecall( (int) EXPR )
#define SL_SAFECALLPTR( PTRTYPE, EXPR ) (PTRTYPE) _sl_safecallptr( (void*) EXPR )

sl_environ sl_init( int argc , char** argv );

sl_environ sl_environ_init( int argc , char** argv );

sl_file sl_input( char* tag, sl_environ env );

sl_file sl_output( char* tag, sl_file input, sl_environ env );

sl_file* create_outputs( int nb_outputs );

//#history functions
int sl_histint( sl_file file, char* item, int* value );
int sl_setint( sl_file file, char* item, const int value );
int sl_settype( sl_file file, const char* value );

void sl_finalize( sl_file file );
size_t sl_esize( sl_file file );


char* sl_filetype( sl_file file );

#define SL_ISFLOAT( TYPE ) (strcmp((TYPE),"float" )==0)
#define SL_ISCOMPLEX( TYPE ) (strcmp((TYPE),"complex" )==0)

char* sf_filetype( sl_file file );

unsigned long int sl_leftsize( sl_file file , int left );

FILE* sl_get_binary_FILE( sl_file file );


int _sl_is_finalized( sl_file file );
int sl_is_finalized( sl_file file );


void sl_close( sl_file file );

#define SL_FREAD( file , data, size ) fread(  (void*)(data) , 1 , (size), sl_get_binary_FILE( (file) ) );
#define SL_FWRITE( file , data, size ) fwrite(  (void*)(data) , 1 , (size), sl_get_binary_FILE( (file) ) );


// command line functions
int sl_getfloat( sl_environ env, char* item , float* value,float* _default );
int sl_getint( sl_environ env, char* item , int* value, int* _default );
int sl_getbool( sl_environ env, char* item , unsigned short int* value, unsigned short int* _default );
char* sl_getstring( sl_environ env, char* item , char* _default );


void sl_error( char * msg );


void sl_set_error( char * msg );
char* sl_get_error( void );
void sl_clear_error( void );

void sl_exit( void );

#endif // __ALT_SIGNAL_LAB_H__
