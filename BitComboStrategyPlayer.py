import ComboStrategyPlayer as csp
import WeightedComboStrategyPlayer as wcsp

class BitComboStrategyPlayer(wcsp.WeightedComboStrategyPlayer):
    """
    Accept an integer as a bitfield indicating which strategies should be
    included in the combination.
    """

    def __init__(self, game, board, bitfld):
        import ComboStrategyPlayer as csp

        super().__init__(game, board)
        self._stratbits = bitfld
        # Is there a way to do a list comprehension for this?
        self._twos = [1]
        for pos in range(len(csp.ComboStrategyPlayer.strats)-1):
            self._twos.append(2 * self._twos[pos])

    @property
    def bitfield(self):
        return (self._stratbits)

    @bitfield.setter
    def bitfield(self, val):
        self._stratbits = val

    def assignstrats(self, bitfld=0, uniformweight=True):
        if bitfld == 0:
            bf = self._stratbits
        else:
            bf = bitfld
        for sidx in range(len(csp.ComboStrategyPlayer.strats)):
            if self._twos[sidx] & bf > 0:
                self.addstrategy(csp.ComboStrategyPlayer.strats[sidx]())
        if uniformweight:
            weights = [1 for _ in range(len(self.strategies))]
            self.weights = weights

if __name__ == "__main__":
    bcsp = BitComboStrategyPlayer(None, None, 7)
    bcsp.assignstrats()
    print(bcsp)
    bcsp.clearstrats()
    bcsp.bitfield = 32 + 64 + 128
    bcsp.assignstrats()
    print(bcsp)
    bcsp.clearstrats()
    bcsp.bitfield = 256 + 512 + 1024 + 2048
    bcsp.assignstrats()
    print(bcsp)

