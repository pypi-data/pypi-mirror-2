
#include "exception.h"
#include "pytgutils.h"
#include "server/device_impl.h"
#include "server/command.h"

#include <tango.h>

using namespace boost::python;

//+-------------------------------------------------------------------------
//
// method : 		PyCmd::is_allowed
//
// description : 	Decide if it is allowed to execute the command
//
// argin : - dev : The device on which the command has to be excuted
//	   - any : The input data
//
// This method returns a boolean set to True if it is allowed to execute
// the command. Otherwise, returns false
//
//--------------------------------------------------------------------------
bool PyCmd::is_allowed(Tango::DeviceImpl *dev, const CORBA::Any &any)
{
    if (py_allowed_defined == true)
    {
        PyDeviceImplBase *dev_ptr = dynamic_cast<PyDeviceImplBase *>(dev);
        //Device_4ImplWrap *dev_ptr = static_cast<Device_4ImplWrap *>(dev);

        AutoPythonGIL __py_lock;

        bool returned_value = true;
        try
        {
            returned_value = call_method<bool>(dev_ptr->the_self, py_allowed_name.c_str());
        }
        catch(error_already_set &eas)
        {
            handle_python_exception(eas);
        }

        return returned_value;
    }
    else
        return true;
}


void allocate_any(CORBA::Any *&any_ptr)
{
    try
    {
        any_ptr = new CORBA::Any();
    }
    catch (bad_alloc)
    {
        Tango::Except::throw_exception(
            "API_MemoryAllocation",
            "Can't allocate memory in server",
            "PyCmd::allocate_any()");
    }
}

void throw_bad_type(const char *type)
{
    TangoSys_OMemStream o;

    o << "Incompatible command argument type, expected type is : Tango::" 
      << type << ends;
    Tango::Except::throw_exception(
            "API_IncompatibleCmdArgumentType",
            o.str(),
            "PyCmd::extract()");
}

template<long tangoTypeConst>
void insert_scalar(boost::python::object &o, CORBA::Any &any)
{
    typedef typename TANGO_const2type(tangoTypeConst) TangoScalarType;
    
    any <<= extract<TangoScalarType>(o);
}

template<>
void insert_scalar<Tango::DEV_VOID>(boost::python::object &o, CORBA::Any &any)
{}

template<>
void insert_scalar<Tango::DEV_BOOLEAN>(boost::python::object &o, CORBA::Any &any)
{
    Tango::DevBoolean value = extract<Tango::DevBoolean>(o);
    CORBA::Any::from_boolean any_value(value);

    any <<= any_value;
}

template<long tangoTypeConst>
void insert_array(boost::python::object &o, CORBA::Any &any)
{
    typedef typename TANGO_const2type(tangoTypeConst) TangoArrayType;

    auto_ptr<TangoArrayType> data(new TangoArrayType());

    convert2array(o, *data);
    
    // By giving a pointer to <<= we are giving ownership of the data buffer to CORBA
    any <<= data.release();
}

template<long tangoTypeConst>
void extract_scalar(const CORBA::Any &any, boost::python::object &o)
{
    typedef typename TANGO_const2type(tangoTypeConst) TangoScalarType;
    
    TangoScalarType data;
    
    if ((any >>= data) == false)
        throw_bad_type(Tango::CmdArgTypeName[tangoTypeConst]);

    o = object(data);
}

template<>
void extract_scalar<Tango::DEV_STRING>(const CORBA::Any &any, boost::python::object &o)
{
    Tango::ConstDevString data;
    
    if ((any >>= data) == false)
        throw_bad_type(Tango::CmdArgTypeName[Tango::DEV_STRING]);

    o = object(data);
}

template<>
void extract_scalar<Tango::DEV_VOID>(const CORBA::Any &any, boost::python::object &o)
{}

template<long tangoTypeConst>
void extract_array(const CORBA::Any &any, boost::python::object &o)
{
    typedef typename TANGO_const2type(tangoTypeConst) TangoArrayType;
    
    TangoArrayType *data;

    if ((any >>= data) == false)
        throw_bad_type(Tango::CmdArgTypeName[tangoTypeConst]);

    o = object(handle<>(CORBA_sequence_to_list<TangoArrayType>::convert(*data)));
}

CORBA::Any *PyCmd::execute(Tango::DeviceImpl *dev, const CORBA::Any &param_any)
{
    PyDeviceImplBase *dev_ptr = dynamic_cast<PyDeviceImplBase *>(dev);
    
    AutoPythonGIL python_guard;
    
    // This call extracts the CORBA any into a python object.
    // So, the result is that param_py = param_any.
    // It is done with some template magic.
    boost::python::object param_py;
    TANGO_DO_ON_DEVICE_DATA_TYPE(in_type, 
        extract_scalar<tangoTypeConst>(param_any, param_py);
    , 
        extract_array<tangoTypeConst>(param_any, param_py);
    );

    // Execute the python call for the command
    object ret_py_obj;
    try 
    {
        if (in_type == Tango::DEV_VOID)
        {
            ret_py_obj = call_method<object>(dev_ptr->the_self, name.c_str());
        }
        else
        {
            ret_py_obj = call_method<object>(dev_ptr->the_self, name.c_str(), param_py);
        }
    } catch(error_already_set &eas) {
        handle_python_exception(eas);
    }
    
    CORBA::Any *ret_any;
    allocate_any(ret_any);
    std::auto_ptr<CORBA::Any> ret_any_guard(ret_any);
    // It does: ret_any = ret_py_obj
    TANGO_DO_ON_DEVICE_DATA_TYPE(out_type, 
        insert_scalar<tangoTypeConst>(ret_py_obj, *ret_any);
    ,
        insert_array<tangoTypeConst>(ret_py_obj, *ret_any);
    );
        
    return ret_any_guard.release();
}
