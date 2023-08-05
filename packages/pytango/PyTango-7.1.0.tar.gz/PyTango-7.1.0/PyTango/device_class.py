import types, operator

from _PyTango import Except, DevFailed
from _PyTango import _DeviceClass, Database
from _PyTango import CmdArgType, AttrDataFormat, AttrWriteType, DispLevel
from _PyTango import UserDefaultAttrProp

from pyutil import Util

from utils import DbData_2_dict, seqStr_2_obj, obj_2_str, is_array
from utils import document_method as __document_method

from globals import class_list, constructed_class
from globals import get_class, get_constructed_class

def _DeviceClass__get_device_class(dev):
    """
    get_device_class(self, dev) -> DeviceClass

            Gets the DeviceClass for the given device

        Parameters :
            - dev - (DeviceImpl) the device object

        Return     : (DeviceClass) the DeviceClass object for the given device"""
    loop = 0
    for tup in class_list:
        if (tup[1].__name__ == dev.__class__.__name__):
            return constructed_class[loop]
        loop += 1
    return None


class PropUtil:
    """An internal Property util class"""

    scalar_int_types = (CmdArgType.DevShort, CmdArgType.DevUShort,
        CmdArgType.DevInt, CmdArgType.DevLong, CmdArgType.DevULong,)

    scalar_long_types = (CmdArgType.DevLong64, CmdArgType.DevULong64)

    scalar_float_types = (CmdArgType.DevFloat, CmdArgType.DevDouble,)

    scalar_numerical_types = scalar_int_types + scalar_long_types + scalar_float_types

    scalar_str_types = (CmdArgType.DevString, CmdArgType.ConstDevString,)

    scalar_types = scalar_numerical_types + scalar_str_types + \
        (CmdArgType.DevBoolean, CmdArgType.DevEncoded,
         CmdArgType.DevUChar, CmdArgType.DevVoid)

    def __init__(self):
        self.db = None
        if Util._UseDb:
            self.db = Database()

    def set_default_property_values(self, dev_class, class_prop, dev_prop):
        """
            set_default_property_values(self, dev_class, class_prop, dev_prop) -> None

                Sets the default property values

            Parameters :
                - dev_class : (DeviceClass) device class object
                - class_prop : (dict<str,>) class properties
                - dev_prop : (dict<str,>) device properties

            Return     : None
        """
        for name in class_prop.keys():
            type = self.get_property_type(name, class_prop)
            val  = self.get_property_values(name, class_prop)
            val  = self.values2string(val, type)
            desc = self.get_property_description(name, class_prop)
            dev_class.add_wiz_class_prop(name, desc, val)

        for name in dev_prop.keys():
            type = self.get_property_type(name, dev_prop)
            val  = self.get_property_values(name, dev_prop)
            val  = self.values2string(val, type)
            desc = self.get_property_description(name, dev_prop)
            dev_class.add_wiz_dev_prop(name, desc, val)

    def get_class_properties(self, dev_class, class_prop):
        """
            get_class_properties(self, dev_class, class_prop) -> None

                    Returns the class properties

                Parameters :
                    - dev_class : (DeviceClass) the DeviceClass object
                    - class_prop : [in, out] (dict<str, None>) the property names. Will be filled
                                   with property values

                Return     : None"""
        # initialize default values
        if class_prop == {} or Util._UseDb == False:
            return

        # call database to get properties
        props = self.db.get_class_property(dev_class.get_name(), class_prop.keys())

        # if value defined in database, store it
        for name in class_prop.keys():
            if props[name]:
                type   = self.get_property_type(name, class_prop)
                values = self.stringArray2values(props[name], type)
                self.set_property_values(name, class_prop, values)
            else:
                print name, " property NOT found in database"

    def get_device_properties(self, dev, class_prop, dev_prop):
        """
            get_device_properties(self, dev, class_prop, dev_prop) -> None

                    Returns the device properties

                Parameters :
                    - dev : (DeviceImpl) the device object
                    - class_prop : (dict<str, obj>) the class properties
                    - dev_prop : [in,out] (dict<str, None>) the device property names

                Return     : None"""
        #    initialize default properties
        if dev_prop == {} or Util._UseDb == False:
            return

        #    Call database to get properties
        props = self.db.get_device_property(dev.get_name(),dev_prop.keys())
        #    if value defined in database, store it
        for name in dev_prop.keys():
            prop_value = props[name]
            if len(prop_value):
                data_type = self.get_property_type(name, dev_prop)
                values = self.stringArray2values(prop_value, data_type)
                if not self.is_empty_seq(values):
                    self.set_property_values(name, dev_prop, values)
                else:
                    #    Try to get it from class property
                    values = self.get_property_values(name, class_prop)
                    if not self.is_empty_seq(values):
                        if not self.is_seq(values):
                            values = [values]
                        data_type = self.get_property_type(name, class_prop)
                        values = self.stringArray2values(values, data_type)
                        if not self.is_empty_seq(values):
                            self.set_property_values(name, dev_prop, values)
            else:
                    #    Try to get it from class property
                values = self.get_property_values(name, class_prop)
                if not self.is_empty_seq(values):
                    if not self.is_seq(values):
                        values = [values]
                    data_type = self.get_property_type(name, class_prop)
                    values = self.stringArray2values(values, data_type)
                    if not self.is_empty_seq(values):
                        self.set_property_values(name, dev_prop, values)

    def is_seq(self, v):
        """
            is_seq(self, v) -> bool

                    Helper method. Determines if the object is a sequence

                Parameters :
                    - v : (object) the object to be analysed

                Return     : (bool) True if the object is a sequence or False otherwise"""
        return operator.isSequenceType(v)

    def is_empty_seq(self, v):
        """
            is_empty_seq(self, v) -> bool

                    Helper method. Determines if the object is an empty sequence

                Parameters :
                    - v : (object) the object to be analysed

                Return     : (bool) True if the object is a sequence which is empty or False otherwise"""
        return self.is_seq(v) and not len(v)

    def get_property_type(self, prop_name, properties):
        """
            get_property_type(self, prop_name, properties) -> CmdArgType

                    Gets the property type for the given property name using the
                    information given in properties

                Parameters :
                    - prop_name : (str) property name
                    - properties : (dict<str,data>) property data

                Return     : (CmdArgType) the tango type for the given property"""
        try:
            tg_type = properties[prop_name][0]
        except:
            tg_type = CmdArgType.DevVoid
        return tg_type

    def set_property_values(self, prop_name, properties, values):
        """
            set_property_values(self, prop_name, properties, values) -> None

                    Sets the property value in the properties

                Parameters :
                    - prop_name : (str) property name
                    - properties : (dict<str,obj>) [in,out] dict which will contain the value
                    - values : (seq) the new property value

                Return     : None"""

        properties[prop_name][2] = values

    def get_property_values(self, prop_name, properties):
        """
            get_property_values(self, prop_name, properties) -> obj

                    Gets the property value

                Parameters :
                    - prop_name : (str) property name
                    - properties : (dict<str,obj>) properties
                Return     : (obj) the value for the given property name"""
        try:
            tg_type = self.get_property_type(prop_name, properties)
            val  = properties[prop_name][2]
        except:
            val = []

        if is_array(tg_type) or (operator.isSequenceType(val) and not len(val)):
            return val
        else:
            if operator.isSequenceType(val) and not type(val) in types.StringTypes:
                return val[0]
            else:
                return val

    def get_property_description(self, prop_name, properties):
        """
            get_property_description(self, prop_name, properties) -> obj

                    Gets the property description

                Parameters :
                    - prop_name : (str) property name
                    - properties : (dict<str,obj>) properties
                Return     : (str) the description for the given property name"""
        return properties[prop_name][1]

    def stringArray2values(self, argin, argout_type):
        """internal helper method"""
        return seqStr_2_obj(argin, argout_type)

    def values2string(self, argin, argout_type):
        """internal helper method"""
        return obj_2_str(argin, argout_type)

