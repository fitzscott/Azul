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

def runXiters(strats, iters):
    trimdstrats = [strat.split(":")[0] for strat in strats]
    for itr in range(iters):
        rungame(strats, itr, itr+1)

def pickstrats(filecount, iters):
    pickcount = 0
    stratsets = []
    for ss in range(filecount):
        fl = open("bestwgtd0" + str(ss+1) + ".txt")
        strats = [oneset.strip() for oneset in fl.readlines()]
        stratsets.append(strats)
        fl.close()
    pickedstrats = []
    while pickcount < 4:
        pickedfile = random.randint(0, filecount-1)
        pickedstratidx = random.randint(0, len(stratsets[pickedfile])-1)
        pickedstrats.append(stratsets[pickedfile][pickedstratidx])
        pickcount += 1
    runXiters(pickedstrats, iters)
        
if __name__ == "__main__":
    # if len(sys.argv) < 6:
    #     print("usage: " + sys.argv[0] + " iterations combo1 c2 c3 c4")
    #     sys.exit(-1)
    iters = int(sys.argv[1])
    # strats = sys.argv[2:5]
    # runXiters(strats, iters)
    pickstrats(4, iters)
