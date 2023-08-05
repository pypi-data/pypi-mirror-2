"""
protlib builds on the struct and SocketServer modules in the standard
library to make it easy to implement binary network protocols. It provides 
support for default and constant struct fields, nested structs, arrays of
structs, better handling for strings and arrays, struct inheritance, and
convenient syntax for instantiating and using your custom structs.
"""

import sys
import struct
import socket
import logging
import warnings
import traceback
from time import mktime
from copy import deepcopy
from select import select
from warnings import warn
from types import NoneType
from datetime import datetime
from StringIO import StringIO
from logging.handlers import RotatingFileHandler
from logging import getLogger, Formatter, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from SocketServer import TCPServer, UDPServer, StreamRequestHandler, DatagramRequestHandler

__all__ = ["CError", "CWarning",
           "CType", "CStruct", "CStructType", "CArray",
           "CChar", "CUChar", "CShort", "CUShort", "CInt", "CUInt", "CLong", "CULong", "CFloat", "CDouble", "CString",
           "Parser", "Logger", "ProtHandler", "TCPHandler", "UDPHandler", "LoggingTCPServer", "LoggingUDPServer",
           "underscorize", "hexdump",
           "BYTE_ORDER", "DEFAULT_TIMEOUT"]

class CError(BaseException):
    """the only exception class raised directly by protlib"""

class CWarning(UserWarning):
    """the only warning class directly used by protlib (except DeprecationWarning)"""

__version_info__ = (1, 1, 0, "final", 0)
__version__ = "{0}.{1}.{2}".format(*__version_info__)

BYTE_ORDER = "!"
DEFAULT_TIMEOUT = 5     # seconds

def _get_default(val):
    return val() if hasattr(val, "__call__") else deepcopy(val)

def _fileize(x):
    return StringIO(x) if isinstance(x, basestring) else x

def _inherit_docstrings(klass):
    for name,field in klass.__dict__.items():
        parent = getattr(klass.__bases__[0], name, None)
        if hasattr(field, "__call__") and not field.__doc__ and parent:
            field.__doc__ = parent.__doc__
    return klass



class CType(object):
    """
    This is the root class of all classes representing C data types in the
    protlib library. It may not be directly instantiated; you must always
    use one of its subtypes instead.
    
    Whenever any CType is instantiated, it is appended to the
    CType.instances list. This is used internally to define the order of 
    fields in a CStruct. However, CStructs themselves are not added to this
    list unless CStruct.get_type() is called.
    
    Users of the protlib library don't need to know or care about this list,
    but they may find it useful for advanced usage.  Theoretically this list
    may cause your program's memory usage to grow if you continually
    instantiate CTypes as your program runs.  In this case you may need to 
    manually remove the CTypes from the end of this list after creating
    them.
    """
    instances = []
    
    def __init__(self, **settings):
        """
        CTypes have three optional keyword arguments:
        
        length -- required for CString and CArray,
                  invalid for everything else
        
        always -- Use this to set a constant value for a field. You won't
                  need to specify this value, and a warning will be raised
                  if the value ever differs from this parameter.
        
        default -- Like the always parameter, except that no warnings are
                   raised when a different value is assigned, parsed, or 
                   serialized. Also, unlike an always parameter, a default 
                   parameter may be  either a value or a callable object.
        """
        self.always = self.default = self.length = None
        extra = [name for name,val in settings.items() if not hasattr(self, name)]
        if extra:
            warn("{0} settings do not include {1}".format(self.__class__.__name__, ", ".join(extra)), CWarning)
        
        self.__dict__.update(settings)
        if self.length is not None and not isinstance(self, (CString, CArray)):
            warn("length has no meaning for {0} objects".format(self.__class__.__name__), CWarning)
        if isinstance(self, CString) and (not isinstance(self.length, int) or self.length <= 0):
            raise CError("CString objects require a length attribute")
        if self.__class__ is CType:
            raise CError("CType may not be directly instantiated; use a subclass such as CInt, CString, etc")
        
        self.instances.append(self)
    
    @property
    def struct_format(self):
        """the format string used to represent this CType in the struct module"""
        return {
            "CChar":   "b",
            "CUChar":  "B",
            "CShort":  "h",
            "CUShort": "H",
            "CInt":    "i",
            "CUInt":   "I",
            "CLong":   "q",
            "CULong":  "Q",
            "CFloat":  "f",
            "CDouble": "d",
            "CString": "{0}s".format(self.length)
        }[self.__class__.__name__]
    
    @property
    def sizeof(self):
        """the number of bytes of binary data needed to represent this CType"""
        return struct.calcsize(BYTE_ORDER + self.struct_format)
    
    def parse(self, f):
        r"""
        Accepts either a string or a file and returns a Python object with 
        the appropriate value.  For example, CInt().parse will return a 
        Python int, etc.  This raises CError if not given enough data.
        
        CString parsing returns the string up to the first null byte, e.g.
        
        CString(length=10).parse("foo\x00barbaz") -> "foo"
        """
        buf = _fileize(f).read(self.sizeof)
        if len(buf) < self.sizeof:
            raise CError("{0} requires {1} bytes and was given {2}".format(self.__class__.__name__, self.sizeof, len(buf)))
        return struct.unpack(BYTE_ORDER + self.struct_format, buf)[0]
    
    def serialize(self, val):
        r"""
        Serializes the given value into binary data using the struct module.
        
        Unserializable problems with the value will raise a CError, e.g.
            CShort().serialize( 2 ** 17 )       # value too large
            CLong().serialize("hello")          # wrong data type
            CArray(5, CInt).serialize([2,3])    # not enough elements
        
        Passing a too-short list to a CArray is okay if a default value
        was provided:
            CArray(2, CChar(default=0)).serialize([1]) -> "\x01\x00"
        
        Passing too much data to a CArray or CString will trigger a
        CWarning, e.g.
            CArray(2, CInt).serialize([5,6,7])
            CString(length=3).serialize("Hello")
        
        Passing a too-short string to a CString is always okay:
            CString(length=4).serialize("Hi") -> "Hi\x00\x00"
        """
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", DeprecationWarning)
                return struct.pack(BYTE_ORDER + self.struct_format, val)
        except:
            exc_class, exc, tb = sys.exc_info()
            cerror = CError("{0!r} is not serializable as a {1}: {2}".format(val, self.__class__.__name__, exc.args[0]))
            raise CError, cerror, tb

