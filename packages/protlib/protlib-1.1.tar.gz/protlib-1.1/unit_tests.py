import protlib
from protlib import *

import os
import sys
import math
import atexit
import socket
import logging
from glob import glob
from time import sleep
from threading import Thread
from StringIO import StringIO

import unittest
from unittest import TestCase

import warnings
warnings.simplefilter("error", CWarning)

socket.setdefaulttimeout(0.1)

def delete_logs():
    atexit._exithandlers[:] = []    # stop the logging module's exit handler
    for suffix in Logger.LEVELS:
        filename = "unit_tests.{0}_log".format(suffix)
        if os.path.exists(filename):
            handlers = logging.getLogger("unit_tests." + suffix).handlers
            if handlers and handlers[0].stream:
                handlers[0].stream.close()
            os.remove(filename)

class NamedPoint(CStruct):
    code = CShort(always = 0x1234)
    x    = CInt()
    y    = CInt()
    name = CString(length=15, default="unnamed")
NP_BUF = "\x124\x00\x00\x00\x05\x00\x00\x00\x06unnamed\x00\x00\x00\x00\x00\x00\x00\x00"

class RenamedPoint(NamedPoint):
    code = CShort(always = 0x4321)

class NamedOrigin(NamedPoint):
    y = CInt(always = 0)            # field order can be different in subclasses
    code = CShort(always = 0x2332)
    x = CInt(always = 0)

SERVER_ADDR = ("127.0.0.1", 7357)
CLIENT_ADDR = ("127.0.0.1", 5737)

class TestHandler(object):
    def named_point(self, np):
        return RenamedPoint(x=np.x, y=np.y)
    
    def renamed_point(self, rp):
        return "Hello World!\n"

class TCPTestHandler(TCPHandler, TestHandler): pass
class UDPTestHandler(UDPHandler, TestHandler): pass

