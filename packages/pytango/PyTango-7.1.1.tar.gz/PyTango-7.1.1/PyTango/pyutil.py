import os, copy

from _PyTango import _Util, Except
from utils import document_method as __document_method
#from utils import document_static_method as __document_static_method
from globals import class_list
from globals import cpp_class_list
from globals import get_constructed_classes

#
# Methods on Util
#

def __Util__get_class_list(self):
    """
        get_class_list(self) -> seq<DeviceClass>

                Returns a list of objects of inheriting from DeviceClass

            Parameters : None

            Return     : (seq<DeviceClass>) a list of objects of inheriting from DeviceClass"""
    return get_constructed_classes()

def __Util__get_device_list_by_class(self,name):
    """
        get_device_list_by_class(self, name) -> seq<DeviceImpl>

                Returns a list of objects of inheriting from DeviceImpl for
                the given Tango class

            Parameters :
                - name : (str) tango class name

            Return     : (seq<DeviceImpl>) a list of objects of inheriting
                         from DeviceImpl for the given Tango class

            Throws     : DevFailed if the Tango class was not found"""
    for cl in self.get_class_list():
        if cl.get_name() == name:
            return cl.get_device_list()

    Except.throw_exception("API_ClassNotFound",
                           "Class " + name + " not found",
                           "Util::get_device_list_by_class")

def __Util__get_device_by_name(self, name):
    """
        get_device_by_name(self, name) -> DeviceImpl

                Returns the DeviceImpl for the given device name

            Parameters :
                - name : (str) tango device name

            Return     : (DeviceImpl) the DeviceImpl for the given device name

            Throws     : DevFailed if the tango device name was not found"""
    cl_list = self.get_class_list()
    dev_list = []
    for cl in cl_list:
        dev_list += cl.get_device_list()

    name_lower = name.lower()
    for dev in dev_list:
        if dev.get_name().lower() == name_lower:
            return dev

    Except.throw_exception("API_DeviceNotFound",
                           "Device " + name + " not found",
                           "Util::get_device_by_name")

class Util(_Util):
    """
        This class is a used to store TANGO device server process data and to
        provide the user with a set of utilities method.

        This class is implemented using the singleton design pattern.
        Therefore a device server process can have only one instance of this
        class and its constructor is not public.

            Example:
                util = PyTango.Util.instance()
                print util.get_host_name()
        """

    def __init__(self, args):
        args = copy.copy(args)
        args[0] = os.path.splitext(args[0])[0]
        _Util.init(args)
        _Util.init_python()

    def add_TgClass(self, klass_device_class, klass_device, device_class_name):
        """Register a new python tango class.
           Example: util.add_TgClass(MotorClass, Motor, 'Motor')"""
        class_list.append((klass_device_class, klass_device, device_class_name))


    def add_Cpp_TgClass(self, device_class_name, tango_device_class_name):
        """Register a new C++ tango class.
           Example:
               if there is a shared library file called MotorClass.so which
               contains a MotorClass class and a _create_MotorClass_class
               method:
               util.add_Cpp_TgClass('MotorClass', 'Motor')
           Note: the parameter 'device_class_name' must match the shared
           library name."""
        cpp_class_list.append((device_class_name, tango_device_class_name))

def __init_Util():
    _Util.get_class_list = __Util__get_class_list
    _Util.get_device_list_by_class = __Util__get_device_list_by_class
    _Util.get_device_by_name = __Util__get_device_by_name

def __doc_Util():
    def document_method(method_name, desc, append=True):
        return __document_method(Util, method_name, desc, append)

#    def document_static_method(method_name, desc, append=True):
#        return __document_static_method(_Util, method_name, desc, append)

