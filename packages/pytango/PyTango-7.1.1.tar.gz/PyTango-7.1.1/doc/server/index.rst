
.. currentmodule:: PyTango

.. highlight:: python
   :linenothreshold: 3
   
The Tango Device Server Python API
==================================

This chapter does not explain what a Tango device or a device server is. 
This is explained in details in "The Tango control system manual" available at 
http://www.tango-controls.org/TangoKernel.
The device server we will detailed in the following example is a Tango device 
server with one Tango class called PyDsExp. This class has two commands called 
IOLong and IOStringArray and two attributes called Long_attr and Short_attr_rw.

Importing python modules
------------------------

To write a Python script which is a Tango device server, you need to import two modules which are :

1. The PyTango module which is the Python to C++ interface
2. The Python classical sys module

This could be done with code like (supposing the PYTHONPATH environment variable is correctly set)::

    import PyTango
    import sys

The main part of a Python device server
---------------------------------------

The rule of this part of a Tango device server is to:
- Create the PyUtil object passing it the Python interpreter command line arguments
- Add to this object the list of Tango class(es) which have to be hosted by this interpreter
- Initialise the device server
- Run the device server loop

The following is a typical code for this main function::

    if __name__ == '__main__':
        py = PyTango.Util(sys.argv)
        py.add_TgClass(PyDsExpClass,PyDsExp,'PyDsExp')
        
        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

**Line 2**
    Create the Util object passing it the interpreter command line arguments
**Line 3**
    Add the Tango class 'PyDsExp' to the device server. The add_TgClass() 
    method of the Util class has three arguments which are the Tango class 
    PyDsExpClass instance, the Tango PyDsExp instance and the Tango class name
**Line 6**
    Initialise the Tango device server
**Line 7**
    Run the device server loop

The PyDsExpClass class in Python
--------------------------------

The rule of this class is to :
- Host and manage data you have only once for the Tango class whatever devices of this class will be created
- Define Tango class command(s)
- Define Tango class attribute(s)

In our example, the code of this Python class looks like::

    class PyDsExpClass(PyTango.DeviceClass):

        cmd_list = { 'IOLong' : [ [ PyTango.ArgType.DevLong, "Number" ],
                                  [ PyTango.ArgType.DevLong, "Number * 2" ] ],
                     'IOStringArray' : [ [ PyTango.ArgType.DevVarStringArray, "Array of string" ],
                                         [ PyTango.ArgType.DevVarStringArray, "This reversed array"] ],
        }

        attr_list = { 'Long_attr' : [ [ PyTango.ArgType.DevLong ,
                                        PyTango.AttrDataFormat.SCALAR ,
                                        PyTango.AttrWriteType.READ],
                                      { 'min alarm' : 1000, 'max alarm' : 1500 } ],

                     'Short_attr_rw' : [ [ PyTango.ArgType.DevShort,
                                           PyTango.AttrDataFormat.SCALAR,
                                           PyTango.AttrWriteType.READ_WRITE ] ]
        }

**Line 1** 
    The PyDsExpClass class has to inherit from the PyTango.PyDeviceClass class
    
**Line 3 to 7**
    Definition of the cmd_list dictionnary defining commands. The IOLong command 
    is defined at lines 3 and 4. The IOStringArray command is defined in line 5 and 6
**Line 10 to 16**
    Definition of the attr_list dictionnary defining attributes. The Long_attr 
    attribute is defined at lines 8 to 11 and the Short_attr_rw attribute is 
    defined at lines 13 to 15
    
If you have something specific to do in the class constructor like
initializing some specific data member, you will have to code a class 
constructor. An example of such a contructor is ::

    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type("TestDevice")

The device type is set at line 3.

Defining commands
-----------------

As shown in the previous example, commands have to be defined in a dictionary called *cmd_list* as a data
member of the xxxClass class of the Tango class. This dictionary has one element per command. The element
key is the command name. The element value is a Python list which defines the command. The generic form
of a command definition is:
    
    ``'cmd_name' : [ [in_type, <"In desc">], [out_type, <"Out desc">], <{opt parameters}>]``

