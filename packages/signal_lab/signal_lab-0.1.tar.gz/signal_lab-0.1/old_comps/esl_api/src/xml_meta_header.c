
#include <stdio.h>

#include <slab/header_utils.h>
#include <slab/xml/meta_header.h>
//#include <slab/xml/xml_sub_header.h>


scew_tree* scew_tree_copy( scew_tree* tree )
{
	scew_tree* new;
	FILE* tmp = tmpfile( );
	scew_writer_tree_fp( tree, tmp );
	fseek( tmp , 0 , SEEK_SET );
	
	scew_parser* parser = scew_parser_create( );
	
	scew_parser_load_file_fp( parser, tmp );
	fclose( tmp );
	
	new = scew_parser_tree( parser );
	
	scew_parser_free( parser );
	
	return new;
}

//scew_tree* slab_meta_output( SLFile slfile,  scew_tree* tree )
//{
//	scew_tree* new = scew_tree_copy(tree);
//	
//	int size = (int) slab_file_size( slfile );
//	int i;
//	char* filename;
//	
//	SLEnviron env = slfile->env;
//	char* datapath = slab_env_get_opt( env , datapath );
//	for (i=0; i< size; i++ )
//	{
//		
//		sprintf( filename, "%datapath/s.rsf" , datapath );
//		eslab_sub_header_set_filename( tree, i, filename );
//	}
//	return new;
//}
//
