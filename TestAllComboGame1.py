import sys
import random
import time
import itertools
import Game as g
import ComboStrategyPlayer as csp
# import WeightedComboStrategyPlayer as wcsp

def rungame(stratssets):
    maxturns = 300
    maxrt = 60.0

    plcnt = len(stratssets)
    playme = g.Game(plcnt)
    playme.loadtiles()
    plyrz = []
    for plnum in range(plcnt):
        plyr = csp.ComboStrategyPlayer(playme, playme.playerboard[plnum])
        for stratidx in stratssets[plnum]:
            plyr.addstrategy(csp.ComboStrategyPlayer.strats[stratidx]())
        print(plyr)
        plyrz.append(plyr)

    playme.show()
    cont = True
    firstplayer = 0
    turnz = 0
    retval = 0
    # while cont:
    gamestart = time.time()
    while cont and turnz < maxturns:  # real games rarely go past 5
        for idxnum in range(plcnt):
            plnum = (firstplayer + idxnum) % plcnt
            if playme.turnover(): #   dispnum == 9:
                # cont = False
                for plnum in range(plcnt):
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
            currtime = time.time()
            rt = currtime - gamestart
            if rt > maxrt:
                print("No final score, ran " + str(rt))
                return(-1)
    print(8 * "+" + "\t\tFinal scoring:")
    for idxnum in range(plcnt):
        playme.playerboard[idxnum].finalscore()
    playme.show()
    currtime = time.time()
    rt = currtime - gamestart
    print("\nSummary of game - run time " + str(rt) + ", final scores:")
    winrarr = playme.winner()
    for plyridx in range(len(plyrz)):
        if plyridx in winrarr:
            winstr = "Winner: "
        else:
            winstr = "Loser:  "
        print(winstr + str(plyrz[plyridx]) + " final score = " + \
              str(plyrz[plyridx].board.score))

    if turnz == maxturns:
        retval = 1
    return (retval)

def tryallcombos(numstrats):
    stratidxs = [idx for idx in range(len(csp.ComboStrategyPlayer.strats))]
    stratcombos = [strts for strts in
                   itertools.combinations(stratidxs, numstrats)]
    while len(stratcombos) > 1:
        stratsset = []
        for plcnt in range(min(4, len(stratcombos))):
            pickstratidx = random.randint(0, len(stratcombos)-1)
            stratsset.append(stratcombos[pickstratidx])
            stratcombos.remove(stratcombos[pickstratidx])
        rungame(stratsset)

if __name__ == "__main__":
    wgt = False
    if len(sys.argv) > 1:
        numstrats = int(sys.argv[1])
    else:
        numstrats = 3
    tryallcombos(numstrats)

