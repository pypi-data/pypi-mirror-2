import types, operator

from _PyTango import StdStringVector
from _PyTango import Database, DbDatum, DbData
from _PyTango import DbDevInfo, DbDevInfos
from _PyTango import DbDevImportInfo, DbDevExportInfo
from _PyTango import DbHistory, DbServerInfo

from utils import seq_2_StdStringVector
from utils import seq_2_DbDevInfos
from utils import DbData_2_dict
from utils import document_method as __document_method

#-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
# DbDatum extension
#-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

def __DbDatum___setitem__(self, k, v):
    self.value_string[k] = v

def __DbDatum___delitem__(self, k):
    self.value_string.__delitem__(k)

def __DbDatum_append(self, v):
    self.value_string.append(v)

def __DbDatum_extend(self, v):
    self.value_string.extend(v)

def __DbDatum___imul__(self, n):
    self.value_string *= n

def __init_DbDatum():
    DbDatum.__len__      = lambda self : len(self.value_string)
    DbDatum.__getitem__  = lambda self, k : self.value_string[k]
    DbDatum.__setitem__  = __DbDatum___setitem__
    DbDatum.__delitem__  = __DbDatum___delitem__
    DbDatum.__iter__     = lambda self : self.value_string.__iter__()
    DbDatum.__contains__ = lambda self, v : self.value_string.__contains__(v)
    DbDatum.__add__      = lambda self, seq : self.value_string + seq
    DbDatum.__mul__      = lambda self, n : self.value_string * n
    DbDatum.__imul__     = __DbDatum___imul__
    DbDatum.append       = __DbDatum_append
    DbDatum.extend       = __DbDatum_extend
    
#    DbDatum.__str__      = __DbDatum___str__
#    DbDatum.__repr__      = __DbDatum___repr__

#-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
# Database extension
#-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

def __Database__add_server(self, servname, dev_info):
    """
        add_server( self, servname, dev_info) -> None

                Add a (group of) devices to the database.

            Parameters :
                - servname : (str) server name
                - dev_info : (sequence<DbDevInfo> | DbDevInfos | DbDevInfo) containing the server device(s) information
            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """

    if not operator.isSequenceType(dev_info) and \
       not isinstance(dev_info, DbDevInfo):
        raise TypeError('value must be a DbDevInfos, a seq<DbDevInfo> or ' \
                        'a DbDevInfo')

    if isinstance(dev_info, DbDevInfos):
        pass
    elif isinstance(dev_info, DbDevInfo):
        dev_info = seq_2_DbDevInfos((dev_info,))
    else:
        dev_info = seq_2_DbDevInfos(dev_info)
    self._add_server(servname, dev_info)

def __Database__export_server(self, dev_info):
    """
        export_server(self, dev_info) -> None

                Export a group of devices to the database.

            Parameters :
                - devinfo : (sequence<DbDevExportInfo> | DbDevExportInfos | DbDevExportInfo)
                            containing the device(s) to export information
            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """

    if not operator.isSequenceType(dev_info) and \
       not isinstance(dev_info, DbDevExportInfo):
        raise TypeError('value must be a DbDevExportInfos, a seq<DbDevExportInfo> or ' \
                        'a DbDevExportInfo')

    if isinstance(dev_info, DbDevExportInfos):
        pass
    elif isinstance(dev_info, DbDevExportInfo):
        dev_info = seq_2_DbDevExportInfos((dev_info),)
    else:
        dev_info = seq_2_DbDevExportInfos(dev_info)
    self._export_server(dev_info)

def __Database__generic_get_property(self, obj_name, value, f):
    """internal usage"""
    ret = None
    if isinstance(value, DbData):
        new_value = value
    elif isinstance(value, DbDatum):
        new_value = DbData()
        new_value.append(value)
    elif type(value) in types.StringTypes:
        new_value = DbData()
        new_value.append(DbDatum(value))
    elif operator.isSequenceType(value):
        new_value = DbData()
        for e in value:
            if isinstance(e, DbDatum):
                new_value.append(e)
            else:
                new_value.append(DbDatum(str(e)))
    elif operator.isMappingType(value):
        new_value = DbData()
        for k, v in value.iteritems():
            if isinstance(v, DbDatum):
                new_value.append(v)
            else:
                new_value.append(DbDatum(k))
        ret = value
    else:
        raise TypeError('value must be a string, PyTango.DbDatum, '\
                        'PyTango.DbData, a sequence or a dictionary')

    f(obj_name, new_value)
    if ret is None: ret = {}
    return DbData_2_dict(new_value, ret)

def __Database__generic_put_property(self, obj_name, value, f):
    """internal usage"""
    if isinstance(value, DbData):
        pass
    elif isinstance(value, DbDatum):
        new_value = DbData()
        new_value.append(value)
        value = new_value
    elif operator.isSequenceType(value) and not type(value) in types.StringTypes:
        new_value = seq_2_DbData(value)
    elif operator.isMappingType(value):
        new_value = DbData()
        for k, v in value.iteritems():
            if isinstance(v, DbDatum):
                new_value.append(v)
                continue
            db_datum = DbDatum(k)
            if operator.isSequenceType(v) and not type(v) in types.StringTypes:
                seq_2_StdStringVector(v, db_datum.value_string)
            else:
                db_datum.value_string.append(str(v))
            new_value.append(db_datum)
        value = new_value
    else:
        raise TypeError('value must be a PyTango.DbDatum, PyTango.DbData,'\
                        'a sequence<DbDatum> or a dictionary')
    return f(obj_name, value)

def __Database__generic_delete_property(self, obj_name, value, f):
    """internal usage"""
    if isinstance(value, DbData):
        new_value = value
    elif isinstance(value, DbDatum):
        new_value = DbData()
        new_value.append(value)
    elif type(value) in types.StringTypes:
        new_value = DbData()
        new_value.append(DbDatum(value))
    elif operator.isSequenceType(value):
        new_value = DbData()
        for e in value:
            if isinstance(e, DbDatum):
                new_value.append(e)
            else:
                new_value.append(DbDatum(str(e)))
    elif operator.isMappingType(value):
        new_value = DbData()
        for k, v in value.iteritems():
            if isinstance(v, DbDatum):
                new_value.append(v)
            else:
                new_value.append(DbDatum(k))
    else:
        raise TypeError('value must be a string, PyTango.DbDatum, '\
                        'PyTango.DbData, a sequence or a dictionary')

    return f(obj_name, new_value)

