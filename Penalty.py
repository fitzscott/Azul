import TileArea as ta

class Penalty(ta.TileArea):
    """
    Penalty - an area where tiles that were received by a player but not played
    go to sit until they are scored (negatively).
    >>> p = Penalty()
    >>> p.addtile('R')
    >>> p.addtile('1')
    >>> p.addtile('R')
    >>> box1 = ta.TileArea()
    >>> print(str(p.score(box1)))
    -4
    >>> p.clear()
    >>> p.addtile('1')
    >>> print(str(p.score(box1)))
    -1
    >>> p.clear()
    >>> print(str(p.score(box1)))
    0
    """

    penalties = [1, 1, 2, 2, 2, 3, 3]  # uniform across instances

    def __init__(self):
        super().__init__()
        # self._firstplayer = False

    def addtile(self, tile):
        if tile == '1' and '1' in self.tiles:
            print("Received a 2nd 1st player tile?")
        else:
            super().addtile(tile)

    # This was replaced with a flag at the PlayerBoard level.
    # @property
    # def firstplayer(self):
    #     for tile in self.tiles:
    #         if tile == '1':
    #             self._firstplayer = True
    #             break
    #     return (self._firstplayer)

    def score(self, box):
        sc = 0
        for tilenum in range(len(self.tiles)):
            if tilenum >= len(Penalty.penalties):  # too many tiles in penalty
                break
            sc += Penalty.penalties[tilenum]
            if self.tiles[tilenum] != '1':
                box.addtile(self.tiles[tilenum])
        self.clear()
        return (sc * -1)

    def clear(self):
        super().clear()
        self._firstplayer = False

    def __str__(self):
        penlen = len(self.tiles)
        retstr = ""
        for idx in range(max(penlen, len(Penalty.penalties))):
            if idx < penlen:
                retstr += self.tiles[idx]
            else:
                retstr += "-"
        return (retstr)

if __name__ == "__main__":
    import doctest

    doctest.testmod()
