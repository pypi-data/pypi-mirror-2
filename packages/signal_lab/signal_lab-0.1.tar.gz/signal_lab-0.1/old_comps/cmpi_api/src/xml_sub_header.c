
#include <slab/error.h>

#include <slab/xml/error.h>
#include <slab/xml/sub_header.h>

scew_element* eslab_get_sub_header(  scew_tree* tree , int rank )
{
	scew_element *element=NULL, *sub_header=NULL;
	scew_attribute* comm_world_rank=NULL;
	scew_element** list=NULL;
	char* chr_value=NULL;
	int value;
	unsigned int i,count;
	
	element = scew_tree_root(tree);
	list = scew_element_list( element, "sub_header", &count );
	
	for(i=0;i<count;i++)
	{
		sub_header = list[i];
		comm_world_rank = scew_attribute_by_name( sub_header, "comm_world_rank" );
		chr_value = (char*) scew_attribute_value(comm_world_rank);
		value = slab_int(chr_value);
		if (value == rank)
			break;
	}
	scew_element_list_free(list);
	return sub_header;
}

char* eslab_sub_header_value( scew_tree* tree , int rank, char* xmltag )
{
	scew_element* sub_header, *elem;
	char* contents;
	
	sub_header = eslab_get_sub_header( tree , rank );
	
	if (!sub_header)
		return 0;
		
	elem = scew_element_by_name( sub_header, xmltag );
	if ( !elem )
	{
		char r[100]; sprintf(r,"no element '%s' in xml sub_header of rank '%i'", xmltag, rank ); 
		slab_error( SLAB_XML_ERROR , r );
		return 0;
	}
	
	contents = (char*)scew_element_contents( elem );
	if ( !contents )
	{
		char r[100]; sprintf(r,"element '%s' in xml sub_header of rank '%i' is NULL", xmltag, rank ); 
		slab_error( SLAB_XML_ERROR , r );
		return 0;
	}
	
	return contents;	
}

int eslab_sub_header_set_value( scew_tree* tree , int rank, char* xmltag, char* value )
{
	scew_element* sub_header, *elem;
	char* contents;
	
	sub_header = eslab_get_sub_header( tree , rank );
	
	if (!sub_header)
		return 0;
		
	elem = scew_element_by_name( sub_header, xmltag );
	if ( !elem )
	{
		scew_element* elem = scew_element_add( sub_header, xmltag );
	}
	
	scew_element_set_contents( elem, value );
	
	return 1;
}

char* eslab_sub_header_filename( scew_tree* tree , int rank, char* xmltag )
{
	return eslab_sub_header_value( tree , rank, "filename" );
}
char* eslab_sub_header_nodename( scew_tree* tree , int rank, char* xmltag )
{
	return eslab_sub_header_value( tree , rank, "nodename" );
}

char* eslab_sub_header_privaterank( scew_tree* tree , int rank, char* xmltag )
{
	return eslab_sub_header_value( tree , rank, "comm_private_rank" );
}

char* eslab_sub_header_get( scew_tree* tree , int rank, char* xmltag )
{
	scew_element* sub_header, *simtab, *elem;
	char* contents;
	
	sub_header = eslab_get_sub_header( tree , rank );
	
	if (!sub_header)
		return 0;
	
	simtab = scew_element_by_name( sub_header, "simtab" );
	if (!simtab)
	{
		char r[100]; sprintf(r,"sub_header of rank '%i' has no element 'simtab'",  rank ); 
		slab_error( SLAB_XML_ERROR , r );
		return 0;
	}
	
	elem = scew_element_by_name( simtab, xmltag );
	if ( !elem )
	{
		char r[100]; sprintf(r,"no element '%s' in xml sub_header of rank '%i'", xmltag, rank ); 
		slab_error( SLAB_XML_ERROR , r );
		return 0;
	}
	
	contents = (char*)scew_element_contents( elem );
	if ( !contents )
	{
		char r[100]; sprintf(r,"element '%s' in xml sub_header of rank '%i' is NULL", xmltag, rank ); 
		slab_error( SLAB_XML_ERROR , r );
		return 0;
	}
	
	return contents;
}

int eslab_sub_header_set( scew_tree* tree , int rank, char* xmltag, char* value )
{
	scew_element* sub_header, *simtab, *elem;
	
	
	sub_header = eslab_get_sub_header( tree , rank );
	
	if (!sub_header)
		return 0;
	
	simtab = scew_element_by_name( sub_header, "simtab" );
	if (!simtab)
	{
		char r[100]; sprintf(r,"sub_header of rank '%i' has no element 'simtab'",  rank ); 
		slab_error( SLAB_XML_ERROR , r );
		return 0;
	}
	
	elem = scew_element_by_name( simtab, xmltag );
	if ( !elem )
			elem = scew_element_add( sub_header, xmltag );
	
	scew_element_set_contents( elem, value );
		
	return 1;

}

char* esl_sub_header_get( scew_tree* tree , int rank, char* xmltag )
{
	char* res = eslab_sub_header_get( tree , rank, xmltag );
	if (!res)
		throw_error_already_set(  );
	return res;
}

void esl_sub_header_set( scew_tree* tree , int rank, char* xmltag, char* value )
{
	if (!eslab_sub_header_set( tree , rank, xmltag , value ))
		throw_error_already_set(  );
}
