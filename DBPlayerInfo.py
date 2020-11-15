import mysql
import WeightedComboStrategyPlayer as wcsp
import time
from datetime import datetime, date

class DBPlayerInfo():
    """
    DBPlayerInfo - track additional information required to refer to
    database tables for a player (general computer, agent, or human)
    """

    def __init__(self, cnct, game, plnum):
        self._StratSetId = -1
        self._StratIds = []
        self._cnct = cnct
        self._game = game
        self._plyrnum = plnum
        self._plyr = None
        self._state2wss = {}
        self._wgtdstratsetid = None
        self._agent = None

    @property
    def StratSetId(self):
        return (self._StratSetId)

    @StratSetId.setter
    def StratSetId(self, val):
        self._StratSetId = val

    @property
    def game(self):
        return (self._game)

    @property
    def cnct(self):
        return(self._cnct)

    def setstate2wgtstratset(self, state, val=None):
        if val is not None:     # assignment
            self._state2wss[state] = val
        return (self._state2wss[state])

    def find_wss(self, curs, state):
        # The weighted strategy set ID keeps getting generated, even when
        # a row exists for strategy ID + weight. Changing the table definition
        # to force that to be unique would catch this error, but need to just
        # get around it for now.
        cnt = 0
        selstr = """
        SELECT WeightedStrategySetID
        FROM weighted_strategy_set 
        WHERE StrategySetID = {0}
            AND WeightSummaryNum = {1}
        """.format(self.StratSetId, state)
        curs.execute(selstr)
        for (wss,) in curs:
            cnt += 1
        if cnt > 0:
            print("Found unexpected WSS = " + str(wss))
            retval = wss
        else:
            retval = -1
        return (retval)

    def getstate2wgtstratset(self, state, agent):
        """
        This is an odd get method. The key may not exist in the structure,
        and if so, it won't exist in the DB.
        :param state: weight state from agent values
        :return: weighted strategy set ID
        """
        if self._agent is None:
            print("agent should be defined for DB info but is not")
            self._agent = agent
        winrt = self._agent.values[state]
        if state not in self._agent.testcount.keys():   # assign default val
            # print("missing test count, assigning")
            self._agent.testcount[state] = 1
        execnt = self._agent.testcount[state]
        epc = str(time.mktime(datetime.today().timetuple())).split(".")[0]
        wrcurs = self.cnct.cursor()
        if state not in self._state2wss.keys():
            wss = self.find_wss(wrcurs, state)      # kludge
            if wss != -1:
                self._state2wss[state] = wss
        if state not in self._state2wss.keys():
            # print("State " + str(state) + " not in " +
            #       str(self._state2wss.keys()))
            # create a new row in the DB
            wssinsstr = """
            INSERT INTO weighted_strategy_set (StrategySetID,
             WeightSummaryNum) VALUES ({0}, {1})
            """.format(self.StratSetId, state)
            # print(wssinsstr)
            wrcurs.execute(wssinsstr)
            wssid = wrcurs.lastrowid
            self.cnct.commit()
            agvinsstr = """
            INSERT INTO agent_value (WeightedStrategySetID, WinRate,
             ExecCnt, UpdateEpoch) VALUES ({0}, {1}, {2}, {3})
            """.format(wssid, winrt, execnt, epc)
            # print(agvinsstr)
            wrcurs.execute(agvinsstr)
            self.setstate2wgtstratset(state, wssid)
        else:
            wssid = self._state2wss[state]
            agvupdstr = """
            UPDATE agent_value 
            SET 
                WinRate = {0},
                ExecCnt = {1},
                UpdateEpoch = {3}
            WHERE WeightedStrategySetID = {2}
            """.format(winrt, execnt, wssid, epc)
            # print(agvupdstr)
            wrcurs.execute(agvupdstr)
        self.cnct.commit()
        wrcurs.close()
        return(wssid)

    @property
    def player(self):
        return (self._plyr)

    @property
    def dbplayerboard(self):
        return(self._game.playerboard[self._plyrnum])

    @property
    def wgtdstratsetid(self):
        return (self._wgtdstratsetid)

    @property
    def state2wss(self):
        return (self._state2wss)

    def setNonAgentGrpId(self, grpid):
        """
        Assign player its strategies & weights.
        :param grpid: CompGrpId in competition_grp_member
        :return:
        """
        self._plyr = wcsp.WeightedComboStrategyPlayer(self.game,
                                                      self.dbplayerboard)
        self._grpid = grpid
        # print("Setting up player with group ID " + str(grpid))
        selstr = """
        SELECT
            s.StrategyTxt,
            s.StrategyID,
            wssm.WeightNum,
            wssm.WeightedStrategySetID,
            ssm.StrategySetID
        FROM competition_grp_member cgm
            JOIN weighted_strategy_set_member wssm
            ON cgm.WeightedStrategySetMemberId = wssm.WeightedStrategySetMemberID
            JOIN strategy_set_member ssm
            ON wssm.StrategySetMemberID = ssm.StrategySetMemberID
            JOIN strategy s
            ON ssm.StrategyID = s.StrategyID
        WHERE cgm.CompGrpId = {0}
        ORDER BY 3 DESC
        """.format(str(grpid))
        # print(selstr)
        curs = self.cnct.cursor(buffered=True)
        curs.execute(selstr)
        wgts = []
        for (strat, stratid, wgt, wssi, ssi) in curs:
            # print(strat)        # Need a strip on strings!
            # print(str(stratid))
            # print(str(wgt))
            # print("player " + str(grpid) + " has strategy " + strat.strip() + " at weight " + str(wgt))
            self._StratIds.append(stratid)
            self._plyr.addstratbystr(strat.strip())
            wgts.append(wgt)
            self._wgtdstratsetid = wssi
            self._StratSetId = ssi      # gets assigned too many times, but ok
        curs.close()
        self._plyr.weights = wgts
        # print("Strategy IDs: " + str(self._StratIds))


    def setStratSetId(self, stratsetid):
        """
        Pull the strategy set identifier
        :param stratsetid: strategy set ID in DB
        :return:
        """
        self._StratSetId = int(stratsetid)
        selstr = """
        SELECT
            ss.StrategySetTxt
        FROM strategy_set ss
        WHERE ss.StrategySetID = {0}
        """.format(stratsetid)
        curs = self.cnct.cursor()
        agstrats = None
        curs.execute(selstr)
        for agstrats in curs:
            agstrats = agstrats[0].strip()     # One return only
        curs.close()
        assert (agstrats is not None)
        # print("Testing agent strategy set " + agstrats)
        return (agstrats)


    def setupAgent(self, stratsetid, agent, plnum, assignvals, state2wss):
        if assignvals:
            agentstrats = self.setStratSetId(stratsetid)
            selstr = """
            SELECT
                av.WeightedStrategySetID,
                wss.WeightSummaryNum,
                av.WinRate,
                av.ExecCnt
            FROM agent_value av
                JOIN weighted_strategy_set wss
                ON av.WeightedStrategySetID = wss.WeightedStrategySetID
                /*JOIN strategy_set ss
                ON wss.StrategySetID = ss.StrategySetID*/
            WHERE wss.StrategySetID = {0}
            """.format(self.StratSetId)
            # print(selstr)
            # now fill in the agent's values, also saving the map from
            # the weight summary (in values) to the weighted strategy set ID.
            curs = self.cnct.cursor(buffered=True)
            # print("Reading & assigning agent values")
            curs.execute(selstr)
            for (wssid, wgts, winrt, execnt) in curs:
                # print(":".join(["   adding weights ", str(wgts), str(winrt),
                #                 str(execnt), str(wssid)]))
                agent.add_value(wgts, winrt, execnt)
                self.setstate2wgtstratset(wgts, wssid) # not DB assignment
            # print("Completed assigning agent values")
            curs.close()
        else:
            # for agstrat in agent.player.strategies:
            #     print("Strategy " + str(agstrat) + " is of type " + str(type(agstrat)))
            self._StratSetId = stratsetid   # avoid a DB call
            stratsstr = [(str(type(strat)).split(".")[1])[:-2]
                         for strat in agent.player.strategies]
            # print("Running for " + "+".join(stratsstr))
            agentstrats = "+".join(stratsstr)
            if state2wss is not None:
                self._state2wss = state2wss
        # print("assigning strategies " + agentstrats)
        agent.assign_player(self._game, self.dbplayerboard, agentstrats, plnum)
        self._agent = agent
        assert(self._agent is not None)
        self._plyr = agent.player

