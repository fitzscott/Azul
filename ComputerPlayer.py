import Player as pl
import random

class ComputerPlayer(pl.Player):
    """
    ComputerPlayer - the default computer behavior is random,
    completely unlike real computers.
    """
    def __init__(self, game, board):
        super().__init__(game, board)

    def taketurn(self):
        """
        taketurn - decide what to do
        :return:
        """
        # get my options from the game
        opts = self.game.options()
        choice = random.randint(0, len(opts)-1)
        print("Choosing " + opts[choice])
        # figure out which color
        if opts[choice][0] == '0' and opts[choice][2] == '1':
            startidx = 3
        else:
            startidx = 2
        color = opts[choice][random.randint(startidx, len(opts[choice])-1)]
        print("Chosen color is " + color)
        tileset = self.game.chooseoption(opts[choice], color)
        # print("tileset is " + str(tileset))
        preprow = random.randint(0, 4)      # _really_ random
        # print("Putting them in prep row " + str(preprow+1))
        self.board.playtiles(preprow, tileset)

    def implementstrategy(self, rec_opt):
        option = rec_opt[0]
        color = rec_opt[1]
        preprow = int(rec_opt[2])
        tileset = self.game.chooseoption(option, color)
        # print("getting tileset " + str(tileset) + " from option " + \
        #       str(option) + " into row " + str(preprow))
        self.board.playtiles(preprow, tileset)


if __name__ == "__main__":
    import Game as gg

    rgame = gg.Game()
    rgame.loadtiles()
    rgame.show()
    cp = ComputerPlayer(rgame, rgame.playerboard[0])
    cp.taketurn()
    rgame.show()
