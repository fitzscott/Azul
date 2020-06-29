import sys
import os
import itertools


def isdupe(narr):
    retval = False
    max_wgt = 5
    for chk in range(max_wgt - 1):
        cnum = chk + 2
        multcnt = 0
        for n in narr:
            if int(n) % cnum == 0:
                multcnt += 1
        if multcnt == len(narr):
            print("Got multiple count " + str(multcnt) + " for " +
                  "".join([str(x) for x in narr]))
            retval = True
            break
    # print("Checked " + str(narr) + ", returned " + str(retval))
    return (retval)


if __name__ == "__main__":
    # print(" ".join(sys.argv))
    # isdupe("55555")
    # isdupe("24242")
    # isdupe("11111")
    # isdupe("12345")
    # isdupe("24241")
    # isdupe("12424")
    # isdupe("22222")
    # sys.exit(-1)
    flnm = sys.argv[1]

    rfl = open(flnm)
    for ln in rfl:
        strats, wgts = ln.strip().split("|")
        newrates = {}
        for wgt in wgts.split(","):
            wt, rate, cnt = wgt.split(":")
            newrates[wt] = (rate, cnt)
    rfl.close()
    siz = len(wt)
    rng = [n+1 for n in range(5)]
    # allcombos = itertools.combinations_with_replacement(rng, siz)
    # allcombos = itertools.permutations(rng, siz)
    allcombos = itertools.product(rng, repeat=siz)
    wfl = open("fild_" + flnm, "w")
    wfl.write(strats + "|")
    jnr = ""
    misdcnt = 0
    fndcnt = 0
    skpdcnt = 0
    allcnt = 0
    for comb in allcombos:
        scomb = "".join([str(c) for c in comb])
        # print("Checking "+ scomb)
        if isdupe(scomb):
            skpdcnt += 1
            continue
        if scomb not in newrates.keys():
            # print("Did not find " + scomb)
            rate = "2.0"
            cnt = "0"
            misdcnt += 1
        else:
            # print("Found " + scomb)
            rate = newrates[scomb][0]
            cnt = newrates[scomb][1]
            fndcnt += 1
        wfl.write(jnr + ":".join([scomb, rate, cnt]))
        allcnt += 1
        jnr = ","
    wfl.write("\n")
    wfl.close()
    print("count all combos = " + str(allcnt))
    print("count original rates = " + str(len(newrates)))
    print("missed, found, skipped = " + str(misdcnt) + ", " + str(fndcnt) + ", " + str(skpdcnt))
