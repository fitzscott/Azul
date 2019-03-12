class Player():
    """
    Player - human or computer making decisions about actions to take

    """
    def __init__(self, game, board):
        self._game = game
        self._playerboard = board

    @property
    def game(self):
        return (self._game)

    @property
    def board(self):
        return (self._playerboard)

    def taketurn(self):
        pass

