import sys
import os
import avflJ


def topvals(strats):
    # Read the values file. If the strategy set is present, use that weighting.
    # If not, let the agent use its default.
    valz = None
    vfnm = avflJ.agentvalzflnm(strats) + ".txt"
    print("Opening file " + vfnm)
    if os.path.exists(vfnm):
        valfl = open(vfnm)
        for ln in valfl:
            print("             Reading line")
            strat, wgts = ln.strip().split("|")
            valz = wgts.split(",")
            print("Number of value entries: " + str(len(valz)))
            bestwgt = ""
            hicntwgt = ""
            maxwr = -1.0
            maxcnt = -1
            twocnt = 0
            for val in valz:
                wgt, wr, c = val.split(":")
                winrt = float(wr)
                cnt = int(c)
                if maxwr < winrt:
                    maxwr = winrt
                    bestwgt = wgt
                if maxcnt < cnt:
                    maxcnt = cnt
                    hicntwgt = wgt
                if winrt == 2.0:
                    twocnt += 1
        print("Number of twos = " + str(twocnt))
        print("Best win rate = " + str(maxwr) + " for " + bestwgt)
        print("Highest count = " + str(maxcnt) + " for " + hicntwgt)
        valfl.close()
    return (valz)

if __name__ == "__main__":
    topvals(sys.argv[1])  # this will be delimited by + with no .txt, etc.
    # flnm = sys.argv[1]
    # wfl = open("fixt_" + flnm, "w")
    # rfl = open(flnm)
    # for ln in rfl:
    #     wfl.write(ln.strip())
    # wfl.write("\n")
    # wfl.close()
    # rfl.close()

