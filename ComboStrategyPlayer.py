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

    def randstrats(self, lo=2, hi=6):
        """
        Pick some random strategies, a random number of times, and add each.
        :param lo: Minimum number of strategies
        :param hi: Maxmum number of strategies
        :return:
        """
        import random
        import MostPrevalentColorStrategy as mpcs
        import FinishUnfinishedStrategy as fus
        import ExactFitStrategy as efs
        import FillRowStrategy as frs
        import FillColumnStrategy as fcs
        import CompleteColorStrategy as ccs
        import MaxPlaceScoreStrategy as mpss
        import MinPenaltyStrategy as mps
        import DisplayHighColorStrategy as dhcs
        import AtMostFitStrategy as amfs
        import CentralPositionStrategy as cps

        strats = [mpcs.MostPrevalentColorStrategy, fus.FinishUnfinishedStrategy,
                  efs.ExactFitStrategy, frs.FillRowStrategy, fcs.FillColumnStrategy,
                  ccs.CompleteColorStrategy, mpss.MaxPlaceScoreStrategy,
                  mps.MinPenaltyStrategy, dhcs.DisplayHighColorStrategy,
                  amfs.AtMostFitStrategy, cps.CentralPositionStrategy]

        stratidxs = [idx for idx in range(len(strats))]
        assert lo >= 2
        for strcnt in range(random.randint(lo, hi)):
            sidx = random.randint(0, len(stratidxs)-1)
            self.addstrategy(strats[stratidxs[sidx]]())
            stratidxs.remove(stratidxs[sidx])

    def __str__(self):
        return (self.__class__.__name__ + ": " + \
                " ".join([a.__class__.__name__ for a in self._strategies]))
