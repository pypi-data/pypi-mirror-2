#pragma once

#include <boost/python.hpp>
#include <tango.h>

#include "defs.h"
#include "tgutils.h"
#include "pyutils.h"
#include "tango_numpy.h"
#include "exception.h"

extern const char *param_must_be_seq;

/**
 * Converter from python sequence of strings to a std::vector<std::string>
 *
 * @param[in] py_value python sequence object or a single string
 * @param[out] result std string vector to be filled
 */
void convert2array(const boost::python::object &py_value, StdStringVector & result);

/**
 * Converter from python sequence to a Tango CORBA sequence
 *
 * @param[in] py_value python sequence object
 * @param[out] result CORBA sequence to be filled
 */
template<typename TangoElementType>
void convert2array(const boost::python::object &py_value, _CORBA_Sequence<TangoElementType> & result)
{
    size_t size = boost::python::len(py_value);
    result.length(size);
    for (size_t i=0; i < size; ++i) {
        result[i] = boost::python::extract<TangoElementType>(py_value[i]);
    }
}

/**
 * Converter from python sequence of strings to a Tango DevVarStringArray
 *
 * @param[in] py_value python sequence object or a single string
 * @param[out] result Tango string array to be filled
 */
void convert2array(const boost::python::object &py_value, Tango::DevVarStringArray & result);

inline void raise_convert2array_DevVarDoubleStringArray()
{
    Tango::Except::throw_exception(
        "PyDs_WrongPythonDataTypeForDoubleStringArray",
        "Converter from python object to DevVarDoubleStringArray needs a python sequence<sequence<double>, sequence<str>>",
        "convert2array()");
}

/**
 * Converter from python sequence<sequence<double>, sequence<str>> to a Tango DevVarDoubleStringArray
 *
 * @param[in] py_value python sequence object
 * @param[out] result Tango array to be filled
 */
inline void convert2array(const boost::python::object &py_value, Tango::DevVarDoubleStringArray & result)
{
    if (!PySequence_Check(py_value.ptr()))
    {
        raise_convert2array_DevVarDoubleStringArray();
    }
    
    size_t size = boost::python::len(py_value);
    if (size != 2)
    {
        raise_convert2array_DevVarDoubleStringArray();
    }
    
    const boost::python::object
        &py_double = py_value[0],
        &py_str    = py_value[1];

    convert2array(py_double, result.dvalue);
    convert2array(py_str, result.svalue);
}

inline void raise_convert2array_DevVarLongStringArray()
{
    Tango::Except::throw_exception(
        "PyDs_WrongPythonDataTypeForLongStringArray",
        "Converter from python object to DevVarLongStringArray needs a python sequence<sequence<int>, sequence<str>>",
        "convert2array()");
}

/**
 * Converter from python sequence<sequence<int>, sequence<str>> to a Tango DevVarLongStringArray
 *
 * @param[in] py_value python sequence object
 * @param[out] result Tango array to be filled
 */
inline void convert2array(const boost::python::object &py_value, Tango::DevVarLongStringArray & result)
{
    if (!PySequence_Check(py_value.ptr()))
    {
        raise_convert2array_DevVarLongStringArray();
    }
    
    size_t size = boost::python::len(py_value);
    if (size != 2)
    {
        raise_convert2array_DevVarLongStringArray();
    }
    
    const boost::python::object 
        py_long = py_value[0],
        py_str  = py_value[1];

    convert2array(py_long, result.lvalue);
    convert2array(py_str, result.svalue);
}

/**
 * Convert a python sequence into a C++ container
 * The C++ container must have the push_back method
 */
template <typename ContainerType = StdStringVector >
struct from_sequence
{
    static inline void convert(boost::python::object seq, ContainerType& a)
    {
        typedef typename ContainerType::value_type T;
        PyObject *seq_ptr = seq.ptr();
        Py_ssize_t len = PySequence_Length(seq_ptr);
        for(Py_ssize_t i = 0; i < len; ++i)
        {
            PyObject *o_ptr = PySequence_GetItem(seq_ptr, i);
            T s = boost::python::extract<T>(o_ptr);
            a.push_back(s);
            boost::python::decref(o_ptr);
        }
    }

