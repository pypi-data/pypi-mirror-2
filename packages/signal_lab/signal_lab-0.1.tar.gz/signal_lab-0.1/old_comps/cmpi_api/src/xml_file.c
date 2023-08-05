
#include <stdlib.h>

#include <scew/scew.h>

#include <slab/file.h>
#include <slab/error.h>
#include <slab/SLIO.h>

#include <slab/mpi/xfile.h>


int slab_mpi_file_init( xsl_file* xfile )
{
	xfile->meta=0;
	xfile->rank_owner=0;
	xfile->tree=0;
	xfile->local=0;
	
	return 1; 

}
slab_mpi_file_allocate( )
{
	xsl_file* xfile = malloc( sizeof(xsl_file) );
	return xfile ;
}

slab_mpi_file_create(  )
{
	xsl_file* xfile = slab_mpi_file_allocate();
	slab_mpi_file_init(xfile);
	return xfile;

}

xsl_file*
xslab_file_input( MPI_Comm comm, char*name, int root, SLEnviron env )
{
	
	int rank;
	int err = MPI_Comm_rank( comm,  &rank );
	
	unsigned long int rd,len;

	xsl_file* xfile = slab_mpi_file_create(  );
	char* xml_str;
	long xml_len;
	scew_tree* tree;
	scew_element* element;
	

	if (rank==root)
	{
		if (!slfile->is_input)
		{
			slab_error( SLAB_XML_ERROR, "eslab_file_read_xml"," file is not input" );
			return 0;
		}
		
		
		char* xl = slab_file_get( slfile, "xml" );
		if (!xl)
		{
			push_error( "eslab_file_read_xml" );
			return 0;
		}
		xml_len = slab_long( xl );
		
		xml_str = malloc(xml_len); 
		
		ulli actual_len = slab_read( slfile, xml_str, xml_len );
	    if ( actual_len != xml_len )
	    {
	    	slab_error( SLAB_XML_ERROR, "eslab_file_read_xml","TODO: wirte errmsg" );
	    	return 0;
	    }
		
	    fclose( xfile->meta->header_stream );
		fclose( xfile->meta->binary_stream );
		
	}
	
	MPI_Bcast( &xml_len, 1, MPI_INT, root, comm );
	
	if (root!=rank)
		xml_str = malloc(xml_len);
	
	MPI_Bcast( xml_str, xml_len,  MPI_CHAR , root, comm );
	
	
	scew_parser * parser = scew_parser_create( );
	
	if (!scew_parser_load_buffer( parser, xml_str, xml_len ) )
	{
		scew_parser_free(parser);
		return 0;
	}
	
	
	xfile->tree = scew_parser_tree(parser);
	
	scew_parser_free(parser);
	
	element = scew_tree_root(tree);
	char* ename = (char*) scew_element_name(element);
	if (strcmp(ename,"RSF"))
	{
		char r[100]; sprintf(r,"root element of xml tree needs to be 'RSF', got '%s' ", ename ); 
		slab_error( SLAB_XML_ERROR, "eslab_file_read_xml", r);
		return 0;
	}

	return xfile;
	
}


