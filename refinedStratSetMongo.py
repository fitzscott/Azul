import sys
import pymongo as pm
import dbmongocfg as dbcfg
import refineWeight as rw

class refinedStratSetMongo():
    """
    Take an existing strategy set and its best weight
    and produce a copied set  with the weights adjacent
    to the best weight.
    """
    def __init__(self, stratsetid, weight, offset, maxwgt):
        self._stratsetid = stratsetid
        self._weight = weight
        self._newstratsetid = stratsetid + offset
        self._maxwgt = maxwgt
        self._db = None
        self._strategies = None

    def connect(self):
        self._mongocon = pm.MongoClient(dbcfg.cnctstr)
        self._db = self._mongocon.azul    # database

    def disconnect(self):
        self._mongocon.close()

    def get_strategies(self):
        # Find the individual strategies in the strategy set
        oness = self._db.strategysets.find_one(
            {"strategysetid": self._stratsetid})
        self._strategies = [stratstr for stratstr in oness["strategies"]]

    def save_refined_strategy(self):
        self.get_strategies()
        # Save the new strategy set
        stratset = {"strategysetid": self._newstratsetid,
                    "strategies": self._strategies}
        print("Inserting " + str(stratset))
        self._db.strategysets.insert_one(stratset)
        # Get the refined set of weights
        nuwgts = rw.refine(str(self._weight), self._maxwgt)
        bloksiz = 1000
        avarr = []
        inscnt = 0
        for nuwgt in nuwgts:
            wgtstr = "".join(str(w) for w in nuwgt)
            agval = {"strategysetid": self._newstratsetid,
                     "strategies": self._strategies,
                     "weight": int(wgtstr), "winrate": 2.0,
                     "count": 0}
            avarr.append(agval)
            inscnt += 1
            if inscnt % bloksiz == 0:
                # print("Inserting set " + str(avarr))
                self._db.agentvalues.insert_many(avarr)
                avarr = []
        if len(avarr) > 0:
            # print("Inserting remainder " + str(avarr))
            self._db.agentvalues.insert_many(avarr)
        print("Inserted total agent values: " + str(inscnt))


if __name__ == "__main__":
    ssid = int(sys.argv[1])
    wgt = int(sys.argv[2])
    if len(sys.argv) > 3:
        offset = int(sys.argv[3])
    else:
        offset = 1000
    if len(sys.argv) > 4:
        maxwgt = int(sys.argv[4])
    else:
        maxwgt = 5

    rssm = refinedStratSetMongo(ssid, wgt, offset, maxwgt)
    rssm.connect()
    rssm.save_refined_strategy()
    rssm.disconnect()
