import pygame
import Game as g

class GraphicGame(g.Game):
    """
    Take game functions and display them in a pygame window
    """
    Gray = (127, 127, 127)
    Colors = { "K": (0,0,0), "W": (191, 191, 255), "B": (0, 31, 255),
               "R": (255, 0, 0), "Y": (255, 191, 0), "-": Gray,
               " ": (159, 159, 159) }

    def __init__(self, numplayers=4):
        super().__init__(numplayers)
        self.loadtiles()
        self._dims = [900, 600]
        self._players = []

    def addCompPlayers(self):
        import ComboStrategyPlayer as csp

        for pidx in range(self.numplayers):
            plyr = csp.ComboStrategyPlayer(self, self.playerboard[pidx])
            plyr.randstrats()       # go with defaults 2 & 6 for now
            self._players.append(plyr)

    def drawboard(self, plnum, preporfinal, topx, topy):
        tiledim = 20

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
                pygame.draw.rect(self._screen, GraphicGame.Colors[col], \
                                 [topx + currcol * tiledim, \
                                  topy + currrow * tiledim, \
                                  tiledim, tiledim])
                currcol += 1
            currrow += 1


    def playbymyself(self):
        """
        Run through event loop, which, for the computer players, doesn't
        involve any keyboard, mouse, etc. input.
        :return:
        """
        pygame.init()
        self._screen = pygame.display.set_mode(self._dims)
        pygame.display.set_caption("Azul")
        self._screen.fill(GraphicGame.Gray)

        clock = pygame.time.Clock()

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
                if self.turnover():  # dispnum == 9:
                    # cont = False
                    for plnum in range(self.numplayers):
                        self.playerboard[plnum].movescore(self.box)
                        self.drawboard(plnum, "P", plnum * 210 + 25, 20)
                        self.drawboard(plnum, "F", plnum * 210 + 127, 20)
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
                # self.drawboard(plnum, "F", plnum * 210 + 125, 20)
                pygame.display.flip()
                pygame.time.wait(100)
            self.show()

        pygame.time.wait(10000)


if __name__ == "__main__":
    gg = GraphicGame()
    gg.addCompPlayers()
    gg.playbymyself()

