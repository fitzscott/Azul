import sys
import os

dirpath = r"C:/Users/Fitzs/PycharmProjects/Azul/"
# flnmpat = "tbcg_"
flnmpat = "x9"

def outputrec(ts, gn, wl, strats, scor):
    print("|".join([ts, str(gn), strats, scor, wl]))

flnms = [flnm for flnm in os.listdir(dirpath)
         if flnmpat == flnm[0:len(flnmpat)]]

for flnm in flnms:
    # print("opening " + flnm + " in " + dirpath)
    fl = open(dirpath + flnm)
    testset = flnm.split("_")[1].split(".")[0]
    gameno = 0

    stratsstr = ""
    win = ""
    score = ""
    for line in fl:
        # print("line is " + line)
        flds = line.strip().split()
        if len(flds) == 0 or flds[0][-1] != ":":
            continue
        # print("processing fields " + str(flds))
        if flds[0] == "Loser:":
            win = "0"
        elif flds[0] == "Winner:":
            win = "1"
        else:
            continue
        stratsstr = "+".join(flds[2:-4])
        score = flds[-1]
        outputrec(testset, gameno, win, stratsstr, score)
        gameno += 1
    fl.close()
    # outputrec(testset, gameno, win, stratsstr, score)
