import sys
import mysql.connector
import random
import time
import dbcfg
import DBPlayerInfo as dbpi
import TestWgtAgentDyn1 as twad
import Game as g
import WeightAgent as wa

class TestWgtAgentDB1():
    """

    """
    def __init__(self, compgrp, iters, agentstrats=None, maxwgt=None,
                 incr=None, alpha=None, epsilon=None, cr8_spc=True,
                 adj_alpha=True):
        self._compgrp = compgrp
        self._iters = iters
        self._agentstrats = agentstrats
        if maxwgt is None:
            self._maxwgt = 5
        else:
            self._maxwgt = maxwgt
        if incr is None:
            self._incr = 1
        else:
            self._incr = incr
        if alpha is None:
            self._alpha = 0.5
        else:
            self._alpha = alpha
        if epsilon is None:
            self._epsilon = 0.2
        else:
            self._epsilon = epsilon
        self._cr8spc = cr8_spc
        self._adjalpha = adj_alpha
        self._cnct = None
        self._plyrz = []
        self._dbplyrz = []
        self._game = None
        self._agent = None
        self._compgrpids = []
        self._agentplnum = None
        self._state = None
        self._state2wss = {}

    @property
    def agent(self):
        return (self._agent)
    
    @agent.setter
    def agent(self, val):
        self._agent = val
        
    def startup(self):
        self._cnct = mysql.connector.connect(**dbcfg.dbcon)

    def shutdown(self):
        self._cnct.close()

    def setupgame(self):
        self._game = g.Game()
        self._game.loadtiles()
        self._dbplyrz = []
        # print(self._game)

    def getrandgrpids(self):
        # We only need to do this once per set, since the competition group is
        # static within a run of X games.
        if len(self._compgrpids) == 0:
            selstr = """
            SELECT
                cg.CompGrpId
            FROM competition_grp cg
            WHERE cg.SetNum = {0}
            """.format(self._compgrp)

            # print(selstr)
            curs = self._cnct.cursor()
            curs.execute(selstr)
            for grpid in curs:
                # print("group id " + str(grpid))
                self._compgrpids.append(int(grpid[0]))
            assert(len(self._compgrpids) > 0)
        return (self._compgrpids)

    def setupplayers(self, cnt=4):
        assert(self._game is not None)
        self._agentplnum = random.randint(0, cnt-1)
        if self.agent is None:
            self.agent = wa.WeightAgent(-1)
            assignvals = True
        else:
            assignvals = False

        grpids = self.getrandgrpids()
        lengrp = len(grpids)
        for plnum in range(cnt):
            dbp = dbpi.DBPlayerInfo(self._cnct, self._game, plnum)
            if plnum != self._agentplnum:
                grpid = grpids[random.randint(0, lengrp-1)]
                dbp.setNonAgentGrpId(grpid)
            else:
                dbp.setupAgent(self._agentstrats, self.agent, plnum,
                               assignvals, self._state2wss)
                # print(agent)
            # print(dbp.player)
            self._dbplyrz.append(dbp)

    def getdbpstate2wss(self):
        ret = None
        for plnum in range(len(self._dbplyrz)):
            s2w = self._dbplyrz[plnum].state2wss
            if s2w is not None and len(s2w.keys()) > 0:
                ret = s2w
                break
        return (ret)

    def saveGameData(self, runtime, winrz):
        """
        Log game statistics & results in MySQL tables
        :param runtime: start-to-finish time for game
        :param winrz: array of winner player numbers, or [-1] if it timed out
        :return:
        """
        if winrz[0] == -1:
            finished = "N"
        else:
            finished = "Y"
        insStats = """
        INSERT INTO game_stats (RunTimeSecs, UpdateTs, FinishFlg)
        VALUES ({0}, CURRENT_TIMESTAMP(), '{1}')
        """.format(runtime, finished)
        # print(insStats)
        wrcurs = self._cnct.cursor()
        wrcurs.execute(insStats)
        gameid = wrcurs.lastrowid
        self._cnct.commit()
        # figure out player ranks
        ranks = self._game.playerranks
        rnkinfo = {}
        plcnt = len(self._dbplyrz)
        for idx in range(plcnt):
            rnkinfo[ranks[idx][0]] = idx
        # print("rank info = " + str(rnkinfo))
        # now save the individual player performances
        for plnum in range(plcnt):
            plyr = self._dbplyrz[plnum]
            scor = plyr.dbplayerboard.score
            if plnum in winrz:
                winflg = "Y"
            else:
                winflg = "N"
            wssi = plyr.wgtdstratsetid
            if plnum in winrz:
                gamerank = 1
            else:
                gamerank = plcnt - int(rnkinfo[plnum])
            if plnum == self._agentplnum:
                state = self.agent.calc_state()
                # wssi = plyr.getstate2wgtstratset(state, self.agent)  # potential DB op
                # potential DB op
                # adjust agent values - reward 1 is best, 0 worst
                rwd = (4 - gamerank) * 1.0 / 3.0
                self.agent.update_vals(rwd)
                wssi = plyr.getstate2wgtstratset(self._state, self.agent)
            insRslts = """
            INSERT INTO game_results (GameId, PlayerPosNum,
                WeightedStrategySetId, ScoreCnt, RankNum, WinFlg)
                VALUES ({0}, {1}, {2}, {3}, {4}, '{5}')
            """.format(gameid, plnum+1, wssi, scor, gamerank, winflg)
            # print(insRslts)
            wrcurs.execute(insRslts)
        self._cnct.commit()
        wrcurs.close()

    def runXtimes(self, iters):
        # print("Running for comp grp set num " + str(self._compgrp))
        plcnt = 4
        self.startup()
        for gameno in range(iters):
            self.setupgame()
            self.setupplayers(plcnt)
            plyrz = [dbp.player for dbp in self._dbplyrz]
            # for plyr in plyrz:
            #     print(plyr)
            self._state = self.agent.take_action()
            gamestart = time.time()
            winrz = twad.rungame(plyrz, plcnt, self._game, gameno, gameno+1)
            currtime = time.time()
            self._state2wss = self.getdbpstate2wss()    # save state-to-WSS
            self.saveGameData(currtime - gamestart, winrz)
        self.shutdown()


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

    twadb = TestWgtAgentDB1(comp_grp, iters, stratset, maxwgt, incr, alpha,
                            epsilon, cr8_spc, adj_alpha)
    twadb.runXtimes(iters)

