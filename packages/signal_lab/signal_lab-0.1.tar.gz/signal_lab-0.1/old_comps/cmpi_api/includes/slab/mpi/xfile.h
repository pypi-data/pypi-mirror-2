

#ifndef _C_SLAB_MPI_XFILE_H__
#define _C_SLAB_MPI_XFILE_H__


#include<mpi.h>
#include<slab/file.h>

//! meta header file struct
typedef struct {
	
	SLFile meta;
	int rank_owner;
	scew_tree* tree;
	
	SLFile local;
	
} xsl_file;


xsl_file*
xslab_file_input( MPI_Comm comm, char*name, int rank, SLEnviron env );

void
slab_mpi_file_bcast( MPI_Comm comm, int from, SLFile* file );


#endif // _C_SLAB_MPI_XFILE_H__

