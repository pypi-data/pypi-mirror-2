from itaps import iBase, iMesh
import numpy
import unittest

class TestTags(unittest.TestCase):
    def setUp(self):
        self.mesh = iMesh.Mesh()

        tag = self.mesh.createTag("foo", 1, 'i')
        self.tag  = iBase.Tag(tag)
        self.tag2 = iBase.Tag( self.mesh.getTagHandle("foo") )

        tag[self.mesh.rootSet] = 1
        for name in "bar", "baz", "quux":
            tmp = self.mesh.createTag(name, 1, 'i')
            tmp[self.mesh.rootSet] = 1
        self.tags = numpy.asarray(self.mesh.getAllTags(self.mesh.rootSet))

    def testDtype(self):
        self.assertEqual(self.tags.dtype, iBase.Tag)

    def testEquality(self):
        self.assertTrue(self.tag == self.tag2)
        self.assertFalse(self.tag != self.tag2)
        self.assertTrue((self.tags == self.tags).all())
        self.assertFalse((self.tags[0:2] != self.tags[0:2]).any())

    def testGet(self):
        self.assertEqual(self.tags[0], self.tag)

    def testSet(self):
        self.tags[1] = self.tag
        self.assertEqual(self.tags[1], self.tag)

    def testSlice(self):
        self.assert_((self.tags[:] == self.tags).all())
        self.assert_((self.tags[0:2] == [self.tags[0], self.tags[1]]).all())
        self.assert_((self.tags[0:4:2] == [self.tags[0], self.tags[2]]).all())
        self.assert_((self.tags[1::-1] == [self.tags[1], self.tags[0]]).all())

    def testSort(self):
        # TODO: assumes array is sorted to begin with
        self.assert_((numpy.sort(self.tags[::-1]) == self.tags).all())
        self.assert_((numpy.sort(self.tags[::-1], kind='mergesort')
                      == self.tags).all())
        self.assert_((numpy.sort(self.tags[::-1], kind='heapsort')
                      == self.tags).all())

        self.assert_((numpy.argsort(self.tags[::-1])
                      == numpy.arange(len(self.tags))[::-1]).all())
        self.assert_((numpy.argsort(self.tags[::-1], kind='mergesort')
                      == numpy.arange(len(self.tags))[::-1]).all())
        self.assert_((numpy.argsort(self.tags[::-1], kind='heapsort')
                      == numpy.arange(len(self.tags))[::-1]).all())


if __name__ == '__main__':
    unittest.main()
