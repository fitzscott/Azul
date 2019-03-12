import TileArea as ta

class Pad(ta.TileArea):
    """
    Pad - one of the (up to) 9 circular areas that hold tiles for players
    to choose from.  When a player chooses a color from a pad, the player
    receives a list of those color tiles, and the remaining tiles go to
    the central area, which is a TileArea.
    >>> p = Pad()
    >>> p.load("YBWY")
    >>> print(p.tiles)
    ['Y', 'B', 'W', 'Y']
    >>> cntrl = ta.TileArea()
    >>> taken = p.takecolor('Y', cntrl)
    >>> print("Player took " + str(taken))
    Player took ['Y', 'Y']
    >>> print("Central area now has " + str(cntrl.tiles))
    Central area now has ['B', 'W']
    >>> print("Pad now has (none) " + str(p.tiles))
    Pad now has (none) []
    """

    def __init__(self):
        super().__init__()

    def load(self, tiles):
        for tile in tiles:
            self.addtile(tile)

    def takecolor(self, color, center):
        """
        takecolor - do the same operation as the parent's takecolor,
        but pass the remainder on to the center.
        :param color: tile color to return to the player
        :param center: place remaining tiles go
        :return: list of colored tiles
        """
        selectedtiles = super().takecolor(color)
        for remtile in self.tiles:
            center.addtile(remtile)
        self.clear()
        return (selectedtiles)

    def __str__(self):
        retstr = ""
        for tile in self.tiles:
            retstr += tile
        return (retstr)

if __name__ == "__main__":
    import doctest

    doctest.testmod()