The first element of the value list is itself a list with the command input data type (one of the PyTango.ArgType
pseudo enumeration value) and optionally a string describing this input argument. The second element of the
value list is also a list with the command output data type (one of the PyTango.ArgType pseudo enumeration
value) and optionally a string describing it.        These two elements are mandatory.   The third list element is
optional and allows additional command definition. The authorized element for this dictionary are summarized
in the following array:

    +-------------------+----------------------+------------------------------------------+
    |      key          |        Value         |             Definition                   |
    +===================+======================+==========================================+
    | "display level"   | DispLevel enum value |       The command display level          |
    +-------------------+----------------------+------------------------------------------+
    | "polling period"  | Any number           |     The command polling period (mS)      |
    +-------------------+----------------------+------------------------------------------+
    | "default command" | True or False        | To define that it is the default command |
    +-------------------+----------------------+------------------------------------------+

Defining attributes
-------------------

                                                                                         
As shown in the previous example, attributes have to be defined in a dictionary called **attr_list** as a data
member of the xxxClass class of the Tango class. This dictionary has one element per attribute. The element
key is the attribute name. The element value is a Python list which defines the attribute. The generic form of
an attribute definition is:

    ``'attr_name' : [ [mandatory parameters], <{opt parameters}>]``

For any kind of attributes, the mandatory parameters are:

    ``[attr data type, attr data format, attr data R/W type]``
    
The attribute data type is one of the possible value for attributes of the PyTango.ArgType pseudo enunmeration.
The attribute data format is one of the possible value of the PyTango.AttrDataFormat pseudo enumeration and
the attribute R/W type is one of the possible value of the PyTango.AttrWriteType pseudo enumeration. For
spectrum attribute, you have to add the maximum X size (a number). For image attribute, you have to add
the maximun X and Y dimension (two numbers). The authorized elements for the dictionnary defining optional
parameters are summarized in the following array

+-------------------+-----------------------------------+------------------------------------------+
|       key         |              value                |            definition                    |
+===================+===================================+==========================================+
| "display level"   | PyTango.DispLevel enum value      |   The attribute display level            |
+-------------------+-----------------------------------+------------------------------------------+
|"polling period"   |          Any number               | The attribute polling period (mS)        |
+-------------------+-----------------------------------+------------------------------------------+
|  "memorized"      | True or True_without_hard_applied | Define if and how the att. is memorized  |
+-------------------+-----------------------------------+------------------------------------------+
|     "label"       |            A string               |       The attribute label                |
+-------------------+-----------------------------------+------------------------------------------+
|  "description"    |            A string               |   The attribute description              |
+-------------------+-----------------------------------+------------------------------------------+
|     "unit"        |            A string               |       The attribute unit                 |
+-------------------+-----------------------------------+------------------------------------------+
|"standard unit"    |           A number                |  The attribute standard unit             |
+-------------------+-----------------------------------+------------------------------------------+
| "display unit"    |            A string               |   The attribute display unit             |
+-------------------+-----------------------------------+------------------------------------------+
|    "format"       |            A string               | The attribute display format             |
+-------------------+-----------------------------------+------------------------------------------+
|  "max value"      |          A number                 |   The attribute max value                |
+-------------------+-----------------------------------+------------------------------------------+
|   "min value"     |           A number                |    The attribute min value               |
+-------------------+-----------------------------------+------------------------------------------+
|  "max alarm"      |           A number                |    The attribute max alarm               |
+-------------------+-----------------------------------+------------------------------------------+
|  "min alarm"      |           A number                |    The attribute min alarm               |
+-------------------+-----------------------------------+------------------------------------------+
| "min warning"     |           A number                |  The attribute min warning               |
+-------------------+-----------------------------------+------------------------------------------+
|"max warning"      |           A number                |  The attribute max warning               |
+-------------------+-----------------------------------+------------------------------------------+
|  "delta time"     |           A number                | The attribute RDS alarm delta time       |
+-------------------+-----------------------------------+------------------------------------------+
|   "delta val"     |           A number                | The attribute RDS alarm delta val        |
+-------------------+-----------------------------------+------------------------------------------+

The PyDsExp class in Python
---------------------------

