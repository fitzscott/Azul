class BoardComponent():
    """
    BoardComponent - base class for the sub-boards that make up the area for
    the individual game players.

    """

    def __init__(self):
        # boards have 5 rows
        self._rows = [[], [], [], [], []]

    @property
    def rows(self):
        return (self._rows)

    def __str__(self):
        return ("generic board")
