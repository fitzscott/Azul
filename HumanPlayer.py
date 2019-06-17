import ComputerPlayer as cp

class HumanPlayer(cp.ComputerPlayer):
    """
    Human player - interpret events from game
    """
    def __init__(self, game, board):
        super().__init__(game, board)

    def __str__(self):
        return (self.__class__.__name__ + ": WhatStrategy Dunno")

    def taketurn(self, event=None):
        import FinalBoardComponent as fbc

        assert event is not None
        # print("in human taketurn")
        disp = event[0]
        color = event[1]
        # Not sure how this could arrive out of range
        preprow = min(max(0, int(event[2])),
                      fbc.FinalBoardComponent.dimension - 1)
        tileset = self.game.chooseoption(disp, color)
        self.board.playtiles(preprow, tileset)
