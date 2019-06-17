import pygame
import Game as g
import sys
import math
import datetime as dt


class GraphicGame(g.Game):
    """
    Take game functions and display them in a pygame window
    """
    Gray = (127, 127, 127)
    Colors = { "K": (0,0,0), "W": (191, 191, 255), "B": (0, 31, 255),
               "R": (255, 0, 0), "Y": (255, 191, 0), " ": Gray,
               "-": (159, 159, 159), "1": (255, 255, 255) }

    def __init__(self, numplayers=4):
        super().__init__(numplayers)
        self.loadtiles()
        self._dims = [900, 600]
        self._players = []
        self._screen = None
        self._revcolors = {}
        self._factoryradius = 40
        self._factlocs = {}
        self._centrallocs = {}
        for ckey in GraphicGame.Colors.keys():
            colors = GraphicGame.Colors[ckey]
            # Is there a way to do a comprehension here instead?
            self._revcolors[ckey] = (255 - colors[0], 255 - colors[1],
                                     255 - colors[2])
        # all the underlying final boards are the same
        self._finalcolors = self.playerboard[0].finalboard.underrows
        self._humanevent = None
        self._clock = None

    @property
    def revcolors(self):
        return(self._revcolors)

    @property
    def factoryradius(self):
        return (self._factoryradius)

    def addCompPlayers(self):
        import ComboStrategyPlayer as csp

        self._players = []
        for pidx in range(self.numplayers):
            plyr = csp.ComboStrategyPlayer(self, self.playerboard[pidx])
            plyr.randstrats()       # go with defaults 2 & 6 for now
            self._players.append(plyr)

    @property
    def tiledim(self):
        return(20)

    def drawboard(self, plnum, preporfinal, topx, topy):

        clr = (0, 0, 0)
        if preporfinal == "P":
            dispstr = str(self.playerboard[plnum].prepboard)
        else:   # final board
            dispstr = str(self.playerboard[plnum].finalboard)
            # clr = (255, 255, 255)
        pygame.draw.rect(self._screen, clr, [topx-1, topy-1, 102, 102], 2)

        currrow = 0
        for row in dispstr.split("\n"):
            if len(row) < 5:
                continue
            # print("Displaying row " + row + " for player " + str(plnum))
            currcol = 0
            for col in row:
                # print("  displaying (" + str(currcol) + "," + str(currrow) + \
                #       " of color " + str(GraphicGame.Colors[col]))
                pygame.draw.rect(self._screen, self.revcolors[col],
                                 [topx + currcol * self.tiledim,
                                  topy + currrow * self.tiledim,
                                  self.tiledim, self.tiledim], 1)
                pygame.draw.rect(self._screen, GraphicGame.Colors[col],
                                 [topx + currcol * self.tiledim + 1,
                                  topy + currrow * self.tiledim + 1,
                                  self.tiledim - 1, self.tiledim - 1])
                # draw a marker for the position in the final board
                if preporfinal == "F" and col == "-":
                    # GraphicGame.Colors[col] == GraphicGame.Gray:
                    circcolor = self._finalcolors[currrow][currcol]
                    pygame.draw.circle(self._screen,
                                       GraphicGame.Colors[circcolor],
                                       [topx + currcol * self.tiledim +
                                        int(self.tiledim / 2),
                                        topy + currrow * self.tiledim +
                                        int(self.tiledim / 2)],
                                       int(self.tiledim / 4))
                currcol += 1
            currrow += 1

    def drawpenalty(self, plnum, topx, topy):
        dispstr = str(self.playerboard[plnum].penalty)
        offset = 0
        for tile in dispstr.strip():
            pygame.draw.rect(self._screen, self.revcolors[tile],
                             [topx + offset * self.tiledim,
                              topy, self.tiledim, self.tiledim], 1)
            pygame.draw.rect(self._screen, GraphicGame.Colors[tile],
                             [topx + offset * self.tiledim + 1,
                              topy, self.tiledim - 1, self.tiledim - 1])
            offset += 1
            if offset == 7:
                break

    def drawfactory(self, centerx, centery, num):
        tiles = self.display[num - 1].tiles
        if self._humanevent is not None:
            selfactnum = int(self._humanevent[0])
            selcolor = self._humanevent[1]
            drawx = True
        else:
            selfactnum = -1
            drawx = False
        if len(tiles) == 0 or num == selfactnum:
            clr = (192, 192, 192)
        else:
            clr = (255, 255, 255)
        pygame.draw.circle(self._screen, clr, (centerx, centery),
                           self.factoryradius)
        self._factlocs[num] = (centerx, centery)

        dispnum = self._font.render(str(num), True, (0, 0, 0), clr)
        self._screen.blit(dispnum, (centerx - 2, centery - self.factoryradius + 1))
        for tileidx in range(len(tiles)):
            if tileidx % 2 == 0:
                x = centerx - self.tiledim - 1
            else:
                x = centerx + 1
            if tileidx < 2:
                y = centery - self.tiledim - 1
            else:
                y = centery + 1
            pygame.draw.rect(self._screen, self.revcolors[tiles[tileidx]],
                             [x, y, self.tiledim, self.tiledim], 1)
            pygame.draw.rect(self._screen, GraphicGame.Colors[tiles[tileidx]],
                             [x + 1, y + 1, self.tiledim - 1, self.tiledim - 1])
            if drawx and num == selfactnum and tiles[tileidx] == selcolor:
                # draw an X through the selected tiles
                pygame.draw.line(self._screen, self.revcolors[tiles[tileidx]],
                                 [x, y], [x+self.tiledim, y+self.tiledim], 2)
                pygame.draw.line(self._screen, self.revcolors[tiles[tileidx]],
                                 [x+self.tiledim, y], [x, y+self.tiledim], 2)


    def drawfactories(self):
        """
        Lay out the factory displays in a rough ellipse.
        :return:
        """
        numfactories = len(self.playerboard) * 2 + 1
        centralheight = 240
        ychange = int(centralheight / numfactories) * 2
        self._factlocs = {}

        # clear the rectangle
        pygame.draw.rect(self._screen, GraphicGame.Gray,
                         [0, 200, self._dims[0], self._dims[1] - 200])
        x = 400
        y = 240
        factnum = 1
        self.drawfactory(x, y, factnum)
        remaining = numfactories - 1
        while remaining > 0:
            xoffset = 0
            if remaining <= int(numfactories / 2) + 1 and \
                remaining >= int(numfactories / 2) - 1:
                ycoffset = 40
                xoffset = -20
            else:
                ycoffset = 0
            y += ychange + ycoffset
            if remaining == numfactories - 1:
                xoffset = 30
            xchange = 75 * (4 - abs(5 - remaining)) + xoffset
            factnum += 1
            self.drawfactory(x - xchange, y, factnum)
            factnum += 1
            self.drawfactory(x + xchange, y, factnum)
            remaining -= 2

    def drawcentral(self):
        y = 320
        x = 330
        rowlen = 8
        tiles = self.centralarea.tiles
        for tileidx in range(len(tiles)):
            if tileidx % rowlen == 0:
                y += self.tiledim + 5
            x = 330 + (tileidx % rowlen) * self.tiledim + 5
            self._centrallocs[tileidx] = (x, y)
            pygame.draw.rect(self._screen, self.revcolors[tiles[tileidx]],
                             [x, y, self.tiledim, self.tiledim], 1)
            pygame.draw.rect(self._screen, GraphicGame.Colors[tiles[tileidx]],
                             [x + 1, y + 1, self.tiledim - 1, self.tiledim - 1])
            if self._humanevent is not None:
                selfactnum = int(self._humanevent[0])
                seltilecolor = self._humanevent[1]
            else:
                selfactnum = -1
                seltilecolor = 'Z'
            # print("Selected factory " + str(selfactnum) + " color " + seltilecolor)
            if selfactnum == 0 and seltilecolor == tiles[tileidx]:
                # draw an X through the selected tiles
                pygame.draw.line(self._screen, self.revcolors[tiles[tileidx]],
                                 [x, y], [x+self.tiledim, y+self.tiledim], 2)
                pygame.draw.line(self._screen, self.revcolors[tiles[tileidx]],
                                 [x+self.tiledim, y], [x, y+self.tiledim], 2)

    def finddisplay(self, x, y):
        retval = (-1, 0)
        for factid in self._factlocs.keys():
            factx, facty = self._factlocs[factid]
            dist = math.sqrt((factx - x) ** 2 + (facty - y) ** 2)
            if dist <= self.factoryradius:
                tiles = self.display[factid - 1].tiles
                if len(tiles) < 1:
                    break
                # Tiles 0 & 2 are left of the X value, 1 & 3 right.
                # Tiles 0 & 1 are above the Y value, 2 & 3 below.
                if x <= factx:
                    if y <= facty:
                        tileidx = 0
                    else:
                        tileidx = 2
                else:
                    if y <= facty:
                        tileidx = 1
                    else:
                        tileidx = 3
                retval = (factid, tiles[min(tileidx, len(tiles)-1)])
        return (retval)

    def findcentral(self, x, y):
        for tileidx in self._centrallocs.keys():
            # print("comparing " + str(x) + "," + str(y) + " vs." + \
            #       str(self._centrallocs[tileidx]))
            if x >= self._centrallocs[tileidx][0] and \
                x < self._centrallocs[tileidx][0] + self.tiledim and \
                y >= self._centrallocs[tileidx][1] and \
                y < self._centrallocs[tileidx][1] + self.tiledim and \
                    tileidx < len(self.centralarea.tiles):
                return (self.centralarea.tiles[tileidx])
        return (None)

    def handleclickevents(self, x, y, plnum):
        """
        A human player choice is made up of two click events:  Choosing a
        color in a factory display and choosing the preparatory row in
        which to place those color tiles.
        :param x: X-axis position
        :param y: Y-axis position
        :param plnum: player number
        :return:
        """
        # print("in handleclickevents")
        factnum, color = self.finddisplay(x, y)
        if factnum != -1:
            # print("clicked in circle " + str(factnum) + ", color " + color)
            self._humanevent = str(factnum) + color
            self.drawall(plnum)
        else:
            centerval = self.findcentral(x, y)
            if centerval is not None:
                self._humanevent = "0" + centerval
                # print("clicked in the central area, event is " + self._humanevent)
                self.drawall(plnum)
            elif y < 140:   # above the penalty line
                # Maybe it's a prep row choice
                # Since there's only one human player, simplify by just
                # translating the X value to a row number.
                topy = 20
                rownum = min(self.tiledim - 1, int((y - topy) / self.tiledim))
                # print("clicked in prep row " + str(rownum))
                if rownum >= 0 and rownum < self.tiledim and \
                        self._humanevent is not None:
                    self._humanevent = self._humanevent[0:2] + str(rownum)

    def chill(self, secs=1):
        self._clock.tick(10)
        pygame.time.wait(secs * 1000)

    def getchoice(self, plyr):
        if self._humanevent is not None and len(self._humanevent) == 3:
            plyr.taketurn(self._humanevent)
            self._humanevent = None
            return (True)
        pygame.time.wait(100)
        # print("getting events in getchoice")
        return (False)

    def drawall(self, plnum):
        self.drawboard(plnum, "P", plnum * 210 + 25, 20)
        self.drawboard(plnum, "F", plnum * 210 + 127, 20)
        self.drawpenalty(plnum, plnum * 210 + 25, 140)
        score = str(self.playerboard[plnum].score)
        dispsco = self._font.render("Score:" + " " * (6 - len(score)) \
                                    + score + " " * (5 - len(score)),
                                    True, (255, 255, 255),
                                    GraphicGame.Gray)
        self._screen.blit(dispsco, (plnum * 210 + 25, 170))
        self.drawfactories()
        self.drawcentral()
        pygame.display.flip()

    def saveresults(self):
        currdttm = dt.datetime.today()
        currmo = currdttm.strftime("%y%m")
        rsltfl = open("rslts" + currmo + ".txt", "a")
        gamestr = currdttm.strftime("%d%H%M%S")
        winrarr = self.winner()
        for plyridx in range(self.numplayers):
            if plyridx in winrarr:
                winstr = "Winner: "
            else:
                winstr = "Loser:  "
            plyr = self._players[plyridx]
            rsltfl.write(gamestr + " " + winstr + str(plyr) + " final score = " + \
                  str(plyr.board.score) + "\n")
        rsltfl.close()

    def playbymyself(self, iters=1, saveRslts=False):
        """
        Run through event loop, which, for the computer players, doesn't
        involve any keyboard, mouse, etc. input.
        :return:
        """
        import HumanPlayer as hp

        pygame.init()
        self._screen = pygame.display.set_mode(self._dims)
        pygame.display.set_caption("Azul")
        # self._font = pygame.font.SysFont("Courier", 12)
        fontlist = pygame.font.get_fonts()
        font = ""
        for preffont in ["verdana", "tahoma", "couriernew", "calibri"]:
            if preffont in fontlist:
                font = preffont
                break
        if font == "":
            font = fontlist[0]
        self._font = pygame.font.SysFont(font, 12)

        self._clock = pygame.time.Clock()

        gamecnt = 0
        while gamecnt < iters:
            self._clock.tick(10)
            self._screen.fill(GraphicGame.Gray)
            cont = True
            maxturns = 300
            firstplayer = 0
            turnz = 0
            # draw board here
            while cont and turnz < maxturns:  # real games rarely go past 5
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        cont = False
                        gamecnt = iters + 1
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clickx, clicky = pygame.mouse.get_pos()
                        self.handleclickevents(clickx, clicky, 0)
                for idxnum in range(self.numplayers):
                    self._clock.tick(10)
                    plnum = (firstplayer + idxnum) % self.numplayers
                    if self.turnover():
                        for plnum in range(self.numplayers):
                            self.playerboard[plnum].movescore(self.box)
                            self.drawall(plnum)
                            if self.playerboard[plnum].firstplayer:
                                firstplayer = plnum
                                self.playerboard[plnum].firstplayer = False
                            if self.playerboard[plnum].finalboard.horizrowcomplete():
                                cont = False
                        if cont:
                            if not self.loadtiles():
                                cont = False
                                break
                        break
                    self.drawall(plnum)
                    # This feels like a kludge.
                    # print("class name is " + self._players[plnum].__class__.__name__ )
                    if self._players[plnum].__class__.__name__ == "HumanPlayer":
                        while not self.getchoice(self._players[plnum]):
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit(0)
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    clickx, clicky = pygame.mouse.get_pos()
                                    self.handleclickevents(clickx, clicky, plnum)
                            pygame.time.wait(500)
                    else:
                        self._players[plnum].taketurn()
                    self.drawall(plnum)
                    pygame.time.wait(100)
                self.show()

            # write "Winner" under winner's board (potentially more than 1)
            print("Finding winner")
            for winrnum in self.winner():
                print("one winner is " + str(winrnum))
                dispwnr = self._font.render("Winner!", True, (0, 0, 0),
                                            (0, 255, 255))
                self._screen.blit(dispwnr, (winrnum * 210 + 25, 190))
                pygame.display.flip()

            print("Game " + str(gamecnt) + " completed.")
            if saveRslts:
                self.saveresults()
            pygame.time.wait(10000)
            self.reset()
            self.loadtiles()
            self.addCompPlayers()
            gamecnt += 1


if __name__ == "__main__":
    gg = GraphicGame()
    gg.addCompPlayers()
    gg.playbymyself(20)