The rule of this class is to implement methods executed by commands and attributes.
In our example, the code of this class looks like::

    class PyDsExp(PyTango.Device_4Impl):

        def __init__(self,cl,name):
            PyTango.Device_4Impl.__init__(self, cl, name)
            print 'In PyDsExp __init__'
            PyDsExp.init_device(self)

        def init_device(self):
            print 'In Python init_device method'
            self.set_state(PyTango.DevState.ON)
            self.attr_short_rw = 66
            self.attr_long = 1246

    #------------------------------------------------------------------

        def delete_device(self):
            print "[Device delete_device method] for device",self.get_name()

    #------------------------------------------------------------------
    # COMMANDS
    #------------------------------------------------------------------

        def is_IOLong_allowed(self):
            return self.get_state() == PyTango.DevState.ON

        def IOLong(self, in_data):
            print "[IOLong::execute] received number",in_data
            in_data = in_data * 2;
            print "[IOLong::execute] return number",in_data
            return in_data;

    #------------------------------------------------------------------

        def is_IOStringArray_allowed(self):
            return self.get_state() == PyTango.DevState.ON

        def IOStringArray(self, in_data):
            l = range(len(in_data)-1, -1, -1);
            out_index=0
            out_data=[]
            for i in l:
                print "[IOStringArray::execute] received String",in_data[out_index]
                out_data.append(in_data[i])
                print "[IOStringArray::execute] return String",out_data[out_index]
                out_index += 1
            self.y = out_data
            return out_data

    #------------------------------------------------------------------
    # ATTRIBUTES
    #------------------------------------------------------------------

        def read_attr_hardware(self, data):
            print 'In read_attr_hardware'

    #------------------------------------------------------------------

        def read_Long_attr(self, the_att):
            print "[PyDsExp::read_attr] attribute name Long_attr"

            # Before PyTango 7.0.0
            #PyTango.set_attribute_value(the_att, self.attr_long)

            # Now:
            the_att.set_value(self.attr_long)

    #------------------------------------------------------------------

        def read_Short_attr_rw(self, the_att):
            print "[PyDsExp::read_attr] attribute name Short_attr_rw"

            # Before PyTango 7.0.0
            #PyTango.set_attribute_value(the_att, self.attr_short_rw)
            
            # Now:
            the_att.set_value(self.attr_short_rw)

    #------------------------------------------------------------------

        def write_Short_attr_rw(self, the_att):
            print "In write_Short_attr_rw for attribute ",the_att.get_name()

            # Before PyTango 7.0.0
            #data = []
            #PyTango.get_write_value(the_att, data)

            # Now:
            data = the_att.get_write_value()
            self.attr_short_rw = data[0]

**Line 1**
    The PyDsExp class has to inherit from the PyTango.Device_4Impl
**Line 3 to 6**
    PyDsExp class constructor. Note that at line 6, it calls the *init_device()* 
    method
**Line 8 to 12**
    The init_device() method. It sets the device state (line 9) and initialises 
    some data members
**Line 16 to 17**
    The delete_device() method. This method is not mandatory. You define it 
    only if you have to do something specific before the device is destroyed
**Line 23 to 30**
    The two methods for the IOLong command. The first method is called 
    *is_IOLong_allowed()* and it is the command is_allowed method (line 23 to 24). 
    The second method has the same name than the command name. It is the method 
    which executes the command. The command input data type is a Tango long
    and therefore, this method receives a Python integer.
**Line 34 to 47**
    The two methods for the IOStringArray command. The first method is its 
    is_allowed method (Line 34 to 35). The second one is the command 
    execution method (Line 37 to 47). The command input data type is a String 
    array. Therefore, the method receives the array in a Python list of Python
    strings.
**Line 53 to 54**
    The *read_attr_hardware()* method. Its argument is a Python sequence of 
    Python integer.
**Line 58 to 65**
    The method executed when the Long_attr attribute is read. Note that before
    PyTango 7 it sets the attribute value with the PyTango.set_attribute_value
    function. Now the same can be done using the set_value of the attribute
    object
**Line 69 to 76**
    The method executed when the Short_attr_rw attribute is read.
**Line 80 to 89**
    The method executed when the Short_attr_rw attribute is written. 
    Note that before PyTango 7 it gets the attribute value with a call to the 
    Attribute method *get_write_value* with a list as argument. Now the write 
    value can be obtained as the return value of the *get_write_value* call. And
    in case it is a scalar there is no more the need to extract it from the list.

General methods
###############

The following array summarizes how the general methods we have in a Tango 
device server are implemented in Python.

+----------------------+-------------------------+-------------+-----------+
|         Name         | Input par (with "self") |return value | mandatory |
+======================+=========================+=============+===========+
|      init_device     |        None             |   None      |  Yes      |
+----------------------+-------------------------+-------------+-----------+
|     delete_device    |        None             |   None      |  No       |
+----------------------+-------------------------+-------------+-----------+
| always_executed_hook |        None             |   None      |  No       |
+----------------------+-------------------------+-------------+-----------+
|    signal_handler    |   Python integer        |   None      |  No       |
+----------------------+-------------------------+-------------+-----------+
| read_attr_hardware   | Python list of integer  |   None      |  No       |
+----------------------+-------------------------+-------------+-----------+

