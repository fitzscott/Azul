import ComputerPlayer as cp
import MostPrevalentColorStrategy as mpcs

class MostPrevalentColorPlayer(cp.ComputerPlayer):
    def __init__(self, game, board):
        super().__init__(game, board)
        self._primestrat = mpcs.MostPrevalentColorStrategy()

    def taketurn(self):
        """
        taketurn - decide what to do
        :return:
        """
        # get my options from the game
        opts = self.game.options()
        rec_opt = self._primestrat.recommend(opts, self.board)
        if rec_opt is not None:
            self.implementstrategy(rec_opt)
        else:
            super().taketurn()
