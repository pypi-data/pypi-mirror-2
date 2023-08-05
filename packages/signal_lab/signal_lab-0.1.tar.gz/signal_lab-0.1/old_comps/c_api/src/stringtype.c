
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include <slab/error.h>
#include <slab/stringtype.h>

// convert string to int
extern
int slab_int( const char* arg )
{
	char* end;
	int i = (int) strtol(arg,&end,10);
	return i;
}

// convert string to long
extern
long int slab_long( const char* arg )
{
	char* end;
	long int i =  strtol(arg,&end,10);
	return i;
}

// convert string to unsigned long
extern
unsigned long int slab_ulong( const char* arg )
{
	char* end;
	unsigned long int i = (unsigned long int) strtoul(arg,&end,10);
	return i;
}

// convert string to unsigned long
extern
ulli slab_ulli( const char* arg )
{
	char* end;
	ulli i = (ulli) strtoull(arg,&end,10);
	return i;
}


// convert string to float
extern
float slab_float( const char* arg )
{
	char* end;
	float f = strtof( arg,&end);
	return f;
}

// convert string to double
extern
double slab_double( const char* arg )
{
	char* end;
	double d = strtod( arg,&end);
	return d;
}


// convert int to string
extern
char* slab_str_int(const int arg )
{
	char *r = malloc(100);
	sprintf(r,"%i",arg);
	return r;
}


// convert long to string
extern
char* slab_str_long( const long arg )
{
	char *r = malloc(100);
	sprintf(r,"%li",arg);
	return r;
}


// convert unsigned long to string
extern
char* slab_str_ulong(const  unsigned long arg )
{
	char *r = malloc(100);
	sprintf(r,"%lu",arg);
	return r;
}

// convert unsigned long long to string
extern
char* slab_str_ulli( const ulli arg )
{
	char *r = malloc(100);
	sprintf(r,"%llu",arg);
	return r;
}

// convert float to string
extern
char* slab_str_float( const float arg )
{
	char *r = malloc(100);
	sprintf(r,"%f",arg);
	return r;
}


// convert double to string
extern
char* slab_str_double( const double arg )
{
	char *r = malloc(100);
	sprintf(r,"%lf",arg);
	return r;
}



extern
int slab_type( char* typename, char* value, void* dest)
{
	return 0;
}

extern
int
type_convert( char* name, char* typename, char* strvalue, void* value, void* def )
{
	if ( !strcmp(typename,"int"))
	{
		if (strvalue)
		{
		 *(int*)value = (int) strtol( strvalue, 0 , 10);
		 return 1;
		}
		else if (def)
		{
			*(int*)value = *(int*) def;
			return 1;
		}
		else
		{
			char r[100]; sprintf(r, "need parameter '%s=' on the comman line" , name );
			slab_error(-2, "type_convert", r );
			return 0;
		}
	}
	else if ( !strcmp(typename,"float"))
	{
		if (strvalue)
		{
		 *(float*)value = (float) strtod( strvalue, 0 );
		 return 1;
		}
		else if (def)
		{
			*(float*)value = *(float*) def;
			return 1;
		}
		else
		{
			char r[100]; sprintf(r, "need parameter '%s=' on the comman line" , name );
			slab_error(-2, "type_convert", r );
			return 0;
		}
	}
	else if ( !strcmp(typename,"double"))
	{
		if (strvalue)
		{
		 *(double*)value = (double) strtod( strvalue, 0 );
		 return 1;
		}
		else if (def)
		{
			*(double*)value = *(double*) def;
			return 1;
		}
		else
		{
			char r[100]; sprintf(r, "need parameter '%s=' on the comman line" , name );
			slab_error(-2, "type_convert", r );
			return 0;
		}
	}
	else if ( !strcmp(typename,"string"))
	{
		if (strvalue)
		{
		 *(char**)value = strvalue;
		 return 1;
		}
		else if (def)
		{
			*(char**)value = *(char**) def;
			return 1;
		}
		else
		{
			char r[100]; sprintf(r, "need parameter '%s=' on the comman line" , name );
			slab_error(-2, "type_convert", r );
			return 0;
		}
	}
	else
	{
		char r[100]; sprintf(r, "no such type %s" , typename );
		slab_error(-2, "type_convert", r );
		return 0;
	}

}

