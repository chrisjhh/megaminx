"""Class representing a face of the dodecahedron"""

import re

class Face:
    
    def __init__(self,char):
        self.colour = char
        self.facets = []
        self.connected_faces = []
        for i in range(10):
            self.facets.append(char)
        for i in range(5):
            self.connected_faces.append(None)

    def __str__(self):
        val = ''.join(self.facets)
        # Use shorthand if all facets are the same
        if re.match(r'(.)\1{9}',val):
            val = '[' + val[0] + ']'
        return val

    def __repr__(self):
        return self.__str__()

    def connect(self,face,edge):
        self.connected_faces[edge] = face

    def rotate_clockwise(self):
        # Get the last two elements and put them at the start
        end = self.facets[-2:]
        self.facets[-2:] = []
        self.facets[0:0] = end
        # Rotate the edges of the connected faces too
        if all(self.connected_faces):
            before = self.connected_edge_facets(4)
            for i in range(5):
                safe = self.connected_edge_facets(i)
                self.set_connected_edge_facets(i,before)
                before = safe

    def rotate_anticlockwise(self):
        # Get the first two elements and put them at the end
        start = self.facets[:2]
        self.facets[:2] = []
        self.facets.extend(start)
        # Rotate the edges of the connected faces too
        if all(self.connected_faces):
            after = self.connected_edge_facets(0)
            for i in range(5):
                safe = self.connected_edge_facets(4-i)
                self.set_connected_edge_facets(4-i,after)
                after = safe

    def edge_facets(self,edge):
        start = edge * 2
        facets = self.facets[start:start+3]
        if edge == 4:
            facets.append(self.facets[0])
        return facets

    def set_edge_facets(self,edge,facets):
        start = edge * 2
        if edge < 4:
            self.facets[start:start+3] = facets
        if edge == 4:
            self.facets[start:start+2] = facets[0:2]
            self.facets[0] = facets[2]


    def connected_edge_facets(self,edge):
        connected_face = self.connected_faces[edge]
        if not connected_face:
            return None
        for i in range(5):
            if connected_face.connected_faces[i] == self:
                return connected_face.edge_facets(i)
        return None

    def set_connected_edge_facets(self,edge,facets):
        connected_face = self.connected_faces[edge]
        if not connected_face:
            raise Exception('No connected face')
        for i in range(5):
            if connected_face.connected_faces[i] == self:
                connected_face.set_edge_facets(i,facets)
                return
        raise Exception('Cannot find common edge')

    def connecting_edge(self,col):
        for i in range(5):
            if self.connected_faces[i].colour == col:
                return i
        return -1

    def opposite_face(self):
        connected_face = self.connected_faces[0]
        if not connected_face:
            raise Exception('No connected face')
        connected_edge = -1
        for i in range(5):
            if connected_face.connected_faces[i] == self:
                connected_edge = i
                break
        if connected_edge == -1:
            raise Exception('No connected edge')
        x = connected_edge + 2
        if x > 4:
            x -= 5
        underside_face = connected_face.connected_faces[x]
        if not underside_face:
            raise Exception('No underside face')
        underside_edge = -1
        for i in range(5):
            if underside_face.connected_faces[i] == connected_face:
                underside_edge = i
                break
        if underside_edge == -1:
            raise Exception('No underside edge')
        y = underside_edge + 3
        if y > 4:
            y -= 5
        opposite_face = underside_face.connected_faces[y]
        return opposite_face


    def parse(self,string):
        if re.match(r'\[.\]',string):
            for i in range(10):
                self.facets[i] = string[1]
        else:
            for i in range(10):
                self.facets[i] = string[i]

    

if __name__ == "__main__":
    f = Face('x')
    print(f)
    f.facets[1] = 'W'
    f.facets[9] = 'e'
    print(f)
    f.rotate_clockwise()
    print(f)
    f.rotate_anticlockwise()
    f.rotate_anticlockwise()
    print(f)
    f.rotate_clockwise()
    print(f)
    for i in range(5):
        print(f.edge_facets(i))
    f.set_edge_facets(0,['a','b','c'])
    print(f)
    f.set_edge_facets(1,['d','e','f'])
    print(f)
    f.set_edge_facets(2,['g','h','i'])
    print(f)
    f.set_edge_facets(3,['j','k','l'])
    print(f)
    f.set_edge_facets(4,['m','n','o'])
    print(f)

    f1 = Face('r')
    f1.connect(f,0)
    f.connect(f1,0)

    f2 = Face('y')
    f2.connect(f,1)
    f.connect(f2,1)

    f3 = Face('g')
    f3.connect(f,2)
    f.connect(f3,2)

    f4 = Face('b')
    f4.connect(f,3)
    f.connect(f4,3)

    f5 = Face('p')
    f5.connect(f,4)
    f.connect(f5,4)

    print(f1,f2,f3,f4,f5)
    f.rotate_clockwise()
    print(f1,f2,f3,f4,f5)
    f.rotate_anticlockwise()
    print(f1,f2,f3,f4,f5)
    f.rotate_anticlockwise()
    print(f1,f2,f3,f4,f5)
    f.rotate_clockwise()
    print(f1,f2,f3,f4,f5)

    f.parse('[V]')
    print(f)
    f.parse('abcdefghij')
    print(f)
