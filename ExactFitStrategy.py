import Strategy as strat

class ExactFitStrategy(strat.Strategy):
    """
    ExactFitStrategy
    Look for options that will fully fit the preparatory board (and of
    course be eligible for the final board.
    """

    # There is no ranking of exact fits - they're all the same.
    # When we combine strategies, though, we need to have some
    # weight to the strategy.  The strategy combinations prefer
    # higher rankings, so we should give it some number higher
    # than zero, certainly, but what should it be?
    # Changing this:  The weight will be the number of tiles placed.
    # defaultweight = 5

    # def __init__(self, defwgt=None):
    #     if defwgt is None:
    #         self._weight = ExactFitStrategy.defaultweight
    #     else:
    #         self._weight = defwgt

    def evaluate(self, options, board, game = None):
        exactfit = []
        slots = [board.prepboard.availableslots(row) for row in range(5)]
        for opt in options:
            dispnum = opt[0]
            colorcount = {}
            for color in opt[2:]:
                if color == "1":
                    continue
                colorcount[color] = colorcount.get(color, 0) + 1
            for ckey in colorcount.keys():  # ckey is color
                for slotidx in range(len(slots)):
                    if colorcount[ckey] == slots[slotidx] and \
                            board.prepboard.canplace(slotidx, ckey):
                        exactfit.append(dispnum + ckey + str(slotidx) + \
                                        "_" + str(colorcount[ckey]))
        return(exactfit)

    def recommend(self, options, board, game = None):
        evs = self.evaluate(options, board, game)
        if len(evs) > 0:
            return(evs[0])
        else:
            return(None)
