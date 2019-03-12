import PlayableColorStrategy as pcs

def getcounttup(ev):
    return (ev[1])

class FillColumnStrategy(pcs.PlayableColorStrategy):
    """
    FillColumnStrategy - look for rows that are partially filled and concentrate
    on those.
    """
    def evaluate(self, options, board, game = None):
        fillcounts = []
        totfillcounts = 0
        for idx in range(5):
            fcn = board.finalboard.columnfillcount(idx)
            if fcn == 5:     # column is full
                continue
            totfillcounts += fcn
            fillcounts.append((idx, fcn))
        if totfillcounts == 0:      # no evaluations - bail out
            # print("FillColumnStrategy found no options")
            return(super().evaluate(options, board, game))
        fillcounts.sort(key=getcounttup, reverse=True)

        evals = []
        fnlbrd = board.finalboard
        # print("Fill column counts " + str(fillcounts))
        for fc in fillcounts:
            for opt in options:
                # print("considering select option " + opt)
                columnnum = fc[0]
                colorstofill = fnlbrd.columnremainingcolors(columnnum)
                # print("remaining colors for " + str(columnnum) + " are " + colorstofill)
                for color in opt[2:]:
                    if color == '1':
                        continue
                    if color in colorstofill:
                        rownum = fnlbrd.getrownum(columnnum, color)
                        if board.prepboard.canplace(rownum, color) and not \
                                board.prepboard.rowfull(rownum):
                            evals.append(opt[0] + color + str(rownum) + "_" + str(fc[1]))
        return (evals)

    def recommend(self, options, board, game = None):
        evals = self.evaluate(options, board, game)
        # print("Fill column evals = " + str(evals))
        if evals is None or len(evals) == 0:
            return(super().recommend(options, board, game))
        else:
            print("FillColumnStrategy chose " + evals[0])
            return (evals[0])
