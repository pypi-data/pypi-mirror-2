#include <iostream>
#include <string>
#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_attribute_event_info()
{
    class_<Tango::AttributeEventInfo>("AttributeEventInfo")
       .def_readwrite("ch_event", &Tango::AttributeEventInfo::ch_event)
       .def_readwrite("per_event", &Tango::AttributeEventInfo::per_event)
       .def_readwrite("arch_event", &Tango::AttributeEventInfo::arch_event)
    ;
}
