import WeightAgent as wa

class TestWAStatic():
    def __init__(self, winstate):
        self._winstate = winstate
        self._agent = wa.WeightAgent(1)
        self._agent.assign_player(None, None,
                                  "ExactFitStrategy+CentralPositionStrategy+MinPenaltyStrategy+MostPrevalentColorStrategy+FillRowStrategy+TopRowsStrategy")

    @property
    def winstate(self):
        return (self._winstate)

    def playalot(self):
        alot = 1000000
        wa = self._agent
        for _ in range(alot):
            state = wa.take_action()
            # This is effectively the update (end of game) section
            if state == self.winstate:
                valchg = 1
            else:
                valchg = 0
            wa.update_vals(valchg)


if __name__ == "__main__":
    twas = TestWAStatic(222222)
    twas.playalot()
    print("Values: " + str(twas._agent.values))
