from __future__ import with_statement
import unittest
import types
import contextPy as cop
from pydcl import requireTypes, require, requireContract, ensureTypes, ensure, ensureContract, requireLayer, ensureLayer, invariantLayer, invariant

firstLayer = cop.layer("1")
secondLayer = cop.layer("2")
thirdLayer = cop.layer("3")
fourthLayer = cop.layer("4")

class RequireTestClass(object):
    
    @requireTypes(self = ["<class '__main__.RequireTestClass'>"])
    def m1(self):
        return "m1"

    @requireTypes(p1 = [int])
    def m2(self, p1):
        return p1
    
    @requireTypes(p1 = [int, float], p2 = [types.NoneType, float])
    def m3(self, p1, p2=None):
        return (p1, p2)
    
    @require("p1 > 0", "p2 > 0")
    def m4(self, p1, p2):
        return p1 + p2
    
    @require("p1 > 0", "p2 > 0")   
    @requireTypes(p1 = [int], p2 = [int])
    def m5(self, p1, p2):
        return p1 + p2    

class EnsureTestClass(object):
    
    def __init__(self):
        self.counter = 0
    
    @ensureTypes(str)
    def m1(self):
        return "m1"
    
    @ensureTypes(str, int)
    def m2(self, p1):
        return p1
    
    @ensureTypes([tuple])
    def m3(self, p1, p2=None):
        return (p1, p2)
    
    @ensure("__result__ > 0")
    def m4(self, p1, p2):
        return p1 + p2
    
    @ensureTypes(int)
    @ensure("__result__ > 0", "p1 < 0")
    def m5(self, p1, p2):
        return p1 + p2
    
    @ensure("self.counter == old(self.counter) + number", "__result__ != 0")
    def inc(self, number):
        if number > 0:
            self.counter += number
        return number

class MultipleTestClass(object):
    
    ccounter = 0
    
    def __init__(self):
        self.counter = 0
    
    @requireTypes(self = ["<class '__main__.MultipleTestClass'>"], p1 = [int, float], p2 = [bool])
    @require("p1 > 0")
    @ensure("self.counter == old(self.counter) + p1", "__result__ == self.counter * p1")
    @ensureTypes(int, float)
    def m1(self, p1, p2):
        if p2:
            self.counter += p1
        return self.counter * p1 
    
    @requireTypes(self = ["<class '__main__.MultipleTestClass'>", "<class '__main__.InheritedTestClass'>"], p1 = [int, float])
    @require("p1 > 0")
    @ensure("__result__ == old(self.counter) + p1")
    @ensureTypes(int, float)
    def m2(self, p1):
        self.counter += p1
        return self.counter
    
    @requireTypes(self = ["<class '__main__.MultipleTestClass'>"], p1 = [int, float], p2 = [bool], __layer__ = (firstLayer, secondLayer))
    @require("p1 > 0", __layer__ = secondLayer)
    @ensure("self.counter == old(self.counter) + p1", "__result__ == self.counter * p1", __layer__ = thirdLayer)
    @ensureTypes(int, float, __layer__ = fourthLayer)
    def m3(self, p1, p2):
        if p2:
            self.counter += p1
        return self.counter * p1     
    
    @requireTypes(cls = [type], p1 = [int, float], p2 = [bool])
    @require("p1 > 0")
    @ensure("cls.ccounter == old(cls.ccounter) + p1", "__result__ == cls.ccounter * p1")
    @ensureTypes(int, float)
    @classmethod
    def cm1(cls, p1, p2):
        if p2:
            cls.ccounter += p1
        return cls.ccounter * p1     
        
    @requireTypes(p1 = [int, float], p2 = [int, float])
    @require("p1 > 0 and p2 > 0")
    @ensure("__result__ == p1 + p2")
    @ensureTypes(int)    
    @staticmethod
    def sm1(p1, p2):
        return p1 + p2
    
    def m4(self):
        self.counter = -1
    
    @invariant()
    def myInvariant(self):
        assert self.counter >= 0
        assert isinstance(self.counter, (int, float))
        assert self.counter < 100
        self.m3(1,False)        

class InheritedTestClass(MultipleTestClass):
    
    @requireTypes(p1 = [int])
    @ensure("__result__ == old(self.counter) + 2 * p1")
    @ensureTypes(int)
    def m2(self, p1):
        super(InheritedTestClass, self).m2(p1)
        self.counter += p1
        return self.counter

