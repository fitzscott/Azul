import ComputerPlayer as cp

class HumanPlayer(cp.ComputerPlayer):
    """
    Human player - interpret events from game
    """
    def __init__(self, game, board):
        super().__init__(game, board)

    def taketurn(self, event=None):
        assert event is not None
        # print("in human taketurn")
        disp = event[0]
        color = event[1]
        preprow = int(event[2])
        tileset = self.game.chooseoption(disp, color)
        self.board.playtiles(preprow, tileset)
