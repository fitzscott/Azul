import DBPlayerInfo as dbi
import pymongo as pm
import time
from datetime import datetime, date
import WeightedComboStrategyPlayer as wcsp

class MongoDBPlayerInfo(dbi.DBPlayerInfo):
    """
    MongoDBPlayerInfo - analogous to MySQL-based DBPlayerInfo, but using
    Mongo's document model instead of relational.
    """
    def __init__(self, cnct, game, plnum):
        super().__init__(cnct, game, plnum)
        self._strategies = None
        self._db = cnct.azul

    @property
    def strategies(self):
        return (self._strategies)

    @strategies.setter
    def strategies(self, val):
        self._strategies = val

    def find_wss(self, curs, state):
        # In Mongo, we don't really need an ID for the weighted strategy
        # set.  We'll just create an identifying string using the
        # strategy set ID and the state.
        return (str(self.StratSetId) + str(state))

    def getstate2wgtstratset(self, state, agent):
        if self._agent is None:
            print("agent should be defined for DB info but is not")
            self._agent = agent
        winrt = self._agent.values[state]
        if state not in self._agent.testcount.keys():   # assign default val
            # print("missing test count, assigning")
            self._agent.testcount[state] = 1
        execnt = self._agent.testcount[state]
        epc = str(time.mktime(datetime.today().timetuple())).split(".")[0]
        doinsert = False
        if state not in self._state2wss.keys():
            wss = self.find_wss(None, state)      # kludge
            if wss != -1:
                self._state2wss[state] = wss
                doinsert = True
        agvalz = self._db.agentvalues
        # if state not in self._state2wss.keys():
        if doinsert:
            # Add document to agent values
            agvdoc = {"strategies": self.strategies,
                      "strategysetid": self.StratSetId,
                      "weight": int(state),
                      "winrate": winrt,
                      "count": execnt,
                      "updtime": epc}
            # print("Inserting " + str(agvdoc))
            agvalz.insert_one(agvdoc)
        else:
            # Update document - filter 1st, then assignment
            # print("Updating {0} {1} w/ {2} {3} {4}".format(self.StratSetId, state, winrt, execnt, epc))
            agvalz.update_one({"strategysetid": self.StratSetId,
                               "weight": int(state)},
                              {"$set": {"winrate": winrt, "count": execnt,
                                        "updtime": epc}})
        return (self.find_wss(None, state))        # not sure why

    def setNonAgentGrpId(self, grpid):
        # We need the competitors data for this.
        self._plyr = wcsp.WeightedComboStrategyPlayer(self.game,
                                                      self.dbplayerboard)
        self._grpid = int(grpid)
        # print("Finding comp group for " + str(grpid))
        grpstrats = self._db.compgroups.find_one({"compid": self._grpid})
        # print("Group strategies = " + str(grpstrats))
        self.strategies = grpstrats["strategies"]
        for strat in self.strategies:
            # print("    Adding strategy " + strat)
            self._plyr.addstratbystr(strat)
        self._plyr.weights = [int(w) for w in str(grpstrats["weight"])]
        self._StratSetId = grpstrats["strategysetid"]
        self._wgtdstratsetid = self.find_wss(None, grpstrats["weight"])

    def setStratSetId(self, stratsetid):
        self.StratSetId = int(stratsetid)
        oness = self._db.strategysets.find_one(
            {"strategysetid": self.StratSetId})
        # print("    Sample agent values for " + str(self.StratSetId) + " = " + str(oness))
        # Copy it, just in case
        self.strategies = [stratstr for stratstr in oness["strategies"]]
        # Result should be the plus-delimited string of strategies.
        return ("+".join(oness["strategies"]))

    def setupAgent(self, stratsetid, agent, plnum, assignvals, state2wss):
        # print("In Mongo agent set up for set {0}, player # {1}".format(stratsetid, plnum))
        ssid = int(stratsetid)
        if assignvals:
            # print("Finding agent values")
            cnt = 0
            agentstrats = self.setStratSetId(ssid)
            agvs = self._db.agentvalues.find({"strategysetid": ssid})
            for agv in agvs:
                agent.add_value(agv["weight"], agv["winrate"], agv["count"])
                self.setstate2wgtstratset(agv["weight"],
                                          self.find_wss(None, agv["weight"]))
                # cnt += 1
                # if cnt % 100 == 0:
                #     print("Loaded {0} agent values so far".format(cnt))
        else:
            # print("Not assigning agent values this time")
            # Tired of fighting this... just pull from the DB, as it's quick.
            # self._StratSetId = ssid # avoid a DB call
            agentstrats = self.setStratSetId(ssid)
            # agentstrats = "+".join(self.strategies)
            if state2wss is not None:
                self._state2wss = state2wss
        agent.assign_player(self._game, self.dbplayerboard, agentstrats, plnum)
        self._agent = agent
        # print(str(self._agent))
        assert(self._agent is not None)
        self._plyr = agent.player