class CChar(CType): pass
class CUChar(CType): pass
class CShort(CType): pass
class CUShort(CType): pass
class CInt(CType): pass
class CUInt(CType): pass
class CLong(CType): pass
class CULong(CType): pass
class CFloat(CType): pass
class CDouble(CType): pass

@_inherit_docstrings
class CString(CType):
    def parse(self, f):
        return CType.parse(self, f).split("\x00")[0]
    
    def serialize(self, val):
        if len(val) > self.length:
            warn("CString has length {0} and was told to serialize a string of length {1}".format(self.length, len(val)), CWarning)
        return CType.serialize(self, val)

@_inherit_docstrings
class CArray(CType):
    def __init__(self, length, ctype, **params):
        """
        You can make an array of any CType, including other arrays. Arrays
        pack and unpack to and from Python lists.  Arrays may either be
        given default/always values themselves or use the default/always
        values of  the CType they are given.  Here are some example CArray
        declarations:

        CArray(5, CInt)
        CArray(5, CString(length=4))
        CArray(8, CLong(default=0))
        CArray(3, CInt, always=[0,0,0])
        CArray(5, CArray(4, CShort))
        """
        if type(ctype) is type and issubclass(ctype, CType):    # CArray(10, CInt) and CArray(10, CInt()) are both allowed
            if issubclass(ctype, CStruct):                      # CArray(10, MyStruct) and CArray(10, MyStruct.get_type()) are both allowed
                ctype = ctype.get_type()
            else:
                ctype = ctype()
        
        if not isinstance(ctype, CType):
            raise CError("Second argument to CArray must be a CType e.g. CInt, CFloat, etc")
        elif isinstance(ctype, CStruct):
            ctype = ctype.__class__
            warn("Second argument to CArray should just be the class {0} rather than an instance of that class".format(ctype.__name__), CWarning)
        
        self.ctype = ctype
        
        for param in ["default","always"]:
            if param not in params and getattr(self.ctype, param, None) is not None:
                params[param] = [_get_default(getattr(self.ctype, param)) for i in range(length)]
        
        CType.__init__(self, length=length, **params)
        
        for param,value in [("always",self.always), ("default",self.default)]:
            if value is not None:
                try:
                    value = _get_default(value) if param=="default" else value
                    self.serialize( _get_converter(self)(value) )
                except:
                    exc_class, exc, tb = sys.exc_info()
                    cerror = CError("{0!r} is not a valid {1} CArray value: {2}".format(value, param, exc.args[0]))
                    raise CError, cerror, tb
    
    @property
    def struct_format(self):
        return self.ctype.struct_format * self.length
    
    def parse(self, f):
        f = _fileize(f)
        return [self.ctype.parse(f) for i in range(self.length)]
    
    def serialize(self, xs):
        if len(xs) > self.length:
            warn("CArray has length {0} and was given {1} elements".format(self.length, len(xs)), CWarning)
            xs = xs[:self.length]
        elif len(xs) < self.length:
            if self.default is not None:
                xs = xs + _get_default(self.default)[len(xs):]    # avoid += to not mutate the original list
            if len(xs) < self.length:
                raise CError("CArray has length {0} and was only given {1} elements".format(self.length, len(xs)))
        
        xs = _get_converter(self)(xs)
        return "".join(self.ctype.serialize(x) for x in xs)

