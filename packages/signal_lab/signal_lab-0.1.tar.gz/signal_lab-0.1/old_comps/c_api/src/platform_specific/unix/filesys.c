

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>

#define LSOF_COMMAND "lsof -a +p %i -Fin 2> /dev/null | grep -m1 -A1 %i 2> /dev/null | tail -n +2 2> /dev/null"

/*
 * List of possible platform specific functions / structures
 *
 * fstat		#include <sys/stat.h>
 * popen		#include <unistd.h>
 *
 * struct stat stats;
 * ino_t
 */

//! get file name from file descriptor
/*  @param fd file descriptor
 *  @return new string or 0 on error
 *
 */
char* slab_getfilename( int fd )
{

	int pid= getpid();
	ino_t file_inode;
	struct stat stats;
	fstat( fd, &stats);
	file_inode = stats.st_ino;

//	int err;
	char r[FILENAME_MAX], *filename;
	filename = malloc(FILENAME_MAX);
	size_t path_size;

	sprintf(r, LSOF_COMMAND, pid, (int) file_inode );

	FILE* lsof_prog = popen( r, "r" );

	if (lsof_prog ==0 )
	{
		return 0;
	}

	path_size = fread( filename, 1, 1024, lsof_prog );

	pclose( lsof_prog );

	if (path_size<=0 || path_size== 1024)
		return 0;

	filename++;
	filename[strlen(filename)-2] = 0;

	return filename;

}


