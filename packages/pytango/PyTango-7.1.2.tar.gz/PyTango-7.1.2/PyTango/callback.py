
from _PyTango import CmdDoneEvent, AttrReadEvent, AttrWrittenEvent
# __CallBackAutoDie, __CallBackPushEvent
from utils import document_method as __document_method


def __init_Callback():
    pass

def __doc_Callback():
    CmdDoneEvent.__doc__ = """
        This class is used to pass data to the callback method in
        asynchronous callback model for command execution.

        It has the following members:
            - device     : (DeviceProxy) The DeviceProxy object on which the call was executed.
            - cmd_name   : (str) The command name
            - argout_raw : (DeviceData) The command argout
            - argout     : The command argout
            - err        : (bool) A boolean flag set to true if the command failed. False otherwise
            - errors     : (sequence<DevError>) The error stack
            - ext        :
    """

    AttrReadEvent.__doc__ = """
        This class is used to pass data to the callback method in
        asynchronous callback model for read_attribute(s) execution.

        It has the following members:
            - device     : (DeviceProxy) The DeviceProxy object on which the call was executed
            - attr_names : (sequence<str>) The attribute name list
            - argout     : (DeviceAttribute) The attribute value
            - err        : (bool) A boolean flag set to true if the command failed. False otherwise
            - errors     : (sequence<DevError>) The error stack
            - ext        :
    """

    AttrWrittenEvent.__doc__ = """
        This class is used to pass data to the callback method in
        asynchronous callback model for write_attribute(s) execution

        It has the following members:
            - device     : (DeviceProxy) The DeviceProxy object on which the call was executed
            - attr_names : (sequence<str>) The attribute name list
            - err        : (bool) A boolean flag set to true if the command failed. False otherwise
            - errors     : (NamedDevFailedList) The error stack
            - ext        :
    """

def init_Callback():
    __init_Callback()
    __doc_Callback()