class CTypeTests(TestCase):
    def test_valid_basic(self):
        for always in [None, 5]:
            for default in [None, 6]:
                for ctype in [CChar,  CShort,  CInt,  CLong,
                              CUChar, CUShort, CUInt, CULong,
                              CFloat, CDouble]:
                    ctype(always=always, default=default)
                CString(length=5, always=always, default=default)
    
    def test_invalid_basic(self):
        self.assertRaises(CError, CType)
        self.assertRaises(CWarning, CInt, length=5)
        self.assertRaises(CWarning, CInt, something=6)
        self.assertRaises(TypeError, CInt, 5)
        self.assertRaises(TypeError, CString, 5)
        self.assertRaises(CError, CInt().parse, "")
        self.assertRaises(CError, CArray(2,CInt).parse, "1234")
    
    def test_integer_boundaries(self):
        for signed,unsigned,exp in [(CChar,CUChar,8), (CShort,CUShort,16), (CInt,CUInt,32), (CLong,CULong,64)]:
            unsigned().serialize(0)
            unsigned().serialize(2**exp - 1)
            self.assertRaises(CError, unsigned().serialize, -1)
            self.assertRaises(CError, unsigned().serialize, 2**exp)
            
            signed().serialize(-2**(exp-1))
            signed().serialize(2**(exp-1) - 1)
            self.assertRaises(CError, signed().serialize, 2**exp - 1)
            self.assertRaises(CError, signed().serialize, -2**(exp-1) - 1)
    
    def test_floating_point_boundaries(self):
        for ctype in [CFloat, CDouble]:
            self.assertTrue( math.isnan(ctype().parse(ctype().serialize(float("nan")))) )
            self.assertEqual(float("inf"), ctype().parse(ctype().serialize(float("inf"))))
            self.assertEqual(float("-inf"), ctype().parse(ctype().serialize(float("-inf"))))
        
        self.assertRaises(CError, CFloat().serialize, sys.float_info.max)
        self.assertRaises(CError, CFloat().serialize, -sys.float_info.max)
        self.assertEqual(0, CFloat().parse(CFloat().serialize(sys.float_info.min)))
        self.assertEqual(0, CFloat().parse(CFloat().serialize(-sys.float_info.min)))
        
        self.assertEqual(sys.float_info.min, CDouble().parse(CDouble().serialize(sys.float_info.min)))
        self.assertEqual(sys.float_info.max, CDouble().parse(CDouble().serialize(sys.float_info.max)))
        self.assertEqual(-sys.float_info.min, CDouble().parse(CDouble().serialize(-sys.float_info.min)))
        self.assertEqual(-sys.float_info.max, CDouble().parse(CDouble().serialize(-sys.float_info.max)))
    
    def test_valid_cstring(self):
        cs = CString(length = 20)
        self.assertEqual(20, len(cs.serialize("Hello World!")))
        self.assertEqual("Hello World!", cs.parse("Hello World!" + "\x00" * 8))
        self.assertEqual("Hello World!", cs.parse("Hello World!\x001234567"))
        
        cs = CString(length = 100)
        self.assertEqual("Hello World!", cs.parse(cs.serialize("Hello World!")))
    
    def test_invalid_cstring(self):
        self.assertRaises(CError, CString)
        self.assertRaises(CError, CString, length=None)
        self.assertRaises(CWarning, CString(length=2).serialize, "Hello")
    
    def test_array_instantiation(self):
        class Point(CStruct):
            x = CInt()
            y = CInt()
        
        CArray(10, CInt)
        CArray(10, CInt())
        CArray(10, Point)
        CArray(10, Point.get_type())
    
    def test_array_packing(self):
        xs = CArray(2, CInt, default=[0,6])
        buf = "\x00\x00\x00\x05\x00\x00\x00\x06"
        self.assertEqual(xs.serialize([5,6]), buf)
        self.assertEqual(xs.serialize([5]), buf)
        self.assertEqual([5,6], xs.parse(buf))
        
        class Words(CStruct):
            message = CArray(2, CString(length=5))
            target = CString(length=6)
        
        self.assertRaises(CWarning, CArray(2,CInt).serialize, [5,6,11])
        self.assertRaises(CWarning, CArray(2, CString(length=5)).serialize, ["Hello","World!"])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", CWarning)
            self.assertEqual(buf, CArray(2,CInt).serialize([5,6,11]))
            self.assertEqual(Words(message=["Bye","Cruel"],         target="Error!").serialize(),
                             Words(message=["Bye","Cruel","World"], target="Error!").serialize())
            protlib.__warningregistry__.clear()
        
        words = Words(message=["hello","world"], target="fair")
        words.message[1:] = []
        self.assertRaises(CError, words.serialize)
    
    def test_array_defaults(self):
        self.assertRaises(CError, CArray, 2, CChar, always=[0])
        self.assertRaises(CError, CArray, 2, CChar, default=[0])
        self.assertRaises(CError, CArray, 2, CChar, always=[0,0,0])
        self.assertRaises(CError, CArray, 2, CChar, default=[0,0,0])
        self.assertRaises(CError, CArray, 2, CChar, default=lambda: [0,0,0])
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", CWarning)
            CArray(2, CChar, always=[0,0,0])
            CArray(2, CChar, default=[0,0,0])
            CArray(2, CChar, default=lambda: [0,0,0])
            protlib.__warningregistry__.clear()
        
        class Point(CStruct):
            xy = CArray(2, CInt, default=[5,6])
        self.assertEqual(Point().xy, [5,6])
        
        class Point(CStruct):
            xy = CArray(2, CInt(default=0))
        self.assertEqual(Point().xy, [0,0])
        
        class Point(CStruct):
            xy = CArray(2, CInt, default=lambda: [5,6])
        self.assertEqual(Point().xy, [5,6])
    
    def test_invalid_arrays(self):
        self.assertRaises(CError, CArray, 10, int)
        self.assertRaises(CWarning, CArray, 10, NamedPoint())
        self.assertRaises(CWarning, CArray(2,CInt).serialize, [5,6,11])
    
    def test_nested_arrays(self):
        matrix = CArray(5, CArray(6, CInt(default=0)))
        self.assertEqual([[0]*6]*5, matrix.parse(matrix.serialize([])))
        
        class Matrix(CStruct):
            xs = CArray(2, CArray(2, CInt))
        Matrix(xs=[[5,6],[7,8]])
        self.assertRaises(CError, Matrix, xs=[])
        self.assertRaises(CError, Matrix, xs=[[0,0], [1,1], [0,1]])
        self.assertRaises(CError, Matrix, xs=[[0,0,0], [1,1,1]])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Matrix(xs=[[0,0], [1,1], [0,1]])
            Matrix(xs=[[0,0,0], [1,1,1]])
            protlib.__warningregistry__.clear()
    
    def test_valid_structs(self):
        np = NamedPoint(x=5, y=6)
        buf = np.serialize()
        pos = NamedPoint(0x1234, 5, 6)
        dup = NamedPoint(0x1234, 5, 6, x=5, y=6)
        parsed = NamedPoint.parse(buf)
        evaled = eval( repr(np) )
        from_file = NamedPoint.parse( StringIO(NP_BUF) )
        
        self.assertEqual(buf, NP_BUF)
        self.assertEqual(np, pos)
        self.assertEqual(np, dup)
        self.assertEqual(np, parsed)
        self.assertEqual(np, evaled)
        self.assertEqual(np, from_file)
    
    def test_struct_equality(self):
        np   = NamedPoint(x=5, y=6)
        same = NamedPoint(x=5, y=6)
        diff = NamedPoint(x=0, y=0)
        
        self.assertTrue(np == same)
        self.assertFalse(np != same)
        self.assertEqual(hash(np), hash(same))
        self.assertEqual([np.code, np.name, np.x, np.y], [same.code, same.name, same.x, same.y])
        
        self.assertTrue(np != diff)
        self.assertFalse(np == diff)
        self.assertNotEqual(hash(np), hash(diff))
        self.assertEqual([np.code, np.name, np.x, np.y], [same.code, same.name, same.x, same.y])
    
    def test_nested_structs(self):
        class Segment(CStruct):
            p1 = NamedPoint.get_type()
            p2 = NamedPoint.get_type()
        Segment(p1=NamedPoint(x=5,y=6), p2=NamedPoint(x=11,y=42))
        Segment.parse(NP_BUF * 2)
        Segment.parse(NP_BUF * 2 + "extra data in buffer")
    
    def test_struct_arrays(self):
        class Segment(CStruct):
            points = CArray(2, NamedPoint)
        Segment()
        Segment([NamedPoint(x=5,y=6), NamedPoint(x=7,y=11)]).serialize()
        seg = Segment([NamedPoint(x=5,y=6), NamedPoint(x=7,y=11)])
        seg.points[:] = []
        self.assertRaises(CError, seg.serialize)
        self.assertRaises(CError, Segment().serialize)
        self.assertRaises(CError, Segment, [NamedPoint(x=5,y=6)])
        self.assertRaises(CError, Segment, [NamedPoint(x=5,y=6)]*3)
    
    def test_invalid_struct_instances(self):
        self.assertRaises(CError, CStruct)
        self.assertRaises(CError, NamedPoint, x = ["wrong", "type"])
        self.assertRaises(CError, NamedPoint, x = 2 ** 33)
        self.assertRaises(CWarning, NamedPoint, x=5, y=6, z=12)
        self.assertRaises(CError, NamedPoint, 0x1234, 5, x=6)
        self.assertRaises(CError, NamedPoint(x=5).serialize)
        self.assertRaises(CWarning, NamedPoint, code=0x4321, x=5, y=6)
        self.assertRaises(CWarning, NamedPoint.parse, "!C\x00\x00\x00\x05\x00\x00\x00\x06unnamed\x00\x00\x00\x00\x00\x00\x00\x00")
    
    def test_invalid_structs(self):
        self.assertRaises(CError, NamedPoint.parse, "not enough data")
        
        class Point(CStruct):
            pass
        self.assertRaises(CError, Point)
        self.assertRaises(CError, Point.parse, "\x00\x00\x00\x00")
        
        class Point(CStruct):
            x = CInt
        self.assertRaises(CError, Point)
        self.assertRaises(CError, Point.parse, "\x00\x00\x00\x00")
        
        class Segment(CStruct):
            p1 = NamedPoint
            p2 = NamedPoint
        self.assertRaises(CError, Segment)
        self.assertRaises(CError, Segment.parse, NP_BUF * 2)
        
        class Segment(CStruct):
            p1 = NamedPoint()
            p2 = NamedPoint()
        self.assertRaises(CError, Segment)
        self.assertRaises(CError, Segment.parse, NP_BUF * 2)
        self.assertRaises(CError, Segment, p1 = "not a Segment instance")
    
    def test_unsubclassed_structs(self):
        self.assertRaises(CError, CStruct)
        self.assertRaises(CError, CStruct.sizeof)
        self.assertRaises(CError, CStruct.get_type)
        self.assertRaises(CError, CStruct.parse, "")
        self.assertRaises(CError, CStruct.struct_format)
    
    def test_duplicate_fields(self):
        class Point(CStruct):
            x = y = CInt()
        self.assertRaises(CWarning, Point)
        self.assertRaises(CWarning, Point.parse, "\x00" * 8)
    
    def test_valid_inheritance(self):
        class Origin(NamedPoint):
            x = y = CInt(always = 0)
        orig = Origin()
        self.assertEqual([orig.x, orig.y], [0, 0])
        self.assertRaises(CWarning, Origin.parse, NP_BUF)
    
    def test_invalid_inheritance(self):
        class Origin(NamedPoint):
            x = y = CChar(always = 0)
        self.assertRaises(CError, Origin)
        
        class Origin(NamedPoint):
            x = y = 0
        self.assertRaises(CError, Origin)
    
    def test_type_coercion(self):
        self.assertEqual(5, NamedPoint(x="5").x)
        self.assertEqual("6", NamedPoint(name=6).name)
        
        class Letter(CStruct):
            c = CChar()
        self.assertEqual(5, Letter(c=5).c)
        self.assertEqual(ord("A"), Letter(c="A").c)
        
        class Letters(CStruct):
            xs = CArray(2, CChar)
        self.assertEqual([5, ord("A")], Letters(xs=[5,"A"]).xs)
        
        class Point(CStruct):
            xy = CArray(2, CChar, default=[5,"\x06"])
        self.assertEqual(Point().xy, [5,6])
        self.assertEqual(Point(xy=[1]).serialize(), "\x01\x06")
        
        class Point(CStruct):
            xy = CArray(2, CChar, default=lambda: [5,"\x06"])
        self.assertEqual(Point().xy, [5,6])
        self.assertEqual(Point(xy=[1]).serialize(), "\x01\x06")
        
        self.assertRaises(CError, NamedPoint, x=5.6)
        self.assertRaises(CError, CArray, 2, CInt, always=[0, 1.2])
        self.assertRaises(CError, CArray, 2, CInt, default=[0, 1.2])
        self.assertRaises(CError, CArray, 2, CInt, default=lambda:[0, 1.2])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", CWarning)
            NamedPoint(x=5.6)
            CArray(2, CInt, always=[0, 1.2])
            CArray(2, CInt, default=[0, 1.2])
            CArray(2, CInt, default=lambda:[0, 1.2])
            protlib.__warningregistry__.clear()

