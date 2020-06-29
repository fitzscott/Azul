import sys
import os

if __name__ == "__main__":
    print(" ".join(sys.argv))
    #sys.exit(-1)
    bsflnm = sys.argv[1].strip().split(".")[0]

    wfl = open("trwr_" + bsflnm + ".txt", "w")
    rfl = open(bsflnm + ".txt")
    for ln in rfl:
        strats, wgts = ln.strip().split("|")
        newrates = []
        for wgt in wgts.split(","):
            wt, rate, cnt = wgt.split(":")
            if len(rate) < 7:
                newrate = rate
            else:
                newrate = rate[0:7]
            newrates.append(":".join([wt, newrate, cnt]))
        wfl.write(strats + "|" + ",".join(newrates) + "\n")
    rfl.close()
    wfl.close()
