import Strategy as strat


class PlayableColorStrategy(strat.Strategy):
    """
    PlayableColorStrategy - look at the options and return a list of ones that
    will be playable.
    """
    def getplayable(self, options, board, game = None):
        playable = []

        prepboard = board.prepboard
        for opt in options:
            num = opt[0]
            for rownum in range(5):
                for color in opt[2:]:
                    if color == '1':
                        continue
                    if not prepboard.rowfull(rownum) and \
                            prepboard.canplace(rownum, color):
                        playable.append(num + color + str(rownum))
        return (playable)

    def evaluate(self, options, board, game = None):
        evcounts = {}
        evals = self.getplayable(options, board)
        for ev in evals:
            evcounts[ev] = evcounts.get(ev, 0) + 1
        evlist = [key + "_" + str(evcounts[key]) for key in evcounts.keys()]
        evlist.sort(key=strat.getcount)
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
    pcs = PlayableColorStrategy()
    # evals = pcs.evaluate(opts, zboard)
    # print(evals)
    evc = pcs.recommend(opts, zboard)
    print(evc)
