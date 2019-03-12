import PlayableColorPlayer as pcp
import FinishUnfinishedStrategy as fus

class FinishUnfinishedPlayer(pcp.PlayableColorPlayer):
    """
    This can't stand on its own, since at the start of the game, there are
    no partially-finished rows.  Its back-up strategy will be PCP.
    """
    def __init__(self, game, board):
        super().__init__(game, board)
        self._primestrat = fus.FinishUnfinishedStrategy()

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
