import PlayableColorStrategy as pcs

class FillRowStrategy(pcs.PlayableColorStrategy):
    """
    FillRowStrategy - look for rows that are partially filled and concentrate
    on those.
    """
    def evaluate(self, options, board, game = None):
        import Strategy

        fillcounts = []
        totfillcounts = 0
        for idx in range(5):
            fcn = board.finalboard.rowfillcount(idx)
            totfillcounts += fcn
            fillcounts.append((idx, fcn))
        if totfillcounts == 0:      # no evaluations - bail out
            # print("FillRowStrategy found no options")
            return(super().evaluate(options, board, game))
        fillcounts.sort(key=Strategy.getcounttup, reverse=True)

        evals = []
        for fc in fillcounts:
            rownum = fc[0]
            for opt in options:
                # print("Checking fill count " + str(fc) + " against " + opt)
                # If the option is for the color available for the row in
                # the fill count, add it to the list.
                # remaining = board.finalboard.rowremainingcolors(fc[0])
                for color in opt[2:]:
                    if color == '1':
                        continue
                    # print("checking remaining " + remaining + " against " + color)
                    # had this (redundant): color in remaining and \
                    if board.prepboard.canplace(rownum, color) and not \
                            board.prepboard.rowfull(rownum):
                        # print("adding option " + opt + " for row " + str(rownum))
                        #print("    " + opt[0] + color + str(rownum) + "_" + str(fc[1]))
                        evals.append(opt[0] + color + str(rownum) + "_" + str(fc[1]))
        # print("Fill row evaluations: " + str(evals))
        return (evals)

    def recommend(self, options, board, game = None):
        evals = self.evaluate(options, board, game)
        if evals is None or len(evals) == 0:
            return(super().recommend(options, board, game))
        else:
            # print("FillRowStrategy chose " + evals[0])
            return (evals[0])
