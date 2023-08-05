from _PyTango import *
from release import Release

__author__ = "\n".join([ "%s <%s>" % x for x in Release.authors.values()])
__version__ = Release.version
__version_number__ = Release.version_number
__version_description__  = Release.version_description
__doc__ = Release.long_description

from base_types import init_base_types as __init_base_types
from pytango_pprint import init_pprint as __init_pprint
from db import init_db as __init_db
from connection import init_Connection as __init_Connection
from device_proxy import init_DeviceProxy as __init_DeviceProxy
from attribute_proxy import init_AttributeProxy as __init_AttributeProxy, AttributeProxy
from group import init_Group as __init_Group, Group
from pyutil import init_PyUtil as __init_PyUtil
from device_server import ChangeEventProp, PeriodicEventProp, ArchiveEventProp
from device_server import AttributeAlarm, EventProperties
from device_server import AttributeConfig, AttributeConfig_2, AttributeConfig_3
from device_server import init_DeviceServer as __init_DeviceServer
from group_reply import init_GroupReply as __init_GroupReply
from group_reply_list import init_GroupReplyList as __init_GroupReplyList
from device_attribute import init_DeviceAttribute as __init_DeviceAttribute
from device_data import init_DeviceData as __init_DeviceData
from pyutil import Util
from device_class import DeviceClass
from device_class import init_DeviceClass as __init_DeviceClass
from callback import init_Callback as __init_Callback
from time_val import __init_TimeVal

from globals import get_class, get_classes
from globals import get_cpp_class, get_cpp_classes
from globals import get_constructed_class, get_constructed_classes
from globals import class_factory, delete_class_list
from globals import class_list, cpp_class_list, constructed_class

from utils import is_scalar as is_scalar_type
from utils import is_array as is_array_type
from utils import is_numerical as is_numerical_type
from utils import is_int as is_int_type
from utils import is_float as is_float_type
from utils import obj_2_str, seqStr_2_obj

from tango_numpy import NumpyType, numpy_type, numpy_spectrum, numpy_image

ArgType = _PyTango.CmdArgType

def __init():
    __init_base_types()
    __init_pprint()
    __init_db()
    __init_Connection()
    __init_DeviceProxy()
    __init_AttributeProxy()
    __init_Group()
    __init_PyUtil()
    __init_DeviceServer()
    __init_DeviceClass()
    __init_DeviceAttribute()
    __init_DeviceData()
    __init_GroupReply()
    __init_GroupReplyList()
    __init_Callback()
    __init_TimeVal()

__init()
