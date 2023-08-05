
#pragma once

#include <tango.h>
#include <cassert>

namespace Tango
{
    typedef std::vector<DbHistory> DbHistoryList;
}

template<int N>
struct tango_name2type
{
};

template<typename N>
struct tango_type2name
{
    enum { };
};

template<int N>
struct tango_name2arraytype
{
};

#define DEF_TANGO_NAME2TYPE(tangoname, tangotype) \
    template<> \
    struct tango_name2type<Tango:: tangoname> \
    { \
        typedef tangotype Type; \
    }; \
    template<> \
    struct tango_type2name<tangotype> \
    { \
        enum {value = Tango:: tangoname}; \
    };

#define DEF_TANGO_NAME2ARRAY(tangoname, tangotype, simple) \
    template<> \
    struct tango_name2arraytype<Tango:: tangoname> \
    { \
        typedef tangotype Type; \
        typedef simple ElementsType; \
    };

#define __TSD_SIMPLE(tangoname, eltangotype, arraytangotype) \
    DEF_TANGO_NAME2TYPE(tangoname, eltangotype) \
    DEF_TANGO_NAME2ARRAY(tangoname, arraytangotype, eltangotype)

#define __TSD_ARRAY(tangoname, eltangotype, arraytangotype) \
    DEF_TANGO_NAME2TYPE(tangoname, arraytangotype) \
    DEF_TANGO_NAME2ARRAY(tangoname, void, eltangotype)

__TSD_SIMPLE( DEV_SHORT,                Tango::DevShort  ,  Tango::DevVarShortArray   );
__TSD_SIMPLE( DEV_LONG,                 Tango::DevLong   ,  Tango::DevVarLongArray   );
__TSD_SIMPLE( DEV_DOUBLE,               Tango::DevDouble ,  Tango::DevVarDoubleArray   );
__TSD_SIMPLE( DEV_STRING,               Tango::DevString ,  Tango::DevVarStringArray   );
__TSD_SIMPLE( DEV_FLOAT,                Tango::DevFloat  ,  Tango::DevVarFloatArray   );
__TSD_SIMPLE( DEV_BOOLEAN,              Tango::DevBoolean,  Tango::DevVarBooleanArray   );
__TSD_SIMPLE( DEV_USHORT,               Tango::DevUShort ,  Tango::DevVarUShortArray   );
__TSD_SIMPLE( DEV_ULONG,                Tango::DevULong  ,  Tango::DevVarULongArray   );
__TSD_SIMPLE( DEV_UCHAR,                Tango::DevUChar  ,  Tango::DevVarUCharArray   );
__TSD_SIMPLE( DEV_LONG64,               Tango::DevLong64 ,  Tango::DevVarLong64Array   );
__TSD_SIMPLE( DEV_ULONG64,              Tango::DevULong64,  Tango::DevVarULong64Array   );
__TSD_SIMPLE( DEV_STATE,                Tango::DevState  ,  Tango::DevVarStateArray   );
__TSD_SIMPLE( DEV_ENCODED,              Tango::DevEncoded,  Tango::DevVarEncodedArray     );

__TSD_SIMPLE( DEV_VOID,                 void             , void);

__TSD_ARRAY(  DEVVAR_CHARARRAY,         _CORBA_Octet     ,  Tango::DevVarCharArray);
__TSD_ARRAY(  DEVVAR_SHORTARRAY,        Tango::DevShort  ,  Tango::DevVarShortArray);
__TSD_ARRAY(  DEVVAR_LONGARRAY,         Tango::DevLong   ,  Tango::DevVarLongArray);
__TSD_ARRAY(  DEVVAR_FLOATARRAY,        Tango::DevFloat  ,  Tango::DevVarFloatArray);
__TSD_ARRAY(  DEVVAR_DOUBLEARRAY,       Tango::DevDouble ,  Tango::DevVarDoubleArray);
__TSD_ARRAY(  DEVVAR_USHORTARRAY,       Tango::DevUShort ,  Tango::DevVarUShortArray);
__TSD_ARRAY(  DEVVAR_ULONGARRAY,        Tango::DevULong  ,  Tango::DevVarULongArray);
__TSD_ARRAY(  DEVVAR_STRINGARRAY,       Tango::DevString ,  Tango::DevVarStringArray);
__TSD_ARRAY(  DEVVAR_LONGSTRINGARRAY,   void             ,  Tango::DevVarLongStringArray);
__TSD_ARRAY(  DEVVAR_DOUBLESTRINGARRAY, void             ,  Tango::DevVarDoubleStringArray);
__TSD_ARRAY(  DEVVAR_BOOLEANARRAY,      Tango::DevBoolean,  Tango::DevVarBooleanArray);
__TSD_ARRAY(  DEVVAR_LONG64ARRAY,       Tango::DevLong64 ,  Tango::DevVarLong64Array);
__TSD_ARRAY(  DEVVAR_ULONG64ARRAY,      Tango::DevULong64,  Tango::DevVarULong64Array);


