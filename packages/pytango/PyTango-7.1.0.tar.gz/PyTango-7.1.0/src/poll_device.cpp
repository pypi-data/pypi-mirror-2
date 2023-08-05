#include <iostream>
#include <string>
#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_poll_device()
{
    class_<Tango::PollDevice>("PollDevice",
        "A structure containing PollDevice information\n"
        "the following members,\n"
        " - dev_name : string\n"
        " - ind_list : sequence<long>\n"
        "\nNew in PyTango 7.0.0")
        .def_readwrite("dev_name", &Tango::PollDevice::dev_name)
        .def_readwrite("ind_list", &Tango::PollDevice::ind_list)
    ;
}
