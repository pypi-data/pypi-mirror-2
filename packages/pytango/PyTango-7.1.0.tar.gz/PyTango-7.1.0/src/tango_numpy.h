
#pragma once

#ifndef DISABLE_PYTANGO_NUMPY

#include <Python.h>

// See "Importing the API" for the why of these weird defines before
// the inclusion of numpy. They are needed so that you can do import_array
// in just one file while using numpy in all the project files.
// http://docs.scipy.org/doc/numpy/reference/c-api.array.html#miscellaneous
// - {
#      define PY_ARRAY_UNIQUE_SYMBOL pytango_ARRAY_API
#      define NO_IMPORT_ARRAY
#      include <numpy/arrayobject.h>
// - }

#include <tango.h>


template<int N>
struct tango_name2numpy
{
    enum { };
};

#define DEF_TANGO2NUMPY(tangoid, numpyid) \
    template<> \
    struct tango_name2numpy<tangoid> \
    { \
        enum {value = numpyid}; \
    }

#define TANGO_const2numpy(tangoid) tango_name2numpy<tangoid>::value


DEF_TANGO2NUMPY(Tango::DEV_STATE, NPY_UINT32 );
DEF_TANGO2NUMPY(Tango::DEV_SHORT, NPY_INT16 );
DEF_TANGO2NUMPY(Tango::DEV_LONG, NPY_INT32 );
DEF_TANGO2NUMPY(Tango::DEV_DOUBLE, NPY_FLOAT64 );
DEF_TANGO2NUMPY(Tango::DEV_FLOAT, NPY_FLOAT32 );
DEF_TANGO2NUMPY(Tango::DEV_BOOLEAN, NPY_BOOL );
DEF_TANGO2NUMPY(Tango::DEV_USHORT, NPY_UINT16 );
DEF_TANGO2NUMPY(Tango::DEV_ULONG, NPY_UINT32 );
// Unassigned Tango::DEV_STRING, mapping to NPY_STRING is not copy-free
DEF_TANGO2NUMPY(Tango::DEV_UCHAR, NPY_UBYTE );
// DEF_TANGO2NUMPY(Tango::DEV_CHAR, NPY_BYTE );
//Unassigned: Tango::DEV_ENCODED
DEF_TANGO2NUMPY(Tango::DEV_LONG64, NPY_INT64 );
DEF_TANGO2NUMPY(Tango::DEV_ULONG64, NPY_UINT64 );

#endif // #ifndef DISABLE_PYTANGO_NUMPY