class DeviceClass(_DeviceClass):
    """Base class for all TANGO device-class class.
       A TANGO device-class class is a class where is stored all
       data/method common to all devices of a TANGO device class"""

    def __init__(self, name):
        _DeviceClass.__init__(self,name)
        self.dyn_att_added_methods = []
        try:
            self.prop_util = PropUtil()
            self.py_dev_list = []
            has_cl_prop = hasattr(self,"class_property_list")
            has_dev_prop = hasattr(self,"device_property_list")
            if has_cl_prop and has_dev_prop:
                self.prop_util.set_default_property_values(self,self.class_property_list, self.device_property_list)
                self.prop_util.get_class_properties(self, self.class_property_list)
                for prop_name in self.class_property_list.keys():
                    setattr(self, prop_name, self.prop_util.get_property_values(prop_name, self.class_property_list))
        except DevFailed, e:
            print "----> ", e
    
    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.get_name())
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.get_name())    
    
    def __throw_create_attribute_exception(self, msg):
        """Helper method to throw DevFailed exception when inside create_attribute"""
        Except.throw_exception("PyDs_WrongAttributeDefinition", msg, "create_attribute()")

    def __throw_create_command_exception(self, msg):
        """Helper method to throw DevFailed exception when inside create_command"""
        Except.throw_exception("PyDs_WrongCommandDefinition", msg, "create_command()")

    def __attribute_factory(self, attr_list):
        """for internal usage only"""
        name = self.get_name()
        class_info = get_class(name)
        my_constructed_class = get_constructed_class(name)
        deviceimpl_class = class_info[1]

        for attr_name, attr_info in self.attr_list.iteritems():
            self.__create_attribute(deviceimpl_class, attr_list, attr_name, attr_info)

    def __create_attribute(self, deviceimpl_class, attr_list, attr_name, attr_info):
        """for internal usage only"""
        name = self.get_name()

        # check for well defined attribute info

        # check parameter
        if not operator.isSequenceType(attr_info):
            msg = "Wrong data type for value for describing attribute %s in " \
                  "class %s\nMust be a sequence with 1 or 2 elements" % (attr_name, name)
            self.__throw_create_attribute_exception(msg)

        if len(attr_info) < 1 or len(attr_info) > 2:
            msg = "Wrong number of argument for describing attribute %s in " \
                  "class %s\nMust be a sequence with 1 or 2 elements" % (attr_name, name)
            self.__throw_create_attribute_exception(msg)

        extra_info = {}
        if len(attr_info) == 2:
            # attr_info[1] must be a dictionary
            # extra_info = attr_info[1], with all the keys lowercase
            for k, v in attr_info[1].iteritems():
                extra_info[k.lower()] = v

        attr_info = attr_info[0]

        attr_info_len = len(attr_info)
        # check parameter
        if not operator.isSequenceType(attr_info) or attr_info_len < 3 or attr_info_len > 5:
            msg = "Wrong data type for describing mandatory information for attribute %s " \
                  "in class %s\nMust be a sequence with 3, 4 or 5 elements" % (attr_name, name)
            self.__throw_create_attribute_exception(msg)

        # get data type
        attr_type = CmdArgType.DevVoid
        try:
            attr_type = CmdArgType(attr_info[0])
        except:
            msg = "Wrong data type in attribute argument for attribute %s in " \
                  "class %s\nAttribute data type (first element in first " \
                  "sequence) must be a PyTango.CmdArgType"
            self.__throw_create_attribute_exception(msg)

        # get format
        attr_format = AttrDataFormat.SCALAR
        try:
            attr_format = AttrDataFormat(attr_info[1])
        except:
            msg = "Wrong data format in attribute argument for attribute %s in " \
                  "class %s\nAttribute data format (second element in first " \
                  "sequence) must be a PyTango.AttrDataFormat"
            self.__throw_create_attribute_exception(msg)

        dim_x, dim_y = 1, 0
        if attr_format == AttrDataFormat.SCALAR:
            if attr_info_len != 3:
                msg = "Wrong data type in attribute argument for attribute %s in " \
                      "class %s\nSequence describing mandatory attribute parameters " \
                      "for scalar attribute must have 3 elements"
                self.__throw_create_attribute_exception(msg)
        elif attr_format == AttrDataFormat.SPECTRUM:
            if attr_info_len != 4:
                msg = "Wrong data type in attribute argument for attribute %s in " \
                      "class %s\nSequence describing mandatory attribute parameters " \
                      "for spectrum attribute must have 4 elements"
                self.__throw_create_attribute_exception(msg)
            try:
                dim_x = int(attr_info[3])
            except:
                msg = "Wrong data type in attribute argument for attribute %s in " \
                      "class %s\n4th element in sequence describing mandatory dim_x " \
                      "attribute parameter for spectrum attribute must be an integer"
                self.__throw_create_attribute_exception(msg)
        elif attr_format == AttrDataFormat.IMAGE:
            if attr_info_len != 5:
                msg = "Wrong data type in attribute argument for attribute %s in " \
                      "class %s\nSequence describing mandatory attribute parameters " \
                      "for image attribute must have 5 elements"
                self.__throw_create_attribute_exception(msg)
            try:
                dim_x = int(attr_info[3])
            except:
                msg = "Wrong data type in attribute argument for attribute %s in " \
                      "class %s\n4th element in sequence describing mandatory dim_x " \
                      "attribute parameter for image attribute must be an integer"
                self.__throw_create_attribute_exception(msg)
            try:
                dim_y = int(attr_info[4])
            except:
                msg = "Wrong data type in attribute argument for attribute %s in " \
                      "class %s\n5th element in sequence describing mandatory dim_y " \
                      "attribute parameter for image attribute must be an integer"
                self.__throw_create_attribute_exception(msg)

        #get write type
        attr_write = AttrWriteType.READ
        try:
            attr_write = AttrWriteType(attr_info[2])
        except:
            msg = "Wrong data write type in attribute argument for attribute %s in " \
                  "class %s\nAttribute write type (third element in first " \
                  "sequence) must be a PyTango.AttrWriteType"
            self.__throw_create_attribute_exception(msg)

        # check that the method(s) to be executed exists
        read_method_name = "read_%s" % attr_name
        write_method_name = "write_%s" % attr_name
        is_allowed_name = "is_%s_allowed" % attr_name

        try:
            display_level = DispLevel(extra_info.get("display level", DispLevel.OPERATOR))
        except:
            msg = "Wrong display level in attribute information for attribute %s in " \
                  "class %s\nAttribute information for display level is not a " \
                  "PyTango.DispLevel" % (attr_name, name)
            self.__throw_create_attribute_exception(msg)

        try:
            polling_period = int(extra_info.get("polling period", -1))
        except:
            msg = "Wrong polling period in attribute information for attribute %s in " \
                  "class %s\nAttribute information for polling period is not an " \
                  "integer" % (attr_name, name)
            self.__throw_create_attribute_exception(msg)

        memorized, hw_memorized = extra_info.get("memorized", "false"), False
        if memorized == "true":
            memorized, hw_memorized = True, True
        elif memorized == "true_without_hard_applied":
            memorized = True
        else:
            memorized = False

        att_prop = self.__create_user_default_attr_prop(attr_name, extra_info)

        self._create_attribute(attr_list, attr_name, attr_type, attr_format,
                               attr_write, dim_x, dim_y,
                               display_level, polling_period,
                               memorized, hw_memorized,
                               read_method_name, write_method_name,
                               is_allowed_name,
                               att_prop)

    def __create_user_default_attr_prop(self, attr_name, extra_info):
        """for internal usage only"""
        p = UserDefaultAttrProp()
        for k, v in extra_info.iteritems():
            k_lower = k.lower()
            method_name = "set_%s" % k_lower.replace(' ','_')
            if hasattr(p, method_name):
                method = getattr(p, method_name)
                method(str(v))
            elif k == 'delta_time':
                p.set_delta_t(str(v))
            elif not k_lower in ('display level', 'polling period', 'memorized'):
                name = self.get_name()
                msg = "Wrong definition of attribute %s in " \
                      "class %s\nThe object extra information '%s' " \
                      "is not recognized!" % (attr_name, name, k)
                self.__throw_create_attribute_exception(msg)
        return p

    def __command_factory(self):
        """for internal usage only"""
        name = self.get_name()
        class_info = get_class(name)
        my_constructed_class = get_constructed_class(name)
        deviceimpl_class = class_info[1]

        if not hasattr(deviceimpl_class, "init_device"):
            msg = "Wrong definition of class %s\n" \
                  "The init_device() method does not exist!" % name
            Except.throw_exception("PyDs_WrongCommandDefinition", msg, "command_factory()")

        for cmd_name, cmd_info in self.cmd_list.iteritems():
            self.__create_command(deviceimpl_class, cmd_name, cmd_info)

    def __create_command(self, deviceimpl_class, cmd_name, cmd_info):
        """for internal usage only"""
        name = self.get_name()

        # check for well defined command info

        # check parameter
        if not operator.isSequenceType(cmd_info):
            msg = "Wrong data type for value for describing command %s in " \
                  "class %s\nMust be a sequence with 2 or 3 elements" % (cmd_name, name)
            self.__throw_create_command_exception(msg)

        if len(cmd_info) < 2 or len(cmd_info) > 3:
            msg = "Wrong number of argument for describing command %s in " \
                  "class %s\nMust be a sequence with 2 or 3 elements" % (cmd_name, name)
            self.__throw_create_command_exception(msg)

        param_info, result_info = cmd_info[0], cmd_info[1]

        if not operator.isSequenceType(param_info):
            msg = "Wrong data type in command argument for command %s in " \
                  "class %s\nCommand parameter (first element) must be a sequence" % (cmd_name, name)
            self.__throw_create_command_exception(msg)

        if len(param_info) < 1 or len(param_info) > 2:
            msg = "Wrong data type in command argument for command %s in " \
                  "class %s\nSequence describing command parameters must contain " \
                  "1 or 2 elements"
            self.__throw_create_command_exception(msg)

        param_type = CmdArgType.DevVoid
        try:
            param_type = CmdArgType(param_info[0])
        except:
            msg = "Wrong data type in command argument for command %s in " \
                  "class %s\nCommand parameter type (first element in first " \
                  "sequence) must be a PyTango.CmdArgType"
            self.__throw_create_command_exception(msg)

        param_desc = ""
        if len(param_info) > 1:
            param_desc = param_info[1]
            if not type(param_desc) in types.StringTypes:
                msg = "Wrong data type in command parameter for command %s in " \
                      "class %s\nCommand parameter description (second element " \
                      "in first sequence), when given, must be a string"
                self.__throw_create_command_exception(msg)

        # Check result
        if not operator.isSequenceType(result_info):
            msg = "Wrong data type in command result for command %s in " \
                  "class %s\nCommand result (second element) must be a sequence" % (cmd_name, name)
            self.__throw_create_command_exception(msg)

        if len(result_info) < 1 or len(result_info) > 2:
            msg = "Wrong data type in command result for command %s in " \
                  "class %s\nSequence describing command result must contain " \
                  "1 or 2 elements" % (cmd_name, name)
            self.__throw_create_command_exception(msg)

        result_type = CmdArgType.DevVoid
        try:
            result_type = CmdArgType(result_info[0])
        except:
            msg = "Wrong data type in command result for command %s in " \
                  "class %s\nCommand result type (first element in second " \
                  "sequence) must be a PyTango.CmdArgType" % (cmd_name, name)
            self.__throw_create_command_exception(msg)

        result_desc = ""
        if len(result_info) > 1:
            result_desc = result_info[1]
            if not type(result_desc) in types.StringTypes:
                msg = "Wrong data type in command result for command %s in " \
                      "class %s\nCommand parameter description (second element " \
                      "in second sequence), when given, must be a string" % (cmd_name, name)
                self.__throw_create_command_exception(msg)

        # If it is defined, get addictional dictionnary used for optional parameters
        display_level, default_command, poll_period = DispLevel.OPERATOR, False, -1

        if len(cmd_info) == 3:
            extra_info = cmd_info[2]
            if not operator.isMappingType(extra_info):
                msg = "Wrong data type in command information for command %s in " \
                      "class %s\nCommand information (third element in sequence), " \
                      "when given, must be a dictionary" % (cmd_name, name)
                self.__throw_create_command_exception(msg)

            if len(extra_info) > 3:
                msg = "Wrong data type in command information for command %s in " \
                      "class %s\nThe optional dictionary can not have more than " \
                      "three elements" % (cmd_name, name)
                self.__throw_create_command_exception(msg)

            for info_name, info_value in extra_info.iteritems():
                info_name_lower = info_name.lower()
                if info_name_lower == "display level":
                    try:
                        display_level = DispLevel(info_value)
                    except:
                        msg = "Wrong data type in command information for command %s in " \
                              "class %s\nCommand information for display level is not a " \
                              "PyTango.DispLevel" % (cmd_name, name)
                        self.__throw_create_command_exception(msg)
                elif info_name_lower == "default command":
                    if not type(info_value) in types.StringTypes:
                        msg = "Wrong data type in command information for command %s in " \
                              "class %s\nCommand information for default command is not a " \
                              "string" % (cmd_name, name)
                        self.__throw_create_command_exception(msg)
                    v = info_value.lower()
                    default_command = v == 'true'
                elif info_name_lower == "polling period":
                    try:
                        polling_period = int(info_value)
                    except:
                        msg = "Wrong data type in command information for command %s in " \
                              "class %s\nCommand information for polling period is not an " \
                              "integer" % (cmd_name, name)
                        self.__throw_create_command_exception(msg)
                else:
                    msg = "Wrong data type in command information for command %s in " \
                          "class %s\nCommand information has unknown key " \
                          "%s" % (cmd_name, name, info_name)
                    self.__throw_create_command_exception(msg)

        # check that the method to be executed exists
        try:
            cmd = getattr(deviceimpl_class, cmd_name)
            if not operator.isCallable(cmd):
                msg = "Wrong definition of command %s in " \
                      "class %s\nThe object exists in class but is not " \
                      "a method!" % (cmd_name, name)
                self.__throw_create_command_exception(msg)
        except AttributeError, ae:
            msg = "Wrong definition of command %s in " \
                  "class %s\nThe command method does not exist!" % (cmd_name, name)
            self.__throw_create_command_exception(msg)

        is_allowed_name = "is_%s_allowed" % cmd_name
        try:
            is_allowed = getattr(deviceimpl_class, is_allowed_name)
            if not operator.isCallable(is_allowed):
                msg = "Wrong definition of command %s in " \
                      "class %s\nThe object '%s' exists in class but is " \
                      "not a method!" % (cmd_name, name, is_allowed_name)
                self.__throw_create_command_exception(msg)
        except:
            is_allowed_name = ""

        self._create_command(cmd_name, param_type, result_type,
                             param_desc, result_desc,
                             display_level, default_command,
                             poll_period, is_allowed_name)

    def device_factory(self, devicelist):
        """for internal usage only"""
        loop = 0
        for tup in class_list:
            if (tup[0].__name__ == self.__class__.__name__):
                tup[1].get_device_class = _DeviceClass__get_device_class
                tmp_dev_list = []
                for dev_name in devicelist:
                    self.z = tup[1](constructed_class[loop],dev_name)
                    self.cpp_add_device(self.z)
                    tmp_dev_list.append(self.z)

                self.dyn_attr(tmp_dev_list)

                for dev in tmp_dev_list:
                    if ((Util._UseDb == True) and (Util._FileDb == False)):
                        self.export_device(dev)
                    else:
                        self.export_device(dev,dev.get_name())
                self.py_dev_list = self.py_dev_list + tmp_dev_list
                break
            loop += 1

    def get_device_list(self):
        """for internal usage only"""
        return self.py_dev_list

    def dyn_attr(self,device_list):
        """
            dyn_attr(self,device_list) -> None

                Default implementation does not do anything
                Overwrite in order to provide dynamic attributes

            Parameters :
                - device_list : (seq<DeviceImpl>) sequence of devices of this class

            Return     : None"""
        pass

    def device_destroyer(self,name):
        """for internal usage only"""
        for d in self.py_dev_list:
            if d.get_name() == name:
                dev_cl = d.get_device_class()
                dev_cl._device_destroyer(name)
                self.py_dev_list.remove(d)
                break
            else:
                err_mess = "Device " + name + " not in tango class device list!"
                Except.throw_exception("API_CantDestroyDevice",err_mess,"DeviceClass::device_destroyer")

