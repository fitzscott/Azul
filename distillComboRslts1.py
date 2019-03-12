import sys

gamenum = 0
maxscore = 0
rslts = []

def outputresults(rslts):
    for result in rslts:
        if int(result[1]) == maxscore:
            win = "1"
        else:
            win = "0"
        print("|".join([str(gamenum), result[0], str(result[1]), win]))

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
        continue
    elif flds[0] == "ComboStrategyPlayer:":
        score = flds[-1]
        # print("    score is " + score)
        maxscore = max(maxscore, int(score))
        for strat in flds[1:-4]:    # end of range not inclusive
            rslts.append((strat, score))

outputresults(rslts)
