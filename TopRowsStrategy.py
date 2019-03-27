import PlayableColorStrategy as pcs

class TopRowsStrategy(pcs.PlayableColorStrategy):
    """
    TopRowsStrategy - prefer the smallest rows over the largest.
    """
    def evaluate(self, options, board, game = None):
        import Strategy

        evals = []
        for opt in options:
            # print("Checking fill count " + str(fc) + " against " + opt)
            # If the option is for the color available for the row in
            # the fill count, add it to the list.
            # remaining = board.finalboard.rowremainingcolors(fc[0])
            for color in opt[2:]:
                if color == '1':
                    continue
                for rownum in range(5):
                    if board.prepboard.canplace(rownum, color) and not \
                            board.prepboard.rowfull(rownum):
                        rank = 4 - rownum
                        evals.append(opt[0] + color + str(rownum) + "_" + str(rank))
        print("Top rows evaluations: " + str(evals))
        return (evals)

    def recommend(self, options, board, game = None):
        evals = self.evaluate(options, board, game)
        if evals is None or len(evals) == 0:
            return(super().recommend(options, board, game))
        else:
            # print("TopRowsStrategy chose " + evals[0])
            return (evals[0])