class UnderscorizeTests(TestCase):
    def test_camelcase(self):
        self.assertEqual("some_struct",   underscorize("SomeStruct"))
        self.assertEqual("ssn_lookup",    underscorize("SSNLookup"))
        self.assertEqual("rs485_adaptor", underscorize("RS485Adaptor"))
        self.assertEqual("rot13_encoded", underscorize("Rot13Encoded"))
        self.assertEqual("request_q",     underscorize("request_q"))
        self.assertEqual("john316",       underscorize("John316"))
    
    def test_already_underscored(self):
        self.assertEqual("rs485adaptor",  underscorize("rs485adaptor"))
        self.assertEqual("rot13_encoded", underscorize("rot13_encoded"))

class BadHandlerTests(TestCase):
    def test_no_structs(self):
        class EmptyHandler(ProtHandler):
            class STRUCT_MOD:
                pass
        self.assertRaises(CError, EmptyHandler)
    
    def test_duplicate_starts(self):
        class DupHandler(ProtHandler):
            class STRUCT_MOD:
                class Foo(CStruct):
                    code = CInt(always = 1)
                class Bar(CStruct):
                    code = CInt(always = 1)
        self.assertRaises(CWarning, DupHandler)
    
    def test_bad_struct_name(self):
        class BadNameHandler(ProtHandler):
            class STRUCT_MOD:
                class Handle(CStruct):
                    code = CInt(always = 1)
        self.assertRaises(CError, BadNameHandler)

