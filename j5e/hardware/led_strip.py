from enum import Enum



class Strip:
    def __init__(self, size):
        self.leds = [(0, 0, 0) for _ in range(size)]
        # valeurs dans [0,255]

    def set_color(self, pos, rgb):
        self.leds[pos] = rgb

    def get_color(self, pos):
        return self.leds[pos]

    def get_all_colors(self, pos):
        return self.leds

    def set_color_all(self, rgb):
        self.leds = [rgb for _ in range(len(self.leds))]

    def set_all_colors(self, rgb_colors):
        self.leds = rgb_colors


class Segment(Strip):
    NB_LEDS = 24

    def __init__(self, size=0):
        """
        size : taille du bandeau
        """
        super(Segment, self).__init__(size if size != 0 else Segment.NB_LEDS)


class Ring(Strip):
    NB_LEDS = 12

    def __init__(self, size=0):
        """
        size : taille de l'anneau
        """
        super(Ring, self).__init__(size if size != 0 else Ring.NB_LEDS)


class GridDims(Enum):
    ROW = 0
    COL = 1
    RING = 2


class Grid:
    SIZE = 5
    # NB_SEGMENTS = Grid.SIZE - 1

    def __init__(self, network, size=0):
        """
        size : taille de la grille
        """
        if size == 0:
            size = Grid.SIZE
        nb_segments = size - 1

        self.rows = [
            [Segment() for _ in range(nb_segments)] for _ in range(size)
        ]
        self.cols = [
            [Segment() for _ in range(nb_segments)] for _ in range(size)
        ]
        self.rings = [[Ring() for _ in range(size)] for _ in range(size)]
        self.network = network

    def set_color(self, axis, posx, posy, pos_seg, rgb):
        # /!\ Achtung ! POSX POY NOT TESTED
        if axis == GridDims.ROW:
            self.rows[posx][posy].set_color(pos_seg, rgb)
        elif axis == GridDims.COL:
            self.cols[posx][posy].set_color(pos_seg, rgb)
        else:
            self.rings[posx][posy].set_color(pos_seg, rgb)

    def get_color(self, axis, posx, posy, pos_seg):
        # /!\ Achtung ! POSX POY NOT TESTED
        if axis == GridDims.ROW:
            return self.rows[posx][posy].get_color(pos_seg)
        elif axis == GridDims.COL:
            return self.cols[posx][posy].get_color(pos_seg)
        else:
            return self.rings[posx][posy].get_color(pos_seg)

    