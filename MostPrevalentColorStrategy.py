import Strategy as strat
import PlayableColorStrategy as pcs

class MostPrevalentColorStrategy(pcs.PlayableColorStrategy):
    """
    MostPrevalentColorStrategy - choose the color that is most prevalent on
    the whole board.  Temper it with the PlayableColorStrategy.
    """

    def evaluate(self, options, board, game = None):
        # get the set of evaluations from the parent
        playlist = super().evaluate(options, board, game)
        # then put together a set of evaluations for this strategy
        prevailingcolors = {}
        for opt in options:
            for color in opt[2:]:
                if color == '1':
                    continue
                prevailingcolors[color] = prevailingcolors.get(color, 0) + 1
        prevailinglist = [key + "_" + str(prevailingcolors[key])
                    for key in prevailingcolors.keys()]
        prevailinglist.sort(key=strat.getcount)
        # print("prevalence: " + str(prevailinglist))
        evals = []
        for prevcol in prevailinglist:
            for potentialplay in playlist:
                if prevcol[0] == potentialplay[1]:
                    evals.append(potentialplay)
        return(evals)

    def recommend(self, options, board, game = None):
        evals = self.evaluate(options, board, game)
        if len(evals) > 0:
            return(evals[0])
        else:
            return (None)
