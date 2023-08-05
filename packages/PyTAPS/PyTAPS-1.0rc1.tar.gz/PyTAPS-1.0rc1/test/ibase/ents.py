from itaps import iBase, iMesh
import numpy
import unittest

class TestEnts(unittest.TestCase):
    def setUp(self):
        self.mesh = iMesh.Mesh()
        self.ent  = self.mesh.createVtx([0,0,0])
        self.ent2 = self.mesh.getEntities()

        more = self.mesh.createVtx([[0,0,0]]*10)
        self.ents = numpy.concatenate(([self.ent], more))

    def testEquality(self):
        self.assert_(self.ent == self.ent2)
        self.assertFalse(self.ent != self.ent2)
        self.assert_((self.ents == self.ents).all())
        self.assertFalse((self.ents[0:2] != self.ents[0:2]).any())

    def testGet(self):
        self.assertEqual(self.ents[0], self.ent)

    def testSet(self):
        self.ents[1] = self.ent
        self.assertEqual(self.ents[1], self.ent)

    def testSlice(self):
        self.assert_((self.ents[:] == self.ents).all())
        self.assert_((self.ents[0:2] == [self.ents[0], self.ents[1]]).all())
        self.assert_((self.ents[0:4:2] == [self.ents[0], self.ents[2]]).all())
        self.assert_((self.ents[1::-1] == [self.ents[1], self.ents[0]]).all())

    def testSort(self):
        # TODO: assumes array is sorted to begin with
        self.assert_((numpy.sort(self.ents[::-1]) == self.ents).all())
        self.assert_((numpy.sort(self.ents[::-1], kind='mergesort')
                      == self.ents).all())
        self.assert_((numpy.sort(self.ents[::-1], kind='heapsort')
                      == self.ents).all())

        self.assert_((numpy.argsort(self.ents[::-1])
                      == numpy.arange(len(self.ents))[::-1]).all())
        self.assert_((numpy.argsort(self.ents[::-1], kind='mergesort')
                      == numpy.arange(len(self.ents))[::-1]).all())
        self.assert_((numpy.argsort(self.ents[::-1], kind='heapsort')
                      == numpy.arange(len(self.ents))[::-1]).all())


if __name__ == '__main__':
    unittest.main()
