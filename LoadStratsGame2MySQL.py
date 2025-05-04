import sys
import mysql.connector
import dbcfg

class LoadStratsGame2MySQL():
    """
    Stripped-down version of the relational model for Azul
    """
    def __init__(self, strats, res):
        self._cnct = None
        self._stratsflnm = strats
        # self._trunc = self._stratsflnm != "-"
        self._gameresflnm = res
        self._stratsids = {}

    def startup(self):
        self._cnct = mysql.connector.connect(**dbcfg.dbcon)

    def shutdown(self):
        self._cnct.close()

    def stdweight(self, strats):
        # We only want a max of 6 "heavy" weights, with the rest being 1.
        # So 9 would be 6 5 4 3 2 1 1 1 1 and
        #    7 would be 6 5 4 3 2 1 1 and
        #    4 would be 4 3 2 1.
        stratcnt = len(strats.split("+"))
        maxwgt = min(5, stratcnt)
        weights = [max(r, 1) for r in range(maxwgt, maxwgt - stratcnt, -1)]
        return ("".join([str(w) for w in weights]))

    def savestrats(self):
        wrcurs = self._cnct.cursor()
        truncstmt = "TRUNCATE TABLE strategy_set_gui"
        wrcurs.execute(truncstmt)
        print("table strategy_set_gui truncated")
        fl = open(self._stratsflnm)
        for ln in fl:
            flds = ln.strip().split(":")
            if len(flds) >= 7:
                (strats, winrt, cnt, z1, z1, z3, wgt) = flds
            else:
                strats = flds[0]
                wgt = self.stdweight(strats)
            insstmt = """
            INSERT INTO strategy_set_gui
                (StrategySetTxt, WeightSummaryNum) VALUES
                ('{0}', {1})""".format(strats, wgt)
            print(insstmt)
            wrcurs.execute(insstmt)
            stratid = wrcurs.lastrowid
            self._cnct.commit()
            self._stratsids[strats] = stratid
        print(str(self._stratsids))
        wrcurs.close()

    def savegameresults(self, trunc=True):
        wrcurs = self._cnct.cursor()
        if trunc:
            truncstmt = "TRUNCATE TABLE game_results_gui"
            wrcurs.execute(truncstmt)
            print("table game_results_gui truncated")
        fl = open(self._gameresflnm)
        cnt = 0
        prevgame = ""
        maxstratid = 1000000
        playpos = 0
        for ln in fl:
            flds = ln.strip().split()
            if len(flds) < 5:
                print("not enough records?: [{0}]".format(ln.strip()))
                continue
            gameid = flds[0]
            if gameid != prevgame:
                playpos = 1
                prevgame = gameid
            else:
                playpos += 1
            winloss = flds[1][0]
            strats = "+".join(flds[3:-4])
            scor = int(flds[-1])
            if strats not in self._stratsids.keys():
                self._stratsids[strats] = maxstratid
                maxstratid += 1
            stratid = self._stratsids[strats]
            insstmt = """
            INSERT INTO game_results_gui
                (GameId, PlayerPosNum, StrategySetID, ScoreCnt, WinFlg) VALUES
                ({0}, {1}, {2}, {3}, '{4}')""".format(gameid, playpos,
                                                      stratid, scor, winloss)
            # print(insstmt)
            wrcurs.execute(insstmt)
            cnt += 1
            if (cnt % 100 == 0):
                self._cnct.commit()
                print("{0} game players / {1} games added".format(cnt, cnt // 4))
        self._cnct.commit()
        print("{0} game players / {1} games added".format(cnt, cnt // 4))
        wrcurs.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: {0} strategyFile resultsFile [truncate]".format(sys.argv[0]))
        sys.exit(-1)

    stratsfl = sys.argv[1]
    resfl = sys.argv[2]
    if len(sys.argv) > 3:
        truncflg = sys.argv[3] == "1"
    else:
        truncflg = True
    lssg2m = LoadStratsGame2MySQL(stratsfl, resfl)
    lssg2m.startup()
    lssg2m.savestrats()
    lssg2m.savegameresults(truncflg)
    lssg2m.shutdown()
