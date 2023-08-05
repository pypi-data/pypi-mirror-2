
#ifndef _SLAB_XML_SLABIO_H_
#define _SLAB_XML_SLABIO_H_

#include <scew/scew.h>
#include <slab/file.h>

scew_tree* eslab_file_read_xml( SLFile slfile );

int eslab_file_write_xml( SLFile slfile, scew_tree* tree );

scew_tree* esl_file_read_xml( SLFile slfile );

void esl_file_write_xml( SLFile slfile, scew_tree* tree );

#endif // _SLAB_XML_SLABIO_H_
