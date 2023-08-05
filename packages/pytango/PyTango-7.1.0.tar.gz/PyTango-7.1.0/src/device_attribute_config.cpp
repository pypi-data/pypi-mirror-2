#include <iostream>
#include <string>
#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_device_attribute_config()
{
    class_<Tango::DeviceAttributeConfig>("DeviceAttributeConfig")
        .def_readonly("name", &Tango::DeviceAttributeConfig::name)
        .def_readonly("writable", &Tango::DeviceAttributeConfig::writable)
        .def_readonly("data_format", &Tango::DeviceAttributeConfig::data_format)
        .def_readonly("data_type", &Tango::DeviceAttributeConfig::data_type)
        .def_readonly("max_dim_x", &Tango::DeviceAttributeConfig::max_dim_x)
        .def_readonly("max_dim_y", &Tango::DeviceAttributeConfig::max_dim_y)
        .def_readwrite("description", &Tango::DeviceAttributeConfig::description)
        .def_readwrite("label", &Tango::DeviceAttributeConfig::label)
        .def_readwrite("unit", &Tango::DeviceAttributeConfig::unit)
        .def_readwrite("standard_unit", &Tango::DeviceAttributeConfig::standard_unit)
        .def_readwrite("display_unit", &Tango::DeviceAttributeConfig::display_unit)
        .def_readwrite("format", &Tango::DeviceAttributeConfig::format)
        .def_readwrite("min_value", &Tango::DeviceAttributeConfig::min_value)
        .def_readwrite("max_value", &Tango::DeviceAttributeConfig::max_value)
        .def_readwrite("min_alarm", &Tango::DeviceAttributeConfig::min_alarm)
        .def_readwrite("max_alarm", &Tango::DeviceAttributeConfig::max_alarm)
        .def_readwrite("writable_attr_name", &Tango::DeviceAttributeConfig::writable_attr_name)
        .def_readwrite("extensions", &Tango::DeviceAttributeConfig::extensions)
    ;
}
