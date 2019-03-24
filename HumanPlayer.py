import Player as pl

class HumanPlayer(pl.Player):
    """
    Human player - interpret events from game
    """
    def __init__(self, game, board):
        super().__init__(game, board)

    def taketurn(self, event=None):
        # event = None
        # i = 0
        # while event is None:
        #     self.game.chill()
        #     event = self.game.getchoice()
        #     i += 1
        #     if i > 1000:
        #         print("Human take turn chilling")
        #         i = 0
        assert event is not None
        print("in human taketurn")
        disp = event[0]
        color = event[1]
        preprow = int(event[2])
        tileset = self.game.chooseoption(disp, color)
        self.board.playtiles(preprow, tileset)
