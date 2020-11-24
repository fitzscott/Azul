import itertools as it

def adjust(wgt, adj):
    # print("".join(adj))
    adj = [wgt[i] + int(adj[i]) - 1 for i in range(len(wgt))]
    return (adj)

def inrange(ref, amin, amax):
    retval = True
    for r in ref:
        if r < amin or r > amax:
            retval = False
            break
    return (retval)

def chkdupes(narr, amax):
    retval = False
    for chk in range(amax - 1):
        cnum = chk + 2
        multcnt = 0
        for n in narr:
            if int(n) % cnum == 0:
                multcnt += 1
        if multcnt == len(narr):
            retval = True
            break
    return (retval)

def refine(wgt, amax=5, amin=1):
    wgtints = [int(w) for w in wgt]
    adjs = it.product("012", repeat=len(wgtints))
    refinments = [adjust(wgtints, a) for a in adjs]
    retrefs = [r for r in refinments if inrange(r, amin, amax)
               and not chkdupes(r, amax)]
    for r in retrefs:
        print("".join(str(r)))
    return (retrefs)

if __name__ == "__main__":
    refine("133513")