@_inherit_docstrings
class CStructType(CType):
    """
    When defining your own struct, you subclass CStruct and give it the
    proper fields:
    
    class Point(CStruct):
        x = CInt()
        y = CInt()
    
    This type is used to include one struct inside another:
    
    class Segment(CStruct):
        p1 = Point.get_type()
        p2 = Point.get_type()
    
    Each call to get_type() returns a CStructType instance, which is used
    to represent the struct type being used.  Other than calling get_type(),
    protlib users should probably never need to interact with this class
    directly.
    """
    
    def __init__(self, subclass, **params):
        """
        In addition to the usual keyword arguments accepted by CTypes,
        this constructor takes the CStruct subclass being represented.
        """
        self.subclass = subclass
        CType.__init__(self, **params)
    
    @property
    def struct_format(self):
        return "".join(ctype.struct_format for name,ctype in self.subclass.get_fields())
    
    def parse(self, f):
        buf = _fileize(f).read(self.sizeof)
        f = StringIO(buf)
        if len(buf) < self.sizeof:
            raise CError("{0} requires {1} bytes and was only given {2} ({3!r})".format(self.subclass.__name__, self.sizeof, len(buf), buf))
        
        params = {}
        for name,ctype in self.subclass.get_fields():
            params[name] = ctype.parse(f)
        return self.subclass(**params)
    
    def serialize(self, inst):
        serialized = ""
        for name,ctype in self.subclass.get_fields():
            val = getattr(inst, name, None)
            if val is None or isinstance(val, CType) and not isinstance(val, CStruct):
                raise CError(name + " not set")
            serialized += ctype.serialize(val)
        return serialized

