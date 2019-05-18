import PlayableColorStrategy as pcs

class AtLeastFitStrategy(pcs.PlayableColorStrategy):
    """
    AtLeastFitStrategy
    Look for options that will fully fit the preparatory board (and of
    course be eligible for the final board.
    This strategy should only be applied toward the end of the game, so rounds
    4 and later, with increasing weight.
    """

    defaultweight = 5

    def evaluate(self, options, board, game = None):
        import Strategy

        round = game.roundnum
        if round < 3:       # Bail out - strategy does not apply
            return (super().evaluate(options, board, game))
        atleastfit = []
        mult = round - 2
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
                    overflow = min(self.defaultweight,
                                   colorcount[ckey] - slots[slotidx])
                    if overflow >= 0 and \
                            board.prepboard.canplace(slotidx, ckey):
                        weight = (self.defaultweight - overflow) * mult
                        atleastfit.append(dispnum + ckey + str(slotidx) + \
                                        "_" + str(weight))
        if len(atleastfit) == 0:
            return (super().evaluate(options, board, game))
        atleastfit.sort(key=Strategy.getcount2, reverse=True)
        # print("At least fit evals: " + str(atleastfit))
        return(atleastfit)

    def recommend(self, options, board, game = None):
        evs = self.evaluate(options, board, game)
        if len(evs) > 0:
            return(evs[0])
        else:
            return(None)
