import PlayableColorStrategy as pcs
class CentralPositionStrategy(pcs.PlayableColorStrategy):
    """
    Rank positions toward the center of the board higher than those toward
    the periphery.
    """
    def evaluate(self, options, board, game = None):
        # Create a map from color & row number to a value
        import FinalBoardComponent as fbc
        import Strategy as strat

        crvals = {}
        pbrd = board.finalboard
        bcolors = pbrd.underrows
        for rownum in range(fbc.FinalBoardComponent.dimension):
            for columnnum in range(fbc.FinalBoardComponent.dimension):
                # 2,2 is the center => highest value
                crvals[(bcolors[rownum][columnnum], rownum)] = 4 - \
                    (abs(rownum - 2) + abs(columnnum - 2))

        evals = []
        for opt in options:
            dispnum = opt[0]
            for color in opt[2:]:
                if color == "1":
                    continue
                for rownum in range(fbc.FinalBoardComponent.dimension):
                    if board.prepboard.canplace(rownum, color) and \
                            not board.prepboard.rowfull(rownum):
                        evals.append(dispnum + color + str(rownum) + "_" + \
                                     str(crvals[(color, rownum)]))
        if len(evals) == 0:
            return (super().evaluate(options, board, game))

        evals.sort(key=strat.getcount)
        # print("Central position evals = "+ str(evals))
        return (evals)
