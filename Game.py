import TileArea as ta
import Pad as pd
import Bag as bg
import CentralArea as ca
import PlayerBoard as pb

class Game():
    """

    """

    colors = "BYRKW"
    countpercolor = 20

    def __init__(self, numplayers=4):
        self._numplayers = numplayers
        self.reset()

    def reset(self):
        self._factorydisplays = []
        for cnt in range(2 * self._numplayers + 1):
            self._factorydisplays.append(pd.Pad())
        self._centralarea = ca.CentralArea()
        self._bag = bg.Bag()
        self._box = ta.TileArea()
        for _ in range(Game.countpercolor):
            for color in Game.colors:
                self._bag.addtile(color)
        self._playerboards = []
        for cnt in range(self._numplayers):
            self._playerboards.append(pb.PlayerBoard())

    def loadtiles(self):
        """
        loadtiles - grab tiles from the bag & put them on the displays
        If we end up with no tiles on display, we're stuck.
        :return: False if stuck game
        """
        tottiles = 0
        for disp in self._factorydisplays:
            self._bag.loadpad(disp, self._box)
            tottiles += len(disp.tiles)
        self._centralarea.addtile('1')
        return (tottiles > 0)

    def __str__(self):
        retstr = ""
        toprow = int(len(self._factorydisplays) / 3)
        for idx in range(toprow):
            retstr += 8 * " " + str(idx) + ":" + str(self._factorydisplays[idx])
        retstr += "\n"
        currcnt = toprow
        cent = str(self._centralarea).split("/")
        space = 30 + len(self._factorydisplays)
        idx = 0
        while currcnt < len(self._factorydisplays)-2:
            retstr += str(currcnt) + ":" + str(self._factorydisplays[currcnt])
            if len(cent) > idx:
                clen = len(cent[idx])
            else:
                clen = 0
            if clen > 0:
                spc = int((space - clen) / 2)
                retstr += spc * " " + cent[idx] + spc * " "
                idx += 1
            else:
                retstr += space * " "
            retstr += str(currcnt+1) + ":" + str(self._factorydisplays[currcnt+1])
            retstr += "\n"
            currcnt += 2
        while currcnt < len(self._factorydisplays):
            retstr += 10 * " " + str(currcnt) + ":" + str(self._factorydisplays[currcnt])
            currcnt += 1
        retstr += "\n\n"
        for pind in range(len(self._playerboards)):
            retstr += " " * 5 + "Player " + str(pind+1) + " " * 3
        retstr += "\n"
        pbstr = ["" for _ in range(7)]
        for plbd in self._playerboards:
            prn = str(plbd).split("\n")
            for idx in range(len(prn)):
                if idx < len(prn) - 1:
                    mult = 4
                else:
                    mult = 3
                pbstr[idx] += prn[idx] + mult * " "
        for linestr in pbstr:
            retstr += linestr + "\n"
        for plbd in self._playerboards:
            retstr += "score: " + str(plbd.score) + 9 * " "
        #print(str(pbstr))
        return(retstr)

    @property
    def centralarea(self):
        return(self._centralarea)

    @property
    def playerboard(self):
        return (self._playerboards)

    @property
    def display(self):
        return (self._factorydisplays)

    @property
    def box(self):
        return (self._box)

    @property
    def bag(self):
        return (self._bag)

    @property
    def numplayers(self):
        return (self._numplayers)

    def turnover(self):
        """
        turnover - when all the display areas and the central area are empty,
        the turn is over.
        :return: Boolean
        """
        for disp in self.display:
            if len(disp.tiles) > 0:
                return(False)
        return (len(self.centralarea.tiles) == 0 or \
                self.centralarea.onlyplayer1())

    def show(self):
        print(self)

    def options(self):
        """
        options - return a list of selections that can be made in the current
        game.
        :return: list of actions, including factory display or central area
        and the tiles available.  The format is display #, followed by a
        colon, followed by the list of tiles (usually 4 for normal displays,
        but different for the central area, and potentially different if
        tiles are running out).
        """
        opts = []
        facts = self._factorydisplays
        for dispidx in range(len(facts)):
            if len(facts[dispidx].tiles) > 0:
                tilestr = ""
                for tile in facts[dispidx].tiles:
                    tilestr += tile
                opts.append(str(dispidx+1) + ":" + tilestr)
        if len(self._centralarea.tiles) > 0 and \
                not self._centralarea.onlyplayer1():
            tilestr = ""
            for tile in self._centralarea.tiles:
                tilestr += tile
            opts.append("0:" + tilestr)
        return(opts)

    def chooseoption(self, opt, color):
        dispnum = int(opt[0])
        if dispnum == 0:
            tileset = self.centralarea.takecolor(color)
        else:
            tileset = self.display[dispnum-1].takecolor(color, self.centralarea)
        return(tileset)

    def winner(self):
        finalscores = [pb.score for pb in self.playerboard]
        topscore = -1
        for score in finalscores:
            topscore = max(topscore, score)
        wnrz = [plnum for plnum in range(len(self.playerboard))
                if self.playerboard[plnum].score == topscore]
        if len(wnrz) > 1:       # then check complete horizontal rows
            horiz = { wnr: self.playerboard[wnr].finalboard.counthorizrowcomplete()
                     for wnr in wnrz}
            tophorizcnt = -1
            for wnrhc in horiz.keys():
                tophorizcnt = max(tophorizcnt, horiz[wnrhc])
            wnrz = [realwnr for realwnr in horiz.keys()
                    if horiz[realwnr] == tophorizcnt]
        return (wnrz)

    def chill(self, secs=1):
        pass

    def getchoice(self, plyr):
        return(None)

if __name__ == "__main__":
    g = Game(4)
    g.loadtiles()
    print(g)
    print("\n\n")
    for _ in range(8):
        for color in Game.colors:
            g.centralarea.addtile(color)
    print(g)