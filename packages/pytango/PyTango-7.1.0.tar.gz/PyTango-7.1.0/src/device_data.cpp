#include <iostream>
#include <string>
#include <boost/python.hpp>
#include <boost/mpl/if.hpp>
#include <tango.h>

#include "pytgutils.h"

using namespace boost::python;



namespace PyDeviceData {

    Tango::CmdArgType get_type(Tango::DeviceData &self)
    {
        /// @todo This should change in Tango itself, get_type should not return int!!
        return static_cast<Tango::CmdArgType>(self.get_type());
    }
    
    /// @name Scalar Insertion
    /// @{
        template <long tangoTypeConst>
        void insert_scalar(Tango::DeviceData &self, object py_value)
        {
            typedef typename TANGO_const2type(tangoTypeConst) TangoScalarType;
            TangoScalarType val;
            val = boost::python::extract<TangoScalarType>(py_value);
            self << val;
        }
        template <>
        void insert_scalar<Tango::DEV_VOID>(Tango::DeviceData &self, object py_value)
        {
            raise_(PyExc_TypeError, "Trying to insert a value in a DEV_VOID DeviceData!");
        }
    /// @}
    // ~Scalar Insertion
    // -----------------------------------------------------------------------

    /// @name Array Insertion
    /// @{
        template <long tangoTypeConst>
        void insert_array(Tango::DeviceData &self, object py_value)
        {
            typedef typename TANGO_const2type(tangoTypeConst) TangoArrayType;

            TangoArrayType val;
            convert2array(py_value, val);
            self << val;
        }
    /// @}
    // ~Array Insertion
    // -----------------------------------------------------------------------

    /// @name Scalar Extraction
    /// @{
        template <long tangoTypeConst>
        object extract_scalar(Tango::DeviceData &self)
        {
            typedef typename TANGO_const2type(tangoTypeConst) TangoScalarType;
            /// @todo CONST_DEV_STRING ell el tracta com DEV_STRING
            TangoScalarType val;
            self >> val;
            return boost::python::object(val);
        }

        template <>
        object extract_scalar<Tango::DEV_VOID>(Tango::DeviceData &self)
        {
            return boost::python::object();
        }

        template <>
        object extract_scalar<Tango::DEV_STRING>(Tango::DeviceData &self)
        {
            typedef std::string TangoScalarType;
            TangoScalarType val;
            self >> val;
            return boost::python::object(val);
        }
    /// @}
    // ~Scalar Extraction
    // -----------------------------------------------------------------------

    /// @name Array extraction
    /// @{
        template<class T>
        boost::python::object convert_array(const T *seq, int convert_to = 0)
        {
            /// @todo convert_to list, or tuple, or numpy...
            return object(handle<>(CORBA_sequence_to_list<T>::convert(*seq)));
        }

        template <long tangoTypeConst>
        object extract_array(Tango::DeviceData &self)
        {
            typedef typename TANGO_const2type(tangoTypeConst) TangoScalarType;
            // Const is the pointed, not the pointer. So cannot modify the data.
            // And that's because the data is still inside "self" after extracting.
            // This also means that we are not supposed to "delete" tmp_ptr.
            const TangoScalarType* tmp_ptr;
            self >> tmp_ptr;

            return convert_array(tmp_ptr);
        }
    /// @}
    // ~Array Extraction
    // -----------------------------------------------------------------------

    object extract(Tango::DeviceData &self)
    {
        TANGO_DO_ON_DEVICE_DATA_TYPE(self.get_type(),
            return extract_scalar<tangoTypeConst>(self);
        ,
            return extract_array<tangoTypeConst>(self);
        );
        return object();
    }

    void insert(Tango::DeviceData &self, long data_type, object py_value)
    {
        TANGO_DO_ON_DEVICE_DATA_TYPE(data_type,
            insert_scalar<tangoTypeConst>(self, py_value);
        , 
            insert_array<tangoTypeConst>(self, py_value);
        );
    }
}

void export_device_data()
{
    class_<Tango::DeviceData> DeviceData("DeviceData",
        init<>())
    ;

    scope scope_dd = DeviceData;

    /// @todo get rid of except_flags everywhere... or really use and export them everywhere!
    enum_<Tango::DeviceData::except_flags>("except_flags")
        .value("isempty_flag", Tango::DeviceData::isempty_flag)
        .value("wrongtype_flag", Tango::DeviceData::wrongtype_flag)
        .value("numFlags", Tango::DeviceData::numFlags)
    ;

    DeviceData
        .def(init<const Tango::DeviceData &>())

        .def("extract", &PyDeviceData::extract)

        .def("insert", &PyDeviceData::insert,
            (arg_("self"), arg_("data_type"), arg_("value")))

        /// @todo do not throw exceptions!!
        .def("is_empty", &Tango::DeviceData::is_empty)

// TODO
//	void exceptions(bitset<numFlags> fl) {exceptions_flags = fl;}
//	bitset<numFlags> exceptions() {return exceptions_flags;}
//	void reset_exceptions(except_flags fl) {exceptions_flags.reset((size_t)fl);}
//	void set_exceptions(except_flags fl) {exceptions_flags.set((size_t)fl);}

        .def("get_type", &PyDeviceData::get_type)
    ;

}
