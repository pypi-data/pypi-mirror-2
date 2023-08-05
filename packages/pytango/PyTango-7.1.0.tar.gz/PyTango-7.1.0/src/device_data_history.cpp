
#include <boost/python.hpp>
#include <tango.h>


using namespace boost::python;


void export_device_data_history()
{

    class_<Tango::DeviceDataHistory, bases<Tango::DeviceData> >
            DeviceDataHistory("DeviceDataHistory", init<>());

    DeviceDataHistory
        .def(init<const Tango::DeviceDataHistory &>())

        .def("has_failed", &Tango::DeviceDataHistory::has_failed)
        .def("get_date", &Tango::DeviceDataHistory::get_date,
            return_internal_reference<>())
        .def("get_err_stack", &Tango::DeviceDataHistory::get_err_stack,
            return_value_policy<copy_const_reference>())
        
    ;
}
