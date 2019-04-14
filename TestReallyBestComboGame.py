import sys
import random
import TestBestComboGame as tbcg
# import SingleStrategyPlayer as ssp
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
import TopRowsStrategy as trs


class TestReallyBestComboGame(tbcg.TestBestComboGame):

    def __init__(self, numplayers):
        super().__init__(numplayers)
        self._plyrz = []
        self._topcombos = []

    def getBestFromFile(self, flnm):
        fl = open(flnm)
        retval = "\n".join(fl.readlines())
        fl.close()
        return (retval)

    @property
    def players(self):
        return (self._plyrz)

    @property
    def topcombos(self):
        return (self._topcombos)

    @topcombos.setter
    def topcombos(self, val):
        self._topcombos = val

    def getstratnamecombos(self, mostsuccessful, delim):
        stratnamecombos = []

        for stratset in mostsuccessful.strip().split("\n"):
            stratnames = stratset.split(":")[0].strip().split(delim)
            if len(stratnames) > 1:
                stratnamecombos.append(stratnames)
                # print("!".join(stratnames))
        # print(str(stratnamecombos))
        return (stratnamecombos)

    def assembletopcombos(self, flnm):
        """
        Take top X combos from each strategy count & assemble in a select list.
        :param cnt: Top X
        :return:
        """
        mostsuccessful = self.getBestFromFile(flnm)
        self.topcombos = self.getstratnamecombos(mostsuccessful, "+")
        # print(str(self.topcombos))

    def rungame(self, flnm):
        maxturns = 300

        self.assembletopcombos(flnm)
        self.loadtiles()
        for plnum in range(len(self.playerboard)):
            plyr = csp.ComboStrategyPlayer(self, self.playerboard[plnum])
            comboidx = random.randint(0, len(self.topcombos) - 1)
            # print("Chose combo " + str(self.topcombos[comboidx]))
            for stratname in self.topcombos[comboidx]:
                for stratcls in tbcg.TestBestComboGame.strats:
                    if stratcls.__name__ == stratname:
                        plyr.addstrategy(stratcls())
            print(plyr)
            self.players.append(plyr)

        self.show()
        cont = True
        firstplayer = 0
        turnz = 0
        retval = 0
        # while cont:
        while cont and turnz < maxturns:  # real games rarely go past 5
            for idxnum in range(4):
                plnum = (firstplayer + idxnum) % 4
                if self.turnover():  # dispnum == 9:
                    # cont = False
                    for plnum in range(4):
                        self.playerboard[plnum].movescore(self.box)
                        if self.playerboard[plnum].firstplayer:
                            firstplayer = plnum
                            self.playerboard[plnum].firstplayer = False
                        if self.playerboard[plnum].finalboard.horizrowcomplete():
                            cont = False
                    if cont:
                        print("\t  " + 8 * "+" + " turn " + str(turnz + 1) + " next")
                        if not self.loadtiles():
                            cont = False
                            retval = 1
                            break
                        self.show()
                    break
                print("Player " + str(plnum + 1) + " turn:")
                self.players[plnum].taketurn()
                self.show()
                turnz += 1
        print(8 * "+" + "\t\tFinal scoring:")
        for idxnum in range(4):
            self.playerboard[idxnum].finalscore()
        self.show()
        print("\nSummary of final scores:")
        winrarr = self.winner()
        for plyridx in range(len(self.players)):
            if plyridx in winrarr:
                winstr = "Winner: "
            else:
                winstr = "Loser:  "
            print(winstr + str(self.players[plyridx]) + " final score = " + \
                  str(self.players[plyridx].board.score))

        if turnz == maxturns:
            retval = 1
        return (retval)


if __name__ == "__main__":
    trbcg = TestReallyBestComboGame(4)
    if len(sys.argv) >= 2:
        flnm = int(sys.argv[1])
    else:
        flnm = "reallythebest8.txt"
    trbcg.rungame(flnm)
