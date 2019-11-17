import Strategy as strat

class MessWithStrategy(strat.Strategy):
    """
    MessWithStrategy - look for the playable color options for the other
    players and rank them higher.
    """
    def __init__(self):
        self._otherboards = []
        self._otherstrats = []

    def getplayable(self, options, board, game = None):
        import PlayableColorStrategy as pcs

        # See if we have the other boards yet
        if len(self._otherboards) == 0:
            for opboard in game.playerboard:
                if opboard != board:
                    self._otherboards.append(opboard)
                    self._otherstrats.append(pcs.PlayableColorStrategy())
        othercolors = {}
        for opbidx in range(len(self._otherboards)):
            ostrat = self._otherstrats[opbidx]
            oboard = self._otherboards[opbidx]
            ocolors = []
            for oplay in ostrat.getplayable(options, oboard, game):
                ocolor = oplay[1]
                if ocolor != '1' and ocolor not in ocolors:
                    ocolors.append(ocolor)
            for oc in ocolors:
                othercolors[oc] = othercolors.get(oc, 0) + 1
        # print("othercolors = " + str(othercolors))
        mincolorcount = 20
        for colkey in othercolors.keys():
            mincolorcount = min(mincolorcount, othercolors[colkey])
        # print("Min color count = " + str(mincolorcount))
        playable = []
        for opt in options:
            for color in opt[2:]:
                if color == '1':
                    continue
                if color in othercolors:
                    num = opt[0]
                    # We don't care whether we can place this color.  All that
                    # matters is whether other players can.
                    for rownum in range(5):
                        ranking = othercolors[color] - mincolorcount + 1
                        playable.append(num + color + str(rownum) + "_" + \
                                        str(ranking))
        return (playable)

    def evaluate(self, options, board, game = None):
        evcounts = {}
        evals = self.getplayable(options, board, game)
        evals.sort(key=strat.getcount2, reverse=True)
        # print("MessWith evals = " + str(evals))
        return(evals)

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
    pcs = MessWithStrategy()
    # evals = pcs.evaluate(opts, zboard)
    # print(evals)
    evc = pcs.recommend(opts, zboard, game)
    print(evc)