def __Database__put_property(self, obj_name, value):
    """
        put_property(self, obj_name, value) -> None

            Insert or update a list of properties for the specified object.
        Parameters :
            - obj_name : (str) object name
            - value : can be one of the following:
                1. DbDatum - single property data to be inserted
                2. DbData - several property data to be inserted
                3. sequence<DbDatum> - several property data to be inserted
                4. dict<str, DbDatum> - keys are property names and value has data to be inserted
                5. dict<str, obj> - keys are property names and str(obj) is property value
                6. dict<str, seq<str>> - keys are property names and value has data to be inserted
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""

    return __Database__generic_put_property(self, obj_name, value, self._put_property)

def __Database__get_property(self, obj_name, value):
    """
        get_property(self, obj_name, value) -> dict<str, seq<str>>

                Query the database for a list of object (i.e non-device) properties.

            Parameters :
                - obj_name : (str) object name
                - value : can be one of the following:
                    1. str [in] - single property data to be fetched
                    2. DbDatum [in] - single property data to be fetched
                    3. DbData [in,out] - several property data to be fetched
                       In this case (direct C++ API) the DbData will be filled with the
                       property values
                    4. sequence<str> [in] - several property data to be fetched
                    5. sequence<DbDatum> [in] - several property data to be fetched
                    6. dict<str, obj> [in,out] - keys are property names
                       In this case the given dict values will be changed to contain the
                       several property values

            Return     : a dictionary which keys are the property names the value
                        associated with each key being a a sequence of strings being the
                        property value.

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""
    return __Database__generic_get_property(self, obj_name, value, self._get_property)

def __Database__get_property_forced(self, obj_name, value):
    return __Database__generic_get_property(self, obj_name, value, self._get_property_forced)

__Database__get_property_forced.__doc__ = __Database__get_property.__doc__

def __Database__delete_property(self, obj_name, value):
    """
        delete_property(self, obj_name, value) -> None

                Delete a the given of properties for the specified object.

            Parameters :
                - obj_name : (str) object name
                - value : can be one of the following:
                    1. str [in] - single property data to be deleted
                    2. DbDatum [in] - single property data to be deleted
                    3. DbData [in] - several property data to be deleted
                    4. sequence<string> [in]- several property data to be deleted
                    5. sequence<DbDatum> [in] - several property data to be deleted
                    6. dict<str, obj> [in] - keys are property names to be deleted
                                             (values are ignored)
                    7. dict<str, DbDatum> [in] - several DbDatum.name are property names
                                                 to be deleted (keys are ignored)
            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""
    return __Database__generic_delete_property(self, obj_name, value, self._delete_property)

def __Database__get_device_property(self, dev_name, value):
    """
        get_device_property(self, dev_name, value) -> dict<str, seq<str>>

            Query the database for a list of device properties.

            Parameters :
                - dev_name : (str) object name
                - value : can be one of the following:
                    1. str [in] - single property data to be fetched
                    2. DbDatum [in] - single property data to be fetched
                    3. DbData [in,out] - several property data to be fetched
                       In this case (direct C++ API) the DbData will be filled with the
                       property values
                    4. sequence<str> [in] - several property data to be fetched
                    5. sequence<DbDatum> [in] - several property data to be fetched
                    6. dict<str, obj> [in,out] - keys are property names
                       In this case the given dict values will be changed to contain the
                       several property values

            Return     : a dictionary which keys are the property names the value
                        associated with each key being a a sequence of strings being the
                        property value.

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""
    return __Database__generic_get_property(self, dev_name, value, self._get_device_property)

def __Database__put_device_property(self, dev_name, value):
    """
        put_device_property(self, dev_name, value) -> None

            Insert or update a list of properties for the specified device.

            Parameters :
                - dev_name : (str) object name
                - value : can be one of the following:
                    1. DbDatum - single property data to be inserted
                    2. DbData - several property data to be inserted
                    3. sequence<DbDatum> - several property data to be inserted
                    4. dict<str, DbDatum> - keys are property names and value has data to be inserted
                    5. dict<str, obj> - keys are property names and str(obj) is property value
                    6. dict<str, seq<str>> - keys are property names and value has data to be inserted
            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""
    return __Database__generic_put_property(self, dev_name, value, self._put_device_property)

def __Database__delete_device_property(self, dev_name, value):
    """
        delete_device_property(self, dev_name, value) -> None

            Delete a the given of properties for the specified device.

            Parameters :
                - dev_name : (str) object name
                - value : can be one of the following:
                    1. str [in] - single property data to be deleted
                    2. DbDatum [in] - single property data to be deleted
                    3. DbData [in] - several property data to be deleted
                    4. sequence<str> [in]- several property data to be deleted
                    5. sequence<DbDatum> [in] - several property data to be deleted
                    6. dict<str, obj> [in] - keys are property names to be deleted (values are ignored)
                    7. dict<str, DbDatum> [in] - several DbDatum.name are property names to be deleted (keys are ignored)

            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""
    return __Database__generic_delete_property(self, dev_name, value, self._delete_device_property)

def __Database__get_device_property_list(self, dev_name, wildcard, array=None):
    """
        get_device_property_list(self, dev_name, wildcard, array=None) -> DbData

                Query the database for a list of properties defined for the
                specified device and which match the specified wildcard.
                If array parameter is given, it must be an object implementing de 'append'
                method. If given, it is filled with the matching property names. If not given
                the method returns a new DbDatum containing the matching property names.

            New in PyTango 7.0.0

            Parameters :
                - dev_name : (str) device name
                - wildcard : (str) property name wildcard
                - array : [out] (sequence) (optional) array that
                              will contain the matching property names.
            Return     : if container is None, return is a new DbDatum containing the
                         matching property names. Otherwise returns the given array
                         filled with the property names

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device"""
    if array is None:
        return self._get_device_property_list(dev_name, wildcard)
    elif isinstance(array, StdStringVector):
        return self._get_device_property_list(dev_name, wildcard, array)
    elif operator.isSequenceType(array) and not type(array) in types.StringTypes:
        res = self._get_device_property_list(dev_name, wildcard)
        for e in res: array.append(e)
        return array

