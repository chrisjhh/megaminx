"""Class representing the megaminx"""

from .face import Face 
from .transform import Transform

solved = '[w][r][G][p][Y][B][x][y][k][g][o][b]'

class Megaminx:

    def __init__(self):
        # Construct the faces and add them
        self.faces = {}
        self.colours = ('w','r','G','p','Y','B','x','y','k','g','o','b')
        for char in self.colours:
            face = Face(char)
            self.faces[char] = face
        # Connect them up
        connections = {
            'w' : ('r','G','p','Y','B'),
            'r' : ('G','w','B','k','y'),
            'G' : ('w','r','y','b','p'),
            'p' : ('b','o','Y','w','G'),
            'Y' : ('g','B','w','p','o'),
            'B' : ('Y','g','k','r','w'),
            'x' : ('y','k','g','o','b'),
            'y' : ('k','x','b','G','r'),
            'k' : ('x','y','r','B','g'),
            'g' : ('B','Y','o','x','k'),
            'o' : ('p','b','x','g','Y'),
            'b' : ('o','p','G','y','x')
        }
        for key in connections.keys():
            edge = 0
            for char in connections[key]:
                self.faces[key].connect(self.faces[char],edge)
                edge += 1

    def get_rotation_transforms(self,face):
        oface = self.faces[face].opposite_face().colour
        topfaces = [f.colour for f in self.faces[face].connected_faces]
        bottomfaces = [f.colour for f in self.faces[oface].connected_faces]
        bottomfaces.reverse()
        xforms = []
        for d in range(1,5):
            xform = {}
            xform['top'] = face
            xform['bot'] = oface
            xform['rot'] = d
            xform[face]= face
            xform[oface] = oface
            for i in range(5):
                j = i + d
                if j >= 5:
                    j -= 5
                xform[topfaces[i]] = topfaces[j]
                xform[bottomfaces[i]] = bottomfaces[j]
            xforms.append(Transform(xform))
        return xforms

    def get_colour_transforms(self):
        # Each colour face could be replaced with any other colour as long
        # as the topological arangement of colours stays the same
        top = self.colours[0]
        bot = self.faces[top].opposite_face().colour
        topfaces = [f.colour for f in self.faces[top].connected_faces]
        botfaces = [f.colour for f in self.faces[bot].connected_faces]
        xforms = []
        for c in self.colours[1:]:
            new_top = c
            new_bot = self.faces[new_top].opposite_face().colour
            new_topfaces = [f.colour for f in self.faces[new_top].connected_faces]
            new_botfaces = [f.colour for f in self.faces[new_bot].connected_faces]
            xform = {}
            xform[top] = new_top
            xform[bot] = new_bot
            for i in range(5):
                xform[topfaces[i]] = new_topfaces[i]
                xform[botfaces[i]] = new_botfaces[i]
            xforms.append(Transform(xform))
        return xforms

    def get_transforms(self):
        if not hasattr(self,'_transforms'):
            top = self.colours[0]
            xforms = self.get_rotation_transforms(top)
            for i in [f.colour for f in self.faces[top].connected_faces]:
                xforms.extend(self.get_rotation_transforms(i))
            self._transforms = xforms
        return self._transforms

    def transformed_state(self,t):
        store = {}
        for col in self.colours:
            store[t[col]] = t.transform(str(self.faces[col]))

        if 'rot' in t:
            # Rotate the top and bottom faces
            top = store[t['top']]
            bot = store[t['bot']]
            tface = Face(t['top'])
            bface = Face(t['bot'])
            tface.parse(top)
            bface.parse(bot)
            #print('%s>%d' % (t['top'],t['rot']))
            for i in range(t['rot']):
                tface.rotate_clockwise()
                bface.rotate_anticlockwise()
            store[t['top']] = str(tface)
            store[t['bot']] = str(bface)

            # Other faces may need rotating too
            for apex in (t['top'],t['bot']):
                joins = [x.colour for x in self.faces[apex].connected_faces]
                for f in joins:
                    before = self.faces[f].connecting_edge(apex)
                    after = self.faces[t[f]].connecting_edge(apex)
                    diff = after - before
                    if diff < 0:
                        diff += 5
                    if diff != 0:
                        face = Face(f)
                        face.parse(store[t[f]])
                        for i in range(diff):
                            face.rotate_clockwise()
                        store[t[f]] = str(face)

        return ''.join([store[i] for i in self.colours])

    def apply(self,solution):
        steps = solution.strip().split(' ')
        for step in steps:
            col = step[0]
            act = step[1]
            face = self.faces[col]
            if act == '>':
                face.rotate_clockwise()
            elif act == '<':
                face.rotate_anticlockwise()

    def unapply(self,solution):
        steps = solution.strip().split(' ')
        steps.reverse()
        for step in steps:
            col = step[0]
            act = step[1]
            face = self.faces[col]
            if act == '<':
                face.rotate_clockwise()
            elif act == '>':
                face.rotate_anticlockwise()


    def __str__(self):
        val = ''
        for col in self.colours:
            val += str(self.faces[col])
        return val

    def parse(self,string):
        offset = 0
        for col in self.colours:
            if string[offset] == '[':
                self.faces[col].parse(string[offset:offset+3])
                offset += 3
            else:
                self.faces[col].parse(string[offset:offset+10])
                offset += 10

if __name__ == "__main__":
    m = Megaminx()
    m.faces['w'].facets[6] = 'Y'
    m.faces['p'].facets[0] = 'w'
    m.faces['Y'].facets[2] = 'p'
    print(m)
    m.faces['Y'].rotate_anticlockwise()
    print(m)    
    val = 'rwwwwwwwGrGGkkkrrrrrpppGGGGGGGYYYpppppppwBBYYYYYwwBBrrrBBBBB[x][y]kkkkkkgggkggggYYBggg[o][b]'
    m.parse(val)
    print(m)
    print(str(m) == val)
    m.faces['B'].rotate_anticlockwise()
    m.faces['w'].rotate_clockwise()
    print(m)
    print(str(m) == solved)

        