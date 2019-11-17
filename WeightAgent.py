import numpy as np
import WeightedComboStrategyPlayer as wcsp

class WeightAgent():
    """
    Crude agent for experimenting with reinforcement learning.
    The agent will have a WeightedComboStrategyPlayer instance.
    The agent will start with a set of strategies and default weights
    for each.  In each execution, the agent will have its weights
    adjusted according to the result of the game played.  We will not
    track individual moves within Azul; the reward will be for the
    whole game.
    Keeping the values function (values) here in the agent, rather than
    in its own module, since it's just a dictionary.
    Also have the environment in this module, though it is not the game
    environment:  It is the strategy weights.
    And the state history is here, too.  Big, messy class.
    """

    def __init__(self, plnum, eps=0.25, alpha=0.5):
        self._playernum = plnum
        self._player = None
        self._epsilon = eps
        self._learnrate = alpha
        self._values = None
        self._state_history = []
        self._min_wgt = 1       # originally 0, but problems in WCSP
        self._max_wgt = 4       # originally 9; then 6
        self._values = {}
        self._defval = 0.5      # For populating the values function
        self._state_hist = []

    def clear_eps(self):
        self._epsilon = 0

    def __str__(self):
        retstr = "Player " + str(self._playernum) + "\n" + \
            "Epsilon = " + str(self._epsilon) + ", alpha = " + \
            str(self._learnrate) + "\nValues = " + str(self._values) + "\n" + \
            str(self._player) + "\n    : " + str(self._player.weights)
        return (retstr)

    @property
    def player(self):
        return (self._player)

    def assign_player(self, game, board, strats, plnum=-1):
        """
        assign_player - set up the Azul player with passed-in strategies.
        :param game: Azul game
        :param board: board assigned to this player
        :param strats: string of strategies separated by plus signs
        :param plnum: player number in the game
        :return: None
        """
        stratarr = strats.strip().split("+")
        wgts = [1 for strat in stratarr]
        self._player = wcsp.WeightedComboStrategyPlayer(game, board, wgts)
        for strat in stratarr:
            self._player.addstratbystr(strat)
        if plnum != -1:
            self._playernum = plnum

    @property
    def weights(self):
        return (self._player.weights)

    @property
    def values(self):
        return (self._values)

    def add_value(self, state, val):
        self._values[state] = val

    @property
    def state_history(self):
        return (self._state_history)

    def add_state(self, state):
        self._state_history.append(state)

    def reset_history(self):
        self._state_history = []

    def calc_state(self):
        """
        calc_state - return an integer representing the weights on the strategies
        :return: integer
        """
        hashval = 0
        wgts = self._player.weights
        for widx in range(len(wgts)):
            hashval += (10 ** widx) * wgts[widx]
        return (hashval)

    def update_wgt(self, widx, delta=1):
        """
        Adjust the weight for one of the strategies
        :param widx: strategy index
        :param delta: adjustment, typically +1 or -1
        :return: None
        """
        self._player.weights[widx] += delta

    def adjustable(self, adjustment):
        """
        List of weights available for adjustment.
        Adjusted weight must be between 0 and 9, inclusive.
        :return: Array of indices
        """
        return([idx for idx in range(len(self.weights))
                if self.weights[idx] + adjustment >= self._min_wgt and
                self.weights[idx] + adjustment <= self._max_wgt])

    def available_actions(self):
        acts = {}
        acts[1] = self.adjustable(1)
        acts[-1] = self.adjustable(-1)
        return (acts)

    def take_action(self):
        change = [1, -1]
        options = self.available_actions()
        next_move = None
        moves = []
        if np.random.rand() < self._epsilon:    # random choice
            # There will be times that we cannot go up or down, so make
            # sure we don't try those.
            for direction in change:
                for idx in options[direction]:
                    moves.append((direction, idx))
            # direction = change[np.random.choice(len(change))]
            # num_opts = len(options[direction])
            idx = np.random.choice(len(moves))
            next_move = (moves[idx][0], moves[idx][1])
        else:           # Select best so far
            curr_wgts = self._player.weights
            best_val = -2
            # best_wgts = None
            # best_state = 0
            for direction in change:
                for idx in options[direction]:
                    self.update_wgt(idx, direction)
                    state = self.calc_state()
                    # think there's a faster way to do this
                    if state not in self.values.keys():
                        self._values[state] = self._defval
                    val = self.values[state]
                    if val > best_val:
                        best_val = val
                        # best_wgts = self._player.weights
                        # best_state = state
                        next_move = (direction, idx)
            # We've tried all the options, so reset to original state.
            self._player.weights = curr_wgts
        # Apply the next move
        self.update_wgt(next_move[1], next_move[0])
        state = self.calc_state()
        # This is clunky.  Figure out how to do it more cleanly.
        if state not in self.values.keys():
            self._values[state] = self._defval
        self.add_state(state)
        return (state)

    def update_vals(self, reward):
        target = reward
        # print("State history is " + str(self.state_history))
        # print("Values is " + str(self.values))
        for prev in reversed(self.state_history):
            prevval = self.values[prev]
            newval = prevval + self._learnrate * (target - prevval)
            self.values[prev] = newval
            target = newval
        self.reset_history()

if __name__ == "__main__":
    import random

    wa = WeightAgent(1)
    wa.assign_player(None, None, "ExactFitStrategy+CentralPositionStrategy+MinPenaltyStrategy+MostPrevalentColorStrategy+FillRowStrategy+TopRowsStrategy")
    print(wa)
    print("Current state is " + str(wa.calc_state()))
    adjwhich = random.randint(0, len(wa.weights)-1)
    wa.update_wgt(adjwhich)
    print("Adjusting " + str(adjwhich) + ", new state: " + str(wa.calc_state()))
    adjwhich = random.randint(0, len(wa.weights)-1)
    wa.update_wgt(adjwhich, -1)
    print("Adjusting " + str(adjwhich) + ", new state: " + str(wa.calc_state()))
    print("Adjustable down indices: " + str(wa.adjustable(-1)))
    # print("Taking 100 actions...")
    # for _ in range(100):
    #     wa.take_action()
    #     print("Current state is " + str(wa.calc_state()))
    # print("State history is " + str(wa.state_history))
