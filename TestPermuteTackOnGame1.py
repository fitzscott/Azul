import sys
import random
import time
import itertools
import Game as g
import ComboStrategyPlayer as csp
import WeightedComboStrategyPlayer as wcsp

def rungame(stratsstrpermu, newstratstr, gameno):
    maxturns = 300
    maxrt = 60.0

    plcnt = 4
    playme = g.Game(plcnt)
    playme.loadtiles()
    plyrz = []
    newplyr = random.randint(0, plcnt-1)
    for plnum in range(plcnt):
        plyr = wcsp.WeightedComboStrategyPlayer(playme,
                                                playme.playerboard[plnum])
        for stratnm in stratsstrpermu[plnum]:
            plyr.addstratbystr(stratnm)
        if plnum == newplyr:
            for stratstr in newstratstr.split("+"):
                plyr.addstratbystr(stratstr)
        plyr.stdweight()
        print(plyr)
        print("Player " + str(plnum) + ": " + str(plyr))
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

def tackongames(stratstr, iters, flnm):
    # Get the list of weighted strategy combinations to use.
    wgtfile = open(flnm)
    wgtcombos = wgtfile.readlines()
    wgtfile.close()
    fullwgtset = [wc.strip().split(":")[0].split("+")
                  for wc in wgtcombos
                  if len(wc) > 0 and stratstr not in wc]
    print("full set of weighted straetegies:\n" + str(fullwgtset))
    for gameno in range(iters):
        stratsset = []
        for plrnum in range(4):
            choice = random.randint(0, len(fullwgtset)-1)
            stratsset.append(fullwgtset[choice])    # Duplicates are ok
        rungame(stratsset, stratstr, gameno)


if __name__ == "__main__":
    # Parameters:   Strategy combo we want to test for its permutations
    #               Whether we want to run against random or best combos
    #               Number of iterations - games to run per permutation
    #                   -1 => figure it out yourself
    if len(sys.argv) < 3:
        print("usage: " + sys.argv[0] + " strategy iterations [strategyFile]")
        sys.exit(-1)
    stratstr = sys.argv[1]
    iters = int(sys.argv[2])
    if len(sys.argv) > 3:
        flnm = sys.argv[3]
    else:
        flnm = "bestwgtd01.txt"
    tackongames(stratstr, iters, flnm)