    static inline void convert(boost::python::object seq, Tango::DbData& a)
    {
        PyObject *seq_ptr = seq.ptr();
        Py_ssize_t len = PySequence_Length(seq_ptr);
        for(Py_ssize_t i = 0; i < len; ++i)
        {
            PyObject *o_ptr = PySequence_GetItem(seq_ptr, i);
            a.push_back(Tango::DbDatum(PyString_AsString(o_ptr)));
            boost::python::decref(o_ptr);
        }
    }

    /**
     * Convert a python dictionary to a Tango::DbData. The dictionary keys must
     * be strings representing the DbDatum name. The dictionary value can be
     * be one of the following:
     * - Tango::DbDatum : in this case the key is not used, and the
     *   item inserted in DbData will be a copy of the value
     * - sequence : it is translated into an array of strings and
     *   the DbDatum inserted in DbData will have name as the dict key and value
     *   the sequence of strings
     * - python object : its string representation is used
     *   as a DbDatum to be inserted
     *
     * @param[in] d the python dictionary to be translated
     * @param[out] db_data the array of DbDatum to be filled
     */
    static inline void convert(boost::python::dict d, Tango::DbData& db_data)
    {
        boost::python::object it = d.iteritems();
        int len = boost::python::extract<int>(d.attr("__len__")()) ;
        for(int i = 0 ; i < len; ++i)
        {
            boost::python::tuple pair = (boost::python::tuple)it.attr("next")();
            boost::python::object key = pair[0];
            boost::python::object value = pair[1];
            PyObject *value_ptr = value.ptr();

            boost::python::extract<Tango::DbDatum> ext(value);
            if(ext.check())
            {
                db_data.push_back(ext());
                continue;
            }

            Tango::DbDatum db_datum(PyString_AsString(key.ptr()));
            if((PySequence_Check(value_ptr)) && (!PyString_Check(value_ptr)))
            {
                from_sequence<StdStringVector>::convert(value, db_datum.value_string);
            }
            else
            {
                boost::python::object value_str = value.attr("__str__")();
                db_datum.value_string.push_back(PyString_AsString(value_str.ptr()));
            }
            db_data.push_back(db_datum);
        }
    }
};

/**
 * Translation between python object to Tango data type.
 *
 * Example:
 * Tango::DevLong tg_value;
 * try
 * {
 *     from_py<Tango::DEV_LONG>::convert(py_obj, tg_value);
 * }
 * catch(boost::python::error_already_set &eas)
 * {
 *     handle_error(eas);
 * }
 */
template<long tangoTypeConst>
struct from_py
{
    typedef typename TANGO_const2type(tangoTypeConst) TangoScalarType;

    static inline void convert(const boost::python::object &o, TangoScalarType &tg)
    {
        convert(o.ptr(), tg);
    }

    static inline void convert(PyObject *o, TangoScalarType &tg)
    {
        // boost::python::object tmp(boost::python::handle<>(o));
        // tg = boost::python::extract<TangoScalartype>(tmp);
        Tango::Except::throw_exception( \
                        "PyDs_WrongPythonDataTypeForAttribute",
                        "Unsupported attribute type translation",
                        "from_py::convert()");
    }
};

#define DEFINE_FAST_TANGO_FROMPY(tangoTypeConst, FN) \
template<> \
struct from_py<tangoTypeConst> \
{ \
    typedef TANGO_const2type(tangoTypeConst) TangoScalarType; \
\
    static inline void convert(const boost::python::object &o, TangoScalarType &tg) \
    { \
        convert(o.ptr(), tg); \
    } \
\
    static inline void convert(PyObject *o, TangoScalarType &tg) \
    { \
        tg = static_cast<TangoScalarType>(FN(o));  \
        if(PyErr_Occurred()) \
            boost::python::throw_error_already_set();  \
    } \
};

#undef max 
#undef min

