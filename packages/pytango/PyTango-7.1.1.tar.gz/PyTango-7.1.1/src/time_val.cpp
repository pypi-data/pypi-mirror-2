#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_time_val()
{
    class_<Tango::TimeVal>("TimeVal")
        .def_readwrite("tv_sec", &Tango::TimeVal::tv_sec)
        .def_readwrite("tv_usec", &Tango::TimeVal::tv_usec)
        .def_readwrite("tv_nsec", &Tango::TimeVal::tv_nsec)
    ;
}
