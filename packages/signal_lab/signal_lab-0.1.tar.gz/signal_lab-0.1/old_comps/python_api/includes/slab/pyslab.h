
#ifndef _PYSLAB_H_
#define _PYSLAB_H_

#include <Python.h>
#include "structmember.h"

#include <slab/environment.h>
#include <slab/file.h>
#include <slab/Dictionary.h>
#include <slab/Iterator.h>
//#include <slab/environment.h>


#ifdef __cplusplus
extern "C" {
#endif

//static
typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
//    PyObject *list;
    PyObject *kw;
    PyObject *options;
    struct SLEnvironment *env;

} SEO;

PyAPI_DATA(PyTypeObject) slab_EnvironmentType;

PyAPI_FUNC(int) PySlabEnv_Check( PyObject* );
PyAPI_FUNC(PyObject*) PySlabEnv_FromEnv( struct SLEnvironment *env );
PyAPI_FUNC(struct SLEnvironment*) PySlabEnv_AsEnv( PyObject* Oenv );

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    struct SLFileStruct *slfile;

	PyObject* header_stream;
	PyObject* binary_stream;
	PyObject* env;

} SLFILE_Object;


//PyAPI_DATA(PyTypeObject) SLFile_Type;
extern PyTypeObject SLFile_Type;






typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    Dict dict;

} PySLDict_Object;

PyAPI_DATA(PyTypeObject) PySLdict_Type;

PyAPI_FUNC(int) PySlabDict_Check( PyObject * Od );

PyAPI_FUNC(PyObject *) PySlabDict_FromDict( Dict d);

PyAPI_FUNC(Dict) PySlabDict_AsDict( PyObject * Od);

//error stuff
PyAPI_FUNC(PyObject*) Py_slab_error_type( int etype );
PyAPI_FUNC(void ) py_set_error_from_slab(void);


typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    sldi iter;

} Py_SLIterator_Object;

PyAPI_DATA(PyTypeObject) Py_SLIterator_Type;

#endif // _PYSLAB_H_