// DEFINE_FAST_TANGO_FROMPY should be enough. However, as python does not
// provide conversion from python integers to all the data types accepted
// by tango we must check the ranges manually. Also now we can add numpy
// support to some extent...
#ifdef DISABLE_PYTANGO_NUMPY
# define DEFINE_FAST_TANGO_FROMPY_NUM(tangoTypeConst, cpy_type, FN) \
    template<> \
    struct from_py<tangoTypeConst> \
    { \
        typedef TANGO_const2type(tangoTypeConst) TangoScalarType; \
        typedef numeric_limits<TangoScalarType> TangoScalarTypeLimits; \
    \
        static inline void convert(const boost::python::object &o, TangoScalarType &tg) \
        { \
            convert(o.ptr(), tg); \
        } \
    \
        static inline void convert(PyObject *o, TangoScalarType &tg) \
        { \
            cpy_type cpy_value = FN(o); \
            if(PyErr_Occurred()) { \
                PyErr_SetString(PyExc_TypeError, "Expecting a numeric type, it is not."); \
                boost::python::throw_error_already_set();  \
            } \
            if (cpy_value > TangoScalarTypeLimits::max()) { \
                PyErr_SetString(PyExc_OverflowError, "Value is too large."); \
                boost::python::throw_error_already_set(); \
            } \
            if (cpy_value < TangoScalarTypeLimits::min()) { \
                PyErr_SetString(PyExc_OverflowError, "Value is too small."); \
                boost::python::throw_error_already_set(); \
            } \
            \
            tg = static_cast<TangoScalarType>(cpy_value);  \
        } \
    };
#else // DISABLE_PYTANGO_NUMPY
# define DEFINE_FAST_TANGO_FROMPY_NUM(tangoTypeConst, cpy_type, FN) \
    template<> \
    struct from_py<tangoTypeConst> \
    { \
        typedef TANGO_const2type(tangoTypeConst) TangoScalarType; \
        typedef numeric_limits<TangoScalarType> TangoScalarTypeLimits; \
    \
        static inline void convert(const boost::python::object &o, TangoScalarType &tg) \
        { \
            convert(o.ptr(), tg); \
        } \
    \
        static inline void convert(PyObject *o, TangoScalarType &tg) \
        { \
            cpy_type cpy_value = FN(o); \
            if(PyErr_Occurred()) { \
                if(PyArray_CheckScalar(o) && \
                ( PyArray_DescrFromScalar(o) \
                    == PyArray_DescrFromType(TANGO_const2numpy(tangoTypeConst)))) \
                { \
                    PyArray_ScalarAsCtype(o, reinterpret_cast<void*>(&tg)); \
                    return; \
                } else \
                    PyErr_SetString(PyExc_TypeError, "Expecting a numeric type," \
                        " but it is not. If you use a numpy type instead of" \
                        " python core types, then it must exactly match (ex:" \
                        " numpy.int32 for PyTango.DevLong)"); \
                    boost::python::throw_error_already_set();  \
            } \
            if (TangoScalarTypeLimits::is_integer) { \
                if (cpy_value > TangoScalarTypeLimits::max()) { \
                    PyErr_SetString(PyExc_OverflowError, "Value is too large."); \
                    boost::python::throw_error_already_set(); \
                } \
                if (cpy_value < TangoScalarTypeLimits::min()) { \
                    PyErr_SetString(PyExc_OverflowError, "Value is too small."); \
                    boost::python::throw_error_already_set(); \
                } \
            } \
            tg = static_cast<TangoScalarType>(cpy_value);  \
        } \
    };
#endif // !DISABLE_PYTANGO_NUMPY

DEFINE_FAST_TANGO_FROMPY_NUM(Tango::DEV_BOOLEAN, long, PyLong_AsLong)
DEFINE_FAST_TANGO_FROMPY_NUM(Tango::DEV_UCHAR, unsigned long, PyLong_AsUnsignedLong)
DEFINE_FAST_TANGO_FROMPY_NUM(Tango::DEV_SHORT, long, PyLong_AsLong)
DEFINE_FAST_TANGO_FROMPY_NUM(Tango::DEV_USHORT, unsigned long, PyLong_AsUnsignedLong)
DEFINE_FAST_TANGO_FROMPY_NUM(Tango::DEV_LONG, long, PyLong_AsLong)
DEFINE_FAST_TANGO_FROMPY_NUM(Tango::DEV_ULONG, unsigned long, PyLong_AsUnsignedLong)
DEFINE_FAST_TANGO_FROMPY(Tango::DEV_STATE, PyLong_AsLong)