def __Database__get_device_attribute_property(self, dev_name, value):
    """
        get_device_attribute_property(self, dev_name, value) -> dict<str, dict<str, seq<str>>>

                Query the database for a list of device attribute properties for the
                specified device. The method returns all the properties for the specified
                attributes.

            Parameters :
                - dev_name : (string) device name
                - value : can be one of the following:
                    1. str [in] - single attribute properties to be fetched
                    2. DbDatum [in] - single attribute properties to be fetched
                    3. DbData [in,out] - several attribute properties to be fetched
                       In this case (direct C++ API) the DbData will be filled with the property
                       values
                    4. sequence<str> [in] - several attribute properties to be fetched
                    5. sequence<DbDatum> [in] - several attribute properties to be fetched
                    6. dict<str, obj> [in,out] - keys are attribute names
                       In this case the given dict values will be changed to contain the several
                       attribute property values

            Return     :  a dictionary which keys are the attribute names the
                                 value associated with each key being a another
                                 dictionary where keys are property names and value is
                                 a DbDatum containing the property value.

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""

    ret = None
    if isinstance(value, DbData):
        new_value = value
    elif isinstance(value, DbDatum):
        new_value = DbData()
        new_value.append(value)
    elif type(value) in types.StringTypes:
        new_value = DbData()
        new_value.append(DbDatum(value))
    elif operator.isSequenceType(value):
        new_value = DbData()
        for e in value:
            if isinstance(e, DbDatum):
                new_value.append(e)
            else:
                new_value.append(DbDatum(str(e)))
    elif operator.isMappingType(value):
        new_value = DbData()
        for k, v in value.iteritems():
            if isinstance(v, DbDatum):
                new_value.append(v)
            else:
                new_value.append(DbDatum(k))
    else:
        raise TypeError('value must be a string, PyTango.DbDatum, '\
                        'PyTango.DbData, a sequence or a dictionary')

    if ret is None: ret = {}

    self._get_device_attribute_property(dev_name, new_value)

    nb_items = len(new_value)
    i = 0
    for j in xrange(nb_items):
        db_datum = new_value[i]
        curr_dict = {}
        ret[db_datum.name] = curr_dict
        nb_props = int(db_datum[0])
        i += 1
        for k in xrange(nb_props):
            db_datum = new_value[i]
            curr_dict[db_datum.name] = db_datum.value_string
            i += 1

        if i == nb_items:
            break
    return ret

def __Database__put_device_attribute_property(self, dev_name, value):
    """
        put_device_attribute_property( self, dev_name, value) -> None

                Insert or update a list of properties for the specified device.

            Parameters :
                - dev_name : (str) device name
                - value : can be one of the following:
                    1. DbData - several property data to be inserted
                    2. sequence<DbDatum> - several property data to be inserted
                    3. dict<str, dict<str, obj>> keys are attribute names and value being another
                       dictionary which keys are the attribute property names and the value
                       associated with each key being:
                       3.1 seq<str>
                       3.2 PyTango.DbDatum

            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""
    if isinstance(value, DbData):
        pass
    elif operator.isSequenceType(value) and not type(value) in types.StringTypes:
        new_value = seq_2_DbData(value)
    elif operator.isMappingType(value):
        new_value = DbData()
        for k1, v1 in value.iteritems():
            attr = DbDatum(k1)
            attr.append(str(len(v1)))
            new_value.append(attr)
            for k2, v2 in v1.iteritems():
                if isinstance(v2, DbDatum):
                    new_value.append(v2)
                    continue
                db_datum = DbDatum(k2)
                if operator.isSequenceType(v2) and not type(v2) in types.StringTypes:
                    seq_2_StdStringVector(v2, db_datum.value_string)
                else:
                    db_datum.value_string.append(str(v2))
                new_value.append(db_datum)
        value = new_value
    else:
        raise TypeError('value must be a PyTango.DbData,'\
                        'a sequence<DbDatum> or a dictionary')
    return self._put_device_attribute_property(dev_name, value)

def __Database__delete_device_attribute_property(self, devname, value):
    """
        delete_device_attribute_property(self, dev_name, value) -> None

                Delete a list of attribute properties for the specified device.

            Parameters :
                - devname : (string) device name
                - propnames : can be one of the following:
                    1. DbData [in] - several property data to be deleted
                    2. sequence<str> [in]- several property data to be deleted
                    3. sequence<DbDatum> [in] - several property data to be deleted
                    3. dict<str, seq<str>> keys are attribute names and value being a list of attribute property names

            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""

    if isinstance(value, DbData):
        new_value = value
    elif operator.isSequenceType(value) and not type(value) in types.StringTypes:
        new_value = seq_2_DbData(value)
    elif operator.isMappingType(value):
        new_value = DbData()
        for k1, v1 in value.iteritems():
            attr = DbDatum(k1)
            attr.append(str(len(v1)))
            new_value.append(attr)
            for k2 in v1:
                new_value.append(DbDatum(k2))
    else:
        raise TypeError('value must be a string, PyTango.DbDatum, '\
                        'PyTango.DbData, a sequence or a dictionary')

    return self._delete_device_attribute_property(dev_name, new_value)

def __Database__get_class_property(self, class_name, value):
    """
        get_class_property(self, class_name, value) -> dict<str, seq<str>>

                Query the database for a list of class properties.

            Parameters :
                - class_name : (str) class name
                - value : can be one of the following:
                    1. str [in] - single property data to be fetched
                    2. PyTango.DbDatum [in] - single property data to be fetched
                    3. PyTango.DbData [in,out] - several property data to be fetched
                       In this case (direct C++ API) the DbData will be filled with the
                       property values
                    4. sequence<str> [in] - several property data to be fetched
                    5. sequence<DbDatum> [in] - several property data to be fetched
                    6. dict<str, obj> [in,out] - keys are property names
                       In this case the given dict values will be changed to contain the
                       several property values

            Return     : a dictionary which keys are the property names the value
                        associated with each key being a a sequence of strings being the
                        property value.

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""
    return __Database__generic_get_property(self, class_name, value, self._get_class_property)

def __Database__put_class_property(self, class_name, value):
    """
        put_class_property(self, class_name, value) -> None

                Insert or update a list of properties for the specified class.

            Parameters :
                - class_name : (str) class name
                - value : can be one of the following:
                    1. DbDatum - single property data to be inserted
                    2. DbData - several property data to be inserted
                    3. sequence<DbDatum> - several property data to be inserted
                    4. dict<str, DbDatum> - keys are property names and value has data to be inserted
                    5. dict<str, obj> - keys are property names and str(obj) is property value
                    6. dict<str, seq<str>> - keys are property names and value has data to be inserted
            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""
    return __Database__generic_put_property(self, class_name, value, self._put_class_property)

def __Database__delete_class_property(self, class_name, value):
    """
        delete_class_property(self, class_name, value) -> None

                Delete a the given of properties for the specified class.

            Parameters :
                - class_name : (str) class name
                - value : can be one of the following:
                    1. str [in] - single property data to be deleted
                    2. DbDatum [in] - single property data to be deleted
                    3. DbData [in] - several property data to be deleted
                    4. sequence<str> [in]- several property data to be deleted
                    5. sequence<DbDatum> [in] - several property data to be deleted
                    6. dict<str, obj> [in] - keys are property names to be deleted
                                             (values are ignored)
                    7. dict<str, DbDatum> [in] - several DbDatum.name are property names
                                                 to be deleted (keys are ignored)
            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""
    return __Database__generic_delete_property(self, class_name, value, self._delete_class_property)

