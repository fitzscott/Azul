import GraphicGame as gg
import random
import sys
import WeightedComboStrategyPlayer as wcsp


class SmartWgtGraphicGame(gg.GraphicGame):
    """
    Use the product of the weighted combination analysis as the base strategies
    for the computer players.
    """
    def __init__(self, numplayers=4):
        super().__init__(numplayers)

    def addCompPlayers(self, flnm="bestwgtd01.txt"):
        # First, get the list of weighted strategy combinations to use.
        wgtfile = open(flnm)
        wgtcombos = wgtfile.readlines()
        wgtfile.close()
        fullwgtset = [wc.strip().split(":")[0]
                      for wc in wgtcombos
                      if len(wc) > 0]

        self._players = []
        for pidx in range(self.numplayers):
            plyr = wcsp.WeightedComboStrategyPlayer(self, self.playerboard[pidx])
            # choose a combo above
            choice = random.randint(0, len(fullwgtset)-1)
            for stratstr in fullwgtset[choice].split("+"):
                plyr.addstratbystr(stratstr)
            plyr.stdweight()
            print("Player " + str(pidx + 1) + " = " + ", ".join(plyr.strstrategies))
            self._players.append(plyr)

    def replaceWithHuman(self, plnum=0):
        import HumanPlayer as hp

        plyr = hp.HumanPlayer(self, self.playerboard[plnum])
        self._players[plnum] = plyr


if __name__ == "__main__":
    if len(sys.argv) > 1:
        iters = int(sys.argv[1])
    else:
        iters = 1
    if len(sys.argv) > 2:
        flnm = sys.argv[2]
    else:
        flnm = "bestwgtd01.txt"

    gg = SmartWgtGraphicGame()
    gg.addCompPlayers(flnm)
    gg.replaceWithHuman(random.randint(0, 3))
    gg.playbymyself(iters)
