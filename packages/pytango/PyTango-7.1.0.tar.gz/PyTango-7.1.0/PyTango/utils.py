import types, operator

from _PyTango import StdStringVector, DbData, DbDevInfos, DbDevExportInfos, CmdArgType, AttrDataFormat

_scalar_int_types = (CmdArgType.DevShort, CmdArgType.DevUShort,
    CmdArgType.DevInt, CmdArgType.DevLong, CmdArgType.DevULong,
    CmdArgType.DevLong64, CmdArgType.DevULong64)

_scalar_float_types = (CmdArgType.DevFloat, CmdArgType.DevDouble,)

_scalar_numerical_types = _scalar_int_types + _scalar_float_types

_scalar_str_types = (CmdArgType.DevString, CmdArgType.ConstDevString,)

_scalar_types = _scalar_numerical_types + _scalar_str_types + \
    (CmdArgType.DevBoolean, CmdArgType.DevEncoded,
     CmdArgType.DevUChar, CmdArgType.DevVoid)

_array_int_types = (CmdArgType.DevVarShortArray, CmdArgType.DevVarUShortArray,
                    CmdArgType.DevVarLongArray, CmdArgType.DevVarULongArray,
                    CmdArgType.DevVarLong64Array, CmdArgType.DevVarULong64Array)

_array_float_types = (CmdArgType.DevVarFloatArray, CmdArgType.DevVarDoubleArray)

_array_numerical_types = _array_int_types + _array_float_types

_array_types = _array_numerical_types + (CmdArgType.DevVarBooleanArray,
    CmdArgType.DevVarStringArray,
    CmdArgType.DevVarCharArray, CmdArgType.DevVarDoubleStringArray,
    CmdArgType.DevVarLongStringArray)

_scalar_to_array_type = {
    CmdArgType.DevBoolean : CmdArgType.DevVarBooleanArray,
    CmdArgType.DevUChar : CmdArgType.DevVarCharArray,
    CmdArgType.DevShort : CmdArgType.DevVarShortArray,
    CmdArgType.DevUShort : CmdArgType.DevVarUShortArray,
    CmdArgType.DevInt : CmdArgType.DevVarLongArray,
    CmdArgType.DevLong : CmdArgType.DevVarLongArray,
    CmdArgType.DevULong : CmdArgType.DevVarULongArray,
    CmdArgType.DevLong64 : CmdArgType.DevVarLong64Array,
    CmdArgType.DevULong64 : CmdArgType.DevVarULong64Array,
    CmdArgType.DevFloat : CmdArgType.DevVarFloatArray,
    CmdArgType.DevDouble : CmdArgType.DevVarDoubleArray,
    CmdArgType.DevString : CmdArgType.DevVarStringArray,
    CmdArgType.ConstDevString : CmdArgType.DevVarStringArray,
}

def is_scalar(tg_type):
    global _scalar_types
    return tg_type in _scalar_types

def is_array(tg_type):
    global _array_types
    return tg_type in _array_types

def is_numerical(tg_type, inc_array=False):
    global _scalar_numerical_types, _array_numerical_types
    if tg_type in _scalar_numerical_types:
        return True
    if not inc_array:
        return False
    return tg_type in _array_numerical_types

def is_int(tg_type, inc_array=False):
    global _scalar_int_types, _array_int_types
    if tg_type in _scalar_int_types:
        return True
    if not inc_array:
        return False
    return tg_type in _array_int_types

def is_float(tg_type, inc_array=False):
    global _scalar_float_types, _array_float_types
    if tg_type in _scalar_float_types:
        return True
    if not inc_array:
        return False
    return tg_type in _array_float_types

def seq_2_StdStringVector(seq, vec=None):
    if isinstance(seq, StdStringVector): return seq
    if vec is None: vec = StdStringVector()
    if not isinstance(vec, StdStringVector):
        raise TypeError('vec must be a PyTango.StdStringVector')
    for e in seq: vec.append(str(e))
    return vec

def StdStringVector_2_seq(vec, seq=None):
    if seq is None: seq = []
    if not isinstance(vec, StdStringVector):
        raise TypeError('vec must be a PyTango.StdStringVector')
    for e in vec: sec.append(str(e))
    return seq

def seq_2_StdDoubleVector(seq, vec=None):
    if isinstance(seq, StdDoubleVector): return seq
    if vec is None: vec = StdDoubleVector()
    if not isinstance(vec, StdDoubleVector):
        raise TypeError('vec must be a PyTango.StdDoubleVector')
    for e in seq: vec.append(str(e))
    return vec

def StdDoubleVector_2_seq(vec, seq=None):
    if seq is None: seq = []
    if not isinstance(vec, StdDoubleVector):
        raise TypeError('vec must be a PyTango.StdDoubleVector')
    for e in vec: sec.append(float(e))
    return seq

def seq_2_DbDevInfos(seq, vec=None):
    if isinstance(seq, DbDevInfos): return seq
    if vec is None: vec = DbDevInfos()
    if not isinstance(vec, DbDevInfos):
        raise TypeError('vec must be a PyTango.DbDevInfos')
    for e in seq: vec.append(e)
    return vec

