#include <boost/python.hpp>
#include <tango.h>

using namespace boost::python;

void export_archive_event_info()
{
    class_<Tango::ArchiveEventInfo>("ArchiveEventInfo")
        .def_readwrite("archive_rel_change", &Tango::ArchiveEventInfo::archive_rel_change)
        .def_readwrite("archive_abs_change", &Tango::ArchiveEventInfo::archive_abs_change)
        .def_readwrite("extensions", &Tango::ArchiveEventInfo::extensions)
    ;
}
