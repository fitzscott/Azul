import TileArea as ta
import random

class Bag(ta.TileArea):
    """
    Bag that holds tiles and fills Pads.  If the bag runs out, refill it from
    the box (another tile area).
    >>> import TileArea as ta
    >>> import Pad as p
    >>> pad = p.Pad()
    >>> bag = Bag()
    >>> box = ta.TileArea()
    >>> bag.addtile('Y')
    >>> bag.addtile('Y')
    >>> box.addtile('Y')    # only 3 total
    >>> boolval = bag.loadpad(pad, box)
    >>> boolval
    False
    >>> print("pad now has " + str(pad.tiles))
    pad now has ['Y', 'Y', 'Y']
    """

    def __init__(self):
        super().__init__()

    def loadpad(self, pad, box, count=4):
        """
        loadpad - pull tiles from the bag at random, sending them to the pad.
        If the bag is empty, request a refill from the box.  If it's still
        empty, the pad has to go without.
        :param pad: Where the drawn tiles go
        :param bag: Holds the refill tiles for the bag
        :param count: How many tiles to draw.
        :return: Boolean - whether full set was returned to the pad
        """
        for tc in range(count):
            if len(self.tiles) == 0:    # need a reload
                for tile in box.tiles:
                    self.addtile(tile)
                    box.tiles.remove(tile)
            if len(self.tiles) == 0:    # still empty
                return(False)
            tile = self.tiles[random.randint(0, len(self.tiles)-1)]
            pad.addtile(tile)
            self.tiles.remove(tile)
        return(True)

if __name__ == "__main__":
    import TileArea as ta
    import Pad as p
    pad = p.Pad()
    bag = Bag()
    box = ta.TileArea()
    for i in range(2):
        for color in "YKBRW":
            bag.addtile(color)
            box.addtile(color)
    bag.loadpad(pad, box)
    print("pad now has " + str(pad.tiles))

    import doctest
    doctest.testmod()
