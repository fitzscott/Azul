import Strategy as strat


class FinishUnfinishedStrategy(strat.Strategy):
    """
    FinishUnfinishedStrategy - look at the options and return a list of ones that
    will be playable.
    """
    defaultweight = 5

    def __init__(self, defwgt=None):
        if defwgt is None:
            self._weight = FinishUnfinishedStrategy.defaultweight
        else:
            self._weight = defwgt

    def getplayable(self, options, board, game = None):
        playable = []

        prepboard = board.prepboard
        for opt in options:
            num = opt[0]
            for rownum in range(5):
                for color in opt[2:]:
                    if color == '1':
                        continue
                    # print("Checking color " + color + " vs. row " + str(prepboard.rows[rownum]))
                    if not prepboard.rowfull(rownum) and \
                            prepboard.canplace(rownum, color) and \
                            color in prepboard.rows[rownum]:
                        playable.append(num + color + str(rownum))
        return (playable)

    def evaluate(self, options, board, game = None):
        evcounts = {}
        evals = self.getplayable(options, board)
        for ev in evals:
            evcounts[ev] = evcounts.get(ev, 0) + 1
        maxev = -1
        for evk in evcounts.keys():
            maxev = max(maxev, evcounts[evk])
        maxev += self._weight
        # Reverse the ordering to favor high rankings.  This will make
        # combining strategies easier later.
        evlist = [key + "_" + str(maxev - evcounts[key]) for key in evcounts.keys()]
        evlist.sort(key=strat.getcount2)
        return(evlist)

    def recommend(self, options, board, game = None):
        recommendations = self.evaluate(options, board, game)
        if len(recommendations) > 0:
            rec = recommendations[0]
        else:
            rec = None
        return(rec)

if __name__ == "__main__":
    import Game as gg

    game = gg.Game()
    game.loadtiles()
    zboard = game.playerboard[0]
    opts = game.options()
    fus = FinishUnfinishedStrategy()
    evals = fus.evaluate(opts, zboard)
    print(evals)
    # evc = fus.recommend(opts, zboard)
    # print(evc)
