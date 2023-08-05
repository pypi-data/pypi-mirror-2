
PyObject* WRAP_MAP_NAME(SIGFUNC)( PyObject* self, PyObject* args )
{

	printf("into %s \n", PY_MAP_NAME(SIGFUNC)  );
	PyObject *penv,*pinputs;

	if (!PyArg_ParseTuple( args, "OO" , &penv, &pinputs ) )
        return NULL;

	Py_INCREF(pinputs);
	Py_INCREF(penv);

	int nbinputs = PySequence_Length( pinputs );
	int nboutputs;

	sl_file* inputs  = _sl_to_files( pinputs );
	PyObject* _sl_from_files( sl_file* files, int nb_files );


	sl_environ env = _sl_to_env( penv );

	sl_file* outputs = MAP_NAME(SIGFUNC)( env , inputs, nbinputs,&nboutputs );


	if(!outputs)
	{
		printf("error outputs %s \n", PY_MAP_NAME(SIGFUNC)  );
		return NULL;
	}

	PyObject* poutputs = _sl_from_files( outputs , nboutputs );

	if(!poutputs) return NULL;

	Py_DECREF(pinputs);
	Py_DECREF(penv);

	return poutputs;
}

PyObject* WRAP_NAME(SIGFUNC)( PyObject* self, PyObject* args )
{

	PyObject *penv,*pinputs,*poutputs;
	if (!PyArg_ParseTuple( args, "OOO" , &penv, &pinputs, &poutputs ) )
        return NULL;

	sl_environ env = _sl_to_env(penv);

	int nbinputs = PySequence_Length( pinputs );

	if ( PyErr_Occurred() ) return NULL;

	int nboutputs = PySequence_Length( poutputs );

	if ( PyErr_Occurred() ) return NULL;

	sl_file* inputs = _sl_to_files(pinputs);
	sl_file* outputs = _sl_to_files(poutputs);

//	sl_file* inputs = malloc( sizeof(sl_file) * nbinputs );
//	sl_file* outputs = malloc( sizeof(sl_file) * nboutputs );
//
//
//	int i;
//	sl_file file;
//	PyObject* pfile;
//	for (i=0;i<nbinputs;i++)
//	{
//		pfile = PySequence_GetItem( pinputs, i );
//		if ( !pfile ) return NULL;
//
//		file = _sl_to_file( pfile );
//		if (!file) return NULL;
//
//		inputs[i]=file;
//	}
//
//
//	for (i=0;i<nboutputs;i++)
//	{
//		pfile = PySequence_GetItem( poutputs, i );
//		if ( !pfile ) return NULL;
//
//		file = _sl_to_file( pfile );
//		if (!file) return NULL;
//
//		outputs[i]=file;
//	}

	int err = SIGFUNC( env, inputs, nbinputs, outputs , nboutputs );

	if (err)
	{
		if ( sl_get_error() )
		{
			PyErr_SetString( PyExc_Exception, sl_get_error() );
			sl_clear_error();
		}

		return NULL;
	}
	else
		Py_RETURN_NONE;

}

