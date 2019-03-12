import PlayableColorStrategy as pcs

class MaxPlaceScoreStrategy(pcs.PlayableColorStrategy):
    """
    For each possible play, see what it'd score in the final board.
    Do not account for whether the play will complete the prep
    board row to send the tile to the final board.
    """

    def evaluate(self, options, board, game = None):
        import FinalBoardComponent as fbc
        import Strategy

        scores = {}
        fb = board.finalboard
        for color in fbc.FinalBoardComponent.colororder:
            for rownum in range(fbc.FinalBoardComponent.dimension):
                columnnum = fb.getcolumnnum(rownum, color)
                sc1 = fb.scoreplacedtile(rownum, columnnum)
                scores[(color, rownum)] = scores.get((color, rownum), 0) + sc1
        scorelist = [(key, scores[key]) for key in scores.keys()]
        if len(scorelist) == 0:
            print("Max placement score returned no options?")
            return (super().evaluate(options, board, game))
        scorelist.sort(key=Strategy.getcounttup, reverse=True)

        pb = board.prepboard
        evals = []
        for score in scorelist:
            color = score[0][0]
            rownum = score[0][1]
            scorenum = score[1]
            for opt in options:
                for optcolor in opt[2:]:
                    if optcolor == '1':
                        continue
                    if color == optcolor and pb.canplace(rownum, color) and \
                            not pb.rowfull(rownum):
                        move = opt[0] + color + str(rownum) + "_" + \
                               str(scorenum)
                        evals.append(move)
        # print("Max score evals: " + str(evals))
        return (evals)
