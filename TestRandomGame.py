import sys
import Game as g
import ComputerPlayer as cp

def rungame():
    """
    Random AF
    :return:
    """
    maxturns = 300

    playme = g.Game(4)
    playme.loadtiles()
    plyrz = []
    for plnum in range(4):
        plyrz.append(cp.ComputerPlayer(playme, playme.playerboard[plnum]))
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
                    print("    next turn")
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
    print("Final scoring here")
    for idxnum in range(4):
        playme.playerboard[idxnum].finalscore()
    playme.show()
    if turnz == maxturns:
        retval = 1
    return (retval)

if __name__ == "__main__":
    rungame()