def seq_2_DbDevExportInfos(seq, vec=None):
    if isinstance(seq, DbDevExportInfos): return seq
    if vec is None: vec = DbDevExportInfos()
    if not isinstance(vec, DbDevExportInfos):
        raise TypeError('vec must be a PyTango.DbDevExportInfos')
    for e in seq: vec.append(e)
    return vec

def seq_2_DbData(seq, vec=None):
    if isinstance(seq, DbData): return seq
    if vec is None: vec = DbData()
    if not isinstance(vec, DbData):
        raise TypeError('vec must be a PyTango.DbData')
    for e in seq: vec.append(e)
    return vec

def DbData_2_dict(db_data, d=None):
    if d is None: d = {}
    if not isinstance(db_data, DbData):
        raise TypeError('db_data must be a PyTango.DbData. A %s found instead' % type(db_data))
    for db_datum in db_data:
        d[db_datum.name] = db_datum.value_string
    return d

def seqStr_2_obj(seq, tg_type, tg_format=None):
    if tg_format:
        return _seqStr_2_obj_from_type_format(seq, tg_type, tg_format)
    return _seqStr_2_obj_from_type(seq, tg_type)

def _seqStr_2_obj_from_type(seq, tg_type):
    
    if type(seq) in types.StringTypes:
        seq = (seq,)
    
    #    Scalar cases
    global _scalar_int_types
    if tg_type in _scalar_int_types:
        return int(seq[0])

    global _scalar_float_types
    if tg_type in _scalar_float_types:
        return float(seq[0])

    global _scalar_str_types
    if tg_type in _scalar_str_types:
        return seq[0]

    if tg_type == CmdArgType.DevBoolean:
        return seq[0].capitalize() == 'True'

    #sequence cases
    if tg_type == CmdArgType.DevVarStringArray:
        return seq

    global _array_int_types
    if tg_type in _array_int_types:
        argout = []
        for x in seq:
            argout.append(int(x))
        return argout

    global _array_float_types
    if tg_type in _array_float_types:
        argout = []
        for x in seq:
            argout.append(float(x))
        return argout

    return []

def _seqStr_2_obj_from_type_format(seq, tg_type, tg_format):
    if tg_format == AttrDataFormat.SCALAR:
        return _seqStr_2_obj_from_type(tg_type, seq)
    elif tg_format == AttrDataFormat.SPECTRUM:
        return _seqStr_2_obj_from_type(_scalar_to_array_type(tg_type), seq)
    elif tg_format == AttrDataFormat.IMAGE:
        if tg_type == CmdArgType.DevString:
            return seq

        global _scalar_int_types
        if tg_type in _scalar_int_types:
            argout = []
            for x in seq:
                tmp = []
                for y in x:
                    tmp.append(int(y))
                argout.append(tmp)
            return argout

        global _scalar_float_types
        if tg_type in _scalar_float_types:
            argout = []
            for x in seq:
                tmp = []
                for y in x:
                    tmp.append(float(y))
                argout.append(tmp)
            return argout
    
    #UNKNOWN_FORMAT
    return _seqStr_2_obj_from_type(tg_type, seq)

def obj_2_str(obj, tg_type):
    """
        obj_2_str(obj, tg_type) -> str

                Converts a python object into a string according to the given tango type

            Parameters :
                - obj : (object) the object to be converted
                - tg_type : (CmdArgType) tango type
            Return     : (str) a string representation of the given object"""
    ret = ""
    if tg_type in _scalar_types:
        # scalar cases
        if operator.isSequenceType(obj):
            if not len(obj):
                return ret
            obj = obj[0]
        ret = str(obj).rstrip()
    else:
        # sequence cases
        ret = '\n'.join([ str(i) for i in obj ])
    return ret

def copy_doc(klass, fnname):
    """Copies documentation string of a method from the super class into the rewritten method of the given class"""
    getattr(klass, fnname).im_func.__doc__ = getattr(klass.__base__, fnname).im_func.__doc__

def document_method(klass, method_name, d, add=True):
    if add:
        cpp_doc = getattr(klass, method_name).__doc__
        if cpp_doc:
            getattr(klass, method_name).im_func.__doc__ = "%s\n%s" % (d, cpp_doc)
            return
    getattr(klass, method_name).im_func.__doc__ = d

def document_static_method(klass, method_name, d, add=True):
    if add:
        cpp_doc = getattr(klass, method_name).__doc__
        if cpp_doc:
            getattr(klass, method_name).__doc__ = "%s\n%s" % (d, cpp_doc)
            return
    getattr(klass, method_name).__doc__ = d

def document_enum(klass, enum_name, desc, append=True):
    # derived = type(base)('derived', (base,), {'__doc__': 'desc'})

    # Get the original enum type
    base = getattr(klass, enum_name)

    # Prepare the new docstring
    if append and base.__doc__ is not None:
        desc = base.__doc__ + "\n" + desc

    # Create a new type, derived from the original. Only difference
    # is the docstring.
    derived = type(base)(enum_name, (base,), {'__doc__': desc})

    # Replace the original enum type with the new one
    setattr(klass, enum_name, derived)
