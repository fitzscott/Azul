import ComputerPlayer as cp

class SingleStrategyPlayer(cp.ComputerPlayer):
    """
    Take a single strategy and stick with it.
    """
    def __init__(self, game, board, strt):
        super().__init__(game, board)
        self._strategy = strt

    def taketurn(self):
        """
        taketurn - decide what to do
        :return:
        """
        # get my options from the game
        opts = self.game.options()
        rec_opt = self._strategy.recommend(opts, self.board)
        if rec_opt is not None:
            self.implementstrategy(rec_opt)
        else:
            super().taketurn()

    def __str__(self):
        return (self.__class__.__name__ + ": " + " " + \
                self._strategy.__class__.__name__)