class CStruct(CType):
    def __init__(self, *args, **values):
        """
        CStruct should never be instantiated directly. Instead, you should
        subclass it when defining a custom struct. Your subclass will be
        given a constructor which takes the fields of your struct as
        positional and/or keyword arguments. However, you don't have to
        provide values for your fields at this time; you can leave struct
        fields unset, although a CError will be raised if you call the 
        serialize method on a CStruct with unset fields.
        """
        if self.__class__ is CStruct:
            raise CError("CStruct may not be instantiated directly; define a subclass instead")
        
        fields = self.get_fields()
        if not fields:
            raise CError("{0} struct contains no CType fields".format(self.__class__.__name__))
        
        field_names = zip(*fields)[0]
        for i,arg in enumerate(args):
            name = field_names[i]
            if name in values and values[name] != arg:
                raise CError("{0} was given a value of {1!r} as a positional argument and {2!r} as a keyword argument".format(name, arg, values[name]))
            values[name] = arg
        
        non_fields = [name for name,value in values.items() if name not in field_names]
        if non_fields:
            warn("{0} fields ({1}) do not include {2}".format(self.__class__.__name__, ", ".join(field_names), ", ".join(non_fields)), CWarning)
        
        for name,ctype in fields:
            maybe = ctype.always if ctype.always is not None else ctype.default
            if maybe is not None:
                setattr(self, name, _get_default(maybe))
        
        for name,value in values.items():
            setattr(self, name, value)
    
    @classmethod
    def get_fields(cls):
        """
        Returns a list of name/value pairs representing this struct's
        fields.  Each pair is the name of the field and the CType instance
        which defines that field.  The list is sorted according to the
        order in which the fields appear in the struct.
        
        Users probably don't need to call this method unless they need to
        introspect their own CStruct subclasses.
        """
        if cls is CStruct:
            raise CError("CStruct classmethods may only be called on subclasses of CStruct")
        
        if "_fields" not in cls.__dict__:   # avoid hasattr because of subclasses
            uninstantiated = [ctype for name,ctype in cls.__dict__.items() 
                                    if type(ctype) is type and issubclass(ctype,CType)]
            if uninstantiated:
                raise CError("Use {0}{2} instead of {0} when declaring a field in your {1} struct".format(uninstantiated[0].__name__, cls.__name__, ".get_type()" if issubclass(uninstantiated[0],CStruct) else "()"))
            
            directly = [cstruct for name,cstruct in cls.__dict__.items() 
                                if isinstance(cstruct, CStruct)]
            if directly:
                raise CError("Use {0}.get_type() instead of {0}() when declaring a field in your {1} struct".format(directly[0].__class__.__name__, cls.__name__))
            
            top = cls
            while CStruct not in top.__bases__:
                for base in top.__bases__:
                    if issubclass(top, CStruct):
                        top = base
                    break
            
            if top is cls:
                fields = [[name,ctype] for name,ctype in cls.__dict__.items() 
                                       if isinstance(ctype, CType)]
                fields.sort(key = lambda pair: CType.instances.index(pair[1]))
                
                positions = [(CType.instances.index(ctype),name,ctype) for name,ctype in fields]
                for i in range(1, len(positions)):
                    if positions[i][0] == positions[i-1][0]:
                        warn("{0} and {1} were declared with the same {2} object; the order of such fields is undefined".format(positions[i-1][1], positions[i][1], positions[i][2].__class__.__name__), CWarning)
                        break
            else:
                fields = deepcopy( top.get_fields() )
                for pair in fields:
                    final = getattr(cls, pair[0])
                    if not isinstance(final, CType):
                        raise CError("{0} field overridden by non-CType {1!r}".format(pair[0], final))
                    elif final.sizeof != pair[1].sizeof:
                        raise CError("{0[0]} field of type {0[1]} was overridden by differently-sized type {1}".format(pair, final.__class__.__name__))
                    pair[1] = final
            
            cls._fields = fields
        return cls._fields
    
    @classmethod
    def get_type(cls, cached=False, **params):
        """
        Returns a CStructType instance representing this struct; see the
        CStructType class for details.
        
        cached -- Indicates whether it's acceptable to return a cached
                  CStructType instance, or whether a new CStructType should
                  be created.  This should never be set to True when using
                  this method to include one struct inside another struct, 
                  which is probably the only time that users will ever call
                  this method.
        """
        if cls is CStruct:
            raise CError("CStruct classmethods may only be called on subclasses of CStruct")
        
        if not ("_type" in cls.__dict__ and cached):    # avoid hasattr because of subclasses
            cls._type = [CStructType(cls, **params)]    # stored in a list so that isinstance(self._type, CType) will evaluate to false
        return cls._type[0]
    
    @classmethod
    def parse(cls, f):
        """
        Returns an instance of this CStruct by parsing the input from the
        string or file given as a parameter.  This raises a CError if not
        enough data is provided.
        """
        return cls.get_type(cached=True).parse(f)
    
    @classmethod
    def sizeof(cls):
        """
        Returns the number of bytes needed to represent this CStruct as
        packed binary data.
        """
        return cls.get_type(cached=True).sizeof
    
    @classmethod
    def struct_format(cls):
        """
        Returns the struct format string used by the struct module to pack
        and unpack this CStruct.
        """
        return cls.get_type(cached=True).struct_format
    
    def serialize(self):
        """
        Returns packed binary data which represents this CStruct instance.
        This raises a CError if any of the fields have not been set.
        """
        return self.get_type(cached=True).serialize(self)
    
    __str__ = serialize
    
    def __repr__(self):
        """
        Returns a literal representation of this struct.  This may be
        copy/pasted into a Python file or interpreter as valid code.  For
        example:
        
        repr(Point(x=5, y=6)) == "Point(x=5, y=6)"
        """
        params = ["{0}={1!r}".format(name, getattr(self,name))
                  for name,ctype in self.get_fields() if hasattr(self,name)]
        return "{0}({1})".format(self.__class__.__name__, ", ".join(params))
    
    @property
    def hashable(self):
        if not hasattr(self, "_hashable"):
            xs = [getattr(self, name, None) for name,ctype in self.get_fields()]
            self._hashable = tuple(tuple(x) if isinstance(x, list) else x for x in xs)
        return self._hashable
    def __hash__(self):
        return hash(self.hashable)
    def __eq__(self, other):
        return self.hashable == getattr(other, "hashable", None)
    def __ne__(self, other):
        return not (self == other)          # Python is stupid for making me do this
    
    def __setattr__(self, name, value):
        """
        Whenever you assign a value to a struct field, that value is
        converted to the appropriate data type.  So if you assign the
        string "5" to a CInt field, it will be converted to the int 5.
        This triggers a CWarning if data is truncated, such as when a
        float is assigned to an integer field, or when a string or list
        is too long.
        
        CChar and CUChar fields may either be assigned an integer or a
        single-character string.  Such strings are converted to integers
        with the builtin ord function.  Thus, while assigning a CInt field
        the value of "5" converts to the int 5, assigning the value "5" to
        a CChar converts to the int 53.
        """
        field = getattr(self.__class__, name, None)
        if isinstance(field, CStructType):
            if not isinstance(value, field.subclass):
                raise CError("{0} assigned to the {1} field {2}.{3}".format(value.__class__.__name__, field.subclass.__name__, self.__class__.__name__, name))
        elif isinstance(field, CType):
            try:
                value = _get_converter(field)(value)
            except:
                exc_class, exc, tb = sys.exc_info()
                cerror = CError("Conversion error: you provided the {0} value {1!r} to the {2} field {3}.{4}: {5}".format(value.__class__.__name__, value, field.__class__.__name__, self.__class__.__name__, name, exc.args[0]))
                raise CError, cerror, tb
            
            try:
                field.serialize(value)
            except:
                exc_class, exc, tb = sys.exc_info()
                cerror = CError("{0!r} is an invalid value for the {1} field {2}.{3}: {4}".format(value, field.__class__.__name__, self.__class__.__name__, name, exc.args[0]))
                raise CError, cerror, tb
            
            if field.always is not None and value != field.always:
                warn("{0}.{1} should always be {2!r} but was given a value of {3!r}".format(self.__class__.__name__, name, field.always, value), CWarning)
        
        object.__setattr__(self, name, value)

