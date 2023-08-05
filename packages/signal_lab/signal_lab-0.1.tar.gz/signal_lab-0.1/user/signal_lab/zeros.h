

int write_zeros( FILE* binary, size_t size, size_t esize );

extern char zeros_like_doc[];
sl_file* zeros_like_map( sl_environ env, sl_file* inputs, int nb_inputs, int *nb_outputs );
int zeros_like( sl_environ env, sl_file* inputs, int nb_inputs , sl_file* outputs, int nb_outputs  );
