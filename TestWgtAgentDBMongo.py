import sys
import TestWgtAgentDB1 as twadb
import pymongo as pm
import dbmongocfg as dbcfg
import MongoDBPlayerInfo as mdpi
import random
import time
from datetime import datetime

class TestWgtAgentDBMongo(twadb.TestWgtAgentDB1):
    """
    Run the test agent from a MongoDB database, instead of MySQL.
    """
    def __init__(self, compgrp, iters, agentstrats=None, maxwgt=None,
                 incr=None, alpha=None, epsilon=None, cr8_spc=True,
                 adj_alpha=True):
        super().__init__(compgrp, iters, agentstrats, maxwgt, incr, alpha,
                         epsilon, cr8_spc, adj_alpha)

    def startup(self):
        self._cnct = pm.MongoClient(dbcfg.cnctstr)

    def shutdown(self):
        self._cnct.close()

    def getrandgrpids(self):
        # print("Getting Mongo group IDs from set")
        if len(self.compgrpids) == 0:
            cs = self._cnct.azul.compset.find({"compset": self.compgrp})
            for c in cs:
                self.compgrpids.append(c["compid"])
            assert(len(self.compgrpids) > 0)
        return (self.compgrpids)

    def setupplayers(self, cnt=4):
        # print("Setting up Mongo players")
        assert(self._game is not None)
        self.agentplnum = random.randint(0, cnt-1)
        assignvals = self.setupagent()

        grpids = self.getrandgrpids()
        # print("Group IDs: " + str(grpids))
        lengrp = len(grpids)
        for plnum in range(cnt):
            dbp = mdpi.MongoDBPlayerInfo(self._cnct, self.game, plnum)
            if plnum != self.agentplnum:
                grpid = grpids[random.randint(0, lengrp-1)]
                # print("Picked group ID " + str(grpid))
                dbp.setNonAgentGrpId(grpid)
            else:
                # print("Setting up agent w/ strats " + str(self.agentstrats))
                dbp.setupAgent(self.agentstrats, self.agent, plnum,
                               assignvals, self.state2wss)
                # print(agent)
            # print(dbp.player)
            self.dbplyrz.append(dbp)

    def saveGameData(self, runtime, winrz):
        # print("Saving Mongo game data")
        if winrz[0] == -1:
            finished = "N"
        else:
            finished = "Y"
        # Determine base for a game ID
        epc = str(time.mktime(datetime.today().timetuple())).split(".")[0]
        gameid = int(str(self.agentstrats) + epc)
        # figure out player ranks
        ranks = self.game.playerranks
        rnkinfo = {}
        plcnt = len(self.dbplyrz)
        for idx in range(plcnt):
            rnkinfo[ranks[idx][0]] = idx
        # now save the individual player performance
        clxn = self._cnct.azul.gameresults
        for plnum in range(plcnt):
            plyr = self.dbplyrz[plnum]
            scor = plyr.dbplayerboard.score
            stratarr = plyr.strategies
            if plnum in winrz:
                winflg = "Y"
            else:
                winflg = "N"
            wssi = plyr.wgtdstratsetid
            if plnum in winrz:
                gamerank = 1
            else:
                gamerank = plcnt - int(rnkinfo[plnum])
            if plnum == self.agentplnum:
                state = self.agent.calc_state()
                # print("State is " + str(state))
                # wssi = plyr.getstate2wgtstratset(state, self.agent)  # potential DB op
                # potential DB op
                # adjust agent values - reward 1 is best, 0 worst
                rwd = (4 - gamerank) * 1.0 / 3.0
                # print("Agent state {0} self {1}".format(state, self.state))
                # print("Updating agent values with reward {0} for state {1}".format(rwd, state))
                self.agent.update_vals(rwd)
                # print("Calling agent values save {0} {1}".format(self.state, self.agent))
                # print("State from agent is " + str(state))
                wssi = plyr.getstate2wgtstratset(int(self.state), self.agent)
                # wssi = plyr.getstate2wgtstratset(int(state), self.agent)
            # Save game data
            # We are going to leave off the strategy array & the weights
            # for the time being.
            # print("    Saving game {0} player {1} score {2}".format(gameid, plnum+1, scor))
            # print("    Strategies are: " + str(stratarr))
            clxn.insert_one({"gameid": gameid, "playerpos": plnum+1,
                             "score": scor, "playerrank": gamerank,
                             "winflag": winflg,
                             "strategysetid": plyr.StratSetId})
                             # "strategysetid": self.agentstrats})    #,
                             # "strategies": stratarr})
            # For the game results, we had been saving the strategies,
            # but we ran out of space in MongoDB Atlas.
            # """.format(gameid, plnum+1, wssi, scor, gamerank, winflg)
            # print(insRslts)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: " + sys.argv[0] + " competitionSetID iterations " +
              "strategySetID [maxwgt increment alpha epsilon createSpace " +
              "decayAlpha]")
    # print(str(sys.argv))
    comp_grp = int(sys.argv[1])
    iters = int(sys.argv[2])
    stratset = sys.argv[3]
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

    twadb = TestWgtAgentDBMongo(comp_grp, iters, stratset, maxwgt, incr,
                                alpha, epsilon, cr8_spc, adj_alpha)
    twadb.runXtimes(iters)
