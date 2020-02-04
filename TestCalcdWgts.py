import sys
import random
import time
import Game as g
import WeightedComboStrategyPlayer as wcsp
import WeightAgent as wa


def rungame(plyrz, plcnt, playme, itr, gameno):
    maxturns = 300
    maxrt = 60.0

    # playme.show()
    cont = True
    firstplayer = 0
    turnz = 0
    retval = [0]
    # while cont:
    gamestart = time.time()
    while cont and turnz < maxturns:  # real games rarely go past 5
        for idxnum in range(plcnt):
            plnum = (firstplayer + idxnum) % plcnt
            if playme.turnover():  # dispnum == 9:
                # cont = False
                for plnum in range(plcnt):
                    playme.playerboard[plnum].movescore(playme.box)
                    if playme.playerboard[plnum].firstplayer:
                        firstplayer = plnum
                        playme.playerboard[plnum].firstplayer = False
                    if playme.playerboard[plnum].finalboard.horizrowcomplete():
                        cont = False
                if cont:
                    # print("\t  " + 8 * "+" + " turn " + str(turnz + 1) + " next")
                    if not playme.loadtiles():
                        cont = False
                        retval = [-1]
                        break
                    # playme.show()
                break
            # print("Player " + str(plnum + 1) + " turn:")
            plyrz[plnum].taketurn()
            # playme.show()
            turnz += 1
            currtime = time.time()
            rt = currtime - gamestart
            if rt > maxrt:
                print("No final score, ran " + str(rt))
                retval = [-1]
                turnz = maxturns
                break
    # print(8 * "+" + "\t\tFinal scoring:")
    for idxnum in range(plcnt):
        playme.playerboard[idxnum].finalscore()
    # playme.show()
    currtime = time.time()
    rt = currtime - gamestart
    winrarr = playme.winner()

    if turnz == maxturns:
        retval = [-1]
    else:
        retval = winrarr
    return (retval)


def runXiters(strats, iters, teststrats, wgts=None):
    trimdstrats = [strat.split(":")[0] for strat in strats]
    plyrwgtcombos = strats      # Unnecessary, but it calms the code a little
    plcnt = 4
    totscor = 0
    placesum = 0
    gamecnt = 0
    placecnt = [0, 0, 0, 0]

    for itr in range(iters):
        # Set up the game.  Ideally, we wouldn't do this every time,
        # but fixing it would mean tweaking a bunch of older code.
        # Add to the to-do list.
        playme = g.Game(plcnt)
        playme.loadtiles()
        plyrz = []
        testplnum = random.randint(0, 3)
        for plnum in range(plcnt):
            plyr = wcsp.WeightedComboStrategyPlayer(playme,
                                                    playme.playerboard[plnum])
            if plnum != testplnum:
                stratidx = random.randint(0, len(plyrwgtcombos)-1)
                for stratstr in plyrwgtcombos[stratidx].split("+"):
                    plyr.addstratbystr(stratstr)
                plyr.stdweight()
            else:
                for stratstr in teststrats.split("+"):
                    plyr.addstratbystr(stratstr)
                plyr.weights = [int(str(wgts)[x]) for x in range(len(str(wgts)))]
            # print(plyr)
            plyrz.append(plyr)
        # print(agent)
        wnrz = rungame(plyrz, plcnt, playme, itr, itr + 1)
        # print(str(playme.playerranks))
        ranks = playme.playerranks
        for ridx in range(len(ranks)):
            if testplnum == ranks[ridx][0]:    # 0 is its rank
                scor = ranks[ridx][1]          # 1 is its score
                # print("Test player scored " + str(scor) + " and placed # " + str(4 - ridx))
                totscor += scor
                placesum += 4 - ridx
                placecnt[3 - ridx] += 1
                gamecnt += 1
                break

    print("    Avg score = " + str(float(totscor) / float(gamecnt)))
    print("    Avg rank  = " + str(float(placesum) / float(gamecnt)))
    print("    Place counts = " + "\t".join([str(p) for p in placecnt]))
    print("    Percentages  = " + "\t".join([str(float(pc) / float(gamecnt) * 100)[:5] for pc in placecnt]))

def pickstrats(stratfile, iters, teststrats=None, wgts=None):
    pickcount = 0
    stratsets = []
    # First, get the list of weighted strategy combinations to use.
    wgtfile = open(stratfile)
    wgtcombos = wgtfile.readlines()
    wgtfile.close()
    fullwgtset = [wc.strip().split(":")[0]
                  for wc in wgtcombos
                  if len(wc) > 0]
    runXiters(fullwgtset, iters, teststrats, wgts)


if __name__ == "__main__":
    stratfile = sys.argv[1]
    iters = int(sys.argv[2])
    if len(sys.argv) > 3:
        strats = sys.argv[3]
    else:
        strats = None
    if len(sys.argv) > 4:
        wgts = int(sys.argv[4])
    else:
        wgts = None
    pickstrats(stratfile, iters, strats, wgts)