class ServerTests:
    def setUp(self):
        self.reset_logs()
        
        self.server = self.ServerClass(SERVER_ADDR, self.HandlerClass)
        t = Thread(target=self.server.serve_forever)
        t.daemon = True
        t.start()
        
        self.client_setup()
        
        self.np = NamedPoint(x=5, y=6)
        self.rp = RenamedPoint(x=5, y=6)
    
    def tearDown(self):
        self.sock.close()
        self.server.shutdown()
        self.server.socket.close()
        self.reset_logs()
    
    def client_teardown(self):
        self.sock.close()
    
    def reset_logs(self):
        for suffix in Logger.LEVELS:
            handlers = logging.getLogger("unit_tests." + suffix).handlers
            if handlers and handlers[0].stream:
                handlers[0].stream.truncate(0)
    
    def read_log(self, name):
        with open("unit_tests." + name + "_log") as f:
            return f.read()
    
    def test_struct_response(self):
        self.send(self.np)
        rp = RenamedPoint.parse(self.f)
        self.assertEqual(rp, self.rp)
    
    def test_string_response(self):
        self.send(self.rp)
        self.assertEqual(self.f.readline(), "Hello World!\n")
    
    def test_too_short(self):
        self.send( self.np.serialize()[:5] )
        sleep(0.2)
        #import pdb ; pdb.set_trace()
        self.assertTrue("struct requires" in self.read_log("error"))
    
    def test_no_handler(self):
        self.send( NamedOrigin() )
        sleep(0.2)
        self.assertTrue("handler not defined" in self.read_log("error"))
    
    def test_unknown(self):
        self.send("raw data")
        sleep(0.2)
        self.assertTrue("unable to resolve" in self.read_log("error"))
    
    def test_multiple_clients(self):
        self.test_struct_response()
        self.client_teardown()
        self.client_setup()
        self.test_struct_response()

class TCPServerTests(ServerTests, TestCase):
    ServerClass = LoggingTCPServer
    HandlerClass = TCPTestHandler
    
    def client_setup(self):
        self.sock = socket.create_connection(SERVER_ADDR)
        self.f = self.sock.makefile("r+b", bufsize=0)
    
    def send(self, data):
        self.f.write(data)
        self.f.flush()

class UDPServerTests(ServerTests, TestCase):
    ServerClass = LoggingUDPServer
    HandlerClass = UDPTestHandler
    
    def client_setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(CLIENT_ADDR)
        self.f = self.sock.makefile("rb")
    
    def send(self, data):
        self.sock.sendto(str(data), SERVER_ADDR)

if __name__ == "__main__":
    delete_logs()
    atexit.register(delete_logs)
    unittest.main()
