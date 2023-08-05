

#ifndef _SLAB_XML_META_HEADER_H_
#define _SLAB_XML_META_HEADER_H_

#include <scew/scew.h>
#include <slab/file.h>

scew_tree* scew_tree_copy( scew_tree* );

scew_tree* slab_meta_output( SLFile slfile,  scew_tree* tree );

#endif // _SLAB_XML_META_HEADER_H_
