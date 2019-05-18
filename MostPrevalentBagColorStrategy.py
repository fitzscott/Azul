import Strategy as strat
import PlayableColorStrategy as pcs

class MostPrevalentBagColorStrategy(pcs.PlayableColorStrategy):
    """
    MostPrevalentBagColorStrategy - choose the color that is most prevalent on
    the whole board.  Temper it with the PlayableColorStrategy.
    """

    def evaluate(self, options, board, game = None):
        # get the set of evaluations from the parent
        playlist = super().evaluate(options, board, game)
        # then put together a set of evaluations for this strategy
        prevailingcolors = game.bag.colorcounts()
        mincount = 20   # Find the baseline color count to normalize
        for color in prevailingcolors.keys():
            mincount = min(mincount, prevailingcolors[color])
        # print("prevailing colors in bag = " + str(prevailingcolors))
        evals = []
        for potentialplay in playlist:
            color = potentialplay[1]
            if color in prevailingcolors:
                rankval = prevailingcolors[color] - mincount + 1
                modplay = potentialplay[0:3] + "_" + str(rankval)
                evals.append(modplay)
        evals.sort(key=strat.getcount2, reverse=True)
        # print("MPBCS evals = " + str(evals))
        return(evals)

    def recommend(self, options, board, game = None):
        evals = self.evaluate(options, board, game)
        if len(evals) > 0:
            return(evals[0])
        else:
            return (None)
