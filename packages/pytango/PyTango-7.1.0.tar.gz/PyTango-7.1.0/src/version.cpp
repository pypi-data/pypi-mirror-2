#include <boost/python.hpp>

#include <tango.h>

using namespace boost::python;

void export_version()
{
    scope().attr("__tangolib_version__") = TgLibVers;
}
