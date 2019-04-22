import ComboStrategyPlayer as csp
import Weight as w

class WeightedComboStrategyPlayer(csp.ComboStrategyPlayer):
    """
    In addition to the set of strategies utilized by the player, there is an
    assigned weight to each strategy, signifying its importance among the
    strategies.
    """

    def __init__(self, game, board, weights=None):
        super().__init__(game, board)
        self._weights = weights

    @property
    def weights(self):
        if self._weights is None:
            self._weights = [r for r in range(len(self.strategies), 0, -1)]
        return (self._weights)

    @weights.setter
    def weights(self, val):
        self._weights = val

    def makeweight(self):
        wgt = w.Weight(self.strategies)
        self.weights = wgt.randweight()

    def wgtstr(self):
        # Probably should be a __str__ method in the Weight class
        wstr = ""
        for wgt in self.weights:
            wstr += str(wgt)
        return(wstr)

    def taketurn(self):
        """
        Copy & paste re-use - ick.
        Better yet, it's clunky, too.
        :return:
        """
        if len(self._strategies) <= 1:
            print(self)
        assert len(self._strategies) > 1
        opts = self.game.options()
        stratidx = 0
        evals = self._strategies[0].evaluate(opts, self.board, self.game)
        rerankedevals = []
        for ev in evals:
            newrank = ev.split("_")[1] * self.weights[stratidx]
            rerankedevals.append(ev[0:3] + "_" + str(newrank))
        evals = [e for e in rerankedevals]
        stratidx += 1
        for strtg in self._strategies[1:]:
            nexteval = strtg.evaluate(opts, self.board, self.game)
            rerankedevals = [ev[0:3] + "_" + str(int(ev.split("_")[1]) *
                             self.weights[stratidx])
                             for ev in nexteval]
            nexteval = [rre for rre in rerankedevals]
            evals = strtg.combineevals(evals, nexteval)
            stratidx += 1
        if len(evals) > 0:
            # print(evals)
            self.implementstrategy(evals[0])
        else:
            super().taketurn()
