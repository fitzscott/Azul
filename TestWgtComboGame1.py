import sys
import random
import time
import Game as g
import WeightedComboStrategyPlayer as wcsp

def rungame(plyrwgtcombos, itr, gameno):
    maxturns = 300
    maxrt = 60.0

    plcnt = len(plyrwgtcombos)
    playme = g.Game(plcnt)
    playme.loadtiles()
    plyrz = []
    for plnum in range(plcnt):
        plyr = wcsp.WeightedComboStrategyPlayer(playme, playme.playerboard[plnum])
        for stratstr in plyrwgtcombos[plnum].split("+"):
            plyr.addstratbystr(stratstr)
        plyr.stdweight()
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
    print("\nSummary of game " + str(gameno) + " in set " + str(itr) +
          " - run time " + str(rt) + ", final scores:")
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

def runXiters(flnm, iters):
    # First, get the list of weighted strategy combinations to use.
    wgtfile = open(flnm)
    wgtcombos = wgtfile.readlines()
    wgtfile.close()
    # For each iteration, run all the listed combinations.
    for itr in range(iters):
        fullwgtset = [wc.strip().split(":")[0]
                      for wc in wgtcombos
                      if len(wc) > 0]
        # Then, for each game, pick a set of at most 4 combos to use,
        # and run the game with them.  Reduce the set of available
        # combinations accordingly.
        gameno = 1
        while len(fullwgtset) > 0:
            plyrcombos = []
            for plcnt in range(min(4, len(fullwgtset))):
                pickidx = random.randint(0, len(fullwgtset)-1)
                plyrcombos.append(fullwgtset[pickidx])
                fullwgtset.remove(fullwgtset[pickidx])
            rungame(plyrcombos, itr, gameno)
            gameno += 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        iters = int(sys.argv[1])
    else:
        iters = 1
    if len(sys.argv) > 2:
        flnm = sys.argv[2]
    else:
        flnm = "wgtset01w.txt"
    runXiters(flnm, iters)
