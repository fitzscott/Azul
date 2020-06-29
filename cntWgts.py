import sys

if __name__ == "__main__":
    for ln in sys.stdin:
        wgts = ln.strip().split(",")
        twocnt = 0
        maxcnt = -1
        maxwgt = ""
        for wgt in wgts:
            w, val, cnt = wgt.split(":")
            if float(val) == 2.0:
                twocnt += 1
            if int(cnt) > maxcnt:
                maxcnt = int(cnt)
                maxwgt = w
        # print(str(len(ln.strip().split(","))))
        print(str(len(wgts)) + " (" + str(twocnt) + " 2s) max " + str(maxcnt) + " " + maxwgt)