_converters = {
    CFloat:  float,
    CDouble: float,
    CString: str,
    CChar:   lambda c: ord(c) if isinstance(c, basestring) else int(c),
    CUChar:  lambda c: ord(c) if isinstance(c, basestring) else int(c)
}
def _to_int(x):
    if isinstance(x, float) and x != int(x):
        warn("Loss of precision when converting a float ({0}) to an integer field".format(x), CWarning)
    return int(x)

for ctype in [CShort, CUShort, CInt, CUInt, CLong, CULong]:
    _converters[ctype] = _to_int
del ctype

def _get_converter(field):
    if isinstance(field, CStructType):
        return lambda cstruct: cstruct
    elif isinstance(field, CArray):
        def converter(xs):
            conv = _get_converter(field.ctype)
            return [conv(x) for x in xs]
        return converter
    else:
        return _converters.get(field.__class__)



_formatter = Formatter("%(asctime)s: %(message)s")

class _AlsoPrint(logging.Handler):
    def emit(self, record):
        print( _formatter.format(record) )

class _NullHandler(logging.Handler):
    def emit(self, record):
        pass

def underscorize(camelcased):
    """
    Takes a CamelCase string and returns a separated_with_underscores
    version of that name in all lower case.  If the name is already all in
    lower case and/or separated with underscores, then the returned string
    is identical to the original.  This function is used to take CStruct
    class names and determine the names of their handler methods.
    
    Here are some example conversions:
        underscorize("SomeStruct")   == "some_struct"
        underscorize("SSNLookup")    == "ssn_lookup"
        underscorize("RS485Adaptor") == "rs485_adaptor"
        underscorize("Rot13Encoded") == "rot13_encoded"
        underscorize("RequestQ")     == "request_q"
        underscorize("John316")      == "john316"
    """
    underscored, prev = "", ""
    for i,c in enumerate(camelcased):
        if (prev and not c.islower() and c != "_"
                 and (prev.islower() and not c.isdigit()
                      or c.isupper() and camelcased[i+1:i+2].islower())):
            underscored += "_"
        underscored += c.lower()
        prev = c
    return underscored

def hexdump(data):
    """
    Returns a multi-line string containing a nicely formatted table of the
    hexadecimal representation of the ordinal values of each character in
    the string passed as a parameter.
    """
    hexed = [hex(ord(char))[2:].rjust(2,"0") for char in data]
    lines = ["     0  1  2  3  4  5  6  7"]
    for i in range(0, len(hexed), 8):
        lines.append("%3i  " % i + " ".join(hexed[i:i+8]))
    return "\n".join(lines)

