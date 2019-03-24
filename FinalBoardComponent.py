import BoardComponent as brd


# Couldn't seem to find this... odd.
def rvrs(str2rv):
    retstr = ""
    for idx in range(len(str2rv), 0, -1):
        retstr += str2rv[idx-1]
    return (retstr)


class FinalBoardComponent(brd.BoardComponent):
    """
    FinalBoard - final stop for tiles.  This is called the "wall" in the game.
    Placing a tile on the board will result in a score.  At the end of the
    game, particular patterns on the board will result in further scores.
    >>> fb = FinalBoardComponent()
    >>> fb.place(0, 'R')
    1
    >>> fb.place(1, 'Y')
    2
    >>> fb.place(1, 'R')
    2
    >>> if not fb.canplace(1, 'Y'):
    ...    print("Can't put another yellow in row 1")
    Can't put another yellow in row 1
    >>> fb.place(0, 'K')
    4
    >>> fb.place(2, 'B')
    3
    >>> fb.place(4, 'B')
    1
    >>> print(fb.columns[2])
    ['R', 'Y', 'B', '-', '-']
    >>> print(fb.underrows[2])
    KWBYR
    >>> print(fb.undercolumns[3])
    KRYBW
    """

    colororder = "BYRKW"
    dimension = 5
    columnorder = colororder[0] + rvrs(colororder[1:])

    def __init__(self):
        super().__init__()
        # 5 rows, with each having 5 positions
        for rownum in range(FinalBoardComponent.dimension):
            for pos in range(FinalBoardComponent.dimension):
                self.rows[rownum].append('-')    # start empty
        # Calculate the potential column positions on the board by columns.
        self._underrows = []
        for ridx in range(FinalBoardComponent.dimension):
            str2add = ""
            for cidx in range(FinalBoardComponent.dimension):
                ordidx = (cidx - ridx) % FinalBoardComponent.dimension
                str2add += FinalBoardComponent.colororder[ordidx]
            self._underrows.append(str2add)
        self._undercols = []
        for cidx in range(FinalBoardComponent.dimension):
            str2add = ""
            for ridx in range(FinalBoardComponent.dimension):
                ordidx = (ridx - cidx) % FinalBoardComponent.dimension
                str2add += FinalBoardComponent.columnorder[ordidx]
            self._undercols.append(str2add)

    def __str__(self):
        retstr = ""
        for row in self.rows:
            for pos in row:
                retstr += pos
            retstr += "\n"
        return (retstr)

    @property
    def columns(self):
        colz = [[] for _ in range(FinalBoardComponent.dimension)]
        for ridx in range(len(self.rows)):
            for cidx in range(len(self.rows[ridx])):
                colz[cidx].append(self.rows[ridx][cidx])
        return (colz)

    @property
    def underrows(self):
        return (self._underrows)

    @property
    def undercolumns(self):
        return (self._undercols)

    def canplace(self, rownum, color):
        """
        Determine whether a given color can be placed in a specified row
        :param rownum: row number where tile is to be placed
        :param color: color of tile to be placed
        :return: True if color can be placed, False otherwise
        """
        return (not color in self.rows[rownum])

    def scoreplacedtile(self, rownum, colnum):
        """
        scoreplacedtile - report point value for placing a tile at a
        specific position.
        :param rownum: tile placed at row #
        :param colnum: tile placed at column #
        :return: score value
        """

        horiz = 0
        vert = 0
        # Check up, down, left, & right for connected neighbors.
        for idx in list(range(rownum-1, -1, -1)):   # up
            if self.rows[idx][colnum] != '-':
                vert += 1
            else:
                break
        for idx in list(range(rownum+1, FinalBoardComponent.dimension)): # down
            if self.rows[idx][colnum] != '-':
                vert += 1
            else:
                break
        for idx in list(range(colnum-1, -1, -1)):   # left
            if self.rows[rownum][idx] != '-':
                horiz += 1
            else:
                break
        for idx in list(range(colnum+1, FinalBoardComponent.dimension)): # right
            if self.rows[rownum][idx] != '-':
                horiz += 1
            else:
                break

        if horiz > 0:
            horiz += 1      # add for tile proper
        if vert > 0:
            vert += 1       # add for tile proper (yes, counts both ways)
        retval = horiz + vert
        if retval == 0:
            retval = 1      # always get at least 1 for solo tile

        return (retval)

    def place(self, rownum, color):
        """
        Put the specified color in the specified row.
        Appropriate color position varies by row.
        :param rownum: row number where tile is to be placed
        :param color: color of tile to be placed
        :return: score from placed tile
        """
        assert self.canplace(rownum, color)
        colnum = (FinalBoardComponent.colororder.find(color) + rownum) % \
                 FinalBoardComponent.dimension
        retval = self.scoreplacedtile(rownum, colnum)
        self.rows[rownum][colnum] = color
        return (retval)

    def rowfillcount(self, rownum):
        cnt = 0
        for tile in self.rows[rownum]:
            if tile != '-':
                cnt += 1
        return (cnt)

    def columnfillcount(self, colnum):
        cnt = 0
        for tile in self.columns[colnum]:
            if tile != '-':
                cnt += 1
        return (cnt)

    def counthorizrowcomplete(self):
        retval = 0
        for rownum in range(len(self.rows)):
            rowfull = self.rowfillcount(rownum) == FinalBoardComponent.dimension
            if rowfull:
                retval += 1
                continue
        return (retval)

    def horizrowcomplete(self):
        """
        horizrowcomplete - determine if a row is completely filled in.
        This signifies the end of the game.
        :return: boolean
        """
        return (self.counthorizrowcomplete() > 0)

    def finalscore(self):
        sc = 0
        # full horizontal rows are worth 2
        # full vertical columns are worth 7
        # complete color sets are worth 10
        colorcnt = {}
        colcnt = [0 for _ in range(FinalBoardComponent.dimension)]
        for row in self.rows:
            rowcnt = 0
            for idx in range(len(row)):
                if row[idx] != '-':
                    rowcnt += 1
                    colcnt[idx] += 1
                    colorcnt[row[idx]] = colorcnt.get(row[idx], 0) + 1
            if rowcnt == FinalBoardComponent.dimension:
                sc += 2
        for cnt in colcnt:
            if cnt == FinalBoardComponent.dimension:
                sc += 7
        for color in colorcnt.keys():
            if colorcnt[color] == FinalBoardComponent.dimension:
                sc += 10
        return(sc)

    def rowremainingcolors(self, rownum):
        # return a string with the colors still eligible to play in the row.
        str2ret = ""
        for tileidx in range(len(self.rows[rownum])):
            if self.rows[rownum][tileidx] == '-':
                str2ret += self.underrows[rownum][tileidx]
        return (str2ret)

    def columnremainingcolors(self, colnum):
        # return a string with the colors still eligible to play in the column.
        str2ret = ""
        for tileidx in range(len(self.columns[colnum])):
            if self.columns[colnum][tileidx] == '-':
                str2ret += self.undercolumns[colnum][tileidx]
        return (str2ret)

    def getrownum(self, columnnum, color):
        retval = None
        for idx in range(len(self._undercols[columnnum])):
            if self._undercols[columnnum][idx] == color:
                retval = idx
                break
        return (retval)

    def getcolumnnum(self, rownum, color):
        retval = None
        for cidx in range(len(self._underrows[rownum])):
            if self._underrows[rownum][cidx] == color:
                retval = cidx
                break
        return (retval)

if __name__ == "__main__":
   import doctest

   doctest.testmod()

    # fb = FinalBoardComponent()
    # print(str(fb.place(0, 'R')))    #    1
    # print(str(fb.place(1, 'Y')))    #    2
    # print(str(fb.place(1, 'R')))    #    2
    # if not fb.canplace(1, 'Y'):
    #     print("Can't put another yellow in row 1")
    # print(str(fb.place(0, 'K')))
    # print(str(fb.place(2, 'B')))
    # print(str(fb.place(4, 'B')))
    # print(fb)
