import PlayableColorStrategy as pcs

class AtMostFitStrategy(pcs.PlayableColorStrategy):
    """
    AtMostFitStrategy
    Look for options that will fully fit the preparatory board (and of
    course be eligible for the final board.
    """

    defaultweight = 5

    def evaluate(self, options, board, game = None):
        import Strategy

        atmostfit = []
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
                    if colorcount[ckey] <= slots[slotidx] and \
                            board.prepboard.canplace(slotidx, ckey):
                        atmostfit.append(dispnum + ckey + str(slotidx) + \
                                        "_" + str(colorcount[ckey]))
        if len(atmostfit) == 0:
            return (super().evaluate(options, board, game))
        atmostfit.sort(key=Strategy.getcount2, reverse=True)
        # print("At most fit evals: " + str(atmostfit))
        return(atmostfit)

    def recommend(self, options, board, game = None):
        evs = self.evaluate(options, board, game)
        if len(evs) > 0:
            return(evs[0])
        else:
            return(None)
