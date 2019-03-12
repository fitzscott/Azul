import BoardComponent as brd

class PrepBoardComponent(brd.BoardComponent):
    """
    PrepBoard - preparatory board for landing tiles before sending them to the final
    board.  This is called "pattern lines" in the game.
    >>> import FinalBoardComponent as fb
    >>> import Penalty as p
    >>> fb1 = fb.FinalBoardComponent()
    >>> p1 = p.Penalty()
    >>> pb = PrepBoardComponent(fb1, p1)
    >>> x = fb1.place(0, 'R')
    >>> x = fb1.place(1, 'Y')
    >>> if pb.canplace(0, 'Y'):
    ...    print("Can place yellow in row 0")
    ...    pb.place(0, 'Y')
    Can place yellow in row 0
    True
    >>> if pb.canplace(0, 'R'):
    ...    print("Can place red in row 0")
    ...    pb.place(0, 'R')
    ... else:
    ...    print("No, row 0 already has a red - no placement")
    No, row 0 already has a red - no placement
    >>> x = pb.place(4, 'K')
    >>> x = pb.place(2, 'W')
    >>> x = pb.place(2, 'W')
    >>> x = pb.place(2, 'W')    # can only place 3 in row 2
    >>> if pb.canplace(2, 'W'):
    ...    if pb.place(2, 'W'):
    ...        print("Somehow added 4th W")
    ...    else:
    ...        print("4th W went to penalty line")
    4th W went to penalty line
    """

    def __init__(self, finalboard, penaltyboard):
        super().__init__()
        # 5 rows, with each having an increasing number of positions
        for rownum in range(5):
            for pos in range(rownum + 1):
                self.rows[rownum].append('-')    # start empty
        self._finalboard = finalboard
        self._penaltyboard = penaltyboard

    def __str__(self):
        retstr = ""
        for row in self.rows:
            retstr += " " * (5 - len(row))
            for pos in row:
                retstr += pos
            retstr += "\n"
        return (retstr)

    def canplace(self, rownum, color):
        """
        Check whether both the final board and the preparatory board can accept
        a tile of a given color.  If the final board already has the color in
        that row, it cannot be added to the preparatory board.  If the prep
        board already has a tile of another color, the tile cannot be
        added to the prep board.  If the prep board is full, the overflow
        will be sent to the penalty board.
        :param rownum: Row number to check for the tile color
        :param color: Tile color
        :return: Boolean
        """
        retval = True
        for pos in self.rows[rownum]:
            if pos != "-" and pos != color:
                retval = False
                break
        if not self._finalboard.canplace(rownum, color):
            retval = False
        return (retval)

    def rowfull(self, rownum):
        filled = 0
        for tile in self.rows[rownum]:
            if tile != '-':
                filled += 1
        # print("filled is " + str(filled))
        return (filled == rownum+1)

    def place(self, rownum, color):
        """
        Place the color tile in the specified row, if possible.
        :param rownum: add tile to this row number
        :param color: add tile of this color
        :return: True if added; False if it goes to penalty line
        """
        # Check canplace & throw an exception if it's False
        retval = False
        if not self.canplace(rownum, color):
            self._penaltyboard.addtile(color)
            return (retval)
        if self.rowfull(rownum):
            # send the tile to the penalty line
            self._penaltyboard.addtile(color)
        else:       # put it in rightmost slot
            for slot in range(len(self.rows[rownum])-1, -1, -1):
                if self.rows[rownum][slot] == '-':
                    self.rows[rownum][slot] = color
                    retval = True
                    break
        return(retval)

    def score(self, rownum, box):
        """
        score - if the specified row is complete, send a tile to the final
        board and send the remainders to the box.
        :param rownum: row to score
        :param box: where extras go
        :return: score to be added to player's total
        """
        if not self.rowfull(rownum):
            retval = 0
        else:
            retval = self._finalboard.place(rownum, self.rows[rownum][0])
            for idx in range(len(self.rows[rownum])-1):
                box.addtile(self.rows[rownum][0])   # guaranteed same color
            for pos in range(rownum + 1):
                self.rows[rownum][pos] = '-'    # back to empty
        return(retval)

    def availableslots(self, rownum):
        slots = 0
        for tile in self.rows[rownum]:
            if tile == '-':
                slots += 1
        # print("filled is " + str(filled))
        return (slots)


if __name__ == "__main__":
   import doctest

   doctest.testmod()

