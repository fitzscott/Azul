import PlayableColorStrategy as pcs

class MinPenaltyStrategy(pcs.PlayableColorStrategy):
    """
    Score moves that result in a penalty low
    """
    def evaluate(self, options, board, game = None):
        import Strategy
        import Penalty

        prep = board.prepboard
        pen = board.penalty

        negpen = []
        for opt in options:
            disp = opt[0]
            # count the number of each color in the option
            colorcounts = {}
            firstplayerpenalty = 0
            for color in opt[2:]:
                if color == '1':
                    firstplayerpenalty = 1
                    continue
                colorcounts[color] = colorcounts.get(color, 0) + 1
            for rownum in range(len(prep.rows)):
                slots = prep.availableslots(rownum)
                for color in colorcounts.keys():
                    if prep.canplace(rownum, color):
                        # All moves without penalty are ranked the same.
                        penaltycnt = min(slots - colorcounts[color], 0) - \
                                     firstplayerpenalty
                        # Keeping the penalty negative for now
                        penalty = -1 * pen.projectpenalty(-1 * penaltycnt)
                        negpen.append((disp + color + str(rownum), penalty))
        # print("negative penalties = " + str(negpen))
        if len(negpen) == 0:
            return (super().evaluate(options, board, game))

        maxpenalty = 0
        for ev in negpen:
            maxpenalty = min(maxpenalty, ev[1])
        # print("max penalty is " + str(maxpenalty))
        negpen.sort(key=Strategy.getcounttup, reverse=True)
        evals = [np[0] + "_" +  str(-1 * maxpenalty + np[1]) for np in negpen]
        # print("Min penalty " + str(evals))
        return (evals)
