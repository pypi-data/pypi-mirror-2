#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_attribute_dimension()
{
    class_<Tango::AttributeDimension>("AttributeDimension")
        .def_readonly("dim_x", &Tango::AttributeDimension::dim_x)
        .def_readonly("dim_y", &Tango::AttributeDimension::dim_y)
    ;
}
