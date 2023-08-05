#include <boost/python.hpp>
#include <tango.h>

#include "defs.h"
#include "pytgutils.h"

using namespace boost::python;

void export_database();

void export_db()
{
    // Note: DbDatum in python is extended to support the python sequence API
    //       in the file ../PyTango/db.py. This way the DbDatum behaves like a
    //       sequence of strings. This allows the user to work with a DbDatum as
    //       if it was working with the old list of strings

    class_<Tango::DbDatum>("DbDatum", init<>())
        .def(init<const char *>())
        .def(init<const Tango::DbDatum &>())
        .def_readwrite("name", &Tango::DbDatum::name)
        .def_readwrite("value_string", &Tango::DbDatum::value_string)
        .def("size", &Tango::DbDatum::size)
        .def("is_empty", &Tango::DbDatum::is_empty)
    ;

    class_<Tango::DbDevExportInfo>("DbDevExportInfo")
        .def_readwrite("name", &Tango::DbDevExportInfo::name)
        .def_readwrite("ior", &Tango::DbDevExportInfo::ior)
        .def_readwrite("host", &Tango::DbDevExportInfo::host)
        .def_readwrite("version", &Tango::DbDevExportInfo::version)
        .def_readwrite("pid", &Tango::DbDevExportInfo::pid)
    ;

     class_<Tango::DbDevImportInfo>("DbDevImportInfo")
        .def_readonly("name", &Tango::DbDevImportInfo::name)
        .def_readonly("exported", &Tango::DbDevImportInfo::exported)
        .def_readonly("ior", &Tango::DbDevImportInfo::ior)
        .def_readonly("version", &Tango::DbDevImportInfo::version)
    ;

     class_<Tango::DbDevInfo>("DbDevInfo")
        .def_readwrite("name", &Tango::DbDevInfo::name)
        .def_readwrite("_class", &Tango::DbDevInfo::_class)
        .def_readwrite("klass", &Tango::DbDevInfo::_class)
        .def_readwrite("server", &Tango::DbDevInfo::server)
    ;

    class_<Tango::DbHistory>("DbHistory",
        init<std::string, std::string, StdStringVector &>())
        .def(init<std::string, std::string, std::string, StdStringVector &>())
        .def("get_name", &Tango::DbHistory::get_name)
        .def("get_attribute_name", &Tango::DbHistory::get_attribute_name)
        .def("get_date", &Tango::DbHistory::get_date)
        .def("get_value", &Tango::DbHistory::get_value)
        .def("is_deleted", &Tango::DbHistory::is_deleted)
    ;

    class_<Tango::DbServerInfo>("DbServerInfo")
         .def_readwrite("name", &Tango::DbServerInfo::name)
         .def_readwrite("host", &Tango::DbServerInfo::host)
         .def_readwrite("mode", &Tango::DbServerInfo::mode)
         .def_readwrite("level", &Tango::DbServerInfo::level)
    ;

    export_database();
}
