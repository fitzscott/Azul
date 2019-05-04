import sys
import random
import time
import itertools
import Game as g
import ComboStrategyPlayer as csp
import WeightedComboStrategyPlayer as wcsp

def rungame(stratsstrpermu, randorbest, gameno):
    maxturns = 300
    maxrt = 60.0

    plcnt = 4
    playme = g.Game(plcnt)
    playme.loadtiles()
    plyrz = []
    permplyr = random.randint(0, plcnt-1)
    for plnum in range(plcnt):
        if plnum == permplyr:
            plyr = wcsp.WeightedComboStrategyPlayer(playme,
                                                    playme.playerboard[plnum])
            for stratnm in stratsstrpermu:
                plyr.addstratbystr(stratnm)
            plyr.stdweight()
            print(plyr)
        else:
            plyr = csp.ComboStrategyPlayer(playme, playme.playerboard[plnum])
            if randorbest == "R":
                plyr.randstrats()
            else:
                plyr.randbeststrats("reallythebest75pct.txt")
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

def tryallpermus(stratstr, randorbest, numiters):
    stratstrlist = stratstr.strip().split(":")[0].split("+")
    if numiters == -1:
        permsiz = len(stratstrlist)
        if permsiz < 4:
            numiters = 100
        elif permsiz < 6:
            numiters = 40
        elif permsiz < 8:
            numiters = 20
        else:
            numiters = 10
    # Don't include all permutations at higher counts - too many.
    # We'll take top X & set the rest to weight 1.
    # Here, only get permutations for those top X, and we'll tack on the rest.
    wgtcnt = min(len(stratstrlist), wcsp.WeightedComboStrategyPlayer.maxwgtcnt)
    stratstrpermus = [stratstr for stratstr in
                      itertools.permutations(stratstrlist, wgtcnt)]
    for ssp in stratstrpermus:
        ssplist = [permu for permu in ssp]
        for stratstr in stratstrlist:
            if stratstr not in ssplist:
                ssplist.append(stratstr)
        for gameno in range(numiters):
            rungame(ssplist, randorbest, gameno)

if __name__ == "__main__":
    # Parameters:   Strategy combo we want to test for its permutations
    #               Whether we want to run against random or best combos
    #               Number of iterations - games to run per permutation
    #                   -1 => figure it out yourself
    if len(sys.argv) < 4:
        print("usage: " + sys.argv[0] + " combo Rand(R)orBest(B) iterations")
        sys.exit(-1)
    stratstr = sys.argv[1]
    randorbest = sys.argv[2].upper()
    numiters = int(sys.argv[3])
    tryallpermus(stratstr, randorbest, numiters)
