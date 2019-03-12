import sys
import random
import Game as g
import PlayableColorPlayer as pcp
import FinishUnfinishedPlayer as fup
import MostPrevalentColorPlayer as mpcp

def rungame():
    """
    Very basic strategy - just play what will stick to the board
    :return:
    """
    maxturns = 300

    playme = g.Game(4)
    playme.loadtiles()
    plyrz = []
    for plnum in range(4):
        sel = random.randint(1,4)
        if  sel < 3:
            plyrz.append(pcp.PlayableColorPlayer(playme, playme.playerboard[plnum]))
            print("player " + str(plnum + 1) + " is PlayableColorPlayer")
        elif sel < 4:
            plyrz.append(mpcp.MostPrevalentColorPlayer(playme, playme.playerboard[plnum]))
            print("player " + str(plnum+1) + " is MostPrevalentColorPlayer")
        else:
            plyrz.append(fup.FinishUnfinishedPlayer(playme, playme.playerboard[plnum]))
            print("player " + str(plnum+1) + " is FinishUnfinishedPlayer")
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
    if turnz == maxturns:
        retval = 1
    return (retval)

if __name__ == "__main__":
    rungame()
