import ComputerPlayer as cp
import PlayableColorStrategy as pcs

class PlayableColorPlayer(cp.ComputerPlayer):
    """
    PlayableColorPlayer - take the simple strategy & use it for choices
    """
    def __init__(self, game, board):
        super().__init__(game, board)
        self._strat = pcs.PlayableColorStrategy()

    def taketurn(self):
        """
        taketurn - decide what to do
        :return:
        """
        # get my options from the game
        opts = self.game.options()
        rec_opt = self._strat.recommend(opts, self.board)
        if rec_opt is not None:
            self.implementstrategy(rec_opt)
        else:
            super().taketurn()
