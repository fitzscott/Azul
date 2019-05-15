import sys
import random
import Game as g
# import SingleStrategyPlayer as ssp
import ComboStrategyPlayer as csp

def rungame(minstrats=2, maxstrats=6):
    maxturns = 300

    playme = g.Game(4)
    playme.loadtiles()
    plyrz = []
    for plnum in range(4):
        plyr = csp.ComboStrategyPlayer(playme, playme.playerboard[plnum])
        # need at least 2 strategies
        plyr.randstrats(minstrats, maxstrats)
        print(plyr)
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

if __name__ == "__main__":
    if len(sys.argv) == 3:
        mncnt = int(sys.argv[1])
        mxcnt = int(sys.argv[2])
        rungame(mncnt, mxcnt)
    else:
        rungame()
