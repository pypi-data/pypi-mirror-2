
#ifndef _SLAB_GET_FILE_NAME_H_
#define _SLAB_GET_FILE_NAME_H_

//! get a file name from an open file descriptor
//  @param fd an open valid file descriptor
//  @return string of name of the file on disk
//   or 0 on error.
//   New Refrence.
char * slab_getfilename( int fd );


#endif // _SLAB_GET_FILE_NAME_H_

