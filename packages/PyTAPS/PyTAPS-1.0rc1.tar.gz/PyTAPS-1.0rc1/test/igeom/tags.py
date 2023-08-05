from itaps import iBase, iGeom
import unittest
import numpy

class TestTags(unittest.TestCase):
    def setUp(self):
        self.geom = iGeom.Geom()

        self.itag = self.geom.createTag('int',    1, 'i')
        self.dtag = self.geom.createTag('double', 1, 'd')
        self.etag = self.geom.createTag('handle', 1, 'E')
        self.btag = self.geom.createTag('byte',   1, 'b')

        self.i3tag = self.geom.createTag('int3',    3, 'i')
        self.d3tag = self.geom.createTag('double3', 3, 'd')
        self.e3tag = self.geom.createTag('handle3', 3, 'E')
        self.b3tag = self.geom.createTag('byte3',   3, 'b')

        self.ent  = self.geom.createBrick(1, 1, 1)
        self.ents = self.geom.getEntities(iBase.Type.all)[0:3]
        self.set  = self.geom.createEntSet(True)

    def tearDown(self):
        self.geom.deleteAll()
        for tag in (self.itag,  self.dtag,  self.etag,  self.btag,
                    self.i3tag, self.d3tag, self.e3tag, self.b3tag):
            self.geom.destroyTag(tag, True)

    def testCreation(self):
        self.assertEqual(self.itag.instance, self.geom)
        self.assertEqual(self.itag.name, 'int')
        self.assertEqual(self.itag.type, 'i')
        self.assertEqual(self.itag.sizeValues, 1)

        self.assertEqual(self.dtag.instance, self.geom)
        self.assertEqual(self.dtag.name, 'double')
        self.assertEqual(self.dtag.type, 'd')
        self.assertEqual(self.dtag.sizeValues, 1)
        self.assertEqual(self.dtag.sizeBytes, 8)

        self.assertEqual(self.etag.instance, self.geom)
        self.assertEqual(self.etag.name, 'handle')
        self.assertEqual(self.etag.type, 'E')
        self.assertEqual(self.etag.sizeValues, 1)

        self.assertEqual(self.btag.instance, self.geom)
        self.assertEqual(self.btag.name, 'byte')
        self.assertEqual(self.btag.type, 'b')
        self.assertEqual(self.btag.sizeValues, 1)
        self.assertEqual(self.btag.sizeBytes, 1)

    def testAlternate(self):
        itag = self.geom.createTag('int_',    1, int)
        dtag = self.geom.createTag('double_', 1, float)
        etag = self.geom.createTag('handle_', 1, iBase.Entity)
        btag = self.geom.createTag('byte_',   1, numpy.byte)

        self.assertEqual(itag.type, 'i')
        self.assertEqual(dtag.type, 'd')
        self.assertEqual(etag.type, 'E')
        self.assertEqual(btag.type, 'b')

    def testDestruction(self):
        self.geom.destroyTag(self.itag, True)
        self.assertRaises(iBase.ITAPSError, self.geom.getTagHandle, 'int')

    def testFind(self):
        t = self.geom.getTagHandle('int')
        self.assertEqual(t.name, self.itag.name)

        self.assertRaises(iBase.ITAPSError, self.geom.getTagHandle, 'potato')


    def testIntData(self):
        self.itag[self.ent] = 42
        self.assertEqual(self.itag[self.ent], 42)

        del self.itag[self.ent]
        self.assertRaises(iBase.ITAPSError, lambda: self.itag[self.ent])

    def testDblData(self):
        self.dtag[self.ent] = 42
        self.assertEqual(self.dtag[self.ent], 42)

        del self.dtag[self.ent]
        self.assertRaises(iBase.ITAPSError, lambda: self.dtag[self.ent])

    def testEHData(self):
        self.etag[self.ent] = self.ent
        self.assertEqual(self.etag[self.ent], self.ent)

        del self.etag[self.ent]
        self.assertRaises(iBase.ITAPSError, lambda: self.etag[self.ent])

    def testRawData(self):
        self.btag[self.ent] = 42
        self.assert_((self.btag[self.ent] == 42).all())

        del self.btag[self.ent]
        self.assertRaises(iBase.ITAPSError, lambda: self.btag[self.ent])


    def testIntArrData(self):
        self.i3tag[self.ent] = [42]*3
        self.assert_((self.i3tag[self.ent] == [42]*3).all())

        del self.i3tag[self.ent]
        self.assertRaises(iBase.ITAPSError, lambda: self.i3tag[self.ent])

    def testDblArrData(self):
        self.d3tag[self.ent] = [42]*3
        self.assert_((self.d3tag[self.ent] == [42]*3).all())

        del self.d3tag[self.ent]
        self.assertRaises(iBase.ITAPSError, lambda: self.d3tag[self.ent])

    def testEHArrData(self):
        self.e3tag[self.ent] = [self.ent]*3
        self.assert_((self.e3tag[self.ent] == [self.ent]*3).all())

        del self.e3tag[self.ent]
        self.assertRaises(iBase.ITAPSError, lambda: self.e3tag[self.ent])

    def testRawArrData(self):
        self.b3tag[self.ent] = [42]*3
        self.assert_((self.b3tag[self.ent] == [42]*3).all())

        del self.b3tag[self.ent]
        self.assertRaises(iBase.ITAPSError, lambda: self.b3tag[self.ent])


    def testArrIntData(self):
        self.itag[self.ents] = [42]*3

        self.assert_((self.itag[self.ents] == [42]*3).all())
        self.assertEqual(self.itag[self.ents[0]], 42)

        del self.itag[self.ents]
        self.assertRaises(iBase.ITAPSError, lambda: self.itag[self.ents])

    def testArrDblData(self):
        self.dtag[self.ents] = [42]*3

        self.assert_((self.dtag[self.ents] == [42]*3).all())
        self.assertEqual(self.dtag[self.ents[0]], 42)

        del self.dtag[self.ents]
        self.assertRaises(iBase.ITAPSError, lambda: self.dtag[self.ents])

    def testArrEHData(self):
        self.etag[self.ents] = self.ents

        self.assert_((self.etag[self.ents] == self.ents).all())
        self.assertEqual(self.etag[self.ents[0]], self.ents[0])

        del self.etag[self.ents]
        self.assertRaises(iBase.ITAPSError, lambda: self.etag[self.ents])

    def testArrRawData(self):
        self.btag[self.ents] = [42]*3

        self.assert_((self.btag[self.ents] == [42]*3).all())
        self.assertEqual(self.btag[self.ents[0]], 42)

        del self.btag[self.ents]
        self.assertRaises(iBase.ITAPSError, lambda: self.btag[self.ents])


    def testArrIntArrData(self):
        self.i3tag[self.ents] = [[1,2,3]]*3

        self.assert_((self.i3tag[self.ents] == [[1,2,3]]*3).all())
        self.assert_((self.i3tag[self.ents[0]] == [1,2,3]).all())

        del self.i3tag[self.ents]
        self.assertRaises(iBase.ITAPSError, lambda: self.i3tag[self.ents])

    def testArrDblArrData(self):
        self.d3tag[self.ents] = [[1,2,3]]*3

        self.assert_((self.d3tag[self.ents] == [[1,2,3]]*3).all())
        self.assert_((self.d3tag[self.ents[0]] == [1,2,3]).all())

        del self.d3tag[self.ents]
        self.assertRaises(iBase.ITAPSError, lambda: self.d3tag[self.ents])

    def testArrEHArrData(self):
        data = numpy.tile(self.ents, (3, 1))
        self.e3tag[self.ents] = data

        self.assert_((self.e3tag[self.ents] == data).all())
        self.assert_((self.e3tag[self.ents[0]] == self.ents).all())

        del self.e3tag[self.ents]
        self.assertRaises(iBase.ITAPSError, lambda: self.e3tag[self.ents])

    def testArrRawArrData(self):
        self.b3tag[self.ents] = [[1,2,3]]*3

        self.assert_((self.b3tag[self.ents] == [[1,2,3]]*3).all())
        self.assert_((self.b3tag[self.ents[0]] == [1,2,3]).all())

        del self.b3tag[self.ents]
        self.assertRaises(iBase.ITAPSError, lambda: self.b3tag[self.ents])


    def testSetIntData(self):
        self.itag[self.set] = 42
        self.assertEqual(self.itag[self.set], 42)

        del self.itag[self.set]
        self.assertRaises(iBase.ITAPSError, lambda: self.itag[self.set])

    def testSetDblData(self):
        self.dtag[self.set] = 42
        self.assertEqual(self.dtag[self.set], 42)

        del self.dtag[self.set]
        self.assertRaises(iBase.ITAPSError, lambda: self.dtag[self.set])
        
    def testSetEHData(self):
        self.etag[self.set] = self.ent
        self.assertEqual(self.etag[self.set], self.ent)

        del self.etag[self.set]
        self.assertRaises(iBase.ITAPSError, lambda: self.etag[self.set])

    def testSetRawData(self):
        self.btag[self.set] = 42
        self.assertEqual(self.btag[self.set], 42)

        del self.btag[self.set]
        self.assertRaises(iBase.ITAPSError, lambda: self.btag[self.set])


    def testSetIntArrData(self):
        self.i3tag[self.set] = [42]*3
        self.assert_((self.i3tag[self.set] == [42]*3).all())

        del self.i3tag[self.set]
        self.assertRaises(iBase.ITAPSError, lambda: self.i3tag[self.set])

    def testSetDblArrData(self):
        self.d3tag[self.set] = [42]*3
        self.assert_((self.d3tag[self.set] == [42]*3).all())

        del self.d3tag[self.set]
        self.assertRaises(iBase.ITAPSError, lambda: self.d3tag[self.set])
        
    def testSetEHArrData(self):
        self.e3tag[self.set] = self.ents
        self.assert_((self.e3tag[self.set] == self.ents).all())

        del self.e3tag[self.set]
        self.assertRaises(iBase.ITAPSError, lambda: self.e3tag[self.set])

    def testSetRawArrData(self):
        self.b3tag[self.set] = [42]*3
        self.assert_((self.b3tag[self.set] == [42]*3).all())

        del self.b3tag[self.set]
        self.assertRaises(iBase.ITAPSError, lambda: self.b3tag[self.set])


    def testGetAll(self):
        self.itag[self.ent] = 42
        self.dtag[self.ent] = 42

        tags = self.geom.getAllTags(self.ent)
        self.assert_(self.itag in tags)
        self.assert_(self.dtag in tags)

    def testSetGetAll(self):
        self.itag[self.set] = 42
        self.dtag[self.set] = 42

        tags = self.geom.getAllTags(self.set)
        self.assert_(self.itag in tags)
        self.assert_(self.dtag in tags)


if __name__ == '__main__':
    unittest.main()
