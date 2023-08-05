
/* Clip the data. */

#include <signal_lab.h>

int main(int argc, char* argv[])
{
    int n1, n2, i1, i2;
    float clip, *trace;
    sl_file in, out; /* Input and output files */

    printf("got here\n");
    /* Initialize RSF */
    sl_environ env = sl_init(argc,argv);
    printf("got here\n");
    /* standard input */
    in = sl_input( "in", env );

    /* standard output */
    out = sl_output( "out", in, env);


    /* check that the input is float */
//    if (SF_FLOAT != sf_gettype(in))
//    	sl_error("Need float input");

    /* n1 is the fastest dimension (trace length) */
    SL_SAFECALL( sl_histint( in,"n1",&n1));

    /* leftsize gets n2*n3*n4*... (the number of traces) */
    n2 = sl_leftsize(in,1);
//
    /* parameter from the command line (i.e. clip=1.5 ) */
    SL_SAFECALL( sl_getfloat(env, "clip",&clip, &clip) );

//    if (!sl_getfloat("clip",&clip)) sf_error("Need clip=");
//
    /* allocate floating point array */
//

    sl_finalize( out );

    trace = malloc( sizeof(float)*n1 );

    FILE *inbin, *outbin;

    inbin=sl_get_binary_FILE(in);

    outbin=sl_get_binary_FILE(out);

    /* loop over traces */
    for (i2=0; i2 < n2; i2++) {

		/*read a trace */
		fread(trace,sizeof(float),n1,inbin);

		/* loop over samples */
		for (i1=0; i1 < n1; i1++) {
			if      (trace[i1] >  clip) trace[i1]= clip;
			else if (trace[i1] < -clip) trace[i1]=-clip;
	}

	/* write a trace */
//	sf_floatwrite(trace,n1,out);
	fwrite(trace,sizeof(float),n1,outbin);
    }

    sl_exit( );
    exit(0);
}