def __init_DeviceClass():
    pass

def __doc_DeviceClass():
    def document_method(method_name, desc, append=True):
        return __document_method(DeviceClass, method_name, desc, append)

    document_method("export_device", """
    export_device(self, dev, corba_dev_name = 'Unused') -> None

            For internal usage only

        Parameters :
            - dev : (DeviceImpl) device object
            - corba_dev_name : (str) CORBA device name. Default value is 'Unused'

        Return     : None
    """ )

    document_method("register_signal", """
    register_signal(self, signo) -> None

            Register a signal.
            Register this class as class to be informed when signal signo
            is sent to to the device server process

        Parameters :
            - signo : (int) signal identifier

        Return     : None
    """ )

    document_method("unregister_signal", """
    unregister_signal(self, signo) -> None

            Unregister a signal.
            Unregister this class as class to be informed when signal signo
            is sent to to the device server process

        Parameters :
            - signo : (int) signal identifier
        Return     : None
    """ )

    document_method("signal_handler", """
    signal_handler(self, signo) -> None

            Signal handler.

            The method executed when the signal arrived in the device server process.
            This method is defined as virtual and then, can be redefined following
            device class needs.

        Parameters :
            - signo : (int) signal identifier
        Return     : None
    """ )

    document_method("get_name", """
    get_name(self) -> str

            Get the TANGO device class name.

        Parameters : None
        Return     : (str) the TANGO device class name.
    """ )

    document_method("get_type", """
    get_type(self) -> str

            Gets the TANGO device type name.

        Parameters : None
        Return     : (str) the TANGO device type name
    """ )

    document_method("get_doc_url", """
    get_doc_url(self) -> str

            Get the TANGO device class documentation URL.

        Parameters : None
        Return     : (str) the TANGO device type name
    """ )

    document_method("set_type", """
    set_type(self, dev_type) -> None

            Set the TANGO device type name.

        Parameters :
            - dev_type : (str) the new TANGO device type name
        Return     : None
    """ )

    document_method("get_cvs_tag", """
    get_cvs_tag(self) -> str

            Gets the cvs tag

        Parameters : None
        Return     : (str) cvs tag
    """ )

    document_method("get_cvs_location", """
    get_cvs_location(self) -> None

            Gets the cvs localtion

        Parameters : None
        Return     : (str) cvs location
    """ )

    document_method("add_wiz_dev_prop", """
    add_wiz_dev_prop(self, str, str) -> None
    add_wiz_dev_prop(self, str, str, str) -> None

            For internal usage only

        Parameters : None
        Return     : None
    """ )

    document_method("add_wiz_class_prop", """
    add_wiz_class_prop(self, str, str) -> None
    add_wiz_class_prop(self, str, str, str) -> None

            For internal usage only

        Parameters : None
        Return     : None
    """ )

def init_DeviceClass():
    __init_DeviceClass()
    __doc_DeviceClass()
