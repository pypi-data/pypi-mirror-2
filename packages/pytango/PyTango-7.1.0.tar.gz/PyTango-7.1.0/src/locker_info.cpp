#include <iostream>
#include <string>
#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

struct PyLockerInfo
{
    static inline boost::python::object get_locker_id(Tango::LockerInfo &li)
    {
        return (li.ll == Tango::CPP) ? 
            boost::python::object(li.li.LockerPid) :
            boost::python::tuple(li.li.UUID);
    }
};

void export_locker_info()
{
    class_<Tango::LockerInfo>("LockerInfo",
        "A structure with information about the locker\n"
        "with the folowing members,\n"
        " - ll : (PyTango.LockerLanguage) the locker language\n"
        " - li : (pid_t / UUID) the locker id\n"
        " - locker_host : (string) the host\n"
        " - locker_class : (string) the class\n"
        "\npid_t should be an int, UUID should be a tuple of four numbers.\n"
        "\nNew in PyTango 7.0.0"
        )
        .def_readonly("ll", &Tango::LockerInfo::ll)
        .add_property("li", &PyLockerInfo::get_locker_id)
        .def_readonly("locker_host", &Tango::LockerInfo::locker_host)
        .def_readonly("locker_class", &Tango::LockerInfo::locker_class)
    ;
}