class Parser(object):
    """
    The classmethod CStruct.parse may be used to read struct objects from
    strings or files, such as by saying "p = Point.parse(f)", but this
    requires that you know the type of struct you need to parse.  This
    class exists to check the data being parsed to see which struct is being
    read with error checking and logging as appropriate.
    """
    
    def __init__(self, logger=None, module=None):
        """
        Arguments:
        
        logger - The instance of the Logger class to use to perform logging.
                 If omitted, a Logger will be created with a handler whose
                 level is 1 + logging.CRITICAL
        
        module - This is exactly the same as the ProtHandler.STRUCT_MOD
                 field; if present then it indicates which module contains
                 the struct classes you want to use. If omitted, then the
                 module where this class is instantiated is used.
                 
                 CError is raised if no CStruct subclasses exist in this
                 module, and a CWarning is triggered if multiple CStruct
                 subclasses are found which begin with the same constant
                 values.
                 
                 This class only detects structs which were defined when
                 it was instantiated.  Structs defined afterwards will not
                 be detected.
        """
        
        self.logger = logger or Logger(rfh_level=CRITICAL+1)
        
        if not module:
            globs = sys._getframe().f_back.f_globals
        else:
            if isinstance(module, basestring):
                module = __import__(module)
            globs = module.__dict__
        
        self.structs = [cstruct for name,cstruct in globs.items()
                        if type(cstruct) is type and issubclass(cstruct,CStruct) and cstruct is not CStruct]
        self.codes = []
        for cstruct in self.structs:
            first = cstruct.get_fields()[0][1]
            if first.always is not None:
                self.codes.append( (first.serialize(first.always), cstruct) )
        self.codes.sort(key = lambda code: len(code[0]))
        if not self.codes:
            raise CError("No structs which begin with constant values were defined in the module " + (module.__name__ if module else "where you instantiated Parser"))
        
        bufs = zip(*self.codes)[0]
        while bufs:
            matches = [b for b in bufs if bufs[0] == b[:len(bufs[0])]]
            if len(matches) > 1:
                structs = ", ".join(cstruct.__name__ for buf,cstruct in self.codes if buf in matches)
                warn("{0} structs exist which always begin with {1!r}: {2}".format(len(matches), bufs[0], structs), CWarning)
            bufs = [b for b in bufs if b not in matches]

    def parse(self, f):
        """
        Accepts a string or file object and returns a string or CStruct
        according to these rules:
         - If a CStruct can be successfully parsed, then it's logged
           and returned.
         - If the data does not correspond to any CStruct, then all
           available data is logged and returned.
         - If the data represents a certain CStruct, but is too short,
           then an error is logged and None is returned.
        """
        f = _fileize(f)
        buf = ""
        for code,cstruct in self.codes:
            diff = len(code) - len(buf)
            if diff:
                buf += f.read(diff)
                if len(buf) < len(code):
                    break
            
            if code == buf:
                bufsize = cstruct.sizeof()
                buf += f.read(bufsize - len(buf))
                self.logger.log_binary(buf, "received")
                
                if len(buf) < bufsize:
                    self.logger.log_error("{0} struct requires {1} bytes, received {2} ({3!r})", cstruct.__name__, bufsize, len(buf), buf)
                    return
                else:
                    inst = cstruct.parse(buf)
                    self.logger.log_struct(inst, "received")
                    return inst
        else:
            buf += f.read()
        
        if buf:
            self.logger.log_binary(buf, "received")
        return buf

