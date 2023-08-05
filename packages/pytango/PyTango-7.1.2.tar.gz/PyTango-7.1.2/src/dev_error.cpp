#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

struct PyDevError
{
    static inline PyObject* get_reason(Tango::DevError &de)
    { return PyString_FromString(de.reason); }

    static inline PyObject* get_desc(Tango::DevError &de)
    { return PyString_FromString(de.desc); }

    static inline PyObject* get_origin(Tango::DevError &de)
    { return PyString_FromString(de.origin); }

};

void export_dev_error()
{
    class_<Tango::DevError>("DevError")
        .add_property("reason", &PyDevError::get_reason)
        .def_readonly("severity", &Tango::DevError::severity)
        .add_property("desc", &PyDevError::get_desc)
        .add_property("origin", &PyDevError::get_origin)
    ;
}
