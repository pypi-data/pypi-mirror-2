#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_attribute_info()
{
    class_<Tango::AttributeInfo, bases<Tango::DeviceAttributeConfig> >
        ("AttributeInfo")
        .def_readonly("disp_level", &Tango::AttributeInfo::disp_level)
    ;
}
