import sys
import TestWgtAgentDBMongo as twadm
import mysql.connector
import dbcfg as dbmys
import time
from datetime import datetime

class TestWgtAgentDBMongoMyS(twadm.TestWgtAgentDBMongo):
    """
    Much the same as the Mongo agent, but since we're using Atlas, there's a
    significantly restrictive disk space limitation, so we'll save game
    results to MySQL, instead.
    """

    def __init__(self, compgrp, iters, agentstrats=None, maxwgt=None,
                 incr=None, alpha=None, epsilon=None, cr8_spc=True,
                 adj_alpha=True):
        super().__init__(compgrp, iters, agentstrats, maxwgt, incr, alpha,
                         epsilon, cr8_spc, adj_alpha)

    def startup(self):
        super().startup()
        self._myscnct = mysql.connector.connect(**dbmys.dbcon)

    def shutdown(self):
        super().shutdown()
        self._myscnct.close()

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
        wrcurs = self._myscnct.cursor()
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
                rwd = (4 - gamerank) * 1.0 / 3.0
                self.agent.update_vals(rwd)
                wssi = plyr.getstate2wgtstratset(int(self.state), self.agent)
            insRslts = """
            INSERT INTO game_results_mongo (GameId, PlayerPosNum,
                WeightedStrategySetId, StrategySetId, ScoreCnt, RankNum,
                 WinFlg) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, '{6}')
            """.format(gameid, plnum + 1, wssi, plyr.StratSetId, scor,
                       gamerank, winflg)
            # print(insRslts)
            wrcurs.execute(insRslts)
        self._myscnct.commit()
        wrcurs.close()
            # clxn.insert_one({"gameid": gameid, "playerpos": plnum+1,
            #                  "score": scor, "playerrank": gamerank,
            #                  "winflag": winflg,
            #                  "strategysetid": plyr.StratSetId})


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

    twadb = TestWgtAgentDBMongoMyS(comp_grp, iters, stratset, maxwgt, incr,
                                   alpha, epsilon, cr8_spc, adj_alpha)
    twadb.runXtimes(iters)

