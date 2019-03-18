import MostPrevalentColorStrategy as mpcs

class CompleteColorStrategy(mpcs.MostPrevalentColorStrategy):
    """
    Seek to complete color sets - one instance of each color in
    each row (also column).
    """

    def evaluate(self, options, board, game = None):
        import FinalBoardComponent as fbc
        import Strategy

        colorcounts = {}
        totalcount = 0
        colcnt = [0 for _ in range(fbc.FinalBoardComponent.dimension)]
        for row in board.finalboard.rows:
            for color in row:
                if color != '-':
                    colorcounts[color] = colorcounts.get(color, 0) + 1
                    totalcount += 1
        if totalcount == 0:
            # print("Complete color found no evaluations")
            return(super().evaluate(options, board, game))
        rankedcolors = [(color, colorcounts[color])
                        for color in colorcounts.keys()
                        if colorcounts[color] !=
                        fbc.FinalBoardComponent.dimension]  # already full
        rankedcolors.sort(key=Strategy.getcounttup, reverse=True)

        evals = []
        prep = board.prepboard
        for rc in rankedcolors:
            color = rc[0]
            for opt in options:
                for optcolor in opt[2:]:
                    if optcolor == "-1":
                        continue
                    if optcolor == color:
                        for rownum in range(fbc.FinalBoardComponent.dimension):
                            if prep.canplace(rownum, color) and \
                                    not prep.rowfull(rownum):
                                move = opt[0] + color + str(rownum) + \
                                       "_" + str(rc[1])
                                evals.append(move)
        # print("Complete color strategy evals: " + str(evals))
        return (evals)

    # I don't think we need to override this
    # def recommend(self, options, board, game = None):
    #     pass
