import sys
import random
import Game as g
import SingleStrategyPlayer as ssp
# import ComboStrategyPlayer as csp
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

def rungame():
    maxturns = 300

    playme = g.Game(4)
    playme.loadtiles()
    plyrz = []
    strats = [efs.ExactFitStrategy, trs.TopRowsStrategy,
               fcs.FillColumnStrategy, ccs.CompleteColorStrategy]
    # strats = [efs.ExactFitStrategy, frs.FillRowStrategy,
    #            fcs.FillColumnStrategy, ccs.CompleteColorStrategy]
    # strats = [mpss.MaxPlaceScoreStrategy, frs.FillRowStrategy,
    #           fcs.FillColumnStrategy, ccs.CompleteColorStrategy]
    # strats = [mpss.MaxPlaceScoreStrategy, frs.FillRowStrategy,
    #           fcs.FillColumnStrategy, mps.MinPenaltyStrategy]
    # strats = [mpss.MaxPlaceScoreStrategy, frs.FillRowStrategy,
    #           dhcs.DisplayHighColorStrategy, mps.MinPenaltyStrategy]
    # strats = [mpss.MaxPlaceScoreStrategy, amfs.AtMostFitStrategy,
    #           dhcs.DisplayHighColorStrategy, mps.MinPenaltyStrategy]
    # strats = [mpss.MaxPlaceScoreStrategy, cps.CentralPositionStrategy,
    #          dhcs.DisplayHighColorStrategy, mps.MinPenaltyStrategy]

    for plnum in range(4):
        plyr = ssp.SingleStrategyPlayer(playme, playme.playerboard[plnum],
                                        strats[plnum]())
        plyrz.append(plyr)

    playme.show()
    cont = True
    firstplayer = 0
    turnz = 0
    retval = 0
    # while cont:
    while cont and turnz < maxturns:  # real games rarely go past 5
        for idxnum in range(4):
            plnum = (firstplayer + idxnum) % 4
            if playme.turnover(): #   dispnum == 9:
                # cont = False
                for plnum in range(4):
                    playme.playerboard[plnum].movescore(playme.box)
                    if playme.playerboard[plnum].firstplayer:
                        firstplayer = plnum
                        playme.playerboard[plnum].firstplayer = False
                    if playme.playerboard[plnum].finalboard.horizrowcomplete():
                        cont = False
                if cont:
                    print("\t  " + 8 * "+" + " turn " + str(turnz+1) + " next")
                    if not playme.loadtiles():
                        cont = False
                        retval = 1
                        break
                    playme.show()
                break
            print("Player " + str(plnum+1) + " turn:")
            plyrz[plnum].taketurn()
            playme.show()
        turnz += 1
    print(8 * "+" + "\t\tFinal scoring:")
    for idxnum in range(4):
        playme.playerboard[idxnum].finalscore()
    playme.show()
    print("\nSummary of final scores:")
    for plyr in plyrz:
        print(str(plyr) + " final score = " + str(plyr.board.score))
    if turnz == maxturns:
        retval = 1
    return (retval)

if __name__ == "__main__":
    rungame()
