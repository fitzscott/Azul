import sys
import os

if __name__ == "__main__":
    print(" ".join(sys.argv))
    sys.exit(-1)
    bsflnm = sys.argv[1].strip().split(".")[0]

    wfl = open("new_" + bsflnm + ".txt", "w")
    rfl = open(bsflnm + ".txt")
    for ln in rfl:
        strats, wgts = ln.strip().split("|")
        newwgts = []
        for wgt in wgts.split(","):
            wt, rate, cnt = wgt.split(":")
            newwgts.append(":".join([wt, rate, "1"]))
        wfl.write(strats + "|" + ",".join(newwgts))
    rfl.close()
    wfl.close()
