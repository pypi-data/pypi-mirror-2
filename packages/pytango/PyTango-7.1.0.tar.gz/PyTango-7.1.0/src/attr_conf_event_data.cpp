#include <iostream>
#include <string>
#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_attr_conf_event_data()
{
    class_<Tango::AttrConfEventData>("AttrConfEventData",
        init<const Tango::AttrConfEventData &>())

        // The original Tango::EventData structure has a 'device' field.
        // However, if we returned this directly we would get a different
        // python device each time. So we are doing our weird things to make
        // sure the device returned is the same where the read action was
        // performed. So we don't return Tango::EventData::device directly.
        // See callback.cpp
        .setattr("device",object())
        .def_readonly("attr_name", &Tango::AttrConfEventData::attr_name)
        .def_readonly("event", &Tango::AttrConfEventData::event)
        .setattr("attr_conf",object())
        .def_readonly("err", &Tango::AttrConfEventData::err)
        .def_readonly("reception_date", &Tango::AttrConfEventData::reception_date)
        .add_property("errors", make_getter(&Tango::AttrConfEventData::errors, 
            return_value_policy<copy_non_const_reference>()))
        .def("get_date", &Tango::AttrConfEventData::get_date,
            return_internal_reference<>())
    ;
}
