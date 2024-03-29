import pymongo as pm
import dbmongocfg as dbcfg
import sys

class LoadGameResults2Mongo():
    def __init__(self, flnm):
        self._flnm = flnm
        self._drv = None
        self._sess = None

    def connect(self):
        self._drv = pm.MongoClient(dbcfg.cnctstr)

    def disconnect(self):
        self._drv.close()

    def load2mongo(self, drop=True):
        self.connect()
        if drop:
            self._drv.azul.drop_collection("gameresults")
            print("collection gameresults dropped")
        clxn = self._drv.azul.gameresults
        savflnm = self._flnm.split("\\")[-1]
        fl = open(self._flnm)
        prevgame = ""
        playpos = -1
        cnt = 0
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
            clxn.insert_one({"gameid": gameid, "playerpos": playpos,
                             "score": scor, "winflag": winloss,
                             "strategysetid": strats})
            cnt += 1
            if (cnt % 100 == 0):
                print("inserted {0} records / {1} games".format(cnt, cnt // 4))
        fl.close()
        print("inserted {0} records / {1} games".format(cnt, cnt // 4))
        self.disconnect()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("usage: {0} gameResultsFile [dropFlag]".format(sys.argv[0]))
        sys.exit(-1)

    if len(sys.argv) > 2:
        dropFlg = sys.argv[2] == "1"
    else:
        dropFlg = True
    lss = LoadGameResults2Mongo(sys.argv[1])
    lss.load2mongo(dropFlg)
