

#ifndef _SLAB_XML_SUB_HEADER_H_
#define _SLAB_XML_SUB_HEADER_H_

#include <scew/scew.h>
#include <slab/file.h>


scew_tree* eslab_new( void );
void eslab_append_sub_header(  scew_tree* tree , int worldrank );


scew_element* eslab_get_sub_header(  scew_tree* tree , int rank );

char* eslab_sub_header_value( scew_tree* tree , int rank, char* xmltag );
int   eslab_sub_header_set_value( scew_tree* tree , int rank, char* xmltag, char* value );

char* eslab_sub_header_filename( scew_tree* tree , int rank );
int   eslab_sub_header_set_filename( scew_tree* tree , int rank, char*value );

char* eslab_sub_header_nodename( scew_tree* tree , int rank );
int   eslab_sub_header_set_nodename( scew_tree* tree , int rank,char* value );

char* eslab_sub_header_privaterank( scew_tree* tree , int rank );
int   eslab_sub_header_set_privaterank( scew_tree* tree , int rank, char* value );

char* eslab_sub_header_get( scew_tree* tree , int rank, char* xmltag );

int eslab_sub_header_set( scew_tree* tree , int rank, char* xmltag, char* value );

char* esl_sub_header_get( scew_tree* tree , int rank, char* xmltag );

void esl_sub_header_set( scew_tree* tree , int rank, char* xmltag, char* value );

#endif // _SLAB_XML_SUB_HEADER_H_
