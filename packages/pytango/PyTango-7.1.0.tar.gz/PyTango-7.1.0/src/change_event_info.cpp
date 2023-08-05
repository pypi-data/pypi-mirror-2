#include <iostream>
#include <string>
#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_change_event_info()
{
    class_<Tango::ChangeEventInfo>("ChangeEventInfo")
        .def_readwrite("rel_change", &Tango::ChangeEventInfo::rel_change)
        .def_readwrite("abs_change", &Tango::ChangeEventInfo::abs_change)
        .def_readwrite("extensions", &Tango::ChangeEventInfo::extensions)
    ;
}
