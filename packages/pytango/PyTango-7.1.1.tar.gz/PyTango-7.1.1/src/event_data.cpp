#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_event_data()
{
    class_<Tango::EventData>("EventData",
        init<const Tango::EventData &>())
    
        // The original Tango::EventData structure has a 'device' field.
        // However, if we returned this directly we would get a different
        // python device each time. So we are doing our weird things to make
        // sure the device returned is the same where the read action was
        // performed. So we don't return Tango::EventData::device directly.
        // See callback.cpp
        .setattr("device", object())
        
        .def_readonly("attr_name", &Tango::EventData::attr_name)
        .def_readonly("event", &Tango::EventData::event)
        
        // The original Tango::EventData structure has "get_attr_value" but
        // we can't refer it directly here because we have to extract value
        // and so on.
        // See callback.cpp
        .setattr("attr_value", object())
        
        .def_readonly("err", &Tango::EventData::err)
        .def_readonly("reception_date", &Tango::EventData::reception_date)
        .add_property("errors", make_getter(&Tango::EventData::errors, 
            return_value_policy<copy_non_const_reference>()))
        
        .def("get_date", &Tango::EventData::get_date, 
            return_internal_reference<>())
    ;
}
