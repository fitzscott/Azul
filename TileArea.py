
class TileArea():
    """
    A TileArea is a collection of tiles in a specific spot in the game.
    >>> ta = TileArea()
    >>> ta.addtile('R')
    >>> ta.addtile('B')
    >>> ta.addtile('R')
    >>> ta.addtile('L')
    >>> print(ta.tiles)
    ['R', 'B', 'R', 'L']
    >>> r = ta.takecolor('R')
    >>> print(r)
    ['R', 'R']
    >>> print(ta.tiles)
    ['B', 'L']
    """

    def __init__(self):
        self._tiles = []

    @property
    def tiles(self):
        return (self._tiles)

    def addtile(self, tile):
        self._tiles.append(tile)

    def takecolor(self, color):
        retset = []
        stayset = []

        for tile in self.tiles:
            if tile == color:
                retset.append(tile)
            else:
                stayset.append(tile)
        self._tiles = stayset
        return (retset)

    def clear(self):
        self._tiles = []

    def __str__(self):
        return(str(self._tiles))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