class Logger(object):
    """
    This class is used by the ProtHandler subclasses to log the messages
    sent and received by the LoggingTCPServer and LoggingUDPServer classes.
    The protlib handler classes inherit from this class, so you won't need
    to instantiate this class directly when writing server programs, but
    you may find this class useful when writing client programs.
    
    Internally this class uses the logging module from the standard library.
    Each log name has a prefix, which by default is the name of the script
    being executed, and a suffix.  There are 5 logs, each with their own
    suffix: hex, raw, struct, error, and stack.  For example, if you're
    running the script "server.py" then these will be the log names and the
    logging levels of their messages:
    
    server.hex - DEBUG level, contains nicely formatted hex dump of the
                 binary data sent and received
    
    server.raw - INFO level, contains Python string literals of the binary
                 data sent and received
    
    server.struct - WARNING level, contains literal representations of each
                    struct sent and received
    
    server.error - ERROR level, contains error messages
    
    server.stack - CRITICAL level, contains stack traces of exceptions
                   thrown by handler methods
    
    For each log, if no handlers already exist, then a RotatingFileHandler
    with a Formatter is instantiated, using the MAX_BYTES and BACKUP_COUNT
    fields for the maxBytes and backupCount parameter, and creating a log
    file in the current directory.  If you'd like to use different handlers
    for your logging, you can simply your own handler(s) and formatter(s)
    for any or all of these logs, and then they will be used instead.  You
    must do this before this class is instantiated, or else your handler(s)
    will simply be used in addition to the default RotatingFileHander.
    
    By default, each of these loggers has its propagate field set to False.
    """
    BACKUP_COUNT = 1
    MAX_BYTES = 1024 ** 2
    DEFAULT_PREFIX = sys.argv[0].split(".")[0] or "__main__"
    LEVELS = {"hex":DEBUG, "raw":INFO, "struct":WARNING, "error":ERROR, "stack":CRITICAL}
    
    def __init__(self, prefix=None, also_print=False, rfh_level=NOTSET, hex_logging=None, log_dir=None):
        """
        Arguments (hex_logging and log_dir are deprecated):
        
        prefix - overrides the default prefix for the log names
        
        also_print - if True, log messages will be printed to the screen
                     in addition to whatever else happens to them
        
        rfh_level - used internally to set the the logging level of the
                    default RotatingFileHandler
        """
        if log_dir:
            warn("log_dir parameter is deprecated and ignored, you should use the logging.handler classes to affect log locations and properties", DeprecationWarning)
        if hex_logging:
            warn("hex_logging parameter is deprecated and ignored, hex dumps are now written to their own separate log", DeprecationWarning)
        
        self.__prefix = prefix or self.DEFAULT_PREFIX
        for suffix in self.LEVELS:
            logger = getLogger(self.__prefix + "." + suffix)
            logger.propagate = False
            
            if not logger.handlers:
                try:
                    handler = RotatingFileHandler(logger.name+"_log", maxBytes=self.MAX_BYTES, backupCount=self.BACKUP_COUNT)
                    handler.setFormatter(_formatter)
                    handler.setLevel(rfh_level)
                except IOError:
                    handler = _NullHandler()    # directory not writable
                
                logger.addHandler(handler)
            
            if also_print:
                logger.addHandler( _AlsoPrint() )
    
    def log_binary(self, data, trans_type="received"):
        """
        Writes the data string to the raw and hex logs.  The trans_type is
        prepended to each log message and indicates whether this data was
        just received or is about to be sent.        
        """
        self.log("hex", trans_type + "\n" + hexdump(data))
        self.log("raw", trans_type + " " + repr(data))
    
    def log_raw(self, data, trans_type="received"):
        """deprecated alias for log_binary"""
        warn("log_raw is deprecated, use log_binary instead", DeprecationWarning)
        self.log_binary(data, trans_type)
    
    def log_struct(self, inst, trans_type="received"):
        """
        Writes a CStruct instance to the struct log.  The trans_type is
        prepended to each log message and indicates whether this data was
        just received or is about to be sent.  
        """
        self.log("struct", trans_type + " " + repr(inst))
    
    def log_error(self, message, *args, **kwargs):
        """
        Writes a message to the error log, calling str.format with the
        extra positional and keyword arguments passed to this function.
        """
        self.log("error", message.format(*args, **kwargs))

    def log_stacktrace(self):
        """writes a stacktrace from the last thrown exception to the stack log"""
        self.log("stack", traceback.format_exc())
    
    def log_and_write(self, f, data):
        """
        Given a file object and a string or CStruct object, log it to
        the appropriate logs, then write it to the file.
        """
        if isinstance(data, CStruct):
            self.log_struct(data, "sending")
            data = data.serialize()
        self.log_binary(data, "sending")
        f.write(data)
    
    def log(self, suffix, message):
        """
        Write a message to the specified log; the suffix parameter should be
        one of "hex", "raw", "struct", "error", or "stack".
        """
        getLogger(self.__prefix + "." + suffix).log(self.LEVELS[suffix], message)

