from itaps import iBase, iMesh
import numpy
import unittest

class TestSets(unittest.TestCase):
    def setUp(self):
        self.mesh = iMesh.Mesh()

        self.set  = iBase.EntitySet(self.mesh.createEntSet(True))
        self.set2 = iBase.EntitySet(self.mesh.getEntSets()[0])
        for i in range(5):
            self.mesh.createEntSet(True)
        self.sets = numpy.asarray(self.mesh.getEntSets())

    def testDtype(self):
        self.assertEqual(self.sets.dtype, iBase.EntitySet)

    def testEquality(self):
        self.assert_(self.set == self.set2)
        self.assertFalse(self.set != self.set2)
        self.assert_((self.sets == self.sets).all())
        self.assertFalse((self.sets[0:2] != self.sets[0:2]).any())

    def testGet(self):
        self.assertEqual(self.sets[0], self.set)

    def testSet(self):
        self.sets[1] = self.set
        self.assertEqual(self.sets[1], self.set)

    def testSlice(self):
        self.assert_((self.sets[:] == self.sets).all())
        self.assert_((self.sets[0:2] == [self.sets[0], self.sets[1]]).all())
        self.assert_((self.sets[0:4:2] == [self.sets[0], self.sets[2]]).all())
        self.assert_((self.sets[1::-1] == [self.sets[1], self.sets[0]]).all())

    def testSort(self):
        # TODO: assumes array is sorted to begin with
        self.assert_((numpy.sort(self.sets[::-1]) == self.sets).all())
        self.assert_((numpy.sort(self.sets[::-1], kind='mergesort')
                      == self.sets).all())
        self.assert_((numpy.sort(self.sets[::-1], kind='heapsort')
                      == self.sets).all())

        self.assert_((numpy.argsort(self.sets[::-1])
                      == numpy.arange(len(self.sets))[::-1]).all())
        self.assert_((numpy.argsort(self.sets[::-1], kind='mergesort')
                      == numpy.arange(len(self.sets))[::-1]).all())
        self.assert_((numpy.argsort(self.sets[::-1], kind='heapsort')
                      == numpy.arange(len(self.sets))[::-1]).all())


if __name__ == '__main__':
    unittest.main()
