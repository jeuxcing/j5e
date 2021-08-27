from enum import Enum

NB_LEDS_SEGMENT = 24 
NB_LEDS_RING = 12
SIZE = 3 #3x3 prototype
NB_SEGMENTS=SIZE - 1

class Segment():

    def __init__(self, size=NB_LEDS_SEGMENT):
        """
        size : taille du bandeau
        """
        self.leds = [(0,0,0) for _ in range(size)]
        #valeurs dans [0,255]
        
    def set_color(self, pos, rgb):
        self.leds[pos]=rgb
    
    def get_color(self, pos):
        return self.leds[pos]

    def get_all_colors(self, pos):
        return self.leds
    
    def set_color_all(self, rgb):
        self.leds=[ rgb for _ in range(len(self.leds))]

    def set_all_colors(self, rgb_colors):
        self.leds=rgb_colors
    
    
class Ring():
#peut être que ça serait bien que ça hérite de Segment dis donc
    def __init__(self, size=NB_LEDS_RING):
        """
        size : taille de l'anneau
        """
        self.leds = [[0]*3 for _ in range(size)] 
        #valeurs dans [0,255]

    def set_color(self, pos, rgb):
        self.leds[pos]=rgb
    
    def get_color(self, pos):
        return self.leds[pos]

    def get_all_colors(self, pos):
        return self.leds
    
    def set_color_all(self, rgb):
        self.leds=[ rgb for _ in range(len(self.leds))]

    def set_all_colors(self, rgb_colors):
        self.leds=rgb_colors

class GridDims(Enum):
    ROW=0, COL=1, RING=2        
        
class Grid():
    def __init__(self, size):
        """
        size : taille de la grille
        """
        self.rows = [ [Segment() for _ in range(NB_SEGMENTS)] for _ in range(size)]
        self.cols = [ [Segment() for _ in range(NB_SEGMENTS)]  for _ in range(size)]
        self.rings = [ [Ring() for _ in range(SIZE) ] for _ in range(SIZE) ]

    def set_color(self, axis, posx, posy, pos_seg, rgb):
        #/!\ Achtung ! POSX POY NOT TESTED
        if axis == GridDims.ROW:
            self.rows[posx][posy].set_color(pos_seg, rgb)
        elif axis == GridDims.COL:
            self.cols[posx][posy].set_color(pos_seg, rgb)            
        else:
            self.rings[posx][posy].set_color(pos_seg, rgb)            
    
    def get_color(self, axis, posx, posy, pos_seg):
        #/!\ Achtung ! POSX POY NOT TESTED
        if axis == GridDims.ROW:
            return self.rows[posx][posy].get_color(pos_seg)
        elif axis == GridDims.COL:
            return self.cols[posx][posy].get_color(pos_seg)
        else:
            return self.rings[posx][posy].get_color(pos_seg)


