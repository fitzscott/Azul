def getcount(ev):
    return (-1 * int(ev.split("_")[1]))     # easier way to reverse?

def getcount2(ev):
    return (int(ev.split("_")[1]))

def getcounttup(ev):
    return (ev[1])


class Strategy():
    """
    Strategy - methods for evaluating how well a particular approach will work.
    """
    def evaluate(self, options, board, game = None):
        """
        :return: list of potential moves
        Generally, a strategy will set up some criteria, then judge the
        options from the game according to those criteria, returning a
        ranked list of possible actions / moves.
        Moves contain 3 components:
            Factory display # to pull tiles from
            Color to collect from the display
            Row number on the preparatory board in which to place the tiles
        Each component is a character, so the move will be a 3-char string.
        In addition, a list of recommended moves will have a ranking
        after the row number, with an underscore separator.
        Combined strategies are also considered a strategy.
        """
        pass

    def recommend(self, options, board, game = None):
        pass

    def combineevals(self, eval1, eval2):
        """
        Combine two evaluations, yielding a new list of evaluations.
        :param eval1:
        :param eval2:
        :return: list of new evaluations, appropriately ranked
        """
        combo = []
        maxrank = -1
        for e1 in eval1:
            for e2 in eval2:
                if e1[0:3] == e2[0:3]:
                    e1rank = int(e1.split('_')[1])
                    e2rank = int(e2.split('_')[1])
                    combo.append(e1[0:3] + "_" + str(e1rank + e2rank))
                    maxrank = max(maxrank, e1rank + e2rank)
        # For the evals that didn't match, add them on the end of the
        # returned combination.
        # Previously, we were assigning maxrank to the rank of the unmatched
        # evaluations, but that doesn't seem to make sense.  Instead, its
        # rank from the previous evaluation should be applied.
        combostripped = [co[0:3] for co in combo]
        for e in eval1:
            if e[0:3] not in combostripped:
                # maxrank += 1
                # combo.append(e[0:3] + "_" + str(maxrank))
                combo.append(e)
        for e in eval2:
            if e[0:3] not in combostripped:
                # maxrank += 1
                # combo.append(e[0:3] + "_" + str(maxrank))
                combo.append(e)
        combo.sort(key=getcount)    # higher is better
        return(combo)
