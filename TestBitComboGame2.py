import sys
import random
import time
import Game as g
import ComboStrategyPlayer as csp
import BitComboStrategyPlayer as bcsp

def rungame(bitfields):
    maxturns = 300
    maxrt = 60.0

    plcnt = len(bitfields)
    playme = g.Game(plcnt)
    playme.loadtiles()
    plyrz = []
    for plnum in range(plcnt):
        plyr = bcsp.BitComboStrategyPlayer(playme, playme.playerboard[plnum],
                                           bitfields[plnum])
        plyr.assignstrats()
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
                print("No final score, bitfield " + str(bitfields[plnum]) +
                      " ran " + str(rt))
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
        plstr = "[BitPlayer:" + str(bitfields[plyridx]) + "] "
        print(winstr + plstr + str(plyrz[plyridx]) + " final score = " + \
              str(plyrz[plyridx].board.score))

    if turnz == maxturns:
        retval = 1
    return (retval)

def tryallbitfields():
    twos = [1]
    for pos in range(len(csp.ComboStrategyPlayer.strats)-1):
        twos.append(2 * twos[pos])
    legitbits = [bf for bf in range(3, 4095)
                 if bf not in twos]
    while len(legitbits) > 1:
        plyrbits = []
        for plcnt in range(min(4, len(legitbits))):
            pickbitidx = random.randint(0, len(legitbits)-1)
            plyrbits.append(legitbits[pickbitidx])
            legitbits.remove(legitbits[pickbitidx])
        rungame(plyrbits)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        iters = int(sys.argv[1])
    else:
        iters = 1
    for runz in range(iters):
        tryallbitfields()
