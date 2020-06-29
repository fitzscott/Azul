import sys
import os

def agentvalzflnm(strats):
    return("agentvalz_" + "_".join(strats.split("+")))


def readvalue(strats):
    # Read the values file. If the strategy set is present, use that weighting.
    # If not, let the agent use its default.
    valz = None
    vfnm = agentvalzflnm(strats) + ".txt"
    print("Opening file " + vfnm)
    if os.path.exists(vfnm):
        valfl = open(vfnm)
        for ln in valfl:
            print("             Reading line")
            strat, wgts = ln.strip().split("|")
            print("Strategy set: " + strat)
            if strat == strats:
                valz = wgts.split(",")
                print("Number of value entries: " + str(len(valz)))
            # read through the rest of the file, even if the strategy set is
            # found, since we'll just append new results to the end of it.
        valfl.close()
        # print("Read weight values: " + str(valz))
    return (valz)

if __name__ == "__main__":
    readvalue(sys.argv[1])  # this will be delimited by + with no .txt, etc.
    # flnm = sys.argv[1]
    # wfl = open("fixt_" + flnm, "w")
    # rfl = open(flnm)
    # for ln in rfl:
    #     wfl.write(ln.strip())
    # wfl.write("\n")
    # wfl.close()
    # rfl.close()

