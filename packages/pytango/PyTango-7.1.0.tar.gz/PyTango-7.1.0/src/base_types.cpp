#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include <tango.h>

#include "defs.h"
#include "pytgutils.h"

#include "base_types_numpy.hpp"

using namespace boost::python;

// from tango_const.h
void export_poll_device();

// from devapi.h
void export_locker_info();
//TODO void export_locking_thread();
void export_dev_command_info();
void export_attribute_dimension();
void export_command_info();
void export_device_info();
void export_device_attribute_config();
void export_attribute_info();
void export_attribute_alarm_info();
void export_change_event_info();
void export_periodic_event_info();
void export_archive_event_info();
void export_attribute_event_info();
void export_attribute_info_ex();
void export_device_data();
void export_device_attribute();
void export_device_data_history();
void export_device_attribute_history();

void export_dev_error();
void export_time_val();

//
// Necessary equality operators for having vectors exported to python
//

namespace Tango
{

inline bool operator==(const Tango::DbDatum& dd1, const Tango::DbDatum& dd2)
{
    return dd1.name == dd2.name && dd1.value_string == dd2.value_string;
}

inline bool operator==(const Tango::DbDevInfo& di1, const Tango::DbDevInfo& di2)
{
    return di1.name == di2.name &&
           di1._class == di2._class &&
           di1.server == di2.server;
}

inline bool operator==(const Tango::DbDevImportInfo& dii1,
                       const Tango::DbDevImportInfo& dii2)
{
    return dii1.name == dii2.name && dii1.exported == dii2.exported &&
           dii1.ior == dii2.ior && dii1.version == dii2.version;
}

inline bool operator==(const Tango::DbDevExportInfo& dei1,
                       const Tango::DbDevExportInfo& dei2)
{
    return dei1.name == dei2.name && dei1.ior == dei2.ior &&
           dei1.host == dei2.host && dei1.version == dei2.version &&
           dei1.pid == dei2.pid;
}

inline bool operator==(const Tango::DbHistory& dh1_, const Tango::DbHistory& dh2_)
{
    Tango::DbHistory &dh1 = const_cast<Tango::DbHistory &>(dh1_);
    Tango::DbHistory &dh2 = const_cast<Tango::DbHistory &>(dh2_);

    return dh1.get_name() == dh2.get_name() &&
           dh1.get_attribute_name() == dh2.get_attribute_name() &&
           dh1.is_deleted() == dh2.is_deleted();
}

inline bool operator==(const Tango::GroupReply& dh1_, const Tango::GroupReply& dh2_)
{
    /// @todo ?
    return false;
}

inline bool operator==(const Tango::TimeVal& tv1, const Tango::TimeVal& tv2)
{
    return tv1.tv_sec == tv2.tv_sec &&
           tv1.tv_usec == tv2.tv_usec &&
           tv1.tv_nsec == tv2.tv_nsec;
}

inline bool operator==(const Tango::DeviceData& dd1_, const Tango::DeviceData& dd2_)
{
    Tango::DeviceData &dd1 = const_cast<Tango::DeviceData &>(dd1_);
    Tango::DeviceData &dd2 = const_cast<Tango::DeviceData &>(dd2_);

    return //dh1.any == dh2.any &&
           dd1.exceptions() == dd2.exceptions();
}

inline bool operator==(const Tango::DeviceDataHistory& ddh1_, const Tango::DeviceDataHistory& ddh2_)
{
    Tango::DeviceDataHistory &ddh1 = const_cast<Tango::DeviceDataHistory &>(ddh1_);
    Tango::DeviceDataHistory &ddh2 = const_cast<Tango::DeviceDataHistory &>(ddh2_);

    return operator==((Tango::DeviceData)ddh1, (Tango::DeviceData)ddh2) &&
           ddh1.failed() == ddh2.failed() &&
           ddh1.date() == ddh2.date(); //&&
           //ddh1.errors() == ddh2.errors();
}

}

/**
 * Converter from python sequence to CORBA sequence
 */
