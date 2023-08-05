#include <iostream>
#include <string>
#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_attribute_info_ex()
{
    class_<Tango::AttributeInfoEx, bases<Tango::AttributeInfo> >
        ("AttributeInfoEx")
        .def_readwrite("alarms", &Tango::AttributeInfoEx::alarms)
        .def_readwrite("events", &Tango::AttributeInfoEx::events)
        .def_readwrite("sys_extensions", &Tango::AttributeInfoEx::sys_extensions)
    ;
}
