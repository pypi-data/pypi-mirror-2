
#ifndef _SLAB_PYTHON_XML_XMLFILE_H__
#define _SLAB_PYTHON_XML_XMLFILE_H__

#include <Python.h>
#include "structmember.h"

#include <scew/scew.h>
#include <slab/file.h>



typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    scew_tree* tree;
    
    PyObject* slfile;
    SLFile file;

} PyESLFile_Object;

extern PyTypeObject PyESLFile_Type;

#endif //  _SLAB_PYTHON_XML_XMLFILE_H__