#define TANGO_type2const(type) tango_type2name<type>::value
#define TANGO_const2type(name) tango_name2type<name>::Type
#define TANGO_const2arraytype(name) tango_name2arraytype<name>::Type
#define TANGO_const2arrayelementstype(name) tango_name2arraytype<name>::ElementsType
#define TANGO_type2arraytype(type) TANGO_const2arraytype(TANGO_type2const(type))
#define TANGO_const2string(name) (Tango::CmdArgTypeName[name])



#define __TANGO_DEPEND_ON_TYPE_AUX(typename_, DOIT) \
    case Tango:: typename_: { \
        static const long tangoTypeConst = Tango:: typename_; \
        DOIT; \
        break; \
    }

#define TANGO_DO_ON_ATTRIBUTE_DATA_TYPE(tid, DOIT) if (true) { \
    switch(tid) { \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_SHORT, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_LONG, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_DOUBLE, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_STRING, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_FLOAT, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_BOOLEAN, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_USHORT, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_ULONG, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_UCHAR, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_LONG64, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_ULONG64, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_STATE, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_ENCODED, DOIT) \
        default: \
            assert(false); \
    } } else (void)0

#define TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE(tid, fn, ...) \
    TANGO_DO_ON_ATTRIBUTE_DATA_TYPE(tid, fn<tangoTypeConst>(__VA_ARGS__))

/// @todo Not sure about who I choosed to comment out from here...
#define TANGO_DO_ON_DEVICE_DATA_TYPE(tid, DOIT_SIMPLE, DOIT_ARRAY) if (true) { \
    switch(tid) { \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_VOID, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_BOOLEAN, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_SHORT, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_LONG, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_FLOAT, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_DOUBLE, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_USHORT, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_ULONG, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_STRING, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_CHARARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_SHORTARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_LONGARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_FLOATARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_DOUBLEARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_USHORTARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_ULONGARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_STRINGARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_LONGSTRINGARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_DOUBLESTRINGARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_STATE, DOIT_SIMPLE) \
/*        __TANGO_DEPEND_ON_TYPE_AUX(CONST_DEV_STRING, DOIT_SIMPLE) */\
/*        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_BOOLEANARRAY, DOIT_ARRAY) */\
/*        __TANGO_DEPEND_ON_TYPE_AUX(DEV_UCHAR, DOIT_SIMPLE)*/ \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_LONG64, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_ULONG64, DOIT_SIMPLE) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_LONG64ARRAY, DOIT_ARRAY) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEVVAR_ULONG64ARRAY, DOIT_ARRAY) \
/*        __TANGO_DEPEND_ON_TYPE_AUX(DEV_INT, DOIT_SIMPLE) */\
/*        __TANGO_DEPEND_ON_TYPE_AUX(DEV_ENCODED, DOIT_SIMPLE)*/ \
        default: \
            assert(false); \
    } } else (void)0

#define TANGO_CALL_ON_DEVICE_DATA_TYPE(tid, fn_simple, fn_array, ...) \
    TANGO_DO_ON_DEVICE_DATA_TYPE(tid, fn_simple<tangoTypeConst>(__VA_ARGS__), fn_array<tangoTypeConst>(__VA_ARGS__))

#define TANGO_DO_ON_NUMERICAL_ATTRIBUTE_DATA_TYPE(tid, DOIT) if (true) { \
    switch(tid) { \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_SHORT, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_LONG, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_DOUBLE, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_FLOAT, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_USHORT, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_ULONG, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_UCHAR, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_LONG64, DOIT) \
        __TANGO_DEPEND_ON_TYPE_AUX(DEV_ULONG64, DOIT) \
        default: \
            assert(false); \
    } } else (void)0

#define TANGO_CALL_ON_NUMERICAL_ATTRIBUTE_DATA_TYPE(tid, fn, ...) \
    TANGO_DO_ON_NUMERICAL_ATTRIBUTE_DATA_TYPE(tid, fn<tangoTypeConst>(__VA_ARGS__))
