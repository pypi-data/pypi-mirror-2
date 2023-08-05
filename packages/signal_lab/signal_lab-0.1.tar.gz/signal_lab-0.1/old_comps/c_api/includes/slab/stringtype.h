

#ifndef _SLAB_STRING_TYPE_H__
#define _SLAB_STRING_TYPE_H__

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#ifndef ulli
#define ulli unsigned long long int
#endif

// convert string to int
extern
int slab_int( const char* arg );

// convert string to long
extern
long int slab_long( const char* arg );
// convert string to unsigned long
unsigned long int slab_ulong(const  char* arg );

// convert string to float
extern
float slab_float( const char* arg );

// convert string to double
extern
double slab_double( const char* arg );


// convert int to string
extern
char* slab_str_int( const int arg );

// convert long to string
extern
char* slab_str_long( const long int arg );

// convert unsigned long to string
extern
char* slab_str_ulong( const unsigned long arg );

// convert unsigned long to string
extern
char* slab_str_ulli( const ulli arg );

// convert float to string
extern
char* slab_str_float( const float arg );

// convert double to string
extern
char* slab_str_double( const double arg );

//! convert a string to a type
extern
int slab_type( char* name, char* value, void* dest);

extern
int
type_convert( char* name, char* typename, char* strvalue, void* value, void* def );


#ifdef __cplusplus
} // end extern "C"
#endif /* __cplusplus */

#endif // _SLAB_STRING_TYPE_H__

