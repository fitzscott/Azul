import ComputerPlayer as cp
# import Strategy as strat
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
import TopRowsStrategy as trs


class ComboStrategyPlayer(cp.ComputerPlayer):
    """
    ComboStrategyPlayer - retain a list of strategies and combine them
    to come to decisions about moves to make.
    """
    strats = [mpcs.MostPrevalentColorStrategy, fus.FinishUnfinishedStrategy,
              efs.ExactFitStrategy, frs.FillRowStrategy, fcs.FillColumnStrategy,
              ccs.CompleteColorStrategy, mpss.MaxPlaceScoreStrategy,
              mps.MinPenaltyStrategy, dhcs.DisplayHighColorStrategy,
              amfs.AtMostFitStrategy, cps.CentralPositionStrategy,
              trs.TopRowsStrategy]

    def __init__(self, game, board):
        super().__init__(game, board)
        self._strategies = []

    @property
    def strstrategies(self):
        return ([str(strat).split(".")[0][1:] for strat in self._strategies])

    @property
    def strategies(self):
        return (self._strategies)

    def clearstrats(self):
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

        stratidxs = [idx for idx in range(len(ComboStrategyPlayer.strats))]
        assert lo >= 2
        for strcnt in range(random.randint(lo, hi)):
            sidx = random.randint(0, len(stratidxs)-1)
            self.addstrategy(ComboStrategyPlayer.strats[stratidxs[sidx]]())
            stratidxs.remove(stratidxs[sidx])

    def __str__(self):
        return (self.__class__.__name__ + ": " + \
                " ".join([a.__class__.__name__ for a in self._strategies]))

    def getbestfromfile(self, flnm="reallythebest.txt"):
        fl = open(flnm)
        retval = "\n".join(fl.readlines())
        fl.close()
        # print("Really best:\n" + str(retval))
        return (retval)

    def getstratnamecombos(self, mostsuccessful, delim):
        stratnamecombos = []

        for stratset in mostsuccessful.strip().split("\n"):
            stratnames = stratset.split(":")[0].strip().split(delim)
            if len(stratnames) >= 2:
                stratnamecombos.append(stratnames)
                # print("!".join(stratnames))
        # print(str(stratnamecombos))
        return (stratnamecombos)

    def randbeststrats(self, flnm="reallythebest4.txt"):        # was 5, but too slow
        mostsuccessful = self.getbestfromfile(flnm)
        stratnamecombos = self.getstratnamecombos(mostsuccessful, "+")
        choice = random.randint(0, len(stratnamecombos)-1)
        for stratname in stratnamecombos[choice]:
            for stratcls in ComboStrategyPlayer.strats:
                if stratcls.__name__ == stratname:
                    self.addstrategy(stratcls())
                    break
