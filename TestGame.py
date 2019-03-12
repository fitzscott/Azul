import sys
import Game as g

playme = g.Game(4)
playme.loadtiles()
playme.show()
cont = True
firstplayer = 0
while cont:
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
                playme.loadtiles()
                playme.show()
            break
        print("Player " + str(plnum+1) + " choose Display Color Row")
        print(" ".join(playme.options()))
        opts = sys.stdin.readline().strip()
        dispnum = int(opts[0])
        # print("factor display chosen is " + str(dispnum))
        if dispnum == -2:
            cont = False
            break
        color = opts[1].upper()
        # print("color chosen is " + color)
        rownum = int(opts[2]) - 1
        # print("row # chosen is " + str(rownum))
        if dispnum == 0:
            tileset = playme.centralarea.takecolor(color)
        else:
            tileset = playme.display[dispnum-1].takecolor(color, playme.centralarea)
        playme.playerboard[plnum].playtiles(rownum, tileset)
        playme.show()
print("Final scoring here")
for idxnum in range(4):
    playme.playerboard[idxnum].finalscore()
playme.show()