DEFINE_FAST_TANGO_FROMPY_NUM(Tango::DEV_LONG64, Tango::DevLong64, PyLong_AsLongLong)
DEFINE_FAST_TANGO_FROMPY_NUM(Tango::DEV_ULONG64, Tango::DevULong64, PyLong_AsUnsignedLongLong)
DEFINE_FAST_TANGO_FROMPY_NUM(Tango::DEV_FLOAT, double, PyFloat_AsDouble)
DEFINE_FAST_TANGO_FROMPY_NUM(Tango::DEV_DOUBLE, double, PyFloat_AsDouble)

/// @bug Not a bug per se, but you should keep in mind: It returns a new
/// string, so if you pass it to Tango with a release flag there will be
/// no problems, but if you have to use it yourself then you must remember
/// to delete[] it!
inline Tango::DevString PyString_AsCorbaString(PyObject* ob)
{
    const char* str = PyString_AsString(ob);
    if (!str)
        return 0;
    return CORBA::string_dup(str);
}
        
// DEFINE_FAST_TANGO_FROMPY(Tango::DEV_STRING, PyString_AsString)
DEFINE_FAST_TANGO_FROMPY(Tango::DEV_STRING, PyString_AsCorbaString)

extern const char *param_must_be_seq;
/// This class is useful when you need a sequence like C++ type for
/// a function argument, and you have exported this type to python.
/// This will try to convert the parameter directly to the C++ object
/// (valid if the argument passed was an instance of the exported type).
/// If it fails, it will use from_sequence::convert to get a copy
/// of the sequence in the expected format.
/// So for example we can get a function that accepts an object of
/// type StdStringVector, or a list of strings, or a tuple of strings...
template<class SequenceT>
class CSequenceFromPython
{
    SequenceT* m_seq;
    bool m_own;
    public:
    CSequenceFromPython(boost::python::object &py_obj)
    {
        boost::python::extract<SequenceT*> ext(py_obj);
        if (ext.check()) {
            m_seq = ext();
            m_own = false;
        } else {
            if (PySequence_Check(py_obj.ptr()) == 0)
                raise_(PyExc_TypeError, param_must_be_seq);
            if (PyString_Check(py_obj.ptr()) != 0)
                raise_(PyExc_TypeError, param_must_be_seq);

            m_own = true;
            //m_seq = new SequenceT(PySequence_Length(Py_obj.ptr()));
            m_seq = new SequenceT();
            std::auto_ptr<SequenceT> guard(m_seq);
            from_sequence<SequenceT>::convert(py_obj, *m_seq);
            guard.release();
        }
    }
    ~CSequenceFromPython()
    {
        if (m_own)
            delete m_seq;
    }
    SequenceT & operator*()
    {
        return *m_seq;
    }
    const SequenceT & operator*() const
    {
        return *m_seq;
    }
};

void from_py_object(boost::python::object &, Tango::AttributeAlarm &);
void from_py_object(boost::python::object &, Tango::ChangeEventProp &);
void from_py_object(boost::python::object &, Tango::PeriodicEventProp &);
void from_py_object(boost::python::object &, Tango::ArchiveEventProp &);
void from_py_object(boost::python::object &, Tango::EventProperties &);

void from_py_object(boost::python::object &, Tango::AttributeConfig &);
void from_py_object(boost::python::object &, Tango::AttributeConfig_2 &);
void from_py_object(boost::python::object &, Tango::AttributeConfig_3 &);

void from_py_object(boost::python::object &, Tango::AttributeConfigList &);
void from_py_object(boost::python::object &, Tango::AttributeConfigList_2 &);
void from_py_object(boost::python::object &, Tango::AttributeConfigList_3 &);