@requireTypes(p1 = [int, float], p2 = [int, float])
@require("p1 > 0 and p2 > 0")
@ensure("__result__ == p1 + p2")
@ensureTypes(int)
def f1(p1, p2):
    return p1 + p2

class PartialMethodTestClass(object):
    
    def __init__(self):
        self.counter = 0
            
    @requireContract()
    def m1(self, count):
        assert type(count) == int    
    
    @requireContract(__layer__ = (firstLayer, secondLayer))
    def m1(self, count):
        assert count > 0
      
    @cop.base  
    def m1(self, count):
        self.counter += count
        return self.counter
    
    @ensureContract()
    def m2(self, count):
        oldCounter = self.counter
        assert type(count) == int
        result = cop.proceed(count)
        assert oldCounter + count == self.counter
        return result   
    
    @ensureContract(__layer__ = (firstLayer, secondLayer))
    def m2(self, count):
        #check old condition --> proceed explicit?
        assert count > 0
        result = cop.proceed(count)
        assert result > 0
        assert result == self.counter
        return result
      
    @cop.base  
    def m2(self, count):
        self.counter += count
        if count == 100:
            self.counter = 0
        return self.counter

class ContractTests(unittest.TestCase):
    
    def setUp(self):
        self.reqObj = RequireTestClass()
        self.ensObj = EnsureTestClass()
        self.mulObj = MultipleTestClass()
        self.inhObj = InheritedTestClass()
        self.partObj = PartialMethodTestClass()
    
    def tearDown(self):
        pass

    def testPartialMethodRequireContract(self):
        self.assertEqual(self.partObj.counter, 0)
        self.assertEqual(str(type(self.partObj.m1)), "<class 'contextPy._layeredmethodinvocationproxy'>")
        self.assertEqual(self.partObj.m1(10), 10)
        
        with (cop.activelayer(requireLayer)):
            self.assertEqual(self.partObj.m1(10), 20)
            self.assertRaises(AssertionError, self.partObj.m1, -10)
            self.assertRaises(AssertionError, self.partObj.m1, 1.0)
            self.assertEqual(self.partObj.m1(10), 30)
        
        self.assertEqual(self.partObj.m1(-10), 20)
        
        with (cop.activelayer(firstLayer)):
            self.assertEqual(self.partObj.m1(10), 30)
            self.assertRaises(AssertionError, self.partObj.m1, -10)
            self.assertEqual(self.partObj.m1(1.0), 31.0)
            
    def testPartialMethodEnsureContract(self):
        self.assertEqual(self.partObj.counter, 0)
        self.assertEqual(str(type(self.partObj.m2)), "<class 'contextPy._layeredmethodinvocationproxy'>")
        self.assertEqual(self.partObj.m2(10), 10)
        self.assertEqual(self.partObj.m2(100), 0)
        self.assertEqual(self.partObj.m2(10), 10)
        
        with (cop.activelayer(ensureLayer)):
            self.assertEqual(self.partObj.m2(10), 20)
            self.assertRaises(AssertionError, self.partObj.m2, -10)
            self.assertRaises(AssertionError, self.partObj.m2, 1.0)
            self.assertEqual(self.partObj.m2(10), 30)
            self.assertRaises(AssertionError, self.partObj.m2, 100)
        
        self.assertEqual(self.partObj.m2(-10), -10)
        
        with (cop.activelayer(firstLayer)):
            self.assertRaises(AssertionError, self.partObj.m2, 1)
            self.assertEqual(self.partObj.m2(10), 1)
            self.assertRaises(AssertionError, self.partObj.m2, -10)
            self.assertEqual(self.partObj.m2(1.0), 2.0)
            self.assertRaises(AssertionError, self.partObj.m2, 100)

    def testRequireTypes(self):
        self.assertEqual(self.reqObj.m1(), "m1")
        self.assertEqual(self.reqObj.m2(1), 1)
        self.assertEqual(self.reqObj.m2(1.0), 1.0)
        self.assertEqual(self.reqObj.m3(1), (1, None))
        self.assertEqual(self.reqObj.m3(1, 1.0), (1, 1.0))
        self.assertEqual(self.reqObj.m3("x", "y"), ("x", "y"))
        
        with (cop.activelayer(requireLayer)):
            self.assertEqual(self.reqObj.m1(), "m1")
            self.assertEqual(self.reqObj.m2(1), 1)
            self.assertRaises(AssertionError, self.reqObj.m2, 1.0)
            self.assertEqual(self.reqObj.m3(1, None), (1, None))
            self.assertEqual(self.reqObj.m3(1, 1.0), (1, 1.0))
            self.assertRaises(AssertionError, self.reqObj.m3, "x", "y")
  
    def testRequire(self):
        self.assertEqual(self.reqObj.m4(1,1), 2)
        self.assertEqual(self.reqObj.m4(1.0,1.0), 2.0)
        self.assertEqual(self.reqObj.m4(1,-1), 0)
        self.assertEqual(self.reqObj.m4(-1.0,1.0), 0.0)
        self.assertEqual(self.reqObj.m5(1,1), 2)
        self.assertEqual(self.reqObj.m5(1.0,1.0), 2.0)
        self.assertEqual(self.reqObj.m5(1,-1), 0)
        self.assertEqual(self.reqObj.m5(-1.0,1.0), 0.0) 
        
        with (cop.activelayer(requireLayer)):
            self.assertEqual(self.reqObj.m4(1,1), 2)
            self.assertEqual(self.reqObj.m4(1.0,1.0), 2.0)
            self.assertRaises(AssertionError, self.reqObj.m4, 1,-1)
            self.assertRaises(AssertionError, self.reqObj.m4, -1.0, 1.0)
            self.assertEqual(self.reqObj.m5(1,1), 2)
            self.assertRaises(AssertionError, self.reqObj.m5, 1.0,1.0)
            self.assertRaises(AssertionError, self.reqObj.m5, 1,-1)
            self.assertRaises(AssertionError, self.reqObj.m5, -1.0,1.0)                   
    
    def testEnsureTypes(self):
        self.assertEqual(self.ensObj.m1(), "m1")
        self.assertEqual(self.ensObj.m2(1), 1)
        self.assertEqual(self.ensObj.m2(1.0), 1.0)
        self.assertEqual(self.ensObj.m3(1), (1, None))
        self.assertEqual(self.ensObj.m3(1, 1.0), (1, 1.0))
        self.assertEqual(self.ensObj.m3("x", "y"), ("x", "y"))
        
        with (cop.activelayer(ensureLayer)):
            self.assertEqual(self.ensObj.m1(), "m1")
            self.assertEqual(self.ensObj.m2(1), 1)
            self.assertEqual(self.ensObj.m2("m2"), "m2")
            self.assertRaises(AssertionError, self.ensObj.m2, 1.0)
            self.assertEqual(self.ensObj.m3(1, None), (1, None))
            self.assertEqual(self.ensObj.m3(1, 1.0), (1, 1.0))
    
    def testEnsure(self):
        self.assertEqual(self.ensObj.m4(1,1), 2)
        self.assertEqual(self.ensObj.m4(1.0,1.0), 2.0)
        self.assertEqual(self.ensObj.m4(1,-1), 0)
        self.assertEqual(self.ensObj.m4(-1.0,1.0), 0.0)
        self.assertEqual(self.ensObj.m5(-1,3), 2)
        self.assertEqual(self.ensObj.m5(1,1), 2)
        self.assertEqual(self.ensObj.m5(1.0,1.0), 2.0)
        self.assertEqual(self.ensObj.m5(-1,1), 0)
        self.assertEqual(self.ensObj.m5(-1.0,2.0), 1.0)
        
        with (cop.activelayer(ensureLayer)):
            self.assertEqual(self.ensObj.m4(1,1), 2)
            self.assertEqual(self.ensObj.m4(1.0,1.0), 2.0)
            self.assertRaises(AssertionError, self.ensObj.m4, 1,-1)
            self.assertRaises(AssertionError, self.ensObj.m4, -1.0,1.0)
            self.assertEqual(self.ensObj.m5(-1,3), 2)
            self.assertRaises(AssertionError, self.ensObj.m5, 1,1)
            self.assertRaises(AssertionError, self.ensObj.m5, 1.0, 1.0)
            self.assertRaises(AssertionError, self.ensObj.m5, -1,1)
            self.assertRaises(AssertionError, self.ensObj.m5, -1.0,2.0)
              
    def testEnsureOldValues(self):      
        self.assertEqual(self.ensObj.counter, 0)
        self.assertEqual(self.ensObj.inc(1), 1)
        self.assertEqual(self.ensObj.counter, 1)
        self.assertEqual(self.ensObj.inc(-1), -1)
        self.assertEqual(self.ensObj.counter, 1)
        self.assertEqual(self.ensObj.inc(0), 0)
        self.assertEqual(self.ensObj.counter, 1)
        
        self.ensObj.counter = 0
        
        with (cop.activelayer(ensureLayer)):
            self.assertEqual(self.ensObj.counter, 0)
            self.assertEqual(self.ensObj.inc(1), 1)
            self.assertEqual(self.ensObj.counter, 1)
            self.assertRaises(AssertionError, self.ensObj.inc, -1)
            self.assertEqual(self.ensObj.counter, 1)
            self.assertRaises(AssertionError, self.ensObj.inc, 0)
            self.assertEqual(self.ensObj.counter, 1)

    def testMultipleAnnotations(self):
        self.assertEqual(self.mulObj.counter, 0)
        self.assertEqual(self.mulObj.m1(1, True), 1)
        self.assertEqual(self.mulObj.counter, 1)
        self.assertEqual(self.mulObj.m1(2, False), 2)
        self.assertEqual(self.mulObj.counter, 1)
        self.assertEqual(self.mulObj.m1(3, True), 12)
        self.assertEqual(self.mulObj.counter, 4)
        self.assertEqual(self.mulObj.m1(" ", False), "    ")
        self.assertEqual(self.mulObj.counter, 4)
        self.assertEqual(self.mulObj.m1(-1, True), -3)
        self.assertEqual(self.mulObj.counter, 3)        

        
        self.mulObj.counter = 0
        with (cop.activelayer(requireLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m1(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m1(2, False), 2)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m1(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m1, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m1, -1, True)
            self.assertEqual(self.mulObj.counter, 4)             
        
        self.mulObj.counter = 0
        with (cop.activelayer(ensureLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m1(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertRaises(AssertionError, self.mulObj.m1, 2, False)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m1(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m1, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertEqual(self.mulObj.m1(-1, True), -3)
            self.assertEqual(self.mulObj.counter, 3)                       
            
        self.mulObj.counter = 0
        with (cop.activelayers(requireLayer, ensureLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m1(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertRaises(AssertionError, self.mulObj.m1, 2, False)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m1(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m1, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m1, -1, True)
            self.assertEqual(self.mulObj.counter, 4)
    
    def testClassMethod(self):
        self.assertEqual(self.mulObj.ccounter, 0)
        self.assertEqual(MultipleTestClass.cm1(1, True), 1)
        self.assertEqual(self.mulObj.ccounter, 1)
        self.assertEqual(self.mulObj.cm1(2, False), 2)
        self.assertEqual(self.mulObj.ccounter, 1)
        self.assertEqual(self.mulObj.cm1(3, True), 12)
        self.assertEqual(self.mulObj.ccounter, 4)
        self.assertEqual(MultipleTestClass.cm1(" ", False), "    ")
        self.assertEqual(self.mulObj.ccounter, 4)
        self.assertEqual(MultipleTestClass.cm1(-1, True), -3)
        self.assertEqual(self.mulObj.ccounter, 3)        

        
        MultipleTestClass.ccounter = 0
        with (cop.activelayer(requireLayer)):
            self.assertEqual(self.mulObj.ccounter, 0)
            self.assertEqual(MultipleTestClass.cm1(1, True), 1)
            self.assertEqual(self.mulObj.ccounter, 1)
            self.assertEqual(self.mulObj.cm1(2, False), 2)
            self.assertEqual(self.mulObj.ccounter, 1)
            self.assertEqual(self.mulObj.cm1(3, True), 12)
            self.assertEqual(self.mulObj.ccounter, 4)
            self.assertRaises(AssertionError, MultipleTestClass.cm1, " ", False)
            self.assertEqual(self.mulObj.ccounter, 4)
            self.assertRaises(AssertionError, MultipleTestClass.cm1, -1, True)
            self.assertEqual(self.mulObj.ccounter, 4)             
        
        MultipleTestClass.ccounter = 0
        with (cop.activelayer(ensureLayer)):
            self.assertEqual(self.mulObj.ccounter, 0)
            self.assertEqual(MultipleTestClass.cm1(1, True), 1)
            self.assertEqual(self.mulObj.ccounter, 1)
            self.assertRaises(AssertionError, self.mulObj.cm1, 2, False)
            self.assertEqual(self.mulObj.ccounter, 1)
            self.assertEqual(self.mulObj.cm1(3, True), 12)
            self.assertEqual(self.mulObj.ccounter, 4)
            self.assertRaises(AssertionError, MultipleTestClass.cm1, " ", False)
            self.assertEqual(self.mulObj.ccounter, 4)
            self.assertEqual(MultipleTestClass.cm1(-1, True), -3)
            self.assertEqual(self.mulObj.ccounter, 3)                       
            
        MultipleTestClass.ccounter = 0
        with (cop.activelayers(requireLayer, ensureLayer)):
            self.assertEqual(self.mulObj.ccounter, 0)
            self.assertEqual(MultipleTestClass.cm1(1, True), 1)
            self.assertEqual(self.mulObj.ccounter, 1)
            self.assertRaises(AssertionError, self.mulObj.cm1, 2, False)
            self.assertEqual(self.mulObj.ccounter, 1)
            self.assertEqual(self.mulObj.cm1(3, True), 12)
            self.assertEqual(self.mulObj.ccounter, 4)
            self.assertRaises(AssertionError, MultipleTestClass.cm1, " ", False)
            self.assertEqual(self.mulObj.ccounter, 4)
            self.assertRaises(AssertionError, MultipleTestClass.cm1, -1, True)
            self.assertEqual(self.mulObj.ccounter, 4)
    
    def testStaticMethod(self):
        self.assertEqual(MultipleTestClass.sm1(1,1), 2)
        self.assertEqual(MultipleTestClass.sm1(0,0), 0)
        self.assertEqual(MultipleTestClass.sm1(1.0,1.0), 2.0)
        self.assertEqual(MultipleTestClass.sm1(-1, -1), -2)
        
        with (cop.activelayer(requireLayer)):
            self.assertEqual(MultipleTestClass.sm1(1,1), 2)
            self.assertRaises(AssertionError, MultipleTestClass.sm1, 0,0)
            self.assertEqual(MultipleTestClass.sm1(1.0,1.0), 2.0)
            self.assertRaises(AssertionError, MultipleTestClass.sm1, -1, -1)
            
        with (cop.activelayer(ensureLayer)):
            self.assertEqual(MultipleTestClass.sm1(1,1), 2)
            self.assertEqual(MultipleTestClass.sm1(0,0), 0)
            self.assertRaises(AssertionError, MultipleTestClass.sm1, 1.0,1.0)
            self.assertEqual(MultipleTestClass.sm1(-1, -1), -2)
            
        with (cop.activelayers(requireLayer, ensureLayer)):
            self.assertEqual(MultipleTestClass.sm1(1,1), 2)
            self.assertRaises(AssertionError, MultipleTestClass.sm1, 0,0)
            self.assertRaises(AssertionError, MultipleTestClass.sm1, 1.0,1.0)
            self.assertRaises(AssertionError, MultipleTestClass.sm1, -1, -1)
               
    def testFunction(self):
        self.assertEqual(f1(1,1), 2)
        self.assertEqual(f1(0,0), 0)
        self.assertEqual(f1(1.0,1.0), 2.0)
        self.assertEqual(f1(-1, -1), -2)
        
        with (cop.activelayer(requireLayer)):
            self.assertEqual(f1(1,1), 2)
            self.assertRaises(AssertionError, f1, 0,0)
            self.assertEqual(f1(1.0,1.0), 2.0)
            self.assertRaises(AssertionError, f1, -1, -1)
            
        with (cop.activelayer(ensureLayer)):
            self.assertEqual(f1(1,1), 2)
            self.assertEqual(f1(0,0), 0)
            self.assertRaises(AssertionError, f1, 1.0,1.0)
            self.assertEqual(f1(-1, -1), -2)
            
        with (cop.activelayers(requireLayer, ensureLayer)):
            self.assertEqual(f1(1,1), 2)
            self.assertRaises(AssertionError, f1, 0,0)
            self.assertRaises(AssertionError, f1, 1.0,1.0)
            self.assertRaises(AssertionError, f1, -1, -1)
    
    def testInheritedMethod(self):
        self.assertEqual(self.inhObj.m1(2, True), 4)
        self.assertEqual(self.inhObj.m1(2, False), 4)
        self.assertEqual(self.inhObj.m1(" ", False), "  ")

        self.inhObj.counter = 0
        with (cop.activelayer(requireLayer)):
            self.assertRaises(AssertionError, self.inhObj.m1, 2, True)
            self.assertRaises(AssertionError, self.inhObj.m1, 2, False)
            self.assertRaises(AssertionError, self.inhObj.m1, " ", False)

        self.inhObj.counter = 0
        with (cop.activelayer(ensureLayer)):        
            self.assertEqual(self.inhObj.m1(2, True), 4)
            self.assertRaises(AssertionError, self.inhObj.m1, 2, False)
            self.assertRaises(AssertionError, self.inhObj.m1, " ", False)
        
        self.inhObj.counter = 0
        with (cop.activelayers(requireLayer, ensureLayer)):        
            self.assertRaises(AssertionError, self.inhObj.m1, 2, True)
            self.assertRaises(AssertionError, self.inhObj.m1, 2, False)
            self.assertRaises(AssertionError, self.inhObj.m1, " ", False)
    
    def testSuperCall(self):
        self.assertEqual(self.mulObj.m2(2), 2)
        self.assertEqual(self.inhObj.m2(2), 4)
        self.assertEqual(self.mulObj.m2(2.0), 4.0)
        self.assertEqual(self.inhObj.m2(2.0), 8.0)       
        self.assertEqual(self.inhObj.m2(2), 12.0)       
        self.assertEqual(self.mulObj.m2(-2), 2.0)
        self.assertEqual(self.inhObj.m2(-2), 8.0)
    
        self.mulObj.counter = 0
        self.inhObj.counter = 0
        with (cop.activelayer(requireLayer)):
            self.assertEqual(self.mulObj.m2(2), 2)
            self.assertEqual(self.inhObj.m2(2), 4)
            self.assertEqual(self.mulObj.m2(2.0), 4.0)
            self.assertRaises(AssertionError, self.inhObj.m2, 2.0)       
            self.assertEqual(self.inhObj.m2(2), 8)
            self.assertRaises(AssertionError, self.mulObj.m2, -2)
            self.assertRaises(AssertionError, self.inhObj.m2, -2)    
    
        self.mulObj.counter = 0
        self.inhObj.counter = 0
        with (cop.activelayer(ensureLayer)):
            self.assertEqual(self.mulObj.m2(2), 2)
            self.assertEqual(self.inhObj.m2(2), 4)
            self.assertEqual(self.mulObj.m2(2.0), 4.0)
            self.assertRaises(AssertionError, self.inhObj.m2, 2.0)
            self.assertRaises(AssertionError, self.inhObj.m2, 2)
            self.assertEqual(self.mulObj.m2(-2), 2.0)
            self.assertRaises(AssertionError, self.inhObj.m2, -2)     
    
        self.mulObj.counter = 0
        self.inhObj.counter = 0
        with (cop.activelayers(requireLayer, ensureLayer)):
            self.assertEqual(self.mulObj.m2(2), 2)
            self.assertEqual(self.inhObj.m2(2), 4)
            self.assertEqual(self.mulObj.m2(2.0), 4.0)
            self.assertRaises(AssertionError, self.inhObj.m2, 2.0)
            self.assertEqual(self.inhObj.m2(2), 8)
            self.assertRaises(AssertionError, self.mulObj.m2, -2)
            self.assertRaises(AssertionError, self.inhObj.m2, -2)     
    
    def testAdditionalLayerAssignments(self):
        self.assertEqual(self.mulObj.counter, 0)
        self.assertEqual(self.mulObj.m3(1, True), 1)
        self.assertEqual(self.mulObj.counter, 1)
        self.assertEqual(self.mulObj.m3(2, False), 2)
        self.assertEqual(self.mulObj.counter, 1)
        self.assertEqual(self.mulObj.m3(3, True), 12)
        self.assertEqual(self.mulObj.counter, 4)
        self.assertEqual(self.mulObj.m3(" ", False), "    ")
        self.assertEqual(self.mulObj.counter, 4)
        self.assertEqual(self.mulObj.m3(-1, True), -3)
        self.assertEqual(self.mulObj.counter, 3)        

        
        self.mulObj.counter = 0
        with (cop.activelayer(requireLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m3(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(2, False), 2)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, -1, True)
            self.assertEqual(self.mulObj.counter, 4)   
            
        self.mulObj.counter = 0
        with (cop.activelayer(firstLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m3(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(2, False), 2)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertEqual(self.mulObj.m3(-1, True), -3)
            self.assertEqual(self.mulObj.counter, 3)  
            
        self.mulObj.counter = 0
        with (cop.activelayer(secondLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m3(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(2, False), 2)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, -1, True)
            self.assertEqual(self.mulObj.counter, 4)
        
        self.mulObj.counter = 0
        with (cop.activelayer(ensureLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m3(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertRaises(AssertionError, self.mulObj.m3, 2, False)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertEqual(self.mulObj.m3(-1, True), -3)
            self.assertEqual(self.mulObj.counter, 3)                       
            
        self.mulObj.counter = 0
        with (cop.activelayer(thirdLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m3(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertRaises(AssertionError, self.mulObj.m3, 2, False)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(TypeError, self.mulObj.m3, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertEqual(self.mulObj.m3(-1, True), -3)
            self.assertEqual(self.mulObj.counter, 3)             
            
        self.mulObj.counter = 0
        with (cop.activelayer(fourthLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m3(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(2, False), 2)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertEqual(self.mulObj.m3(-1, True), -3)
            self.assertEqual(self.mulObj.counter, 3) 
            
        self.mulObj.counter = 0
        with (cop.activelayers(thirdLayer, fourthLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m3(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertRaises(AssertionError, self.mulObj.m3, 2, False)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(TypeError, self.mulObj.m3, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertEqual(self.mulObj.m3(-1, True), -3)
            self.assertEqual(self.mulObj.counter, 3)    
            
        self.mulObj.counter = 0
        with (cop.activelayers(fourthLayer, thirdLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m3(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertRaises(AssertionError, self.mulObj.m3, 2, False)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertEqual(self.mulObj.m3(-1, True), -3)
            self.assertEqual(self.mulObj.counter, 3)                  
            
        self.mulObj.counter = 0
        with (cop.activelayers(requireLayer, ensureLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m3(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertRaises(AssertionError, self.mulObj.m3, 2, False)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, -1, True)
            self.assertEqual(self.mulObj.counter, 4)
            
        self.mulObj.counter = 0
        with (cop.activelayers(firstLayer, secondLayer, thirdLayer, fourthLayer)):
            self.assertEqual(self.mulObj.counter, 0)
            self.assertEqual(self.mulObj.m3(1, True), 1)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertRaises(AssertionError, self.mulObj.m3, 2, False)
            self.assertEqual(self.mulObj.counter, 1)
            self.assertEqual(self.mulObj.m3(3, True), 12)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, " ", False)
            self.assertEqual(self.mulObj.counter, 4)
            self.assertRaises(AssertionError, self.mulObj.m3, -1, True)
            self.assertEqual(self.mulObj.counter, 4)            
    
    def testInvariants(self):
        self.assertEqual(self.mulObj.m2(2), 2)
        self.assertEqual(self.mulObj.m2(-4), -2)
        self.assertEqual(self.mulObj.m2(10), 8)
        self.assertEqual(self.mulObj.m2(100), 108)
        
        self.mulObj.counter = 0
        with (cop.activelayer(invariantLayer)):
            self.assertEqual(self.mulObj.m2(2), 2)
            self.assertRaises(AssertionError, self.mulObj.m2, -4)
            self.assertEqual(self.mulObj.counter, -2)
            self.assertRaises(AssertionError, self.mulObj.m2, 10)
            self.assertEqual(self.mulObj.counter, -2)
            self.mulObj.counter = 0
            self.assertRaises(AssertionError, self.mulObj.m2, 100)
            self.assertRaises(AssertionError, self.mulObj.m4)
    
    def testAutomaticMappingUseCasesToLayer(self):
        pass
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContractTests)
    unittest.TextTestRunner(verbosity=1).run(suite)