import ComputerPlayer as cp
import Strategy as strat

class ComboStrategyPlayer(cp.ComputerPlayer):
    """
    ComboStrategyPlayer - retain a list of strategies and combine them
    to come to decisions about moves to make.
    """
    def __init__(self, game, board):
        super().__init__(game, board)
        self._strategies = []

    def addstrategy(self, strtg):
        """
        addstrategy
        :param strtg: class to instantiate for inclusion in the strategy list
        :return:
        """
        self._strategies.append(strtg)

    def taketurn(self):
        assert len(self._strategies) > 1
        opts = self.game.options()
        evals = self._strategies[0].evaluate(opts, self.board, self.game)
        for strtg in self._strategies[1:]:
            nexteval = strtg.evaluate(opts, self.board, self.game)
            evals = strtg.combineevals(evals, nexteval)
        if len(evals) > 0:
            # print(evals)
            self.implementstrategy(evals[0])
        else:
            super().taketurn()

    def __str__(self):
        return (self.__class__.__name__ + ": " + \
                " ".join([a.__class__.__name__ for a in self._strategies]))
