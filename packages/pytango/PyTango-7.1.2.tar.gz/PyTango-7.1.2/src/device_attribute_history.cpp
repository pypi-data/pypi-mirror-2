#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_device_attribute_history()
{

    class_<Tango::DeviceAttributeHistory, bases<Tango::DeviceAttribute> >
            DeviceAttributeHistory("DeviceAttributeHistory", init<>());

    DeviceAttributeHistory
        .def(init<const Tango::DeviceAttributeHistory &>())

        .def("has_failed", &Tango::DeviceAttributeHistory::has_failed)
    ;
}