Implementing a command
######################

Commands are defined as described above. Nevertheless, some methods implementing 
them have to be written. These methods names are fixed and depend on command 
name. They have to be called:

    ``is_<Cmd_name>_allowed`` and ``<Cmd_name>``

For instance, with a command called MyCmd, its is_allowed method has to be 
called is_MyCmd_allowed and its execution method has to be called simply MyCmd. 
The following array gives some more info on these methods.

+-----------------------+-------------------------+--------------------+-----------+
|        Name           | Input par (with "self") | return value       | mandatory |
+=======================+=========================+====================+===========+
| is_<Cmd_name>_allowed |        None             | Python boolean     |  No       |
+-----------------------+-------------------------+--------------------+-----------+
|      Cmd_name         | Depends on cmd type     |Depends on cmd type |  Yes      |
+-----------------------+-------------------------+--------------------+-----------+

Tango has more data types than Python which is more dynamic. The input and
output values of the commands are translated according to the array below.
Not that if PyTango is compiled with numpy support the numpy type will be
the used for the input arguments. Also, it is recomended to use numpy arrays
of the appropiate type for output arguments as well, as it is much more efficient.

+-------------------------+-------------------------------------------+
|   Tango data type       |              Python type                  |
+=========================+===========================================+
|          DEV_VOID       |                    No data                |
+-------------------------+-------------------------------------------+
|       DEV_BOOLEAN       | bool                                      |
+-------------------------+-------------------------------------------+
|         DEV_SHORT       | int                                       |
+-------------------------+-------------------------------------------+
|         DEV_LONG        | int                                       |
+-------------------------+-------------------------------------------+
|        DEV_LONG64       | long (on a 32 bits computer) or           |
|                         | int (on a 64 bits computer)               |
+-------------------------+-------------------------------------------+
|         DEV_FLOAT       | float                                     |
+-------------------------+-------------------------------------------+
|       DEV_DOUBLE        | float                                     |
+-------------------------+-------------------------------------------+
|        DEV_USHORT       | int                                       |
+-------------------------+-------------------------------------------+
|        DEV_ULONG        | int                                       |
+-------------------------+-------------------------------------------+
|        DEV_ULONG64      | long (on a 32 bits computer) or           |
|                         | int (on a 64 bits computer)               |
+-------------------------+-------------------------------------------+
|        DEV_STRING       | str                                       |
+-------------------------+-------------------------------------------+
|    DEVVAR_CHARARRAY     | numpy.array(dtype=numpy.uint8) or         |
|                         | sequence<int>                             |
+-------------------------+-------------------------------------------+
|    DEVVAR_SHORTARRAY    | numpy.array(dtype=numpy.int16) or         |
|                         | sequence<int>                             |
+-------------------------+-------------------------------------------+
|    DEVVAR_LONGARRAY     | numpy.array(dtype=numpy.int32) or         |
|                         | sequence<int>                             |
+-------------------------+-------------------------------------------+
|   DEVVAR_LONG64ARRAY    | numpy.array(dtype=numpy.int64) or         |
|                         | sequence<long> (on a 32 bits computer) or |
|                         | sequence<int> (on a 64 bits computer)     |
+-------------------------+-------------------------------------------+
|    DEVVAR_FLOATARRAY    | numpy.array(dtype=numpy.float32) or       |
|                         | sequence<float>                           |
+-------------------------+-------------------------------------------+
|   DEVVAR_DOUBLEARRAY    | numpy.array(dtype=numpy.float64) or       |
|                         | sequence<float>                           |
+-------------------------+-------------------------------------------+
|   DEVVAR_USHORTARRAY    | numpy.array(dtype=numpy.uint16) or        |
|                         | sequence<int>                             |
+-------------------------+-------------------------------------------+
|   DEVVAR_ULONGARRAY     | numpy.array(dtype=numpy.uint32) or        |
|                         | sequence<int>                             |
+-------------------------+-------------------------------------------+
|  DEVVAR_ULONG64ARRAY    | numpy.array(dtype=numpy.uint64) or        |
|                         | sequence<long> (on a 32 bits computer) or |
|                         | sequence<int> (on a 64 bits computer)     |
+-------------------------+-------------------------------------------+
|   DEVVAR_STRINGARRAY    | sequence<str>                             |
+-------------------------+-------------------------------------------+
|                         | A sequence with two elements:             |
| DEVVAR_LONGSTRINGARRAY  |  1. numpy.array(dtype=numpy.int32) or     |
|                         |     sequence<int>                         |
|                         |  2. sequence<str>                         |
+-------------------------+-------------------------------------------+
|                         | A sequence with two elements:             |
|DEVVAR_DOUBLESTRINGARRAY |  1. numpy.array(dtype=numpy.float32) or   |
|                         |     sequence<float>                       |
|                         |  2. sequence<str>                         |
+-------------------------+-------------------------------------------+

