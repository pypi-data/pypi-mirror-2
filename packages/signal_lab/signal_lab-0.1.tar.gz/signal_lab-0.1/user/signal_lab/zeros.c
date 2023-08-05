
#include <signal_lab.h>

int write_zeros( FILE* binary, size_t size, size_t esize )
{
	fseek( binary , size*esize , SEEK_SET );
}


char zeros_like_doc[] = "This method can create zeros from a header file";

sl_file* zeros_like_map( sl_environ env, sl_file* inputs, int nb_inputs, int *nb_outputs )
{
	if (nb_inputs!=1)
	{
		sl_set_error( "function 'zeros_like' takes one input file" );
		return NULL;
	}

	*nb_outputs=1;
	sl_file* outputs = create_outputs( *nb_outputs );

	if (!outputs) return 0;

	outputs[0] = sl_output( "out", inputs[0], env );

	if (!outputs[0]) return 0;

	return outputs;
}

int zeros_like( sl_environ env, sl_file* inputs, int nb_inputs , sl_file* outputs, int nb_outputs  )
{

	if (nb_outputs!=1)
	{
		sl_set_error( "function 'zeros_like' takes one output argument" );
		return -1;
	}

	sl_file output = outputs[0];

	FILE* bin = sl_get_binary_FILE( output );

	size_t esize = sl_esize( output );

	size_t size = sl_leftsize( output, 0 );

	write_zeros( bin, size, esize );

	return 0;
}