def __Database__get_class_attribute_property(self, class_name, value):
    """
        get_class_attribute_property( self, class_name, value) -> dict<str, dict<str, seq<str>>

                Query the database for a list of class attribute properties for the
                specified class. The method returns all the properties for the specified
                attributes.

            Parameters :
                - class_name : (str) class name
                - propnames : can be one of the following:
                    1. str [in] - single attribute properties to be fetched
                    2. DbDatum [in] - single attribute properties to be fetched
                    3. DbData [in,out] - several attribute properties to be fetched
                       In this case (direct C++ API) the DbData will be filled with the property
                       values
                    4. sequence<str> [in] - several attribute properties to be fetched
                    5. sequence<DbDatum> [in] - several attribute properties to be fetched
                    6. dict<str, obj> [in,out] - keys are attribute names
                       In this case the given dict values will be changed to contain the several
                       attribute property values

            Return     : a dictionary which keys are the attribute names the
                         value associated with each key being a another
                         dictionary where keys are property names and value is
                         a sequence of strings being the property value.

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""

    ret = None
    if isinstance(value, DbData):
        new_value = value
    elif isinstance(value, DbDatum):
        new_value = DbData()
        new_value.append(value)
    elif type(value) in types.StringTypes:
        new_value = DbData()
        new_value.append(DbDatum(value))
    elif operator.isSequenceType(value):
        new_value = DbData()
        for e in value:
            if isinstance(e, DbDatum):
                new_value.append(e)
            else:
                new_value.append(DbDatum(str(e)))
    elif operator.isMappingType(value):
        new_value = DbData()
        for k, v in value.iteritems():
            if isinstance(v, DbDatum):
                new_value.append(v)
            else:
                new_value.append(DbDatum(k))
    else:
        raise TypeError('value must be a string, PyTango.DbDatum, '\
                        'PyTango.DbData, a sequence or a dictionary')

    self._get_class_attribute_property(class_name, new_value)

    if ret is None: ret = {}

    nb_items = len(new_value)
    i = 0
    for j in xrange(nb_items):
        db_datum = new_value[i]
        curr_dict = {}
        ret[db_datum.name] = curr_dict
        nb_props = int(db_datum[0])
        i += 1
        for k in xrange(nb_props):
            db_datum = new_value[i]
            curr_dict[db_datum.name] = db_datum.value_string
            i += 1

        if i == nb_items:
            break
    return ret

def __Database__put_class_attribute_property(self, class_name, value):
    """
        put_class_attribute_property(self, class_name, value) -> None

                Insert or update a list of properties for the specified class.

            Parameters :
                - class_name : (str) class name
                - propdata : can be one of the following:
                    1. PyTango.DbData - several property data to be inserted
                    2. sequence<DbDatum> - several property data to be inserted
                    3. dict<str, dict<str, obj>> keys are attribute names and value
                       being another dictionary which keys are the attribute property
                       names and the value associated with each key being:
                       3.1 seq<str>
                       3.2 PyTango.DbDatum

            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)"""

    if isinstance(value, DbData):
        pass
    elif operator.isSequenceType(value) and not type(value) in types.StringTypes:
        new_value = seq_2_DbData(value)
    elif operator.isMappingType(value):
        new_value = DbData()
        for k1, v1 in value.iteritems():
            attr = DbDatum(k1)
            attr.append(str(len(v1)))
            new_value.append(attr)
            for k2, v2 in v1.iteritems():
                if isinstance(v2, DbDatum):
                    new_value.append(v2)
                    continue
                db_datum = DbDatum(k2)
                if operator.isSequenceType(v2) and not type(v2) in types.StringTypes:
                    seq_2_StdStringVector(v2, db_datum.value_string)
                else:
                    db_datum.value_string.append(str(v2))
                new_value.append(db_datum)
        value = new_value
    else:
        raise TypeError('value must be a PyTango.DbData,'\
                        'a sequence<DbDatum> or a dictionary')
    return self._put_class_attribute_property(class_name, value)

def __Database__delete_class_attribute_property(self, class_name, value):
    """
        delete_class_attribute_property(self, class_name, value) -> None

                Delete a list of attribute properties for the specified class.

            Parameters :
                - class_name : (str) class name
                - propnames : can be one of the following:
                    1. DbData [in] - several property data to be deleted
                    2. sequence<str> [in]- several property data to be deleted
                    3. sequence<DbDatum> [in] - several property data to be deleted
                    4. dict<str, seq<str>> keys are attribute names and value being a
                       list of attribute property names
            Return     : None

            Throws     : ConnectionFailed, CommunicationFailed
                         DevFailed from device (DB_SQLError)"""

    if isinstance(value, DbData):
        new_value = value
    elif operator.isSequenceType(value) and not type(value) in types.StringTypes:
        new_value = seq_2_DbData(value)
    elif operator.isMappingType(value):
        new_value = DbData()
        for k1, v1 in value.iteritems():
            attr = DbDatum(k1)
            attr.append(str(len(v1)))
            new_value.append(attr)
            for k2 in v1:
                new_value.append(DbDatum(k2))
    else:
        raise TypeError('value must be a DbDatum, DbData, '\
                        'a sequence or a dictionary')

    return self._delete_class_attribute_property(class_name, new_value)

def __Database__get_service_list(self, filter='.*'):
    import re
    data = self.get_property('CtrlSystem', 'Services')
    res = {}
    filter = re.compile(filter)
    for service in data['Services']:
        service_name, service_value = service.split(':')
        if not filter.match(service_name) is None:
            res[service_name] = service_value
    return res
    
def __Database__str__(self):
    return "Database(%s, %s)" % (self.get_db_host(), self.get_db_port())

def __init_Database():
    Database.add_server                       = __Database__add_server
    Database.export_server                    = __Database__export_server
    Database.put_property                     = __Database__put_property
    Database.get_property                     = __Database__get_property
    Database.get_property_forced              = __Database__get_property_forced
    Database.delete_property                  = __Database__delete_property
    Database.get_device_property              = __Database__get_device_property
    Database.put_device_property              = __Database__put_device_property
    Database.delete_device_property           = __Database__delete_device_property
    Database.get_device_property_list         = __Database__get_device_property_list
    Database.get_device_attribute_property    = __Database__get_device_attribute_property
    Database.put_device_attribute_property    = __Database__put_device_attribute_property
    Database.delete_device_attribute_property = __Database__delete_device_attribute_property
    Database.get_class_property               = __Database__get_class_property
    Database.put_class_property               = __Database__put_class_property
    Database.delete_class_property            = __Database__delete_class_property
    Database.get_class_attribute_property     = __Database__get_class_attribute_property
    Database.put_class_attribute_property     = __Database__put_class_attribute_property
    Database.delete_class_attribute_property  = __Database__delete_class_attribute_property
    Database.get_service_list                 = __Database__get_service_list
    Database.__str__                          = __Database__str__
    Database.__repr__                         = __Database__str__
    
def __doc_Database():
    def document_method(method_name, desc, append=True):
        return __document_method(Database, method_name, desc, append)

    Database.__doc__ = """
    Database is the high level Tango object which contains the link to the static database.
    Database provides methods for all database commands : get_device_property(), put_device_property(), info(), etc..
    To create a Database, use the default constructor.
    Example:
        db = Database()
    The constructor uses the TANGO_HOST env. variable to determine which instance of the Database to connect to."""

    document_method("write_filedatabase", """
    write_filedatabase(self) -> None

            Force a write to the file if using a file based database.

        Parameters : None
        Return     : None

        New in PyTango 7.0.0
    """ )

    document_method("reread_filedatabase", """
    reread_filedatabase(self) -> None

            Force a complete refresh over the database if using a file based database.

        Parameters : None
        Return     : None

        New in PyTango 7.0.0
    """ )

    document_method("build_connection", """
    build_connection(self) -> None

            Tries to build a connection to the Database server.

        Parameters : None
        Return     : None

        New in PyTango 7.0.0
    """ )

    document_method("check_tango_host", """
    check_tango_host(self, tango_host_env) -> None

            Check the TANGO_HOST environment variable syntax and extract
            database server host(s) and port(s) from it.

        Parameters :
            - tango_host_env : (str) The TANGO_HOST env. variable value
        Return     : None

        New in PyTango 7.0.0
    """ )

    document_method("check_access_control", """
    check_access_control(self, dev_name) -> AccessControlType

            Check the access for the given device for this client.

        Parameters :
            - dev_name : (str) device name
        Return     : the access control type as a AccessControlType object

        New in PyTango 7.0.0
    """ )

    document_method("is_control_access_checked", """
    is_control_access_checked(self) -> bool

            Returns True if control access is checked or False otherwise.

        Parameters : None
        Return     : (bool) True if control access is checked or False

        New in PyTango 7.0.0
    """ )

    document_method("set_access_checked", """
    set_access_checked(self, val) -> None

            Sets or unsets the control access check.

        Parameters :
            - val : (bool) True to set or False to unset the access control
        Return     : None

        New in PyTango 7.0.0
    """ )

    document_method("get_access_except_errors", """
    get_access_except_errors(self) -> DevErrorList

            Returns a reference to the conctrol access exceptions.

        Parameters : None
        Return     : DevErrorList

        New in PyTango 7.0.0
    """ )

    document_method("get_info", """
    get_info(self) -> str

            Query the database for some general info about the tables.

        Parameters : None
        Return     : a multiline string
    """ )

    document_method("get_host_list", """
    get_host_list(self) -> DbDatum
    get_host_list(self, wildcard) -> DbDatum

            Returns the list of all host names registered in the database.

        Parameters :
            - wildcard : (str) (optional) wildcard (eg: 'l-c0*')
        Return     : DbDatum with the list of registered host names
    """ )

    document_method("get_services", """
    get_services(self, serv_name, inst_name) -> DbDatum

            Query database for specified services.

        Parameters :
            - serv_name : (str) service name
            - inst_name : (str) instance name (can be a wildcard character ('*'))
        Return     : DbDatum with the list of available services

        New in PyTango 3.0.4
    """ )

    document_method("register_service", """
    register_service(self, serv_name, inst_name, dev_name) -> None

            Register the specified service wihtin the database.

        Parameters :
            - serv_name : (str) service name
            - inst_name : (str) instance name
            - dev_name : (str) device name
        Return     : None

        New in PyTango 3.0.4
    """ )

    document_method("unregister_service", """
    unregister_service(self, serv_name, inst_name) -> None

            Unregister the specified service from the database.

        Parameters :
            - serv_name : (str) service name
            - inst_name : (str) instance name
        Return     : None

        New in PyTango 3.0.4
    """ )

    document_method("add_device", """
    add_device(self, dev_info) -> None

            Add a device to the database. The device name, server and class
            are specified in the DbDevInfo structure

            Example :
                dev_info = DbDevInfo()
                dev_info.name = 'my/own/device'
                dev_info.class = 'MyDevice'
                dev_info.server = 'MyServer/test'
                db.add_device(dev_info)

        Parameters :
            - dev_info : (DbDevInfo) device information
        Return     : None
    """ )

    document_method("delete_device", """
    delete_device(self, dev_name) -> None

            Delete the device of the specified name from the database.

        Parameters :
            - dev_name : (str) device name
        Return     : None
    """ )

    document_method("import_device", """
    import_device(self, dev_name) -> DbDevImportInfo

            Query the databse for the export info of the specified device.

            Example :
                dev_imp_info = db.import_device('my/own/device')
                print dev_imp_info.name
                print dev_imp_info.exported
                print dev_imp_info.ior
                print dev_imp_info.version

        Parameters :
            - dev_name : (str) device name
        Return     : DbDevImportInfo
    """ )

    document_method("export_device", """
    export_device(self, dev_export) -> None

            Update the export info for this device in the database.

            Example :
                dev_export = DbDevExportInfo()
                dev_export.name = 'my/own/device'
                dev_export.ior = <the real ior>
                dev_export.host = <the host>
                dev_export.version = '3.0'
                dev_export.pid = '....'
                db.export_device(dev_export)

        Parameters :
            - dev_export : (DbDevExportInfo) export information
        Return     : None
    """ )

    document_method("unexport_device", """
    unexport_device(self, dev_name) -> None

            Mark the specified device as unexported in the database

            Example :
               db.unexport_device('my/own/device')

        Parameters :
            - dev_name : (str) device name
        Return     : None
    """ )

    document_method("get_device_name", """
    get_device_name(self, serv_name, class_name) -> DbDatum

            Query the database for a list of devices served by a server for
            a given device class

        Parameters :
            - serv_name : (str) server name
            - class_name : (str) device class name
        Return     : DbDatum with the list of device names
    """ )

    document_method("get_device_exported", """
    get_device_exported(self, filter) -> DbDatum

            Query the database for a list of exported devices whose names
            satisfy the supplied filter (* is wildcard for any character(s))

        Parameters :
            - filter : (str) device name filter (wildcard)
        Return     : DbDatum with the list of exported devices
    """ )

    document_method("get_device_domain", """
    get_device_domain(self, wildcard) -> DbDatum

            Query the database for a list of of device domain names which
            match the wildcard provided (* is wildcard for any character(s)).
            Domain names are case insensitive.

        Parameters :
            - wildcard : (str) domain filter
        Return     : DbDatum with the list of device domain names
    """ )

    document_method("get_device_family", """
    get_device_family(self, wildcard) -> DbDatum

            Query the database for a list of of device family names which
            match the wildcard provided (* is wildcard for any character(s)).
            Family names are case insensitive.

        Parameters :
            - wildcard : (str) family filter
        Return     : DbDatum with the list of device family names
    """ )

    document_method("get_device_member", """
    get_device_member(self, wildcard) -> DbDatum

            Query the database for a list of of device member names which
            match the wildcard provided (* is wildcard for any character(s)).
            Member names are case insensitive.

        Parameters :
            - wildcard : (str) member filter
        Return     : DbDatum with the list of device member names
    """ )

    document_method("get_device_alias", """
    get_device_alias(self, alias) -> str

            Get the device name from an alias.

        Parameters :
            - alias : (str) alias
        Return     : device name
    """ )

    document_method("get_alias", """
    get_alias(self, alias) -> str

            Get the device alias name from its name.

        Parameters :
            - alias : (str) device name
        Return     : alias

        New in PyTango 3.0.4
    """ )

    document_method("get_device_alias_list", """
    get_device_alias_list(self, filter) -> DbDatum

            Get device alias list. The parameter alias is a string to filter
            the alias list returned. Wildcard (*) is supported.

        Parameters :
            - filter : (str) a string with the alias filter (wildcard (*) is supported)
        Return     : DbDatum with the list of device names

        New in PyTango 7.0.0
    """ )

    document_method("get_class_for_device", """
    get_class_for_device(self, dev_name) -> str

            Return the class of the specified device.

        Parameters :
            - dev_name : (str) device name
        Return     : a string containing the device class
    """ )

    document_method("get_class_inheritance_for_device", """
    get_class_inheritance_for_device(self, dev_name) -> DbDatum

            Return the class inheritance scheme of the specified device.

        Parameters :
            - devn_ame : (str) device name
        Return     : DbDatum with the inheritance class list

        New in PyTango 7.0.0
    """ )

    document_method("get_class_for_device", """
    get_class_for_device(self, dev_name) -> str

            Return the class of the specified device.

        Parameters :
            - dev_name : (str) device name
        Return     : a string containing the device class
    """ )

    document_method("get_device_exported_for_class", """
    get_device_exported_for_class(self, class_name) -> DbDatum

            Query database for list of exported devices for the specified class.

        Parameters :
            - class_name : (str) class name
        Return     : DbDatum with the list of exported devices for the

        New in PyTango 7.0.0
    """ )

    document_method("put_device_alias", """
    put_device_alias(self, dev_name, alias) -> None

            Query database for list of exported devices for the specified class.

        Parameters :
            - dev_name : (str) device name
            - alias : (str) alias name
        Return     : None
    """ )

    document_method("delete_device_alias", """
    delete_device_alias(self, alias) -> void

            Delete a device alias

        Parameters :
            - alias : (str) alias name
        Return     : None
    """ )

    document_method("_add_server", """
    _add_server(self, serv_name, dev_info) -> None

            Add a a group of devices to the database.
            This corresponds to the pure C++ API call.

        Parameters :
            - serv_name : (str) server name
            - dev_info : (DbDevInfos) server device(s) information
        Return     : None
    """ )

    document_method("delete_server", """
    delete_server(self, server) -> None

            Delete the device server and its associated devices from database.

        Parameters :
            - server : (str) name of the server to be deleted with
                       format: <server name>/<instance>
        Return     : None
    """ )

    document_method("_export_server", """
    _export_server(self, dev_info) -> None

            Export a group of devices to the database.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_info : (DbDevExportInfos) device(s) to export information
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("unexport_server", """
    unexport_server(self, server) -> None

            Mark all devices exported for this server as unexported.

        Parameters :
            - server : (str) name of the server to be unexported with
                       format: <server name>/<instance>
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("get_server_info", """
    get_server_info(self, server) -> DbServerInfo

            Query the database for server information.

        Parameters :
            - server : (str) name of the server to be unexported with
                       format: <server name>/<instance>
        Return     : DbServerInfo with server information

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
    """ )

    document_method("put_server_info", """
    put_server_info(self, info) -> None

            Add/update server information in the database.

        Parameters :
            - info : (DbServerInfo) new server information
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
    """ )

    document_method("delete_server_info", """
    delete_server_info(self, server) -> None

            Delete server information of the specifed server from the database.

        Parameters :
            - server : (str) name of the server to be deleted with
                       format: <server name>/<instance>
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
    """ )

    document_method("get_server_class_list", """
    get_server_class_list(self, server) -> DbDatum

            Query the database for a list of classes instancied by the
            specified server. The DServer class exists in all TANGO servers
            and for this reason this class is removed from the returned list.

        Parameters :
            - server : (str) name of the server to be deleted with
                       format: <server name>/<instance>
        Return     : DbDatum containing list of class names instanciated by
                     the specified server

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
    """ )

    document_method("get_server_name_list", """
    get_server_name_list(self) -> DbDatum

            Return the list of all server names registered in the database.

        Parameters : None
        Return     : DbDatum containing list of server names

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
    """ )

    document_method("get_instance_name_list", """
    get_instance_name_list(self, serv_name) -> DbDatum

            Return the list of all instance names existing in the database for the specifed server.

        Parameters :
            - serv_name : (str) server name with format <server name>
        Return     : DbDatum containing list of instance names for the specified server

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
    """ )

    document_method("get_server_list", """
    get_server_list(self) -> DbDatum
    get_server_list(self, wildcard) -> DbDatum

            Return the list of all servers registered in the database.
            If wildcard parameter is given, then the the list of servers registred on the
            specified host (we refer 'host' in the context of tango device, i.e. following
            the tango naming convention 'host/family/member') is returned

        Parameters :
            - wildcard : (str) host wildcard
        Return     : DbDatum containing list of registered servers
    """ )

    document_method("get_host_server_list", """
    get_host_server_list(self, host_name) -> DbDatum

            Query the database for a list of servers registred on the specified host.

        Parameters :
            - host_name : (str) host name
        Return     : DbDatum containing list of servers for the specified host

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
    """ )

    document_method("get_device_class_list", """
    get_device_class_list(self, server) -> DbDatum

            Query the database for a list of devices and classes served by
            the specified server. Return a list with the following structure:
            [device name, class name, device name, class name, ...]

        Parameters :
            - server : (str) name of the server with format: <server name>/<instance>
        Return     : DbDatum containing list with the following structure:
                     [device_name, class name]

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
    """ )

    document_method("_get_property", """
    _get_property(self, obj_name, props) -> None

            Query the database for a list of object (i.e non-device)
            properties. The property names are specified by the
            DbData (seq<DbDatum>) structures. The method returns the
            properties in the same DbDatum structures
            This corresponds to the pure C++ API call.

        Parameters :
            - obj_name : (str) object name
            - props [in, out] : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("_get_property_forced", """
    _get_property_forced(self, obj_name, props) -> None

            Query the database for a list of object (i.e non-device)
            properties. The property names are specified by the
            DbData (seq<DbDatum>) structures. The method returns the
            properties in the same DbDatum structures
            This corresponds to the pure C++ API call.

        Parameters :
            - obj_name : (str) object name
            - props [in, out] : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("_delete_property", """
    _delete_property(self, obj_name, props) -> None

            Delete a list of properties for the specified object.
            This corresponds to the pure C++ API call.

        Parameters :
            - obj_name : (str) object name
            - props : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("get_property_history", """
    get_property_history(self, obj_name, prop_name) -> DbHistoryList

            Get the list of the last 10 modifications of the specifed object
            property. Note that propname can contain a wildcard character
            (eg: 'prop*')

        Parameters :
            - serv_name : (str) server name
            - prop_name : (str) property name
        Return     : DbHistoryList containing the list of modifications

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("get_object_list", """
    get_object_list(self, wildcard) -> DbDatum

            Query the database for a list of object (free properties) for
            which properties are defined and which match the specified
            wildcard.

        Parameters :
            - wildcard : (str) object wildcard
        Return     : DbDatum containing the list of object names matching the given wildcard

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("get_object_property_list", """
    get_object_property_list(self, obj_name, wildcard) -> DbDatum

            Query the database for a list of properties defined for the
            specified object and which match the specified wildcard.

        Parameters :
            - obj_name : (str) object name
            - wildcard : (str) property name wildcard
        Return     : DbDatum with list of properties defined for the specified
                     object and which match the specified wildcard

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("_get_device_property", """
    _get_device_property(self, dev_name, props) -> None

            Query the database for a list of device properties for the
            specified device. The property names are specified by the
            DbData (seq<DbDatum>) structures. The method returns the
            properties in the same DbDatum structures
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - props : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("_put_device_property", """
    _put_device_property(self, dev_name, props) -> None

            Insert or update a list of properties for the specified device.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - props : (DbData) property data
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("_delete_device_property", """
    _delete_device_property(self, dev_name, props) -> None

            Delete a list of properties for the specified device.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - props : (DbData) property names to be deleted
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("get_device_property_history", """
    get_device_property_history(self, dev_name, prop_name) -> DbHistoryList

            Get the list of the last 10 modifications of the specified device
            property. Note that propname can contain a wildcard character
            (eg: 'prop*').
            This corresponds to the pure C++ API call.

        Parameters :
            - serv_name : (str) server name
            - prop_name : (str) property name
        Return     : DbHistoryList containing the list of modifications

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("_get_device_property_list", """
    _get_device_property_list(self, dev_name, wildcard) -> DbDatum
    _get_device_property_list(self, dev_name, wildcard, container) -> None

            Query the database for a list of properties defined for the
            specified device and which match the specified wildcard.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - wildcard : (str) property name wildcard
            - container [out] : (StdStringVector) array that will contain the matching
                                property names
        Return     : DbDatum containing the list of property names or None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("_get_device_attribute_property", """
    _get_device_attribute_property(self, dev_name, props) -> None

            Query the database for a list of device attribute properties for
            the specified device. The attribute names are specified by the
            DbData (seq<DbDatum>) structures. The method returns all the
            properties for the specified attributes in the same DbDatum structures.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - props [in, out] : (DbData) attribute names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("_put_device_attribute_property", """
    _put_device_attribute_property(self, dev_name, props) -> None

            Insert or update a list of attribute properties for the specified device.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - props : (DbData) property data
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("_delete_device_attribute_property", """
    _delete_device_attribute_property(self, dev_name, props) -> None

            Delete a list of attribute properties for the specified device.
            The attribute names are specified by the vector of DbDatum structures. Here
            is an example of how to delete the unit property of the velocity attribute of
            the id11/motor/1 device using this method :

            db_data = PyTango.DbData();
            db_data.append(DbDatum("velocity"));
            db_data.append(DbDatum("unit"));
            db.delete_device_attribute_property("id11/motor/1", db_data);

            This corresponds to the pure C++ API call.

        Parameters :
            - serv_name : (str) server name
            - props : (DbData) attribute property data
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("get_device_attribute_property_history", """
    get_device_attribute_property_history(self, dev_name, att_name, prop_name) -> DbHistoryList

            Get the list of the last 10 modifications of the specified device
            attribute property. Note that propname and devname can contain a
            wildcard character (eg: 'prop*').

        Parameters :
            - devn_ame : (str) device name
            - attn_ame : (str) attribute name
            - prop_name : (str) property name
        Return     : DbHistoryList containing the list of modifications

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("_get_class_property", """
    _get_class_property(self, class_name, props) -> None

            Query the database for a list of class properties. The property
            names are specified by the DbData (seq<DbDatum>) structures.
            The method returns the properties in the same DbDatum structures.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props [in, out] : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("_put_class_property", """
    _put_class_property(self, class_name, props) -> None

            Insert or update a list of properties for the specified class.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props : (DbData) property data to be inserted
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("_delete_class_property", """
    _delete_class_property(self, class_name, props) -> None

            Delete a list of properties for the specified class.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props  : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("get_class_property_history", """
    get_class_property_history(self, class_name, prop_name) -> DbHistoryList

            Get the list of the last 10 modifications of the specified class
            property. Note that propname can contain a wildcard character
            (eg: 'prop*').

        Parameters :
            - class_name : (str) class name
            - prop_name : (str) property name
        Return     : DbHistoryList containing the list of modifications

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("get_class_list", """
    get_class_list(self, wildcard) -> DbDatum

            Query the database for a list of classes which match the specified wildcard

        Parameters :
            - wildcard : (str) class wildcard
        Return     : DbDatum containing the list of matching classes

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("get_class_property_list", """
    get_class_property_list(self, class_name) -> DbDatum

            Query the database for a list of properties defined for the specified class.

        Parameters :
            - class_name : (str) class name
        Return     : DbDatum containing the list of properties for the specified class

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("_get_class_attribute_property", """
    _get_class_attribute_property(self, class_name, props) -> None

            Query the database for a list of class attribute properties for
            the specified objec. The attribute names are returned with the
            number of properties specified as their value. The first DbDatum
            element of the returned DbData vector contains the first
            attribute name and the first attribute property number. The
            following DbDatum element contains the first attribute property
            name and property values.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props [in,out] : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("_put_class_attribute_property", """
    _put_class_attribute_property(self, class_name, props) -> None

            Insert or update a list of attribute properties for the specified class.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props : (DbData) property data
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("get_class_attribute_property_history", """
    get_class_attribute_property_history(self, dev_name, attr_name, prop_name) -> DbHistoryList

            Delete a list of properties for the specified class.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - attr_name : (str) attribute name
            - prop_name : (str) property name
        Return     : DbHistoryList containing the list of modifications

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("get_class_attribute_list", """
    get_class_attribute_list(self, class_name, wildcard) -> DbDatum

            Query the database for a list of attributes defined for the specified
            class which match the specified wildcard.

        Parameters :
            - class_name : (str) class name
            - wildcard : (str) attribute name
        Return     : DbDatum containing the list of matching attributes for the given class

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("get_attribute_alias", """
    get_attribute_alias(self, alias) -> str

            Get the full attribute name from an alias.

        Parameters :
            - alias : (str) attribute alias
        Return     :  full attribute name

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("get_attribute_alias_list", """
    get_attribute_alias_list(self, filter) -> DbDatum

            Get attribute alias list. The parameter alias is a string to
            filter the alias list returned. Wildcard (*) is supported. For
            instance, if the string alias passed as the method parameter
            is initialised with only the * character, all the defined
            attribute alias will be returned. If there is no alias with the
            given filter, the returned array will have a 0 size.

        Parameters :
            - filter : (str) attribute alias filter
        Return     : DbDatum containing the list of matching attribute alias

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("put_attribute_alias", """
    put_attribute_alias(self, attr_name, alias) -> None

            Set an alias for an attribute name. The attribute alias is
            specified by aliasname and the attribute name is specifed by
            attname. If the given alias already exists, a DevFailed exception
            is thrown.

        Parameters :
            - attr_name : (str) full attribute name
            - alias : (str) alias
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("delete_attribute_alias", """
    delete_attribute_alias(self, alias) -> None

            Remove the alias associated to an attribute name.

        Parameters :
            - alias : (str) alias
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """ )

    document_method("export_event", """
    export_event(self, event_data) -> None

            Export an event to the database.

        Parameters :
            - eventdata : (sequence<str>) event data (same as DbExportEvent Database command)
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

    document_method("unexport_event", """
    export_event(self, event) -> None

            Export an event to the database.

        Parameters :
            - event : (str) event
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
    """ )

def __doc_DbDatum():
    def document_method(method_name, desc, append=True):
        return __document_method(DbDatum, method_name, desc, append)

    DbDatum.__doc__ = """
    A single database value which has a name, type, address and value
    and methods for inserting and extracting C++ native types. This is
    the fundamental type for specifying database properties. Every
    property has a name and has one or more values associated with it.
    A status flag indicates if there is data in the DbDatum object or
    not. An additional flag allows the user to activate exceptions.

    Note: DbDatum is extended to support the python sequence API.
          This way the DbDatum behaves like a sequence of strings.
          This allows the user to work with a DbDatum as if it was
          working with the old list of strings.

    New in PyTango 7.0.0"""

    document_method("size", """
    size(self) -> int

            Returns the number of separate elements in the value.

        Parameters : None
        Return     : the number of separate elements in the value.

        New in PyTango 7.0.0
    """ )

    document_method("is_empty", """
    is_empty(self) -> bool

            Returns True or False depending on whether the
            DbDatum object contains data or not. It can be used to test
            whether a property is defined in the database or not.

        Parameters : None
        Return     : (bool) True if no data or False otherwise.

        New in PyTango 7.0.0
    """ )

def __doc_DbDevExportInfo():
    DbDevExportInfo.__doc__ = """
    import info for a device (should be retrived from the database) with
    the following members:
        - name : device name
        - ior : CORBA reference of the device
        - host : name of the computer hosting the server
        - version : str
        - pid : process identifier"""

def __doc_DbDevImportInfo():
    DbDevImportInfo.__doc__ = """
    import info for a device (should be retrived from the database) with
    the following members:
        - name : device name
        - exported : 1 if device is running, 0 else
        - ior : CORBA reference of the device
        - version : str"""

def __doc_DbDevInfo():
    DbDevInfo.__doc__ = """
    A structure containing available information for a device with
    the following members:
        - name : str
        - _class : str
        - server : str"""

def __doc_DbHistory():
    def document_method(method_name, desc, append=True):
        return __document_method(DbHistory, method_name, desc, append)

    DbHistory.__doc__ = """
    A structure containing the modifications of a property. No public members."""

    document_method("get_name", """
    get_name(self) -> str

            Returns the property name.

        Parameters : None
        Return     : (str) property name
    """ )

    document_method("get_attribute_name", """
    get_attribute_name(self) -> str

            Returns the attribute name (empty for object properties or device properties)

        Parameters : None
        Return     : (str) attribute name
    """ )

    document_method("get_date", """
    get_date(self) -> str

            Returns the update date

        Parameters : None
        Return     : (str) update date
    """ )

    document_method("get_value", """
    get_value(self) -> DbDatum

            Returns a COPY of the property value

        Parameters : None
        Return     : (DbDatum) a COPY of the property value
    """ )

    document_method("is_deleted", """
    is_deleted(self) -> bool

            Returns True if the property has been deleted or False otherwise

        Parameters : None
        Return     : (bool) True if the property has been deleted or False otherwise
    """ )

def __doc_DbServerInfo():
    DbServerInfo.__doc__ = """
    A structure containing available information for a device server with
    the following members:
        - name : str
        - host : str
        - mode : str
        - level : str"""

def init_db():
    __init_DbDatum()
    __doc_DbDatum()
    __init_Database()
    __doc_Database()
    __doc_DbDevExportInfo()
    __doc_DbDevImportInfo()
    __doc_DbDevInfo()
    __doc_DbHistory()
    __doc_DbServerInfo()

