

#include <Python.h>

//static inline void
static void
byteswap2( void* buffer, int count )
{
    char* buffer_tmp= (char*)buffer;
    char tmp0;
    char tmp1;
    int i;
    for ( i=0; i< count; i++ )
    {
        tmp0 = buffer_tmp[0];
        tmp1 = buffer_tmp[1];

        buffer_tmp[0] = tmp1;
        buffer_tmp[1] = tmp0;

        buffer_tmp+=2;
    }
}

//static inline void
static void
byteswap4( void* buffer, int count )
{
    char* buffer_tmp= (char*)buffer;
    char tmp0;
    char tmp1;
    char tmp2;
    char tmp3;
    int i;
    for ( i=0; i< count; i++ )
    {
        tmp0 = buffer_tmp[0];
        tmp1 = buffer_tmp[1];
        tmp2 = buffer_tmp[2];
        tmp3 = buffer_tmp[3];

        buffer_tmp[0] = tmp3;
        buffer_tmp[1] = tmp2;
        buffer_tmp[2] = tmp1;
        buffer_tmp[3] = tmp0;

        buffer_tmp+=4;
    }
}

//static inline void
static void
byteswap8( void* buffer, int count )
{
    char* buffer_tmp=(char*)buffer;
    char tmp0;
    char tmp1;
    char tmp2;
    char tmp3;
    int i;
    for ( i=0; i< count; i++ )
    {
        tmp0 = buffer_tmp[0];
        tmp1 = buffer_tmp[1];
        tmp2 = buffer_tmp[2];
        tmp3 = buffer_tmp[3];

        buffer_tmp[0] = buffer_tmp[7];
        buffer_tmp[1] = buffer_tmp[6];
        buffer_tmp[2] = buffer_tmp[5];
        buffer_tmp[3] = buffer_tmp[4];

        buffer_tmp[4] = tmp3;
        buffer_tmp[5] = tmp2;
        buffer_tmp[6] = tmp1;
        buffer_tmp[7] = tmp0;

        buffer_tmp+=8;
    }
}

static inline void
byteswap16( void* buffer, int count )
{
    char* buffer_tmp=(char*)buffer;
    char tmp0;
    int i;
    for ( i=0; i< count; i++ )
    {
        tmp0 = buffer_tmp[0];
        buffer_tmp[0] = buffer_tmp[15];
        buffer_tmp[15] = tmp0;

        tmp0 = buffer_tmp[1];
        buffer_tmp[1] = buffer_tmp[14];
        buffer_tmp[14] = tmp0;

        tmp0 = buffer_tmp[2];
        buffer_tmp[2] = buffer_tmp[13];
        buffer_tmp[13] = tmp0;

        tmp0 = buffer_tmp[3];
        buffer_tmp[3] = buffer_tmp[12];
        buffer_tmp[12] = tmp0;

        tmp0 = buffer_tmp[4];
        buffer_tmp[4] = buffer_tmp[11];
        buffer_tmp[11] = tmp0;

        tmp0 = buffer_tmp[5];
        buffer_tmp[5] = buffer_tmp[10];
        buffer_tmp[10] = tmp0;

        tmp0 = buffer_tmp[6];
        buffer_tmp[6] = buffer_tmp[9];
        buffer_tmp[9] = tmp0;

        tmp0 = buffer_tmp[7];
        buffer_tmp[7] = buffer_tmp[8];
        buffer_tmp[8] = tmp0;


        buffer_tmp+=8;
    }
}

static PyObject*
PySLAB_read( PyObject* __self, PyObject* args, PyObject *keywds )
{

    PyObject* self = NULL;
    PyObject* pybuffer = NULL;
    unsigned int byteswap = 0;
    int count = -1;
    void* buffer;
    Py_ssize_t buffer_len;
    unsigned int nread= 0;
    unsigned int esize= 1;


    static char *kwlist[] = { "self", "buffer", "count", "esize","byteswap",  NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "O|OiII", kwlist,
                                     &self, &pybuffer, &count, &esize, &byteswap) )
        return NULL;


    if ( pybuffer == NULL || pybuffer==Py_None )
    {
        if ( count <= 0 )
        {
            PyErr_SetString( PyExc_ValueError, "either 'buffer' or 'count' arguments must be set" );
            return NULL;
        }
        else
        {
            pybuffer = PyBuffer_New( count*esize );
        }

    }
    else
    {
        Py_INCREF( pybuffer );
    }

    if (PyObject_AsWriteBuffer(pybuffer,&buffer,&buffer_len) == -1)
    {
        Py_DECREF( pybuffer );
        return 0;
    }

    if (count <= 0 )
    {
        count = buffer_len/esize;
    }
    else if (count > buffer_len/esize )
    {
        Py_DECREF( pybuffer );
        PyErr_SetString( PyExc_ValueError, "argument 'count' may not be larger than the buffer size" );
        return NULL;
    }

    FILE* stream = PyFile_AsFile( self );

    if (stream ==NULL )
    {
        Py_DECREF( pybuffer );
        PyErr_SetString( PyExc_ValueError, "first argument must be a file instance" );

        return NULL;
    }

    nread = fread( buffer, esize, count, stream );

    if ( nread != count )
    {

        Py_DECREF( pybuffer );
        PyErr_Format( PyExc_IOError, "count not read %i elements from file '%s' ( nread %i, esize=%i )" ,count, PyString_AsString(PyFile_Name(self)) , nread, esize );
        return NULL;
    }

    if (byteswap)
    {
        switch (esize)
        {

        case 1:
            break;
        case 2:
            byteswap2( buffer, count );
            break;
        case 4:
            byteswap4( buffer, count );
            break;
        case 8:
            byteswap8( buffer, count );
            break;

        default:
            PyErr_Format( PyExc_ValueError, "count not byteswap array with esize %i", esize );
            return NULL;
        };
    }

    //int PyObject_AsWriteBuffer(PyObject *obj, void **buffer, Py ssize t *buffer len)

    return pybuffer;
}

static PyObject*
PyIs_Big_Endian( PyObject* self )
{
    union { long l; char c[sizeof (long)]; } u;
    u.l = 1;

    int is_big_e = u.c[sizeof (long) - 1] == 1;

    if (is_big_e)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;

}

static PyMethodDef slab_methods[] = {

    {"read",  (PyCFunction)PySLAB_read, METH_VARARGS|METH_KEYWORDS,
     "read( buffer=None, count=-1, byteswap=False ) -> buffer"},
    {"is_big_endian",  (PyCFunction)PyIs_Big_Endian, METH_NOARGS,
     "is_big_endian( ) -> bool"},

     {NULL,  NULL}  /* Sentinel */
};



#ifndef PyMODINIT_FUNC  /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
initc_signal_lab(void)
{
//    import_array( );

    PyObject* m;

    m = Py_InitModule3("c_signal_lab", slab_methods,
                       "c_signal_lab");
}
