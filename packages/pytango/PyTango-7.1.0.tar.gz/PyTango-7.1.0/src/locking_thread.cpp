#include <iostream>
#include <string>
#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_locking_thread()
{
    class_<Tango::LockingThread>("LockingThread")
    ;
}