The following code is an example of how you write code executed when a client
read an attribute which is called Long_attr::

    def read_Long_attr(self, the_att):
        print "[PyDsExp::read_attr] attribute name Long_attr"
        the_att.set_value(self.attr_long)

**Line 1**
    Method declaration with "the_att" being an instance of the Attribute class 
    representing the Long_attr attribute
**Line 3**
    Set the attribute value using the method set_value() with the attribute 
    value as parameter
    
The following code is an example of how you write code executed when a client 
write the Short_attr_rw attribute::

    def write_Short_attr_rw(self, the_att):
        print "In write_Short_attr_rw for attribute ",the_att.get_name()
        self.attr_short_rw = the_att.get_write_value()

**Line 1**
    Method declaration with "the_att" being an instance of the Attribute class 
    representing the Short_attr_rw attribute
**Line 3**
    Get the value sent by the client using the method *get_write_value()* and
    store it in the device object. Our attribute is a scalar short attribute so
    the return value is an int.

Implementing an attribute
#########################

Attributes are defined as described in chapter 5.3.2. Nevertheless, some methods
implementing them have to be written. These methods names are fixed and depend 
on attribute name. They have to be called:

    ``is_<Attr_name>_allowed`` and ``read_<Attr_name>`` or/and ``write_<Attr_name>``

For instance, with an attribute called MyAttr, its is_allowed method has to be 
called is_MyAttr_allowed, its read method has to be called read_MyAttr and 
its write method has to be called write_MyAttr. The following array gives some 
more info on these methods.

+-------------+-------------+--------------------+
| data format | data type   |  python type       |
+=============+=============+====================+
| SCALAR      | DEV_BOOLEAN | bool               |
|             +-------------+--------------------+
|             | DEV_UCHAR   | int                |
|             +-------------+--------------------+
|             | DEV_SHORT   | int                |
|             +-------------+--------------------+
|             | DEV_USHORT  | int                |
|             +-------------+--------------------+
|             | DEV_LONG    | int                |
|             +-------------+--------------------+
|             | DEV_ULONG   | int                |
|             +-------------+--------------------+
|             | DEV_LONG64  | int/long           |
|             +-------------+--------------------+
|             | DEV_ULONG64 | int/long           |
|             +-------------+--------------------+
|             | DEV_FLOAT   | float              |
|             +-------------+--------------------+
|             | DEV_DOUBLE  | float              |
|             +-------------+--------------------+
|             | DEV_STRING  | str                |
+-------------+-------------+--------------------+
| SPECTRUM    | DEV_BOOLEAN | sequence<bool>     |
| or          +-------------+--------------------+
| IMAGE       | DEV_UCHAR   | sequence<int>      |
|             +-------------+--------------------+
|             | DEV_SHORT   | sequence<int>      |
|             +-------------+--------------------+
|             | DEV_USHORT  | sequence<int>      |
|             +-------------+--------------------+
|             | DEV_LONG    | sequence<int>      |
|             +-------------+--------------------+
|             | DEV_ULONG   | sequence<int>      |
|             +-------------+--------------------+
|             | DEV_LONG64  | sequence<int/long> |
|             +-------------+--------------------+
|             | DEV_ULONG64 | sequence<int/long> |
|             +-------------+--------------------+
|             | DEV_FLOAT   | sequence<float>    |
|             +-------------+--------------------+
|             | DEV_DOUBLE  | sequence<float>    |
|             +-------------+--------------------+
|             | DEV_STRING  | sequence<str>      |
+-------------+-------------+--------------------+

For SPECTRUM and IMAGES the actual sequence object used depends on the context 
where the tango data is used, and the availability of ``numpy``.

1. for properties the sequence is always a ``list``
    Example:
    
    >>> import PyTango
    >>> db = PyTango.Database()
    >>> s = db.get_property(["TangoSynchrotrons"])
    >>> print type(s)
    <type 'list'>

2. for attribute/command values
    - ``numpy.ndarray`` if PyTango was compiled with numpy support (default) and ``numpy`` is installed.
    - ``list`` otherwise
    
