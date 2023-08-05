
//#include <slab/slabmpi.h>

//#include <slab/mpi/xfile.h>
//#include <scew/scew.h>
//#include <slab/file.h>
//#include <slab/error.h>
//#include <slab/xml/error.h>
//#include <slab/SLIO.h>
//#include <slab/stringtype.h>

#include <slab/xml.h>


int main( int argc, char** argv )
{
	SLEnviron env; 
	SLFile f,ot;
	
	scew_tree* tree;
	char* n1; 
	
	env = slab_env_init(argc,argv);
	f = sl_input( "f.xsf", env );
	ot = sl_output( "q.xsf", f, env );
	
	tree = esl_file_read_xml( f );
	
	n1 = esl_sub_header_get( tree, 0, "n1");
	
	esl_sub_header_set( tree, 0, "n1", "33" );
	
	printf( "n1=%s\n", n1 );
	
	esl_file_write_xml( ot, tree );

	return 0;
}

