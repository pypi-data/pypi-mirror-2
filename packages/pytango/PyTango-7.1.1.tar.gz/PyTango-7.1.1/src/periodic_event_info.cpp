#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_periodic_event_info()
{
    class_<Tango::PeriodicEventInfo>("PeriodicEventInfo",
        "A structure containing available periodic event information for an attribute\n"
        "with the folowing members,\n"
        " - period : string\n"
        " - extensions : vector of strings\n"
        )
        .def_readwrite("period", &Tango::PeriodicEventInfo::period)
        .def_readwrite("extensions", &Tango::PeriodicEventInfo::extensions)
    ;
}
