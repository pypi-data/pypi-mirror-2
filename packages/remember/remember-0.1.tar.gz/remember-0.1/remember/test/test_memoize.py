try:
    import unittest2 as unittest
except ImportError:
    import unittest


from remember import memoize


class TestMemoizeMixin(object):
    def setUp(self):
        self.in1 = 1, 2
        self.in2 = 1, 2
        self.assertIsNot(self.in1, self.in2)
        
    def test_equal_and_identical(self):
        ret1 = self.identity(self.in1)
        ret2 = self.identity(self.in2)

        self.assertIs(ret1, ret2)
        self.assertIs(self.in1, ret2)
        
        self.assertIs(self.listify(self.in1), self.listify(self.in1))
        
        
class TestMemoizeAllowUnhashable(unittest.TestCase, TestMemoizeMixin):
    def setUp(self):
        TestMemoizeMixin.setUp(self)
        
        self.identity = memoize.memoize()(lambda x: x)
        self.listify = memoize.memoize()(list)
        
    def test_no_unhashable(self): 
        self.identity([1])
        
    def test_equal_and_identical_unhashable(self):
        x = [1, 2]
        a = self.listify(x)
        b = self.listify(x)
        self.assertIsNot(a, b)
               
               
class TestMemoizeNoUnhashable(unittest.TestCase, TestMemoizeMixin):
    def setUp(self):
        TestMemoizeMixin.setUp(self)
    
        self.identity = memoize.memoize(allow_unhashable=False)(lambda x: x)
        self.listify = memoize.memoize(allow_unhashable=False)(list)
        
    def test_no_unhashable(self): 
        with self.assertRaises(TypeError):
            self.identity([1])

