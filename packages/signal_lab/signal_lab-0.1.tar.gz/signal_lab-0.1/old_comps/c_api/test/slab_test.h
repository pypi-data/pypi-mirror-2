
#ifndef _SLAB_TEST_H_
#define _SLAB_TEST_H_

#include <string.h>
#include <Python.h>

#define SLAB_TEST_METHOD( METH ) PyObject* sltest_##METH( void )
#define PYSLAB_TEST_METHOD( METH )   { #METH, (PyCFunction) sltest_##METH, METH_NOARGS, #METH },

#define sl_assert(cond, msg ) if ( !(cond) ) {Sl_Assert( msg, __LINE__, __FILE__ );return 0;}
#define sl_assertfalse(cond, msg ) if (cond) {Sl_Assert( msg, __LINE__, __FILE__ );return 0;}

#define slab_return Py_INCREF(Py_None); return Py_None;


void Sl_Assert( char* msg, int line, char* file );

//tests

//dictionary

#define TEST_METHOD(METH) SLAB_TEST_METHOD(METH);
#include "all_test_methods.h"
#undef TEST_METHOD


#endif // _SLAB_TEST_H_
