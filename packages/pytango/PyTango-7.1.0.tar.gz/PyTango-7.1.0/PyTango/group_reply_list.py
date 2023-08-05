# -*- coding: utf-8 -*-

from utils import document_method as __document_method
from _PyTango import GroupReplyList
from _PyTango import GroupCmdReplyList
from _PyTango import GroupAttrReplyList

def __GroupReplyList__getitem__(self, item):
    # Accessing an item in GroupReplyList and friends makes a C++ copy
    # of the item calling the copy constructor. But the copy constructor
    # of GroupReply is not fair: It extracts the data from the original
    # object!! So, we will only call the original getitem once, the
    # successive calls will just return the cached object.
    try:
        return self.__listCache[item]
    except AttributeError:
        self.__listCache = dict()
    except Exception:
        pass

    r = self.__GroupReplyList_original_getitem__(item)
    self.__listCache[item] = r
    return r

def __GroupReplyList__iter__(self):
    # Same problem as getitem. In this case it is easier for me to just
    # reimplement __iter__ in terms of __getitem__
    for x in xrange(len(self)):
        yield self[x]

def __init_GroupReplyList():
    GroupReplyList.__GroupReplyList_original_getitem__ = GroupReplyList.__getitem__
    GroupReplyList.__getitem__ = __GroupReplyList__getitem__

    GroupCmdReplyList.__GroupReplyList_original_getitem__ = GroupCmdReplyList.__getitem__
    GroupCmdReplyList.__getitem__ = __GroupReplyList__getitem__

    GroupAttrReplyList.__GroupReplyList_original_getitem__ = GroupAttrReplyList.__getitem__
    GroupAttrReplyList.__getitem__ = __GroupReplyList__getitem__

    GroupReplyList.__iter__ = __GroupReplyList__iter__
    GroupCmdReplyList.__iter__ = __GroupReplyList__iter__
    GroupAttrReplyList.__iter__ = __GroupReplyList__iter__

def __doc_GroupReplyList():
    pass

def init_GroupReplyList():
    __init_GroupReplyList()
    __doc_GroupReplyList()
