import GraphicGame as gg
import random
import sys
import ComboStrategyPlayer as csp
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


class SmarterGraphicGame(gg.GraphicGame):
    """
    use some successful 3-strategy combos for players
    """

    def getBestFromFile(self, numstrats):
        flnm = "bestcombo_" + str(numstrats) + ".txt"
        fl = open(flnm)
        return ("\n".join(fl.readlines()))

    def addCompPlayers(self, numstrats=0):
        import ComboStrategyPlayer as csp


        strats = [mpcs.MostPrevalentColorStrategy, fus.FinishUnfinishedStrategy,  # 0 1
                  efs.ExactFitStrategy, frs.FillRowStrategy, fcs.FillColumnStrategy, # 2 3 4
                  ccs.CompleteColorStrategy, mpss.MaxPlaceScoreStrategy,  # 5 6
                  mps.MinPenaltyStrategy, dhcs.DisplayHighColorStrategy,  # 7 8
                  amfs.AtMostFitStrategy, cps.CentralPositionStrategy]  # 9 10

        if numstrats == 0:
            # Most successful 3-strategy combinations (maybe):
            mostsuccessful = """
            CentralPositionStrategy + DisplayHighColorStrategy + FillColumnStrategy: 0.883720930233
            CentralPositionStrategy + MaxPlaceScoreStrategy + MostPrevalentColorStrategy: 0.811320754717
            FillRowStrategy + MaxPlaceScoreStrategy + MostPrevalentColorStrategy: 0.795454545455
            DisplayHighColorStrategy + FillRowStrategy + MaxPlaceScoreStrategy: 0.767441860465
            CentralPositionStrategy + DisplayHighColorStrategy + FillRowStrategy: 0.762711864407
            
            CentralPositionStrategy + FillColumnStrategy + FillRowStrategy: 0.754716981132
            CentralPositionStrategy + FillColumnStrategy + MostPrevalentColorStrategy: 0.741935483871
            CentralPositionStrategy + DisplayHighColorStrategy + MostPrevalentColorStrategy: 0.727272727273
            
            FillColumnStrategy + MaxPlaceScoreStrategy + MostPrevalentColorStrategy: 0.716981132075
            CentralPositionStrategy + FillRowStrategy + MostPrevalentColorStrategy: 0.714285714286
            DisplayHighColorStrategy + MaxPlaceScoreStrategy + MostPrevalentColorStrategy: 0.7
            CentralPositionStrategy + DisplayHighColorStrategy + MaxPlaceScoreStrategy: 0.69387755102
            
            DisplayHighColorStrategy + FillRowStrategy + MostPrevalentColorStrategy: 0.666666666667
            FillColumnStrategy + FillRowStrategy + MostPrevalentColorStrategy: 0.627450980392
            FillColumnStrategy + FillRowStrategy + MaxPlaceScoreStrategy: 0.625
            
            CentralPositionStrategy + FillRowStrategy + MaxPlaceScoreStrategy: 0.62
            CentralPositionStrategy + FillColumnStrategy + MaxPlaceScoreStrategy: 0.62
            DisplayHighColorStrategy + FillColumnStrategy + MaxPlaceScoreStrategy: 0.609756097561
            
            AtMostFitStrategy + FillColumnStrategy + MaxPlaceScoreStrategy: 0.565217391304
            AtMostFitStrategy + CentralPositionStrategy + FillRowStrategy: 0.553191489362
            """
            delim = " + "
            numstrats = 3
        else:
            mostsuccessful = self.getBestFromFile(numstrats)
            print(mostsuccessful)
            delim = "+"

        # This was a pain to put together.  Smarter way?
        # bestcombos = [[10, 8, 4], [10, 6, 0], [3, 6, 0], [8, 3, 6], [10, 8, 3],
        #               [10, 4, 3], [10, 4, 0], [10, 8, 0],
        #               [4, 6, 0], [10, 3, 0], [8, 6, 0], [10, 8, 6],
        #               [8, 3, 0], [4, 3, 0], [4, 3, 6],
        #               [10, 3, 6], [10, 4, 6], [8, 4, 6],
        #               [9, 4, 6], [9, 10, 3]]
        self._players = []
        stratnamecombos = []
        for stratset in mostsuccessful.strip().split("\n"):
            stratnames = stratset.split(":")[0].strip().split(delim)
            if len(stratnames) == numstrats:
                stratnamecombos.append(stratnames)
                print("!".join(stratnames))
        for pidx in range(self.numplayers):
            plyr = csp.ComboStrategyPlayer(self, self.playerboard[pidx])
            # choose a combo above
            choice = random.randint(0, len(stratnamecombos)-1)
            for stratname in stratnamecombos[choice]:
                for stratcls in strats:
                    if stratcls.__name__ == stratname:
                        plyr.addstrategy(stratcls())
                        break
            print("Player " + str(pidx+1) + ":" + ",".join(plyr.strstrategies))
            self._players.append(plyr)

    def replaceWithHuman(self, plnum=0):
        import HumanPlayer as hp

        plyr = hp.HumanPlayer(self, self.playerboard[plnum])
        self._players[plnum] = plyr

if __name__ == "__main__":
    gg = SmarterGraphicGame()
    gg.addCompPlayers(8)
    gg.replaceWithHuman(3)
    gg.playbymyself(1)
