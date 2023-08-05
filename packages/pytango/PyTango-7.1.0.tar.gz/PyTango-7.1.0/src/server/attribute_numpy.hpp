
// This header file is just some template functions moved apart from
// attribute.cpp, and should only be included there.

#pragma once

#include "tango_numpy.h"


namespace PyAttribute {

#   define __fallback(tangoTypeConst) \
        __pyvalue_to_array_sequence<tangoTypeConst>( \
               py_val, pdim_x, pdim_y, fname, isImage, res_dim_x, res_dim_y);    
    
    template<long tangoTypeConst>
    inline typename TANGO_const2type(tangoTypeConst)*
        __pyvalue_to_array_numpy(PyObject* py_val, long* pdim_x, long* pdim_y, const std::string &fname, bool isImage, long& res_dim_x, long& res_dim_y)
    {
        typedef typename TANGO_const2type(tangoTypeConst) TangoScalarType;
        typedef typename TANGO_const2arraytype(tangoTypeConst) TangoArrayType;
        static const int typenum = TANGO_const2numpy(tangoTypeConst);
        
        if (!PyArray_Check(py_val)) {
            return __fallback(tangoTypeConst);
        }

        int nd = PyArray_NDIM(py_val);
        npy_intp* dims = PyArray_DIMS(py_val);
        size_t len = 0;

        // Is the array exactly what we need? I mean: The type we need and with
        // continuous aligned memory?
        const bool exact_array = (
                    PyArray_CHKFLAGS(py_val, NPY_C_CONTIGUOUS | NPY_ALIGNED)
                &&  (PyArray_TYPE(py_val) == typenum) );

        if (isImage) {
            // If dimensions are manually specified (nd must be 1), I don't
            // know how to handle from numpy
            if (nd == 1)
                return __fallback(tangoTypeConst);
            
            // Check: This is an image!
            if (nd != 2)
                Tango::Except::throw_exception(
                    "PyDs_WrongNumpyArrayDimensions",
                    "Expecting a 2 dimensional numpy array (IMAGE attribute).",
                    fname + "()");
            
            // If dimensions are manually limited and it's an image, I just
            // know that if the limit is the real size, then I can safely
            // ignore it, else let the default path take care...
            bool dims_ok = true;
            if (pdim_x)
                dims_ok = dims_ok && (*pdim_x == dims[1]);
            if (pdim_y)
                dims_ok = dims_ok && (*pdim_y == dims[0]);
            if (!dims_ok)
                return __fallback(tangoTypeConst);
            
            len = dims[0]*dims[1];
            res_dim_x = dims[1];
            res_dim_y = dims[0];
        } else {
            // Check: This is an spectrum!
            if (nd != 1)
                Tango::Except::throw_exception(
                    "PyDs_WrongNumpyArrayDimensions",
                    "Expecting a 1 dimensional numpy array (SPECTRUM attribute).",
                    fname + "()");
            
            // If x dimension is limited then I only know how to behave
            // if the array is exact
            if (pdim_x) {
                // if x_dim is bad, instead of throwing an exception I will let
                // __pyvalue_to_array_sequence throw it:
                const bool dims_ok = (*pdim_x <= dims[0]);
                if (!exact_array || !dims_ok)
                    return __fallback(tangoTypeConst);
                len = *pdim_x;
            } else
                len = dims[0];
            res_dim_x = len;
            res_dim_y = 0;
        }

        TangoScalarType *tg_data = new TangoScalarType[len];
        void *vd_data = tg_data;
        
        if (exact_array) {
            // The array is exactly what we need, so a plain memcpy is
            // enough!
            /// @todo If it is read only we need the copy, but if the
            /// attribute is read/write, Tango will do the copy himself on
            /// the calll to set_value(...), so there's no need for us
            /// to make an extra one...
            memcpy(vd_data, PyArray_DATA(py_val), len*sizeof(TangoScalarType));
        } else {
            // We use numpy to create a copy of the array into the continuous
            // memory location that we specify.
            PyObject* py_cont;
            
            py_cont = PyArray_SimpleNewFromData(nd, dims, typenum, vd_data);
            if (!py_cont) {
                delete [] tg_data;
                throw_error_already_set();
            }
            
            if (PyArray_CopyInto(
                    (PyArrayObject*)py_cont,
                    (PyArrayObject*)py_val) < 0)
            {
                Py_DECREF(py_cont);
                delete [] tg_data;
                throw_error_already_set();
            }
            
            Py_DECREF(py_cont);
        }

        return tg_data;
    }

    template<>
    inline TANGO_const2type(Tango::DEV_STRING)*
        __pyvalue_to_array_numpy<Tango::DEV_STRING>(PyObject* py_val, long* pdim_x, long* pdim_y, const std::string &fname, bool isImage, long& res_dim_x, long& res_dim_y)
    {
        return __fallback(Tango::DEV_STRING);
    }

    template<>
    inline TANGO_const2type(Tango::DEV_ENCODED)*
        __pyvalue_to_array_numpy<Tango::DEV_ENCODED>(PyObject* py_val, long* pdim_x, long* pdim_y, const std::string &fname, bool isImage, long& res_dim_x, long& res_dim_y)
    {
        return __fallback(Tango::DEV_ENCODED);
    }
}
