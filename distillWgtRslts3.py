# We will receive whether a given permutation won or lost.  We will produce
# that plus its associated combination (the strategies ordered alphabetically).
import sys

setno = ""
gameno = ""
runtime = ""
plnum = 1

for line in sys.stdin:
    flds = line.strip().split()
    if len(flds) == 0:
        continue
    if flds[0] == "Summary":
        gameno = flds[3]
        setno = flds[6]
        runtime = flds[10][:-1]
        plnum = 1
        continue
    if flds[0] == "Winner:":
        winflg = "1"
    else:
        winflg = "0"
    score = flds[-1]
    stratlist = flds[2:-4]
    permstr = "+".join(stratlist)
    stratlist.sort()
    combstr = "+".join(stratlist)
    print("|".join([setno, gameno, str(plnum), runtime, winflg, score,
                    permstr, combstr]))
    plnum += 1
