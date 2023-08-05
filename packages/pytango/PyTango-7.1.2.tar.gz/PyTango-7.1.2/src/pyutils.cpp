#include <boost/python.hpp>

#include "defs.h"
#include "pyutils.h"

using namespace boost::python;

bool is_method_defined(object &obj, const std::string &method_name)
{
    return is_method_defined(obj.ptr(), method_name);
}

bool is_method_defined(PyObject *obj, const std::string &method_name)
{
    bool exists, is_method;
    is_method_defined(obj, method_name, exists, is_method);
    return exists && is_method;
}

void is_method_defined(object &obj, const std::string &method_name,
                       bool &exists, bool &is_method)
{
    is_method_defined(obj.ptr(), method_name, exists, is_method);
}

void is_method_defined(PyObject *obj, const std::string &method_name,
                       bool &exists, bool &is_method)
{
    exists = is_method = false;

    PyObject *meth = PyObject_GetAttrString_(obj, method_name.c_str());

    exists = NULL != meth;

    if (!exists)
    {
        PyErr_Clear();
        return;
    }

    is_method = (1 == PyCallable_Check(meth));
    Py_DECREF(meth);
}
