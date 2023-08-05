import unittest
import numpy

# numpy.zeros_like and friends are broken for C subclasses of ndarray.
# This hacks around it.
def zeros_like(a):
    if isinstance(a, numpy.ndarray):
        res = numpy.zeros(a.shape, a.dtype, order=a.flags.fnc)
        res = res.view(type(a))
        res.__array_finalize__(a)
        return res
    return numpy.zeros_like(a)

class TestCase(unittest.TestCase):
    def assertArray(self, a, b):
        """Assert that two NumPy arrays are identical"""
        a, b = numpy.asanyarray(a), numpy.asanyarray(b)
        self.assertTrue(a.shape == b.shape)
        self.assertTrue((a == b).all())

    def assertArraySorted(self, a, b):
        """Assert that two NumPy arrays are identical when sorted"""
        self.assertArray(numpy.sort(a), numpy.sort(b))

    def assertOut(self, func, *args, **kw):
        expected = kw['ex']
        out = zeros_like(expected)

        self.assertArray(func(*args), expected)
        self.assertArray(func(out=out, *args), out)
        self.assertArray(out, expected)

main = unittest.main
