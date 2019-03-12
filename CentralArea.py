import TileArea as ta

class CentralArea(ta.TileArea):
    """
    Central area - area in the middle of all the pads, where the unselected
    tiles go when a player selects a given color.  Also contains the 1st
    player tile, which goes to the first player to draw out of the middle.
    >>> ca = CentralArea()
    >>> for cnt in range(3):    # did not know about the ellipsis in doctests
    ...     ca.addtile('R')
    ...     ca.addtile('B')
    ...     ca.addtile('Y')
    >>> print(ca.tileplayer1)
    True
    >>> seltiles = ca.takecolor('Y')
    >>> print(seltiles)
    ['Y', 'Y', 'Y', '1']
    >>> print(ca.tileplayer1)
    False
    >>> seltiles = ca.takecolor('R')
    >>> print(seltiles)
    ['R', 'R', 'R']
    """

    def __init__(self):
        super().__init__()
        self._firstplayer = True

    @property
    def tileplayer1(self):
        return (self._firstplayer)

    def addtile(self, tile):
        if tile == '1':
            self._firstplayer = True
            if '1' in self.tiles:
                return ()
        super().addtile(tile)

    def takecolor(self, color):
        retlist = super().takecolor(color)
        if self._firstplayer:
            retlist.append('1')
            if '1' in self.tiles:
                self.tiles.remove('1')
            self._firstplayer = False
        return (retlist)

    def reset(self):
        self._firstplayer = True

    def __str__(self):
        retstr = ""
        idx = 0
        halfway = int(len(self.tiles) / 2) + 1
        self.tiles.sort()
        for tile in self.tiles:
            idx += 1
            if idx > halfway:
                retstr += "/"
                idx = 0
            retstr += tile
        return (retstr)

    def onlyplayer1(self):
        return (len(self.tiles) == 1 and self.tiles[0] == '1')

if __name__ == "__main__":
    import doctest

    doctest.testmod()
