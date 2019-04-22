from itertools import permutations
import random

class Weight():
    """
    Handle weights assigned to strategies in strategy combinations.
    These weights will be unique integer weights.
    """

    def __init__(self, stratset):
        self._strategies = stratset

    def generateweights(self):
        numweights = len(self._strategies)
        perms = permutations(range(1, numweights+1))
        return([p for p in perms])

    def randweight(self):
        wgts = self.generateweights()
        choice = random.randint(0, len(wgts)-1)
        return (wgts[choice])


