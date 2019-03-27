import sys
import os

dirpath = "Data"
flnmpat = "tbcg_"
# flnmpat = "x9"

def outputrec(ts, gn, pln, wl, strats, scor):
    print("|".join([ts, str(gn), str(pln), strats, scor, wl]))

flnms = [flnm for flnm in os.listdir(dirpath)
         if flnmpat == flnm[0:len(flnmpat)]]

for flnm in flnms:
    # print("opening " + flnm + " in " + dirpath)
    fl = open(dirpath + "/" + flnm)
    testset = flnm.split("_")[1].split(".")[0]
    gameno = 0

    stratsstr = ""
    win = ""
    score = ""
    plnum = 0
    for line in fl:
        # print("line is " + line)
        flds = line.strip().split()
        if flds[0] == "Summary":
            gameno += 1
            plnum = 0
        if len(flds) == 0 or flds[0][-1] != ":":
            continue
        # print("processing fields " + str(flds))
        plnum += 1
        if flds[0] == "Loser:":
            win = "0"
        elif flds[0] == "Winner:":
            win = "1"
        else:
            continue
        stratsstr = "+".join(flds[2:-4])
        score = flds[-1]
        outputrec(testset, gameno, plnum, win, stratsstr, score)
    fl.close()
    # outputrec(testset, gameno, win, stratsstr, score)
