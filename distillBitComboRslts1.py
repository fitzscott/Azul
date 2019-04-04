import sys

gamenum = 0
maxscore = 0
rslts = []
plyrnum = 0

def outputresults(rslts):
    for result in rslts:
        if int(result[2]) == maxscore:
            win = "1"
        else:
            win = "0"
        print("|".join([str(gamenum), str(result[0]), result[1], \
                        str(result[2]), win, result[3]]))

if len(sys.argv) == 2:
    gamenum = int(sys.argv[1])

for line in sys.stdin:
    # print("line is " + line)
    flds = line.strip().split()
    # print("fields are: " + ":".join(flds))
    if len(flds) == 0:  # ?
        continue
    if flds[0] == "Summary":
        # output goes here
        if len(rslts) == 0:
            continue
        outputresults(rslts)
        gamenum += 1
        maxscore = 0
        rslts = []
        plyrnum = 0
        continue
    elif "ComboStrategyPlayer:" in flds[2]:
        score = flds[-1]
        plyrnum += 1
        if "Rand" in flds[1]:
            bitflg = "0"
        else:
            bitflg = "1"
        # print("    score is " + score)
        maxscore = max(maxscore, int(score))
        for strat in flds[3:-4]:    # end of range not inclusive
            rslts.append((plyrnum, strat, score, bitflg))

outputresults(rslts)
