import sys
import refineWeight as rw

def refdFile(strats, wgt, mx=5, mn=1):
    print("processing strategies " + strats)
    print("getting weight refinements for " + str(wgt))
    unm = "_".join(strats.split("+"))
    flnm = "refd_agentvalz_" + unm + ".txt"
    allwgts = rw.refine(wgt, mx, mn)
    print("all weights are" + str(allwgts))
    fl = open(flnm, "w")
    fl.write(strats + "|")
    rarr = []
    for rwgt in allwgts:
        rwgtstr = "".join([str(r) for r in rwgt])
        rarr.append(rwgtstr + ":2.0:0")
    fl.write(",".join(rarr))
    fl.write("\n")
    fl.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: {0} plusDelimdStrats weight".format(sys.argv[0]))
        sys.exit(-1)
    if len(sys.argv) > 3:
        mx = int(sys.argv[3])
    else:
        mx = 5

    refdFile(sys.argv[1], sys.argv[2], mx)