class ProtHandler(Logger):
    """
    Root class for protocol handerls, which itself inherits from Logger for
    ease of providing informative logging for handler methods.  Do not
    subclass this class directly; instead you should subclass either the
    TCPHandler or UDPHandler class, as appropriate.
    """
    LOG_PREFIX = LOG_TO_SCREEN = STRUCT_MOD = False
    
    def __init__(self, server=None):
        """you'll probably never need to instantiate this class directly"""
        if hasattr(self, "LOG_DIR"):
            warn("LOG_DIR field is deprecated and ignored, you should use the logging.handler classes to affect log locations and properties", DeprecationWarning)
        if hasattr(self, "HEX_LOGGING"):
            warn("HEX_LOGGING field is deprecated and ignored, hex dumps are now written to their own separate log", DeprecationWarning)
        
        Logger.__init__(self, prefix = self.LOG_PREFIX, also_print = self.LOG_TO_SCREEN,
                              rfh_level = INFO if isinstance(server, (LoggingTCPServer, LoggingUDPServer, NoneType)) else 1+CRITICAL)
        self.__parser = Parser(logger=self, module=self.STRUCT_MOD or self.__class__.__module__)
        
        for buf,cstruct in self.__parser.codes:
            if underscorize(cstruct.__name__) in dir(TCPHandler):
                raise CError("You can't name your struct {0} because that's also the name of a standard handler method".format(cstruct.__name__))
        
        self.__handled = 0
        self.__prefix = int(mktime( datetime.now().timetuple() ))
    
    def log(self, suffix, message):
        """
        Overrides Logger.log to add a prefix to every log message which
        uniquely identifies the binary data being sent/received.
        """
        message = "({0}_{1}) {2}".format(self.__prefix, self.__handled, message)
        Logger.log(self, suffix, message)
    
    def dispatch(self, data):
        """
        Given a string or cstruct, this calls the appropriate handler method
        and returns the result.  If no handler method exists for a cstruct,
        an error is logged.
        """
        if isinstance(data, basestring):
            return self.raw_data(data)
        
        codename = underscorize(data.__class__.__name__)
        if not hasattr(self, codename):
            self.log_error("{0} handler not defined", codename)
        else:
            return getattr(self, codename)(data)
    
    def reply(self, data):
        """given a string or cstruct, log the data and write it to self.wfile"""
        if isinstance(data, CStruct):
            self.log_struct(data, "sending")
            data = data.serialize()
        self.log_binary(data, "sending")
        self.wfile.write(data)
        self.wfile.flush()
    
    def raw_data(self, data):
        """
        Default handler for raw data.  Override this method if you want to
        actually respond to data which is not parsable into a cstruct.  By
        default this method simply logs an error.
        """
        if data:
            self.log_error("unable to resolve {0!r} to a struct", data)
    
    def handle(self):
        """
        Continually reads data from self.rfile and calls the appropriate
        handler method until no more data is available.
        """
        try:
            data = self.__parser.parse(self)
            while data:
                response = self.dispatch(data)
                if response:
                    self.reply(response)
                
                self.__handled += 1
                data = self.__parser.parse(self)
        except:
            self.log_stacktrace()

class TCPHandler(ProtHandler, StreamRequestHandler):
    """
    Subclass this class for use with the SocketServer.TCPServer class or any
    of its subclasses, such as protlib.LoggingTCPServer
    """
    
    def __init__(self, request, client_addr, server):
        """you'll probably never need to instantiate this class directly"""
        ProtHandler.__init__(self, server)
        StreamRequestHandler.__init__(self, request, client_addr, server)
    
    def read(self, n=None):
        """
        Repeatedly calls select on self.rfile and returns the next n bytes,
        or however much data is available by the time the socket times out.
        If the user has called socket.setdefaulttimeout(), then that value
        is used, otherwise the global DEFAULT_TIMEOUT constant is used,
        which is 5 seconds.
        """
        buf = ""
        while True:
            r,w,exc = select([self.rfile], [], [], socket.getdefaulttimeout() or DEFAULT_TIMEOUT)
            c = r[0].read(1) if r else ""
            buf += c                                    # shlemiel the painter
            if not r or not c or n and len(buf) >= n:
                break
        return buf

class UDPHandler(ProtHandler, DatagramRequestHandler):
    """
    Subclass this class for use with the SocketServer.UDPServer class or any
    of its subclasses, such as protlib.LoggingUDPServer
    """
    
    def __init__(self, request, client_addr, server):
        """you'll probably never need to instantiate this class directly"""
        ProtHandler.__init__(self, server)
        DatagramRequestHandler.__init__(self, request, client_addr, server)
    
    def read(self, n=-1):
        """returns the result of calling read on self.rfile"""
        return self.rfile.read(n)

class LoggingUDPServer(UDPServer):
    """
    When using a ProtHandler subclass with any other SocketServer class,
    the level of the RotatingFileHandler is set to 1 + logging.CRITICAL;
    with this class it's instead set to logging.INFO.
    
    Also, the allow_reuse_address field is set to True for this class.
    """
    allow_reuse_address = True

class LoggingTCPServer(TCPServer):
    """
    When using a ProtHandler subclass with any other SocketServer class,
    the level of the RotatingFileHandler is set to 1 + logging.CRITICAL;
    with this class it's instead set to logging.INFO.
    
    Also, the allow_reuse_address field is set to True for this class.
    """
    allow_reuse_address = True
