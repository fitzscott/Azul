import pygame
import Game as g

class GraphicGame(g.Game):
    """
    Take game functions and display them in a pygame window
    """
    Gray = (127, 127, 127)
    Colors = { "K": (0,0,0), "W": (191, 191, 255), "B": (0, 31, 255),
               "R": (255, 0, 0), "Y": (255, 191, 0), "-": Gray,
               " ": (159, 159, 159), "1": (255, 255, 255) }

    def __init__(self, numplayers=4):
        super().__init__(numplayers)
        self.loadtiles()
        self._dims = [900, 600]
        self._players = []
        self._screen = None
        self._revcolors = {}
        for ckey in GraphicGame.Colors.keys():
            colors = GraphicGame.Colors[ckey]
            # Is there a way to do a comprehension here instead?
            self._revcolors[ckey] = (255 - colors[0], 255 - colors[1],
                                     255 - colors[2])

    @property
    def revcolors(self):
        return(self._revcolors)

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
        factoryradius = 40
        tiles = self.display[num - 1].tiles
        if len(tiles) == 0:
            clr = (192, 192, 192)
        else:
            clr = (255, 255, 255)
        pygame.draw.circle(self._screen, clr, (centerx, centery),
                           factoryradius)

        dispnum = self._font.render(str(num), True, (0, 0, 0), clr)
        self._screen.blit(dispnum, (centerx - 2, centery - factoryradius + 1))
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


    def drawfactories(self):
        """
        Lay out the factory displays in a rough ellipse.
        :return:
        """
        numfactories = len(self.playerboard) * 2 + 1
        centralheight = 240
        ychange = int(centralheight / numfactories) * 2

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
            pygame.draw.rect(self._screen, self.revcolors[tiles[tileidx]],
                             [x, y, self.tiledim, self.tiledim], 1)
            pygame.draw.rect(self._screen, GraphicGame.Colors[tiles[tileidx]],
                             [x + 1, y + 1, self.tiledim - 1, self.tiledim - 1])

    def playbymyself(self, iters=1):
        """
        Run through event loop, which, for the computer players, doesn't
        involve any keyboard, mouse, etc. input.
        :return:
        """
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

        clock = pygame.time.Clock()

        gamecnt = 0
        while gamecnt < iters:
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
                for idxnum in range(self.numplayers):
                    clock.tick(10)
                    plnum = (firstplayer + idxnum) % self.numplayers
                    if self.turnover():
                        for plnum in range(self.numplayers):
                            self.playerboard[plnum].movescore(self.box)
                            self.drawboard(plnum, "P", plnum * 210 + 25, 20)
                            self.drawboard(plnum, "F", plnum * 210 + 127, 20)
                            self.drawpenalty(plnum, plnum * 210 + 25, 140)
                            score = str(self.playerboard[plnum].score)
                            dispsco = self._font.render("Score: "+ score +
                                                        (3 - len(score)) * " ",
                                                        True, (255, 255, 255),
                                                        (0, 0, 0))
                            self._screen.blit(dispsco, (plnum * 210 + 25, 170))
                            pygame.display.flip()
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
                    self._players[plnum].taketurn()
                    self.drawboard(plnum, "P", plnum * 210 + 25, 20)
                    self.drawpenalty(plnum, plnum * 210 + 25, 140)
                    self.drawcentral()
                    # self.drawboard(plnum, "F", plnum * 210 + 125, 20)
                    score = self.playerboard[plnum].score
                    dispsco = self._font.render("Score: " + str(score),
                                                True, (255, 255, 255),
                                                (0, 0, 0))
                    self._screen.blit(dispsco, (plnum * 210 + 25, 170))
                    self.drawfactories()
                    self.drawcentral()
                    pygame.display.flip()
                    pygame.time.wait(100)
                self.show()

            pygame.time.wait(6000)
            self.reset()
            self.loadtiles()
            self.addCompPlayers()
            gamecnt += 1


if __name__ == "__main__":
    gg = GraphicGame()
    gg.addCompPlayers()
    gg.playbymyself(100)

