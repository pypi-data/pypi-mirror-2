#pragma once

#include <boost/python.hpp>

#define arg_(a) boost::python::arg(a)

#if PY_VERSION_HEX < 0x02050000
typedef int Py_ssize_t;
#endif

inline PyObject *PyObject_GetAttrString_(PyObject *o, const std::string &attr_name)
{
#if PY_VERSION_HEX < 0x02050000
    char *attr = const_cast<char *>(attr_name.c_str());
#else
    const char *attr = attr_name.c_str();
#endif
    return PyObject_GetAttrString(o, attr);
}

inline PyObject *PyImport_ImportModule_(const std::string &name)
{
#if PY_VERSION_HEX < 0x02050000
    char *attr = const_cast<char *>(name.c_str());
#else
    const char *attr = name.c_str();
#endif
    return PyImport_ImportModule(attr);
}

inline void raise_(PyObject *type, const char *message)
{
    PyErr_SetString(type, message);
    boost::python::throw_error_already_set();
}

/// You should run any I/O intensive operations (like requesting data through
/// the network) in the context of an object like this.
class AutoPythonAllowThreads
{
    PyThreadState *m_save;
    
public:
    
    inline void giveup() { if (m_save) { PyEval_RestoreThread(m_save); m_save = 0; } }
    
    inline AutoPythonAllowThreads() { m_save = PyEval_SaveThread(); } ;
    inline ~AutoPythonAllowThreads() {giveup();} ;
};

/**
 * Determines if the given method name exists and is callable
 * within the python class
 *
 * @param[in] obj object to search for the method
 * @param[in] method_name the name of the method
 *
 * @return returns true is the method exists or false otherwise
 */
bool is_method_defined(boost::python::object &obj, const std::string &method_name);

/**
 * Determines if the given method name exists and is callable
 * within the python class
 *
 * @param[in] obj object to search for the method
 * @param[in] method_name the name of the method
 *
 * @return returns true is the method exists or false otherwise
 */
bool is_method_defined(PyObject *obj, const std::string &method_name);

/**
 * Determines if the given method name exists and is callable
 * within the python class
 *
 * @param[in] obj object to search for the method
 * @param[in] method_name the name of the method
 * @param[out] exists set to true if the symbol exists or false otherwise
 * @param[out] is_method set to true if the symbol exists and is a method
 *             or false otherwise
 */
void is_method_defined(PyObject *obj, const std::string &method_name,
                       bool &exists, bool &is_method);

/**
 * Determines if the given method name exists and is callable
 * within the python class
 *
 * @param[in] obj object to search for the method
 * @param[in] method_name the name of the method
 * @param[out] exists set to true if the symbol exists or false otherwise
 * @param[out] is_method set to true if the symbol exists and is a method
 *             or false otherwise
 */
void is_method_defined(boost::python::object &obj, const std::string &method_name,
                       bool &exists, bool &is_method);

#define PYTANGO_MOD \
    boost::python::object pytango((boost::python::handle<>(boost::python::borrowed(PyImport_AddModule("PyTango")))));
    
#define CALL_METHOD(retType, self, name, ...) \
    boost::python::call_method<retType>(self, name , __VA_ARGS__);
    
