# File: mini_geometry.py
# Author: T.J. Jankun-Kelly <tjk@cse.msstate.edu>
"""Geometry for the Mini Cooper model.

The Cooper model is formed of various groups. Each group has a name (the
"part") that determines which part it belongs to. For example, the "Roof" part
possesses geometry that belongs to the roof of the car. To get the
starting and ending indices of the faces belonging to the part, use the group
function; this can be used to render only that face:
    mini = MiniGeometry()
    <load vertex buffer and index buffer from mini.vertexdata & mini.indices>
    for part in mini.parts:   
        start, end = mini.group(part)
        offset = sizeof(GLushort) * mini.indicesPerFace * start
        count = mini.indicesPerFace * (end - start)
        glDrawElements(GL_TRIANGLES, count, GL_UNSIGNED_SHORT, offset)
        
"""
from __future__ import division

import array
import collections

class MiniGeometry(object):
    """A class that loads and stores the Mini geometry.
    """

    def __init__(self, adjacency = False):
        # Read in geometry
        # Format:
        #   numVertices
        #   vx vy vz nx ny nz tu tv
        #   ...
        #   numFaces
        #   vertexIndex0 vertexIndex1 ... vertexIndexN (3 or 6 if adjacency)
        #   ...
        #   numGroups
        #   faceStart faceEnd name
        filename = "mini_geometry.txt" if not adjacency \
                                       else "mini_geometry_adjacency.txt"
        with open(filename, 'r') as geom:
            # Store the vertex + attribute data in one array. Easier for
            # copying to the GPU later
            self._numVertices = int(geom.readline())
            self._data = array.array('f', [0.0]*(8*self._numVertices))
            for i in range(self._numVertices):
                line = geom.readline()
                self._data[8*i:8*(i+1)] = array.array('f', [float(x) for x in
                                                            line.split()])
                    
            # Store the face indices in one array of unsigned shorts for easier
            # copying to the GPU later
            self._numFaces = int(geom.readline())
            self._idxCount = 3 if not adjacency else 6
            self._indices = array.array('H', 
                                        [0]*(self._idxCount*self._numFaces))
            for i in range(self._numFaces):
                line = geom.readline()
                self._indices[self._idxCount*i:self._idxCount*(i+1)] = \
                              array.array('H', [int(x) for x in line.split()])
                if i + 1 == self._numFaces:
                    break
            
            # Store groups (and names) in and ordered dictionary
            self._groups = collections.OrderedDict()
            geom.readline() # Ignore the count
            for line in geom:
                start, end = (int(x) for x in line.split()[:2])
                name = " ".join(line.split()[2:])
                self._groups[name] = start, end
    @property
    def numVertices(self):
        """The number of vertices in the geometry.
        """
        return self._numVertices
        
    @property
    def vertexdata(self):
        """Return all the vertices and their attributes in the model.
        
        This is a flat array of floats where the vertices and their attributes
        take up every eight entries: The first three are the vertex position,
        the next three the normal, and the last two the texcoords.
        """
        return array.array('f', self._data)
    
    def vertex(self, index):
        """Return a specific vertex in the model.
        """
        return self._data[8*index:8*index+3]

    def normal(self, index):
        """Return a specific normal in the model.
        """
        return self._data[8*index+3:8*index+6]
    
    def texcoord(self, index):
        """Return a specific normal in the model.
        """
        return self._data[8*index+6:8*index+8]
    
    @property
    def storesAdjacency(self):
        """Determines if adjacency information is stored or not.
        """
        return self._idxCount == 6
        
    @property
    def indicesPerFace(self):
        """Returns the number of indices per face. Usually 3 unless adjacency
        infomation is stored.
        """
        return self._idxCount

    @property
    def numFaces(self):
        """The number of faces in the geometry.
        """
        return self._numFaces
    
    @property   
    def indices(self):
        """Return all the faces in the model.
        
        The indices are either 3 per face (for non-adjacency geometry) or 6 per 
        face. See MiniGeometry.storesAdjacency
        """
        return array.array('H', self._indices)
    
    def face(self, index):
        """Return a specific face in the model.
        """
        return self._indices[self._idxCount*index:self._idxCount*(index+1)]
    
    @property
    def groups(self):
        """Return the dictionary of names to group slices.
        """
        return collections.OrderedDict(self._groups)
        
    def group(self, part):
        """Return the beginning and ending offset of indices for a part.
        """
        return self._groups[part]

    @property
    def parts(self):
        """Return the names of all the parts in the geometry.
        """
        return self._groups.keys()