template<typename CorbaSequence>
struct convert_PySequence_to_CORBA_Sequence
{
    convert_PySequence_to_CORBA_Sequence()
    {
        // Register converter from python sequence to CorbaSequence
        boost::python::converter::registry::push_back(
            &convertible,
            &construct,
            boost::python::type_id<CorbaSequence>());
    }

    // Check if given Python object is convertible to a sequence.
    // If so, return obj, otherwise return 0
    static void* convertible(PyObject* obj)
    {
        return (PySequence_Check(obj)) ? obj : NULL;
    }

    static void construct(PyObject* obj,
                          boost::python::converter::rvalue_from_python_stage1_data* data)
    {
            
        typedef boost::python::converter::rvalue_from_python_storage<CorbaSequence> CorbaSequence_storage;

        void* const storage = reinterpret_cast<CorbaSequence_storage*>(data)->storage.bytes;

        CorbaSequence *ptr = new (storage) CorbaSequence();
        convert2array(object(handle<>(obj)), *ptr);
        data->convertible = storage;
    }
    
};

int raise_asynch_exception(long thread_id, boost::python::object exp_klass)
{
    return PyThreadState_SetAsyncExc(thread_id, exp_klass.ptr());
}

void export_base_types()
{
    enum_<PyTango::ExtractAs>("ExtractAs")
        .value("Numpy", PyTango::ExtractAsNumpy)
        .value("Tuple", PyTango::ExtractAsTuple)
        .value("List", PyTango::ExtractAsList)
        .value("String", PyTango::ExtractAsString)
        .value("PyTango3", PyTango::ExtractAsPyTango3)
        .value("Nothing", PyTango::ExtractAsNothing)
    ;
    
    // Export some std types

    class_<StdStringVector>("StdStringVector")
        .def(vector_indexing_suite<StdStringVector, true>());

    class_<StdLongVector>("StdLongVector")
        .def(vector_indexing_suite<StdLongVector, true>());

    class_<StdDoubleVector>("StdDoubleVector")
        .def(vector_indexing_suite<StdDoubleVector, true>());

    class_<Tango::CommandInfoList>("CommandInfoList")
        .def(vector_indexing_suite<Tango::CommandInfoList, true>());

    class_<Tango::AttributeInfoList>("AttributeInfoList")
        .def(vector_indexing_suite<Tango::AttributeInfoList, true>());

    class_<Tango::AttributeInfoListEx>("AttributeInfoListEx")
        .def(vector_indexing_suite<Tango::AttributeInfoListEx, true>());

    class_<std::vector<Tango::Attr *> >("AttrList")
        .def(vector_indexing_suite<std::vector<Tango::Attr *>, true>());

    //class_<Tango::EventDataList>("EventDataList")
    //    .def(vector_indexing_suite<Tango::EventDataList>());

    class_<Tango::DbData>("DbData")
        .def(vector_indexing_suite<Tango::DbData, true>());

    class_<Tango::DbDevInfos>("DbDevInfos")
        .def(vector_indexing_suite<Tango::DbDevInfos, true>());

    class_<Tango::DbDevExportInfos>("DbDevExportInfos")
        .def(vector_indexing_suite<Tango::DbDevExportInfos, true>());

    class_<Tango::DbDevImportInfos>("DbDevImportInfos")
        .def(vector_indexing_suite<Tango::DbDevImportInfos, true>());

    class_<std::vector<Tango::DbHistory> >("DbHistoryList")
        .def(vector_indexing_suite<std::vector<Tango::DbHistory>, true>());

    class_<Tango::DeviceDataHistoryList>("DeviceDataHistoryList")
        .def(vector_indexing_suite<Tango::DeviceDataHistoryList, true>());

    typedef std::vector<Tango::GroupReply> StdGroupReplyVector_;
    class_< StdGroupReplyVector_ >("StdGroupReplyVector")
        .def(vector_indexing_suite<StdGroupReplyVector_, true>());

    typedef std::vector<Tango::GroupCmdReply> StdGroupCmdReplyVector_;
    class_< StdGroupCmdReplyVector_ >("StdGroupCmdReplyVector")
        .def(vector_indexing_suite<StdGroupCmdReplyVector_, true>());

    typedef std::vector<Tango::GroupAttrReply> StdGroupAttrReplyVector_;
    class_< StdGroupAttrReplyVector_ >("StdGroupAttrReplyVector")
        .def(vector_indexing_suite<StdGroupAttrReplyVector_, true>());

    //to_python_converter<CORBA::String_member, CORBA_String_member_to_str>();
    to_python_converter<_CORBA_String_member, CORBA_String_member_to_str2>();
    to_python_converter<_CORBA_String_element, CORBA_String_element_to_str>();

    to_python_converter<Tango::DevErrorList, CORBA_sequence_to_tuple<Tango::DevErrorList> >();

    to_python_converter<Tango::DevVarCharArray, CORBA_sequence_to_list<Tango::DevVarCharArray> >();
    to_python_converter<Tango::DevVarShortArray, CORBA_sequence_to_list<Tango::DevVarShortArray> >();
    to_python_converter<Tango::DevVarLongArray, CORBA_sequence_to_list<Tango::DevVarLongArray> >();
    to_python_converter<Tango::DevVarFloatArray, CORBA_sequence_to_list<Tango::DevVarFloatArray> >();
    to_python_converter<Tango::DevVarDoubleArray, CORBA_sequence_to_list<Tango::DevVarDoubleArray> >();
    to_python_converter<Tango::DevVarUShortArray, CORBA_sequence_to_list<Tango::DevVarUShortArray> >();
    to_python_converter<Tango::DevVarULongArray, CORBA_sequence_to_list<Tango::DevVarULongArray> >();
    to_python_converter<Tango::DevVarStringArray, CORBA_sequence_to_list<Tango::DevVarStringArray> >();
    to_python_converter<Tango::DevVarLongStringArray, CORBA_sequence_to_list<Tango::DevVarLongStringArray> >();
    to_python_converter<Tango::DevVarDoubleStringArray, CORBA_sequence_to_list<Tango::DevVarDoubleStringArray> >();
    to_python_converter<Tango::DevVarLong64Array, CORBA_sequence_to_list<Tango::DevVarLong64Array> >();
    to_python_converter<Tango::DevVarULong64Array, CORBA_sequence_to_list<Tango::DevVarULong64Array> >();

    //to_python_converter<unsigned char, UChar_to_str>();
    
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarCharArray>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarShortArray>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarLongArray>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarFloatArray>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarDoubleArray>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarUShortArray>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarULongArray>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarStringArray>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarLongStringArray>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarDoubleStringArray>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarLong64Array>();
    convert_PySequence_to_CORBA_Sequence<Tango::DevVarULong64Array>();

    convert_numpy_to_integer<Tango::DEV_UCHAR>();
    convert_numpy_to_integer<Tango::DEV_SHORT>();
    convert_numpy_to_integer<Tango::DEV_LONG>();
    convert_numpy_to_float<Tango::DEV_FLOAT>();
    convert_numpy_to_float<Tango::DEV_DOUBLE>();
    convert_numpy_to_integer<Tango::DEV_USHORT>();
    convert_numpy_to_integer<Tango::DEV_ULONG>();
    convert_numpy_to_integer<Tango::DEV_LONG64>();
    convert_numpy_to_integer<Tango::DEV_ULONG64>();
    
    // from tango_const.h
    export_poll_device();

    // from devapi.h
    export_locker_info();
    //TODO export_locking_thread();
    export_dev_command_info();
    export_attribute_dimension();
    export_command_info();
    export_device_info();
    export_device_attribute_config();
    export_attribute_info();
    export_attribute_alarm_info();
    export_change_event_info();
    export_periodic_event_info();
    export_archive_event_info();
    export_attribute_event_info();
    export_attribute_info_ex();
    export_device_data();
    export_device_attribute();
    export_device_data_history();
    export_device_attribute_history();

    export_dev_error();
    export_time_val();
    
    def("raise_asynch_exception", &raise_asynch_exception);
}
