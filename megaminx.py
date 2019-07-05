"""Class representing the megaminx"""

from .face import Face 

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
            'r' : ('w','B','k','y','G'),
            'G' : ('w','r','y','b','p'),
            'p' : ('w','G','b','o','Y'),
            'Y' : ('w','p','o','g','B'),
            'B' : ('w','Y','g','k','r'),
            'x' : ('y','k','g','o','b'),
            'y' : ('x','b','G','r','k'),
            'k' : ('x','y','r','B','g'),
            'g' : ('x','k','B','Y','o'),
            'o' : ('x','g','Y','p','b'),
            'b' : ('x','o','p','G','y')
        }
        for key in connections.keys():
            edge = 0
            for char in connections[key]:
                self.faces[key].connect(self.faces[char],edge)
                edge += 1

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

        