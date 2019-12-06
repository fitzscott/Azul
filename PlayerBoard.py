import FinalBoardComponent as fbc
import PrepBoardComponent as pbc
import Penalty as p

class PlayerBoard():
    """
    PlayerBoard contains the board components that make up the player's
    game area.
    """

    def __init__(self, num = 0):
        self._playernum = num
        self._finalboard = fbc.FinalBoardComponent()
        self._penalty = p.Penalty()
        self._prepboard = pbc.PrepBoardComponent(self._finalboard, self._penalty)
        self._score = 0
        self._firstplayer = False
        self._projfinalboard = fbc.FinalBoardComponent()

    @property
    def finalboard(self):
        return (self._finalboard)

    @property
    def prepboard(self):
        return (self._prepboard)

    @property
    def penalty(self):
        return (self._penalty)

    @property
    def score(self):
        return (self._score)

    @property
    def firstplayer(self):
        return (self._firstplayer)

    @firstplayer.setter
    def firstplayer(self, val):
        self._firstplayer = val

    @property
    def projfinalboard(self):
        return(self._projfinalboard)

    def __str__(self):
        retstr = ""
        fbspl = str(self.finalboard).split("\n")
        pbspl = str(self.prepboard).split("\n")
        for idx in range(len(pbspl)):
            retstr += pbspl[idx] + "\t" + fbspl[idx] + "\n"
        retstr += 6 * " " + str(self.penalty)
        return(retstr)

    def playtiles(self, rownum, tiles):
        """
        playtiles - game will pass the player board a set of tiles to be played
        in a particular row.  Check whether it's possible & send to penalty
        otherwise.
        :param rownum: Row on the prep board
        :param tiles: Set of (guaranteed to be same color) tiles
        :return:
        """
        for tile in tiles:
            if tile == "1":
                self._penalty.addtile(tile)
                self._firstplayer = True
            elif not self._prepboard.canplace(rownum, tile):
                self._penalty.addtile(tile)
            else:
                self._prepboard.place(rownum, tile)
                # Update the projected final board immediately if full
                if self._prepboard.rowfull(rownum):
                    # print("adding tile " + tile + " to projected board row " \
                    #       + str(rownum))
                    self._projfinalboard.place(rownum, tile)

    def movescore(self, box):
        for idx in range(len(self._prepboard.rows)):
            self._score += self._prepboard.score(idx, box)
        self._score += self.penalty.score(box)
        if self._score < 0:
            self._score = 0

    def finalscore(self):
        # print("running PB final score, before = " + str(self._score))
        self._score += self.finalboard.finalscore()
        # print("running PB final score, after = " + str(self._score))

if __name__ == "__main__":
    pb = PlayerBoard()
    print(pb)

    import Pad as pd
    import CentralArea as ca

    pad = pd.Pad()
    pad.load(['R', 'Y', 'K', 'R'])
    ca1 = ca.CentralArea()
    seltiles = pad.takecolor('R', ca1)
    pb.playtiles(1, seltiles)
    print(pb)
    print("central area: " + str(ca1))
    pb.playtiles(2, seltiles)
    print(pb)
    pb.playtiles(0, seltiles)
    print(pb)

    import TileArea as ta
    box = ta.TileArea()
    pb.movescore(box)
    print(pb)
    print("score is " + str(pb.score))

    pad.load(['K', 'B', 'B', 'K'])
    seltiles = pad.takecolor('K', ca1)
    pb.playtiles(0, seltiles)
    pb.movescore(box)
    print(pb)
    print("score is " + str(pb.score))
