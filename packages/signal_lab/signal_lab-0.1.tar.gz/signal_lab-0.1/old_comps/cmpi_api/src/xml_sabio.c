
#include <slab/error.h>
#include <slab/SLIO.h>
#include <slab/stringtype.h>

#include <slab/xml/error.h>
#include <slab/xml/slabio.h>


scew_tree* eslab_file_read_xml( SLFile slfile )
{
	if (!slfile->is_input)
	{
		slab_error( SLAB_XML_ERROR, "eslab_file_read_xml: file is not input" );
		return 0;
	}
	
	long xml_len;
	scew_tree* tree;
	scew_element* element;
	
	char* xl = slab_file_get( slfile, "xml" );
	if (!xl)
	{
		push_error();
		return 0;
	}
	xml_len = slab_long( xl );
	
	char* xml_str = malloc(xml_len); 
	
    ulli actual_len = slab_read( slfile, xml_str, xml_len );
    if ( actual_len != xml_len )
    {
    	slab_error( SLAB_XML_ERROR, "TODO: wirte errmsg" );
    	return 0;
    }
		
	
	scew_parser * parser = scew_parser_create( );
	
	if (!scew_parser_load_buffer( parser, xml_str, xml_len ) )
	{
		scew_parser_free(parser);
		return 0;
	}
	
	
	tree = scew_parser_tree(parser);
	
	scew_parser_free(parser);
	
	element = scew_tree_root(tree);
	char* ename = (char*) scew_element_name(element);
	if (strcmp(ename,"RSF"))
	{
		char r[100]; sprintf(r,"root element of xml tree needs to be 'RSF', got '%s' ", ename ); 
		slab_error( SLAB_XML_ERROR, r);
		return 0;
	}
	return tree;
}

int eslab_file_write_xml( SLFile slfile, scew_tree* tree )
{
	if (slfile->is_input)
	{
		slab_error( SLAB_XML_ERROR, "eslab_file_read_xml: file is not output" );
		return 0;
	}
	long int start = ftell( slfile->binary_stream );
	
	FILE* tmp = tmpfile( );
	scew_writer_tree_fp(tree,tmp);
	
	long int stop = ftell( tmp );
	char* r = malloc(stop);
	
	fseek(tmp,0,SEEK_SET);
	fread( r, 1, stop, tmp );
	
	char* s;
	s = slab_str_long( stop );
	slab_file_set( slfile, "xml", s );
	slab_finalize_output( slfile );
	slab_write( slfile, r, stop );
	
	if ( slab_error_occured() )
		return 0;
	
	free(r);
	fclose(tmp);
	
	return 1;
}

scew_tree* esl_file_read_xml( SLFile slfile )
{
	scew_tree* t;
	t = eslab_file_read_xml( slfile );
	
	if (!t)
		throw_error_already_set(  );
	
	return t;
}

void esl_file_write_xml( SLFile slfile, scew_tree* tree )
{
	if (!eslab_file_write_xml( slfile,tree ))
		throw_error_already_set(  );
}
