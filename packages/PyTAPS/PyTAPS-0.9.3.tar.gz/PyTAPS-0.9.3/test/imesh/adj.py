from itaps import iBase, iMesh
import unittest

topo = iMesh.Topology # shorthand

class TestAdj(unittest.TestCase):
    def setUp(self):
        self.mesh = iMesh.Mesh()
        self.verts = [[0,0,0], [0,0,1], [0,1,0], [0,1,1]]
        self.ents = self.mesh.createVtx(self.verts)

        self.lines = [ 
            self.mesh.createEnt(topo.line_segment, self.ents[0:2] )[0],
            self.mesh.createEnt(topo.line_segment, self.ents[1:3] )[0],
            self.mesh.createEnt(topo.line_segment, self.ents[2:4] )[0],
            self.mesh.createEnt(topo.line_segment, self.ents[::-3])[0] ]

    def testSquare(self):
        quad = self.mesh.createEnt(topo.quadrilateral, self.lines)[0]

        self.assertEqual(self.mesh.getNumOfType(iBase.Type.vertex),  4)
        self.assertEqual(self.mesh.getNumOfType(iBase.Type.edge),    4)
        self.assertEqual(self.mesh.getNumOfType(iBase.Type.face),    1)

        self.assertEqual(self.mesh.getNumOfTopo(topo.point),         4)
        self.assertEqual(self.mesh.getNumOfTopo(topo.line_segment),  4)
        self.assertEqual(self.mesh.getNumOfTopo(topo.quadrilateral), 1)

        self.mesh.deleteEnt(quad)
        self.assertEqual(self.mesh.getNumOfType(iBase.Type.face),    0)
        self.assertEqual(self.mesh.getNumOfTopo(topo.quadrilateral), 0)

        self.mesh.deleteEnt(self.lines)
        self.assertEqual(self.mesh.getNumOfType(iBase.Type.edge),    0)
        self.assertEqual(self.mesh.getNumOfTopo(topo.line_segment),  0)

        self.mesh.deleteEnt(self.ents)
        self.assertEqual(self.mesh.getNumOfType(iBase.Type.vertex),  0)
        self.assertEqual(self.mesh.getNumOfTopo(topo.point),         0)

    def testAdj(self):
        adj = self.mesh.getEntAdj(self.ents[1], iBase.Type.all)
        self.assert_((adj == self.lines[0:2]).all())

        adj = self.mesh.getEntAdj(self.ents, iBase.Type.all)

        for i in range( len(adj) ):
            self.assertEqual(adj.length(i), 2)

        self.assert_((adj[0] == self.lines[::3]).all())
        self.assert_((adj[1] == self.lines[0:2]).all())
        self.assert_((adj[2] == self.lines[1:3]).all())
        self.assert_((adj[3] == self.lines[2:4]).all())

        self.assertEqual(adj[0,0], self.lines[0])
        self.assertEqual(adj[2,1], self.lines[2])

        self.assertRaises(IndexError, adj.__getitem__, (0,2))

    def test2ndAdj(self):
        quad = self.mesh.createEnt(topo.quadrilateral, self.lines)[0]

        adj = self.mesh.getEnt2ndAdj(self.ents[1], iBase.Type.edge,
                                     iBase.Type.vertex)
        self.assert_((adj == self.ents[0:3:2]).all())

        adj = self.mesh.getEnt2ndAdj(self.ents, iBase.Type.edge,
                                     iBase.Type.vertex)

        for i in range( len(adj) ):
            self.assertEqual(adj.length(i), 2)

        self.assert_((adj[0] == self.ents[1::2]).all())
        self.assert_((adj[1] == self.ents[0::2]).all())
        self.assert_((adj[2] == self.ents[1::2]).all())
        self.assert_((adj[3] == self.ents[0::2]).all())

        self.assertEqual(adj[0,0], self.ents[1])
        self.assertEqual(adj[2,1], self.ents[3])

        self.assertRaises(IndexError, adj.__getitem__, (0,2))

    def testAdjIndices(self):
        set = self.mesh.createEntSet(True)
        set.add(self.ents)
        ents, adj = set.getAdjEntIndices(iBase.Type.all, topo.all,
                                         iBase.Type.all)

        self.assert_((ents == self.ents).all())
        self.assert_((adj.data == self.lines).all())

        self.assert_( (adj.indices[0] == [0,3]).all() )
        self.assert_( (adj.indices[1] == [0,1]).all() )
        self.assert_( (adj.indices[2] == [1,2]).all() )
        self.assert_( (adj.indices[3] == [2,3]).all() )

if __name__ == '__main__':
    unittest.main()

