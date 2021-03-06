import sys
import random
import time
import Game as g
import ComboStrategyPlayer as csp
import BitComboStrategyPlayer as bcsp

def rungame(bitfield, beststrats=True):
    maxturns = 300
    maxrt = 60.0

    playme = g.Game(4)
    playme.loadtiles()
    plyrz = []
    bitplayer = random.randint(0, 3)
    for plnum in range(4):
        if plnum == bitplayer:
            plyr = bcsp.BitComboStrategyPlayer(playme, playme.playerboard[plnum],
                                               bitfield)
            plyr.assignstrats()
        else:
            plyr = csp.ComboStrategyPlayer(playme, playme.playerboard[plnum])
            if beststrats:
                plyr.randbeststrats()
            else:
                plyr.randstrats()
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
            currtime = time.time()
            rt = currtime - gamestart
            if rt > maxrt:
                print("No final score, bitfield " + str(bitfield) + " ran " + str(rt))
                return(-1)
    print(8 * "+" + "\t\tFinal scoring:")
    for idxnum in range(4):
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
        if plyridx == bitplayer:
            plstr = "[BitPlayer:" + str(bitfield) + "] "
        else:
            plstr = "[RandPlayer] "
        print(winstr + plstr + str(plyrz[plyridx]) + " final score = " + \
              str(plyrz[plyridx].board.score))

    if turnz == maxturns:
        retval = 1
    return (retval)

def tryallbitfields():
    twos = [1]
    for pos in range(len(csp.ComboStrategyPlayer.strats)-1):
        twos.append(2 * twos[pos])
    for bf in range(3, 4095):
        if bf not in twos:
            rungame(bf, False)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        bitfield = int(sys.argv[1])
        rungame(bitfield, False)
    # else:
    #     bitfield = 4 + 16 + 64 + 1024 + 2048
    # rungame(bitfield)
    else:
        tryallbitfields()
