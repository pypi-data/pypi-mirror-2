#include <boost/python.hpp>

#include <tango.h>

using namespace boost::python;

void export_device_info()
{
    class_<Tango::DeviceInfo>("DeviceInfo",
        "A structure containing available information for a device with the\n"
        "following members,\n"
        " - dev_class : string\n"
        " - server_id : string\n"
        " - server_host : string\n"
        " - server_version : integer\n"
        " - doc_url : string")
        .def_readonly("dev_class", &Tango::DeviceInfo::dev_class)
        .def_readonly("server_id", &Tango::DeviceInfo::server_id)
        .def_readonly("server_host", &Tango::DeviceInfo::server_host)
        .def_readonly("server_version", &Tango::DeviceInfo::server_version)
        .def_readonly("doc_url", &Tango::DeviceInfo::doc_url)
        .def_readonly("dev_type", &Tango::DeviceInfo::dev_type)
    ;
}
