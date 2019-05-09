import sys

gameno = 0
for line in sys.stdin:
    flds = line.strip().split()
    if len(flds) == 0:
        continue
    if flds[0] == "Summary":
        intgameno = flds[3]
        intsetno = flds[6]
        runtime = flds[10][0:-1]
        gameno += 1
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
    print("|".join([str(gameno), intgameno, intsetno, runtime, winflg, score,
                    permstr, combstr]))
