#include <iostream>
#include <string>
#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_attribute_alarm_info()
{
    class_<Tango::AttributeAlarmInfo>("AttributeAlarmInfo")
        .def_readwrite("min_alarm", &Tango::AttributeAlarmInfo::min_alarm)
        .def_readwrite("max_alarm", &Tango::AttributeAlarmInfo::max_alarm)
        .def_readwrite("min_warning", &Tango::AttributeAlarmInfo::min_warning)
        .def_readwrite("max_warning", &Tango::AttributeAlarmInfo::max_warning)
        .def_readwrite("delta_t", &Tango::AttributeAlarmInfo::delta_t)
        .def_readwrite("delta_val", &Tango::AttributeAlarmInfo::delta_val)
        .def_readwrite("extensions", &Tango::AttributeAlarmInfo::extensions)
    ;
}