#    document_static_method("instance", """
#    instance(exit = True) -> Util
#
#            Static method that gets the singleton object reference.
#            If the class has not been initialised with it's init method,
#            this method print a message and abort the device server process
#
#        Parameters :
#            - exit : (bool)
#
#        Return     : (Util) the tango Util object
#    """ )

    document_method("set_trace_level", """
    set_trace_level(self, level) -> None

            Set the process trace level.

        Parameters :
            - level : (int) the new process level
        Return     : None
    """ )

    document_method("get_trace_level", """
    get_trace_level(self) -> int

            Get the process trace level.

        Parameters : None
        Return     : (int) the process trace level.
    """ )

    document_method("get_ds_inst_name", """
    get_ds_inst_name(self) -> str

            Get a COPY of the device server instance name.

        Parameters : None
        Return     : (str) a COPY of the device server instance name.

        New in PyTango 3.0.4
    """ )

    document_method("get_ds_exec_name", """
    get_ds_exec_name(self) -> str

            Get a COPY of the device server executable name.

        Parameters : None
        Return     : (str) a COPY of the device server executable name.

        New in PyTango 3.0.4
    """ )

    document_method("get_ds_name", """
    get_ds_name(self) -> str

            Get the device server name.
            The device server name is the <device server executable name>/<the device server instance name>

        Parameters : None
        Return     : (str) device server name

        New in PyTango 3.0.4
    """ )

    document_method("get_host_name", """
    get_host_name(self) -> str

            Get the host name where the device server process is running.

        Parameters : None
        Return     : (str) the host name where the device server process is running

        New in PyTango 3.0.4
    """ )

    document_method("get_pid_str", """
    get_pid_str(self) -> str

            Get the device server process identifier as a string.

        Parameters : None
        Return     : (str) the device server process identifier as a string

        New in PyTango 3.0.4
    """ )

    document_method("get_pid", """
    get_pid(self) -> TangoSys_Pid

            Get the device server process identifier.

        Parameters : None
        Return     : (int) the device server process identifier
    """ )

    document_method("get_tango_lib_release", """
    get_tango_lib_release(self) -> int

            Get the TANGO library version number.

        Parameters : None
        Return     : (int) The Tango library release number coded in
                     3 digits (for instance 550,551,552,600,....)
    """ )

    document_method("get_version_str", """
    get_version_str(self) -> str

            Get the IDL TANGO version.

        Parameters : None
        Return     : (str) the IDL TANGO version.

        New in PyTango 3.0.4
    """ )

    document_method("get_server_version", """
    get_server_version(self) -> str

            Get the device server version.

        Parameters : None
        Return     : (str) the device server version.
    """ )

    document_method("set_server_version", """
    set_server_version(self, vers) -> None

            Set the device server version.

        Parameters :
            - vers : (str) the device server version
        Return     : None
    """ )

    document_method("set_serial_model", """
    set_serial_model(self, ser) -> None

            Set the serialization model.

        Parameters :
            - ser : (SerialModel) the new serialization model. The serialization model must
                    be one of BY_DEVICE, BY_CLASS, BY_PROCESS or NO_SYNC
        Return     : None
    """ )

    document_method("get_serial_model", """
    get_serial_model(self) ->SerialModel

            Get the serialization model.

        Parameters : None
        Return     : (SerialModel) the serialization model
    """ )

    document_method("connect_db", """
    connect_db(self) -> None

            Connect the process to the TANGO database.
            If the connection to the database failed, a message is
            displayed on the screen and the process is aborted

        Parameters : None
        Return     : None
    """ )

    document_method("reset_filedatabase", """
    reset_filedatabase(self) -> None

            Reread the file database.

        Parameters : None
        Return     : None
    """ )

    document_method("unregister_server", """
    unregister_server(self) -> None

            Unregister a device server process from the TANGO database.

        Parameters : None
        Return     : None
    """ )

    document_method("get_dserver_device", """
    get_dserver_device(self) -> DServer

            Get a reference to the dserver device attached to the device server process.

        Parameters : None
        Return     : (DServer) the dserver device attached to the device server process

        New in PyTango 7.0.0
    """ )

    document_method("server_init", """
    server_init(self, with_window = False) -> None

            Initialize all the device server pattern(s) embedded in a device server process.

        Parameters :
            - with_window : (bool) default value is False
        Return     : None

        Throws     : DevFailed If the device pattern initialistaion failed
    """ )

    document_method("server_run", """
    server_run(self) -> None

            Run the CORBA event loop.
            This method runs the CORBA event loop. For UNIX or Linux operating system,
            this method does not return. For Windows in a non-console mode, this method
            start a thread which enter the CORBA event loop.

        Parameters : None
        Return     : None
    """ )

    document_method("trigger_cmd_polling", """
    trigger_cmd_polling(self, dev, name) -> None

            Trigger polling for polled command.
            This method send the order to the polling thread to poll one object registered
            with an update period defined as "externally triggerred"

        Parameters :
            - dev : (DeviceImpl) the TANGO device
            - name : (str) the command name which must be polled
        Return     : None

        Throws     : DevFailed If the call failed
    """ )

    document_method("trigger_attr_polling", """
    trigger_attr_polling(self, dev, name) -> None

            Trigger polling for polled attribute.
            This method send the order to the polling thread to poll one object registered
            with an update period defined as "externally triggerred"

        Parameters :
            - dev : (DeviceImpl) the TANGO device
            - name : (str) the attribute name which must be polled
        Return     : None
    """ )

    document_method("set_polling_threads_pool_size", """
    set_polling_threads_pool_size(self, thread_nb) -> None

            Set the polling threads pool size.

        Parameters :
            - thread_nb : (int) the maximun number of threads in the polling threads pool
        Return     : None

        New in PyTango 7.0.0
    """ )

    document_method("get_polling_threads_pool_size", """
    get_polling_threads_pool_size(self) -> int

            Get the polling threads pool size.

        Parameters : None
        Return     : (int) the maximun number of threads in the polling threads pool
    """ )
    
    document_method("get_sub_dev_diag", """
    get_sub_dev_diag(self) -> SubDevDiag

            Get the internal sub device manager

        Parameters : None
        Return     : (SubDevDiag) the sub device manager
        
        New in PyTango 7.0.0
    """ )

    document_method("reset_filedatabase", """
    reset_filedatabase(self) -> None

            Reread the file database

        Parameters : None
        Return     : None
        
        New in PyTango 7.0.0
    """ )

    document_method("get_database", """
    get_database(self) -> Database

            Get a reference to the TANGO database object

        Parameters : None
        Return     : (Database) the database
        
        New in PyTango 7.0.0
    """ )

    document_method("unregister_server", """
    unregister_server(self) -> None

            Unregister a device server process from the TANGO database.
            If the database call fails, a message is displayed on the screen 
            and the process is aborted

        Parameters : None
        Return     : None
        
        New in PyTango 7.0.0
    """ )
    
    document_method("get_device_list_by_class", """
    get_device_list_by_class(self, class_name) -> sequence<DeviceImpl>

            Get the list of device references for a given TANGO class.
            Return the list of references for all devices served by one implementation
            of the TANGO device pattern implemented in the process.
            
        Parameters :
            - class_name : (str) The TANGO device class name
            
        Return     : (sequence<DeviceImpl>) The device reference list
        
        New in PyTango 7.0.0
    """ )
    
    document_method("get_device_by_name", """
    get_device_by_name(self, dev_name) -> DeviceImpl

            Get a device reference from its name

        Parameters :
            - dev_name : (str) The TANGO device name
        Return     : (DeviceImpl) The device reference
        
        New in PyTango 7.0.0
    """ )
    
    document_method("get_dserver_device", """
    get_dserver_device(self) -> DServer

            Get a reference to the dserver device attached to the device server process

        Parameters : None
        Return     : (DServer) A reference to the dserver device
        
        New in PyTango 7.0.0
    """ )
    
    document_method("get_device_list", """
    get_device_list(self) -> sequence<DeviceImpl>

            Get device list from name.
            It is possible to use a wild card ('*') in the name parameter
            (e.g. "*", "/tango/tangotest/n*", ...)
            
        Parameters : None
        Return     : (sequence<DeviceImpl>) the list of device objects
        
        New in PyTango 7.0.0
    """ )
    
#    document_static_method("init_python", """
#    init_python() -> None
#
#            Static method
#            For internal usage.
#
#        Parameters : None
#        Return     : None
#    """ )

def init_PyUtil():
    __init_Util()
    __doc_Util()
