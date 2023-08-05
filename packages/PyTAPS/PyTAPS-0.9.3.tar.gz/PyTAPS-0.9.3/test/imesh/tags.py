from itaps import iBase, iMesh
import unittest
from numpy import *

class TestTags(unittest.TestCase):
    def setUp(self):
        self.mesh = iMesh.Mesh()

        self.itag = self.mesh.createTag('int',    1, 'i')
        self.dtag = self.mesh.createTag('double', 1, 'd')
        self.etag = self.mesh.createTag('handle', 1, 'E')
        self.btag = self.mesh.createTag('bytes',  3, 'b')

        self.ents = self.mesh.createVtx([[1,2,3], [4,5,6], [7,8,9]])
        self.ent = self.ents[0]
        self.set = self.mesh.createEntSet(True)

    def testCreation(self):
        self.assertEqual(self.itag.instance, self.mesh)
        self.assertEqual(self.itag.name, 'int')
        self.assertEqual(self.itag.type, 'i')
        self.assertEqual(self.itag.sizeValues, 1)

        self.assertEqual(self.dtag.instance, self.mesh)
        self.assertEqual(self.dtag.name, 'double')
        self.assertEqual(self.dtag.type, 'd')
        self.assertEqual(self.dtag.sizeValues, 1)
        self.assertEqual(self.dtag.sizeBytes, 8)

        self.assertEqual(self.etag.instance, self.mesh)
        self.assertEqual(self.etag.name, 'handle')
        self.assertEqual(self.etag.type, 'E')
        self.assertEqual(self.etag.sizeValues, 1)

        self.assertEqual(self.btag.instance, self.mesh)
        self.assertEqual(self.btag.name, 'bytes')
        self.assertEqual(self.btag.type, 'b')
        self.assertEqual(self.btag.sizeValues, 3)
        self.assertEqual(self.btag.sizeBytes, 3)

    def testDestruction(self):
        self.mesh.destroyTag(self.itag, True)
        self.assertRaises(iBase.ITAPSError, self.mesh.getTagHandle, 'int')

    def testFind(self):
        t = self.mesh.getTagHandle('int')
        self.assertEqual(t.name, self.itag.name)

        self.assertRaises(iBase.ITAPSError, self.mesh.getTagHandle, 'potato')

    def testIntData(self):
        self.itag.setData(self.ent, 42)
        self.assertEqual(self.itag.getData(self.ent),      42)
        self.assertEqual(self.itag.getData(self.ent, 'i'), 42)

        self.itag.remove(self.ent)
        self.assertRaises(iBase.ITAPSError, self.itag.getData, self.ent)

    def testDblData(self):
        self.dtag.setData(self.ent, 42.0)
        self.assertEqual(self.dtag.getData(self.ent),      42)
        self.assertEqual(self.dtag.getData(self.ent, 'd'), 42)

        self.dtag.remove(self.ent)
        self.assertRaises(iBase.ITAPSError, self.dtag.getData, self.ent)

    def testEHData(self):
        self.etag.setData(self.ent, self.ent)
        self.assertEqual(self.etag.getData(self.ent),      self.ent)
        self.assertEqual(self.etag.getData(self.ent, 'E'), self.ent)

        self.etag.remove(self.ent)
        self.assertRaises(iBase.ITAPSError, self.etag.getData, self.ent)        

    def testRawData(self):
        data = array([1,2,3], int8)
        self.btag.setData(self.ent, data)
        self.assert_( (self.btag.getData(self.ent)      == data).all() )
        self.assert_( (self.btag.getData(self.ent, 'b') == data).all() )

        self.btag.remove(self.ent)
        self.assertRaises(iBase.ITAPSError, self.btag.getData, self.ent)

    def testGetAll(self):
        self.itag.setData(self.ent, 42)
        self.dtag.setData(self.ent, 42)

        tags = self.mesh.getAllTags(self.ent)
        self.assert_(self.itag in tags)
        self.assert_(self.dtag in tags)

    def testIntArrData(self):
        self.itag.setData(self.ents, 3*[42])

        self.assert_((self.itag.getData(self.ents)      == 3*[42]).all())
        self.assert_((self.itag.getData(self.ents, 'i') == 3*[42]).all())

        self.assertEqual(self.itag.getData(self.ents[0]),      42)
        self.assertEqual(self.itag.getData(self.ents[0], 'i'), 42)

        self.itag.remove(self.ents)
        self.assertRaises(iBase.ITAPSError, self.itag.getData, self.ents)

    def testDblArrData(self):
        self.dtag.setData(self.ents, 3*[42])

        self.assert_((self.dtag.getData(self.ents)      == 3*[42]).all())
        self.assert_((self.dtag.getData(self.ents, 'd') == 3*[42]).all())

        self.assertEqual(self.dtag.getData(self.ents[0]),      42)
        self.assertEqual(self.dtag.getData(self.ents[0], 'd'), 42)

        self.dtag.remove(self.ents)
        self.assertRaises(iBase.ITAPSError, self.dtag.getData, self.ents)

    def testEHArrData(self):
        self.etag.setData(self.ents, self.ents)

        self.assert_((self.etag.getData(self.ents)      == self.ents).all())
        self.assert_((self.etag.getData(self.ents, 'E') == self.ents).all())

        self.assertEqual(self.etag.getData(self.ents[0]),      self.ents[0])
        self.assertEqual(self.etag.getData(self.ents[0], 'E'), self.ents[0])

        self.etag.remove(self.ents)
        self.assertRaises(iBase.ITAPSError, self.etag.getData, self.ents)

    def testRawArrData(self):
        data = array(3*[1,2,3], int8)
        self.btag.setData(self.ents, data)

        self.assert_((self.btag.getData(self.ents)      == data).all())
        self.assert_((self.btag.getData(self.ents, 'b') == data).all())

        self.assert_((self.btag.getData(self.ents[0])      == data[0:3]).all())
        self.assert_((self.btag.getData(self.ents[0], 'b') == data[0:3]).all())

        self.btag.remove(self.ents)
        self.assertRaises(iBase.ITAPSError, self.btag.getData, self.ents)


    def testIntSetData(self):
        self.itag.setData(self.set, 42)
        self.assertEqual(self.itag.getData(self.set),      42)
        self.assertEqual(self.itag.getData(self.set, 'i'), 42)

        self.itag.remove(self.set)
        self.assertRaises(iBase.ITAPSError, self.itag.getData, self.set)

    def testDblSetData(self):
        self.dtag.setData(self.set, 42)
        self.assertEqual(self.dtag.getData(self.set),      42)
        self.assertEqual(self.dtag.getData(self.set, 'd'), 42)

        self.dtag.remove(self.set)
        self.assertRaises(iBase.ITAPSError, self.dtag.getData, self.set)
        
    def testEHSetData(self):
        self.etag.setData(self.set, self.ent)
        self.assertEqual(self.etag.getData(self.set),      self.ent)
        self.assertEqual(self.etag.getData(self.set, 'E'), self.ent)

        self.etag.remove(self.set)
        self.assertRaises(iBase.ITAPSError, self.etag.getData, self.set)

    def testRawSetData(self):
        data = array([1,2,3], int8)
        self.btag.setData(self.set, data)

        self.assert_((self.btag.getData(self.set)      == data).all())
        self.assert_((self.btag.getData(self.set, 'b') == data).all())

        self.btag.remove(self.set)
        self.assertRaises(iBase.ITAPSError, self.btag.getData, self.set)

    def testGetAllSet(self):
        self.itag.setData(self.set, 42)
        self.dtag.setData(self.set, 42)

        tags = self.mesh.getAllTags(self.set)
        self.assert_(self.itag in tags)
        self.assert_(self.dtag in tags)


if __name__ == '__main__':
    unittest.main()
