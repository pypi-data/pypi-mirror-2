#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include <tango.h>

using namespace boost::python;

void export_command_info()
{
    class_<Tango::CommandInfo , bases<Tango::DevCommandInfo> >("CommandInfo")
        .def_readonly("disp_level", &Tango::CommandInfo::disp_level)
        ;
}
