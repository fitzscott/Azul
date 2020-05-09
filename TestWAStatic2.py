import sys
import os
import random
import time
import Game as g
import WeightedComboStrategyPlayer as wcsp
import WeightAgent as wa


def agentvalzflnm(strats):
    return("agentvalz-" + "-".join(strats.split("+")))


def runXiters(strats, iters, agentstrats, wgts=None, maxwgt=None, incr=None,
              alpha=None, epsilon=None):
    # trimdstrats = [strat.split(":")[0] for strat in strats]
    agent = wa.WeightAgent(-1)
    plyrwgtcombos = strats      # Unnecessary, but it calms the code a little
    plcnt = 4
    # Assign previously-recorded values to agent
    if wgts is not None:
        wvalz = wgts.split(",")
        for wval in wvalz:
            sinfo = wval.split(":")
            state, val = sinfo[0:2]
            if len(sinfo) > 2:
                runcount = int(sinfo[2])
            else:
                runcount = 1
            agent.add_value(state, val, runcount)
            # print("added " + str(val) + " to state " + str(state))
        # print("test run counts = " + str(agent.testcount))
    agent.assign_player(None, None, agentstrats, 4)
    if incr is not None:
        agent.max_weight = maxwgt
        agent.increment = incr
    if alpha is not None:
        agent.alpha = alpha
    if epsilon is not None:
        agent.epsilon = epsilon

    for itr in range(iters):
        # Set up the game.  Ideally, we wouldn't do this every time,
        # but fixing it would mean tweaking a bunch of older code.
        # Add to the to-do list.
        # print(agent)
        state = agent.take_action()
        assert(state != 0)
        # hard-code some win conditions
        stsum = 0
        for s in str(state):
            stsum += int(s)
        if stsum == 16:
            if random.randint(1, 10) > 1:
                rwd = 1.0
            else:
                rwd = 0.1
        elif stsum == 7:
            if random.randint(1, 10) > 2:
                rwd = 0.5
        else:
            if random.randint(1, 10) > 9:
                rwd = 0.1
            else:
                rwd = 0.0
        # print(":".join(["State", str(state), "Reward", str(rwd),
        #                 "Strategies", "+".join(agent.player.strstrategies)]))
        agent.update_vals(rwd)
        # agent.update_vals(stsum)    # just for the hell of it
    # print(str(agent))
    agvflnm = agentvalzflnm(agentstrats)
    if os.path.exists(agvflnm + ".bak"):
        os.remove(agvflnm + ".bak")
    if os.path.exists(agvflnm + ".txt"):
        os.rename(agvflnm + ".txt", agvflnm + ".bak")
    valfl = open(agvflnm + ".txt", "w")
    valfl.write(agentstrats + "|" + agent.get_val_str() + "\n")
    valfl.close()


def readvalue(strats):
    # Read the values file. If the strategy set is present, use that weighting.
    # If not, let the agent use its default.
    valz = None
    vfnm = agentvalzflnm(strats) + ".txt"
    if os.path.exists(vfnm):
        valfl = open(vfnm)
        for ln in valfl:
            strat, wgts = ln.strip().split("|")
            if strat == strats:
                valz = wgts
            # read through the rest of the file, even if the strategy set is
            # found, since we'll just append new results to the end of it.
        valfl.close()
        # print("Read weight values: " + str(valz))
    return (valz)

def pickstrats(stratfile, iters, agentstrats=None, maxwgt=None, incr=None,
               alpha=None, epsilon=None):
    pickcount = 0
    stratsets = []
    # First, get the list of weighted strategy combinations to use.
    wgtfile = open(stratfile)
    wgtcombos = wgtfile.readlines()
    wgtfile.close()
    fullwgtset = [wc.strip().split(":")[0]
                  for wc in wgtcombos
                  if len(wc) > 0]
    if agentstrats is None:
        # We'll exclude the prevalent color strategy for now.
        agentstrats = "CentralPositionStrategy+ExactFitStrategy+FillRowStrategy+MinPenaltyStrategy+TopRowsStrategy"
    wgts = readvalue(agentstrats)
    runXiters(fullwgtset, iters, agentstrats, wgts, maxwgt, incr, alpha, epsilon)


if __name__ == "__main__":
    stratfile = sys.argv[1]
    iters = int(sys.argv[2])
    if len(sys.argv) > 3:
        strats = sys.argv[3]
    else:
        strats = None
    if len(sys.argv) > 5:
        maxwgt = int(sys.argv[4])
        incr = int(sys.argv[5])
    else:
        maxwgt = None
        incr = None
    if len(sys.argv) > 6:
        alpha = float(sys.argv[6])
    else:
        alpha = 0.5
    if len(sys.argv) > 7:
        epsilon = float(sys.argv[7])
    else:
        epsilon = 0.25      # very high, really
    pickstrats(stratfile, iters, strats, maxwgt, incr, alpha, epsilon)
