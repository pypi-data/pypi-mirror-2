
#include <stdio.h>
#include <stdlib.h>

#include <signal_lab.h>


int main( int argc, char** argv )
{

	sl_environ env = sl_init(argc,argv);

	sl_file input = sl_input( "f.rsf", env );

	unsigned long int n1;
	n1 =sl_leftsize( input, 0 );

	printf( "total file size is '%i' \n" , (int) n1 );

	float* data = (float*) malloc( sizeof(float) * n1 );


	SL_FREAD( input, data, n1 );

	int i;
	for ( i=0;i<n1;i++)
	{
		printf( "'%f' \n" , data [i] );
	}

	sl_exit( );
	return 1;
}
