from itaps import iBase, iGeom
import numpy
import testhelper as unittest

class TestArray(unittest.TestCase):
    def setUp(self):
        self.geom = iGeom.Geom()

        self.set = self.geom.createEntSet(True)
        for i in range(5):
            self.geom.createEntSet(True)
        self.sets = self.geom.getEntSets()

        self.bset = iBase.EntitySet(self.set)
        self.bsets = numpy.asarray(self.sets)

        self.tag = self.geom.createTag("foo", 1, 'i')
        self.tag[self.set] = 1
        for name in "bar", "baz", "quux":
            tmp = self.geom.createTag(name, 1, 'i')
            tmp[self.set] = 1
        self.tags = self.geom.getAllTags(self.set)

        self.btag = iBase.Tag(self.tag)
        self.btags = numpy.asarray(self.tags)

    def tearDown(self):
        for s in self.sets:
            self.geom.destroyEntSet(s)
        # Make sure we don't delete any core tags
        for t in "foo", "bar", "baz", "quux":
            self.geom.destroyTag(self.geom.getTagHandle(t), True)

    def testSetArray(self):
        sets = iBase.Array(self.sets)
        self.assertArray(sets, self.sets)
        self.assertEqual(type(sets), iBase.Array)
        self.assertEqual(sets.instance, self.geom)
        self.assertEqual(sets.dtype.type, iBase.EntitySet)

        sets = iBase.Array(self.bsets, instance=self.geom)
        self.assertArray(sets, self.sets)
        self.assertEqual(type(sets), iBase.Array)
        self.assertEqual(sets.instance, self.geom)
        self.assertEqual(sets.dtype.type, iBase.EntitySet)

    def testSetArrayList(self):
        sets = iBase.Array(self.sets.tolist())
        self.assertArray(sets, self.sets)
        self.assertEqual(type(sets), iBase.Array)
        self.assertEqual(sets.instance, self.geom)
        self.assertEqual(sets.dtype.type, iBase.EntitySet)

        sets = iBase.Array(self.bsets.tolist(), instance=self.geom)
        self.assertArray(sets, self.sets)
        self.assertEqual(type(sets), iBase.Array)
        self.assertEqual(sets.instance, self.geom)
        self.assertEqual(sets.dtype.type, iBase.EntitySet)

    def testSetArrayScalar(self):
        sets = iBase.Array(self.set)
        self.assertEqual(sets, self.sets[0:1])
        self.assertEqual(type(sets), iBase.Array)
        self.assertEqual(sets.instance, self.geom)
        self.assertEqual(sets.dtype.type, iBase.EntitySet)

        sets = iBase.Array(self.bset, instance=self.geom)
        self.assertEqual(sets, self.sets[0:1])
        self.assertEqual(type(sets), iBase.Array)
        self.assertEqual(sets.instance, self.geom)
        self.assertEqual(sets.dtype.type, iBase.EntitySet)

    def testSetEquality(self):
        self.assertEqual(self.set,  self.set)
        self.assertEqual(self.set,  self.bset)
        self.assertEqual(self.bset, self.set)

        self.assertArray(self.sets,  self.sets)
        self.assertArray(self.sets,  self.bsets)
        self.assertArray(self.bsets, self.sets)

        self.assertFalse((self.sets[0:2] != self.sets[0:2]).any())
        self.assertFalse((self.sets[0:2] != self.bsets[0:2]).any())
        self.assertFalse((self.bsets[0:2] != self.sets[0:2]).any())

    def testSetIn(self):
        self.assertTrue(self.set  in self.sets)
        self.assertTrue(self.bset in self.sets)
        self.assertTrue(self.set  in self.bsets)

    def testSetGet(self):
        self.assertEqual(self.sets[0], self.set)
        self.assertEqual(self.sets[0].instance, self.geom)

    def testSetSet(self):
        sets = self.sets.copy()
        sets[1] = self.set
        self.assertEqual(sets[1], self.set)
        self.assertEqual(sets[0].instance, self.geom)

    def _testSetSort(self):
        # TODO: assumes array is sorted to begin with
        self.assertArray(numpy.sort(self.sets[::-1]), self.sets)
        self.assertArray(numpy.sort(self.sets[::-1], kind='mergesort'),
                         self.sets)
        self.assertArray(numpy.sort(self.sets[::-1], kind='heapsort'),
                         self.sets)

        self.assertArray(numpy.argsort(self.sets[::-1]),
                         numpy.arange(len(self.sets))[::-1])
        self.assertArray(numpy.argsort(self.sets[::-1], kind='mergesort'),
                         numpy.arange(len(self.sets))[::-1])
        self.assertArray(numpy.argsort(self.sets[::-1], kind='heapsort'),
                         numpy.arange(len(self.sets))[::-1])

    def testTagArray(self):
        tags = iBase.Array(self.tags)
        self.assertArray(tags, self.tags)
        self.assertEqual(type(tags), iBase.Array)
        self.assertEqual(tags.instance, self.geom)
        self.assertEqual(tags.dtype.type, iBase.Tag)

        tags = iBase.Array(self.btags, instance=self.geom)
        self.assertArray(tags, self.tags)
        self.assertEqual(type(tags), iBase.Array)
        self.assertEqual(tags.instance, self.geom)
        self.assertEqual(tags.dtype.type, iBase.Tag)

    def testTagArrayList(self):
        tags = iBase.Array(self.tags.tolist())
        self.assertArray(tags, self.tags)
        self.assertEqual(type(tags), iBase.Array)
        self.assertEqual(tags.instance, self.geom)
        self.assertEqual(tags.dtype.type, iBase.Tag)

        tags = iBase.Array(self.btags.tolist(), instance=self.geom)
        self.assertArray(tags, self.tags)
        self.assertEqual(type(tags), iBase.Array)
        self.assertEqual(tags.instance, self.geom)
        self.assertEqual(tags.dtype.type, iBase.Tag)

    def testTagArrayScalar(self):
        tags = iBase.Array(self.tag)
        self.assertEqual(tags, self.tags[0:1])
        self.assertEqual(type(tags), iBase.Array)
        self.assertEqual(tags.instance, self.geom)
        self.assertEqual(tags.dtype.type, iBase.Tag)

        tags = iBase.Array(self.btag, instance=self.geom)
        self.assertEqual(tags, self.tags[0:1])
        self.assertEqual(type(tags), iBase.Array)
        self.assertEqual(tags.instance, self.geom)
        self.assertEqual(tags.dtype.type, iBase.Tag)

    def testTagEquality(self):
        self.assertEqual(self.tag,  self.tag)
        self.assertEqual(self.tag,  self.btag)
        self.assertEqual(self.btag, self.tag)

        self.assertArray(self.tags,  self.tags)
        self.assertArray(self.tags,  self.btags)
        self.assertArray(self.btags, self.tags)

        self.assertFalse((self.tags[0:2] != self.tags[0:2]).any())
        self.assertFalse((self.tags[0:2] != self.btags[0:2]).any())
        self.assertFalse((self.btags[0:2] != self.tags[0:2]).any())

    def testTagIn(self):
        self.assertTrue(self.tag  in self.tags)
        self.assertTrue(self.btag in self.tags)
        self.assertTrue(self.tag  in self.btags)

    def testTagGet(self):
        self.assertEqual(self.tags[0], self.tag)
        self.assertEqual(self.tags[0].instance, self.geom)

    def testTagSet(self):
        self.tags[1] = self.tag
        self.assertEqual(self.tags[1], self.tag)
        self.assertEqual(self.tags[0].instance, self.geom)

    def _testTagSort(self):
        # TODO: assumes array is sorted to begin with
        self.assertArray(numpy.sort(self.tags[::-1]), self.tags)
        self.assertArray(numpy.sort(self.tags[::-1], kind='mergesort'),
                         self.tags)
        self.assertArray(numpy.sort(self.tags[::-1], kind='heapsort'),
                         self.tags)

        self.assertArray(numpy.argsort(self.tags[::-1]),
                         numpy.arange(len(self.tags))[::-1])
        self.assertArray(numpy.argsort(self.tags[::-1], kind='mergesort'),
                         numpy.arange(len(self.tags))[::-1])
        self.assertArray(numpy.argsort(self.tags[::-1], kind='heapsort'),
                         numpy.arange(len(self.tags))[::-1])


if __name__ == '__main__':
    unittest.main()
