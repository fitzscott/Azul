import PlayableColorStrategy as pcs

class DisplayHighColorStrategy(pcs.PlayableColorStrategy):
    """
    From the available displays, choose one with the highest count of a
    single color.
    """

    def evaluate(self, options, board, game = None):
        import Strategy

        displaycolorcounts = {}

        for opt in options:
            display = opt[0]
            for color in opt[2:]:
                if color == "1":
                    continue
                displaycolorcounts[(display, color)] = \
                    displaycolorcounts.get((display, color), 0) + 1
        if len(displaycolorcounts) == 0:
            return (super().evaluate(options, board, game))

        e1 = [(dispcolorkey, displaycolorcounts[dispcolorkey])
                 for dispcolorkey in displaycolorcounts.keys()]
        e1.sort(key=Strategy.getcounttup, reverse=True)
        prep = board.prepboard
        evals = []
        for ev in e1:
            display = ev[0][0]
            color = ev[0][1]
            score = ev[1]
            for rownum in range(len(prep.rows)):
                if prep.canplace(rownum, color) and not prep.rowfull(rownum):
                    evals.append(display + color + str(rownum) + \
                                 "_" + str(score))
        # print("Display high counts evals " + str(evals))
        return (evals)