The following code is an example of how you write code executed when a client read an attribute which is
called Long_attr::
    
    def read_Long_attr(self, the_att):
        print "[PyDsExp::read_attr] attribute name Long_attr"
        the_att.set_value(self.attr_long)

**Line 1**
    Method declaration with "the_att" being an instance of the Attribute
    class representing the Long_attr attribute
**Line 3**
    Set the attribute value using the method set_value() with the attribute 
    value as parameter.
    
The following code is an example of how you write code executed when a client 
write the Short_attr_rw attribute::

    def write_Short_attr_rw(self,the_att):
        print "In write_Short_attr_rw for attribute ",the_att.get_name()
        self.attr_short_rw = the_att.get_write_value(data)

**Line 1**
       Method declaration with "the_att" being an instance of the Attribute 
       class representing the Short_attr_rw attribute
**Line 3**
    Get the value sent by the client using the method get_write_value() and
    store the value written in the device object. Our attribute is a scalar 
    short attribute so the return value is an int

Dynamic attributes
##################

It is also possible to create dynamic attributes within a Python device server. 
There are several ways to create dynamic attributes. One of the way, is to 
create all the devices within a loop, then to create the dynamic attributes and
finally to make all the devices available for the external world. In C++ device
server, this is typically done within the <Device>Class::device_factory() method.
In Python device server, this method is generic and the user does not have one.
Nevertheless, this generic device_factory method calls a method named dyn_attr()
allowing the user to create his dynamic attributes. It is simply necessary to
re-define this method within your <Device>Class and to create the dynamic 
attribute within this method:

    ``dyn_attr(self, dev_list)``
    
    where dev_list is a list containing all the devices created by the 
    generic device_factory() method.

There is another point to be noted regarding dynamic attribute within Python 
device server. The Tango Python device server core checks that for each 
attribute it exists methods named <attribute_name>_read and/or <attribute_name>_write and/or 
is_<attribute_name>_allowed. Using dynamic attribute, it is not possible to 
define these methods because attributes name and number are known only at run-time. 
To address this issue, the Device_3Impl::add_attribute() method has a diferent
signature for Python device server which is:

    ``add_attribute(self, attr, r_meth = None, w_meth = None, is_allo_meth = None)``
    
    attr is an instance of the Attr class, r_meth is the method which has to be 
    executed with the attribute is read, w_meth is the method to be executed 
    when the attribute is written and is_allo_meth is the method to be executed
    to implement the attribute state machine. The method passed here as argument
    as to be class method and not object method. Which argument you have to use 
    depends on the type of the attribute (A WRITE attribute does not need a 
    read method). Note, that depending on the number of argument you pass to this
    method, you may have to use Python keyword argument. The necessary methods 
    required by the Tango Python device server core will be created automatically
    as a forward to the methods given as arguments.

Mixing Tango classes (Python and C++) in a Python Tango device server
---------------------------------------------------------------------

Within the same python interpreter, it is possible to mix several Tango classes. 
Here is an example of the main function of a device server with two Tango classes
called IRMiror and PLC::

    import PyTango
    import sys

    if __name__ == '__main__':
        py = PyTango.Util(sys.argv)
        py.add_TgClass(PLCClass,PLC,'PLC')
        py.add_TgClass(IRMirrorClass,IRMirror,'IRMirror')
        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

:Line 6: The Tango class PLC is registered in the device server
:Line 7: The Tango class IRMirror is registered in the device server

It is also possible to add C++ Tango class in a Python device server as soon as:
    1. The Tango class is in a shared library
    2. It exist a C function to create the Tango class

For a Tango class called MyTgClass, the shared library has to be called 
MyTgClass.so and has to be in a directory listed in the LD_LIBRARY_PATH 
environment variable. The C function creating the Tango class has to be called 
_create_MyTgClass_class() and has to take one parameter of type "char \*" which 
is the Tango class name. Here is an example of the main function of the same 
device server than before but with one C++ Tango class called SerialLine::

    import PyTango
    import sys
    
    if __name__ == '__main__':
        py = PyTango.Util(sys.argv)
        py.add_Cpp_TgClass('SerialLine', 'SerialLine')
        py.add_TgClass(PLCClass, PLC, 'PLC')
        py.add_TgClass(IRMirrorClass, IRMirror, 'IRMirror')
        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

:Line 6: The C++ class is registered in the device server
:Line 8 and 9: The two Python classes are registered in the device server

Server API
----------

.. toctree::
    :maxdepth: 2

    device
    device_class
    attribute
    util
