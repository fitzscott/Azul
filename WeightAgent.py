import numpy as np
import WeightedComboStrategyPlayer as wcsp
import random

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
        self._values = {}
        self._testcount = {}
        self._state_history = []
        self._min_wgt = 1       # originally 0, but problems in WCSP
        self._max_wgt = 3       # originally 9; then 6
        self._increment = 1
        self._defval = 2.0      # For populating values function - optimistic
        self._state_hist = []
        self._localwgts = None
        self._createspace = True

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
        if self._localwgts is None:
            self._localwgts = [1 for strat in stratarr]
        self._player = wcsp.WeightedComboStrategyPlayer(game, board,
                                                        self._localwgts)
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

    @property
    def testcount(self):
        return (self._testcount)

    @property
    def max_weight(self):
        return(self._max_wgt)

    @max_weight.setter
    def max_weight(self, val):
        self._max_wgt = val

    @property
    def increment(self):
        return (self._increment)

    @increment.setter
    def increment(self, val):
        self._increment = val

    @property
    def alpha(self):
        return (self._learnrate)

    @alpha.setter
    def alpha(self, val):
        self._learnrate = val

    @property
    def epsilon(self):
        return (self._epsilon)

    @epsilon.setter
    def epsilon(self, val):
        self._epsilon = val

    @property
    def createspace(self):
        return (self._createspace)

    @createspace.setter
    def createspace(self, val):
        self._createspace = val

    def add_value(self, state, val, runcount=1):
        # print("Adding value " + str(val) + " and test count " +
        #       str(runcount) + " to state " + str(state))
        self._values[int(state)] = float(val)
        self._testcount[int(state)] = int(runcount)

    @property
    def state_history(self):
        return (self._state_history)

    def add_state(self, state):
        self._state_history.append(state)

    def reset_history(self):
        self._state_history = []

    def set_wgts(self, wgts):
        self._player.weights = [w for w in wgts]

    def chkdupes(self, narr):
        retval = False
        for chk in range(self.max_weight - 1):
            cnum = chk + 2
            multcnt = 0
            for n in narr:
                if int(n) % cnum == 0:
                    multcnt += 1
            if multcnt == len(narr):
                # print("Got multiple count " + str(multcnt) + " for " +
                #       "".join([str(x) for x in narr]))
                retval = True
                break
        # print("Checked " + nstr + ", returned " + str(retval))
        return (retval)

    def calc_state(self):
        """
        calc_state - return an integer representing the weights on the strategies
        :return: integer
        """
        hashval = 0
        wgts = self._player.weights
        if not self.chkdupes(wgts):         # redundant but leaving it for now
            for widx in range(len(wgts)):
                hashval += (10 ** widx) * wgts[widx]
        return (hashval)

    def update_wgt(self, widx, delta=1, update_local=False):
        """
        Adjust the weight for one of the strategies
        :param widx: strategy index
        :param delta: adjustment, typically +1 or -1
        :param update_local: save the agent's weights, too
        :return: None
        """

        # print("pre-assert weights = " + str(self._player.weights) +
        #       ", index: " + str(widx) + ", delta: " + str(delta))
        assert (self.weights[widx] >= self._min_wgt and
                self.weights[widx] <= self._max_wgt)
        self._player.weights[widx] += delta * self.increment
        if update_local:
            self._localwgts[widx] += delta * self.increment
        # print("updated player weights = " + str(self._player.weights))
        # print("updated weights = " + str(self.weights))

    def goodadjust(self, idx, adjustment):
        retval = True

        if self.weights[idx] + adjustment * self.increment < self._min_wgt \
                or self.weights[idx] + adjustment * self.increment \
                > self._max_wgt:
            retval = False
        else:
            dupchk = [w for w in self.weights]
            dupchk[idx] += adjustment * self.increment
            retval = not self.chkdupes(dupchk)
        return (retval)

    def adjustable(self, adjustment):
        """
        List of weights available for adjustment.
        Adjusted weight must be between min and max, inclusive.
        :return: Array of indices
        """
        # print("weights in adjustable = " + str(self.weights))
        return([idx for idx in range(len(self.weights))
                if self.goodadjust(idx, adjustment)])

    def best_value_state(self):
        # Instead of building the search space, assume it is complete and
        # just choose the state with the highest value.
        best_val = -2
        best_state = -1
        for wgt in self.values.keys():
            if self.values[wgt] > best_val:
                best_val = self.values[wgt]
                best_state = wgt
        # print("Best state is " + str(best_state) + ", value " + str(best_val))
        return (best_state)

    def random_value_state(self):
        # Not sure if this is necessary...
        states = [st for st in self.values.keys()]
        spsiz = len(states)
        rndwgtidx = random.randint(0, spsiz-1)
        # print("States are: " + str(states))
        # print("Random index is " + str(rndwgtidx))
        return (states[rndwgtidx])

    def available_actions(self, poswgt=1):
        acts = {}
        # poswgt will weight the upward direction, since it seems like we are
        # not reaching all the options "on top".
        # print("    wgts: " + str(self.weights))
        # print("    plyr wgts: " + str(self._player.weights))
        acts[1] = self.adjustable(1) * poswgt
        # print("positive actions = " + str(acts[1]))
        acts[-1] = self.adjustable(-1)
        # print("negative actions = " + str(acts[-1]))
        return (acts)

    def take_action(self):
        change = [1, -1]
        next_move = (0,0)
        next_state = None
        if np.random.rand() < self._epsilon:    # random choice
            if not self.createspace:
                next_state = self.random_value_state()
            else:
                # There will be times that we cannot go up or down, so make
                # sure we don't try those.
                options = self.available_actions(1)     # was 5; checking completeness
                # print("    random choice")
                moves = []
                for direction in change:
                    for idx in options[direction]:
                        moves.append((idx, direction))
                if len(moves) > 0:
                    chidx = np.random.choice(len(moves))
                    next_move = (moves[chidx][0], moves[chidx][1])
        else:           # Select best so far
            if not self.createspace:
                next_state = self.best_value_state()
            else:
                options = self.available_actions(1)
                # print("    best so far choice")
                curr_wgts = [w for w in self._player.weights]
                # print("current weights = " + str(curr_wgts))
                best_val = -2
                # best_wgts = None
                # best_state = 0
                for direction in change:
                    for idx in options[direction]:
                        self.update_wgt(idx, direction)
                        state = self.calc_state()
                        if state != 0:      # reject factors / duplicates
                            # think there's a faster way to do this
                            if state not in self.values.keys():
                                self._values[state] = self._defval
                            val = self.values[state]
                            if val > best_val:
                                best_val = val
                                # best_wgts = self._player.weights
                                # best_state = state
                                next_move = (idx, direction)
                        else:
                            print("Rejected " + str(self.weights))
                        self.set_wgts(curr_wgts)
                # print("weights are " + str(self.weights) + ", next move: " + str(next_move))
        if not self.createspace:
            state = next_state
        else:
            # Apply the next move
            self.update_wgt(next_move[0], next_move[1], True)  # index then direction
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
        # print("Counts are " + str(self.testcount))
        for prev in reversed(self.state_history):
            prevval = self.values[prev]
            # Adjust the learning rate by the number of tests run
            # newval = prevval + self._learnrate * (target - prevval)
            # Update the test count for this state
            self.testcount[prev] = self.testcount.get(prev, 0) + 1
            adjalpha = 1 + self.testcount[prev] / 100.0
            newval = prevval + self._learnrate * (target - prevval) / adjalpha
            self.values[prev] = newval
            target = newval
        self.reset_history()

    def get_val_str(self):
        retval = ",".join([":".join([str(state), str(self.values[state]),
                                    str(self.testcount.get(state, 0))])
                           for state in self.values.keys()])
        return (retval)

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
