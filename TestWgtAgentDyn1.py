import sys
import os
import random
import time
import Game as g
import WeightedComboStrategyPlayer as wcsp
import WeightAgent as wa


def rungame(plyrz, plcnt, playme, itr, gameno):
    maxturns = 300
    maxrt = 60.0

    # playme.show()
    cont = True
    firstplayer = 0
    turnz = 0
    retval = [0]
    # while cont:
    gamestart = time.time()
    while cont and turnz < maxturns:  # real games rarely go past 5
        for idxnum in range(plcnt):
            plnum = (firstplayer + idxnum) % plcnt
            if playme.turnover():  # dispnum == 9:
                # cont = False
                for plnum in range(plcnt):
                    playme.playerboard[plnum].movescore(playme.box)
                    if playme.playerboard[plnum].firstplayer:
                        firstplayer = plnum
                        playme.playerboard[plnum].firstplayer = False
                    if playme.playerboard[plnum].finalboard.horizrowcomplete():
                        cont = False
                if cont:
                    # print("\t  " + 8 * "+" + " turn " + str(turnz + 1) + " next")
                    if not playme.loadtiles():
                        cont = False
                        retval = [-1]
                        break
                    # playme.show()
                break
            # print("Player " + str(plnum + 1) + " turn:")
            plyrz[plnum].taketurn()
            # playme.show()
            turnz += 1
            currtime = time.time()
            rt = currtime - gamestart
            if rt > maxrt:
                # print("No final score, ran " + str(rt))
                retval = [-1]
                turnz = maxturns
                break
    # print(8 * "+" + "\t\tFinal scoring:")
    for idxnum in range(plcnt):
        playme.playerboard[idxnum].finalscore()
    # playme.show()
    currtime = time.time()
    rt = currtime - gamestart
    winrarr = playme.winner()

    if turnz == maxturns:
        retval = [-1]
    else:
        retval = winrarr
    return (retval)


def agentvalzflnm(strats):
    return("agentvalz_" + "_".join(strats.split("+")))


def runXiters(strats, iters, agentstrats, wgts=None, maxwgt=None, incr=None,
              alpha=None, epsilon=None, cr8_spc=True, adj_alpha=True):
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
    if incr is not None:
        agent.max_weight = maxwgt
        agent.increment = incr
    if alpha is not None:
        agent.alpha = alpha
    if epsilon is not None:
        agent.epsilon = epsilon
    if not cr8_spc:
        # print("not creating search space")
        agent.createspace = False
    if not adj_alpha:
        agent.scaled_alpha = False

    for itr in range(iters):
        # Set up the game.  Ideally, we wouldn't do this every time,
        # but fixing it would mean tweaking a bunch of older code.
        # Add to the to-do list.
        playme = g.Game(plcnt)
        playme.loadtiles()
        plyrz = []
        agentplnum = random.randint(0, 3)
        for plnum in range(plcnt):
            if plnum != agentplnum:
                plyr = wcsp.WeightedComboStrategyPlayer(playme,
                                                        playme.playerboard[plnum])
                stratidx = random.randint(0, len(plyrwgtcombos)-1)
                for stratstr in plyrwgtcombos[stratidx].split("+"):
                    plyr.addstratbystr(stratstr)
                plyr.stdweight()
            else:
                agent.assign_player(playme, playme.playerboard[plnum],
                                    agentstrats, agentplnum)
                plyr = agent.player
            # print(plyr)
            plyrz.append(plyr)
        # print(agent)
        state = agent.take_action()
        assert(state != 0)
        wnrz = rungame(plyrz, plcnt, playme, itr, itr + 1)
        if agentplnum in wnrz:
            # print("Agent won!  How odd...")
            rwd = 1.0
        else:
            rwd = 0.0
            for ridx in range(len(playme.playerranks)):
                if agentplnum == playme.playerranks[ridx][0]:
                    rwd = ridx * 1.0 / 3.0
        # print(":".join(["State", str(state), "Reward", str(rwd),
        #                 "Strategies", "+".join(agent.player.strstrategies)]))
        agent.update_vals(rwd)
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
               alpha=None, epsilon=None, cr8_spc=True, adj_alpha=True):
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
    runXiters(fullwgtset, iters, agentstrats, wgts, maxwgt, incr, alpha,
              epsilon, cr8_spc, adj_alpha)


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
    if len(sys.argv) > 8:
        cr8_spc = int(sys.argv[8]) == 1
    else:
        cr8_spc = True
    if len(sys.argv) > 9:
        adj_alpha = int(sys.argv[9]) == 1
    else:
        adj_alpha = True

    pickstrats(stratfile, iters, strats, maxwgt, incr, alpha, epsilon,
               cr8_spc, adj_alpha)
