# soduku solver

# game_engine.py

# define the grid
# define a complete list
Complete = range(1, 10)  # initially all cells can have any value
Possible = [[Complete for i in range(9)] for j in range(9)]
old_possible = [[Complete for i in range(9)] for j in range(9)]
CompleteLetters = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
lines = []

RESULT_SOLVED = 1
RESULT_CONFLICT = 2
RESULT_UNSOLVED = 3

def InitGame():
    global Possible, old_possible, lines
    Possible = []
    Possible = [[Complete for i in range(9)] for j in range(9)]
    old_possible = []
    old_possible = [[Complete for i in range(9)] for j in range(9)]


def LoadGame(difficulty):
    global lines
    # preset table
    lines = []

    if difficulty == 0:
        #Easy puzzle
        lines.append('568271-34')
        lines.append('--23-58-1')
        lines.append('----9-2-5')
        lines.append('756129348')
        lines.append('3-95641-7')
        lines.append('241783596')
        lines.append('1-5-3----')
        lines.append('6-49-87--')
        lines.append('89-652413')

    if difficulty == 1:
        #Medimum Puzzle
        lines.append('---------')
        lines.append('-3-8-9-7-')
        lines.append('6-8-2-1-4')
        lines.append('3--798--1')
        lines.append('--41-63--')
        lines.append('1--432--7')
        lines.append('8-7-4-5-3')
        lines.append('-6-3-7-2-')
        lines.append('---------')

    if difficulty == 2:
        #Harder Puzzle
        lines.append('--4-7----')
        lines.append('---8-----')
        lines.append('7---35-9-')
        lines.append('-7--9-6--')
        lines.append('4-91--8--')
        lines.append('--1--892-')
        lines.append('---517--6')
        lines.append('--3--2-7-')
        lines.append('------2-4')

    if difficulty == 3:
       #Very Hard
        lines.append('-7---3--2')
        lines.append('-1----9--')
        lines.append('---865-7-')
        lines.append('-----92--')
        lines.append('8-9---6-3')
        lines.append('--24-----')
        lines.append('-2-348---')
        lines.append('--1----2-')
        lines.append('3--5---6-')

    if difficulty == 4:
        # Very Very Hard
        lines.append('-2----7--')
        lines.append('--1--3---')
        lines.append('9---8--6-')
        lines.append('5-------3')
        lines.append('-7--6--4-')
        lines.append('---1--2--')
        lines.append('--3-7---5')
        lines.append('-4---9-8-')
        lines.append('6--2--1--')
    return lines

def RemoveGivenFromPossible(lines):
    global Possible
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            c = lines[y][x]
            if c != '-':
                n = int(c)
                Possible[y][x] = [n]


def PrintGrid():
    # print possible, if 1 element print the elemnt, if more than 1 print -
    global Possible
    for y in range(9):
        for x in range(9):
            if (x == 3) or (x == 6):
                print '|',
            if len(Possible[y][x]) == 1:
                print str(Possible[y][x][0]),
            else:
                print '-',
        print
        if (y == 2) or (y == 5):
            print('----------------------')
    print


def PossibleToString(row, col):
    s = ''
    count = 0
    for n in Possible[row][col]:
        s += str(n)
        count += 1
    # pad to size 9
    for t in range(9 - count):
        s += ' '
    return s


def OldPossibleToString(row, col):
    s = ''
    count = 0
    for n in old_possible[row][col]:
        s += str(n)
        count += 1
    # pad to size 9
    for t in range(9 - count):
        s += ' '
    return s


def PrintPossible():
    global Possible
    for row in range(9):
        for col in range(9):
            if (col == 3) or (col == 6):
                print '|',
            print PossibleToString(row, col),
        # print str(Possible[row][col]) + ',',
        print
        if (row == 2) or (row == 5):
            print('---------------------------------------------------------------------------------------------')
    print


def PrintOldPossible():
    for row in range(9):
        for col in range(9):
            if (col == 3) or (col == 6):
                print '|',
            print OldPossibleToString(row, col),
        # print str(Possible[row][col]) + ',',
        print
        if (row == 2) or (row == 5):
            print('---------------------------------------------------------------------------------------------')
    print


def GetRowList(row):
    # return list for given row, where cell value is known
    global Possible
    l = []
    for col in range(9):
        if len(Possible[row][col]) == 1:
            n = Possible[row][col]
            # print str(n[0]) + ',',
            l.extend(n)
    # print str(l)
    return l


def GetEntireRowList(row):
    # return list for given row
    global Possible
    l = []
    for col in range(9):
        n = Possible[row][col]
        l.append(n)
    # print str(l)
    return l


def GetColList(col):
    # return list for given column, where cell value is known
    global Possible
    l = []
    for row in range(9):
        if len(Possible[row][col]) == 1:
            n = Possible[row][col]
            l.extend(n)
    return l


def GetEntireColList(col):
    # return list for given column
    global Possible
    l = []
    for row in range(9):
        n = Possible[row][col]
        l.append(n)
    return l


def EliminateRowColMatches():
    found = False
    for row in range(9):
        r = set(GetRowList(row))
        for col in range(9):
            l = set(Possible[row][col])
            if len(l) > 1:
                s1 = l - r  # eliminiate other vaues in this row
                # print str(l) + '-' + str(r) + '=' + str(s1) + ' ',
                c = set(GetColList(col))
                s2 = s1 - c  # eliminiate other values in this col
                # print str(s1) + '-' + str(c) + '=' + str(s2) + ' ',
                if len(s2) > 0:
                    Possible[row][col] = list(s2)  # replace possible with what is left
                if len(Possible[row][col]) == 1:
                    Possible[row][col] = [list(s2)[0]]
                    print 'EliminateRowColMatches single at ' + str(row) + ',' + str(col) + ' value ' + str(Possible[row][col])
                    # print str(l) + '-' + str(r) + '-' + str(c) + '=' + str(s2)
                    found = True
    return found


def GetBoxStartPos(box):
    col = box % 3 * 3
    row = box / 3 * 3
    return col, row


def GetBoxList(box):
    # return list of numbers in given box, when they are known
    c, r = GetBoxStartPos(box)
    l = []
    for col in range(c, c + 3):
        for row in range(r, r + 3):
            if len(Possible[row][col]) == 1:
                n = Possible[row][col]
                l.extend(n)
    # print str(l)
    return l


def GetEntireBoxList(box):
    # return list of all entries in the given box
    c, r = GetBoxStartPos(box)
    l = []
    for col in range(c, c + 3):
        for row in range(r, r + 3):
            n = Possible[row][col]
            l.append(n)
    return l


def FillGivenMissingInBox(box, l):
    # given box number and list of known cells, fill in the unknown cell
    global Possible
    s = set(range(1, 10))  # 1 to 9 is all values possible
    missing = list(s - set(l))
    # find missing cell and load with missing
    c, r = GetBoxStartPos(box)
    for col in range(c, c + 3):
        for row in range(r, r + 3):
            if len(Possible[row][col]) > 1:
                Possible[row][col] = missing
                print 'FillMissingInBox ' + str(missing) + ' at ' + str(row) + ',' + str(col)
                return


def FillMissingInBox():
    # check if 1 cell missing in 3x3 box, if so, fill with missing value
    found = False
    for box in range(9):
        b = GetBoxList(box)
        if len(b) == 8:
            FillGivenMissingInBox(box, b)
            found = True
    return found


def EliminateValueFromBox(box, value):
    # take out the value from given box
    found = False
    c, r = GetBoxStartPos(box)
    for col in range(c, c + 3):
        for row in range(r, r + 3):
            # print str(Possible[row][col]) + ',' + str([value])
            snew = set(Possible[row][col]) - set([value])
            if len(snew) > 1:
                Possible[row][col] = list(snew)
                found = True
    return found


def EliminateSinglesInBox():
    # if any single possible in box, eliminiate this number from all entries in box
    found = False
    for box in range(9):
        blist = GetBoxList(box)
        for c in blist:
            f = EliminateValueFromBox(box, c)
            if f == True:
                found = True
    return found


def GetBoxListPosForNum(boxList, num, checkRow):
    # check each box if num is present
    # return list of row positions of the num, or '-1' if miss
    L = []
    for box in boxList:
        found = False
        c, r = GetBoxStartPos(box)
        cFound = 0
        rFound = 0
        for col in range(c, c + 3):
            for row in range(r, r + 3):
                if (len(Possible[row][col]) == 1) and (Possible[row][col][0] == num):
                    found = True
                    cFound = col
                    rFound = row
        if found == True:  # found num in box
            if checkRow == True:
                L.extend([rFound])
            else:
                L.extend([cFound])
        else:  # not found in box
            L.extend([-1])
    # print 'BoxList boxlist ' + str(boxList) + ' for num ' + str(num) + ' is ' + str(L)
    return L


def MissingAndPosInBoxList(L):
    # return number of missing numbers and position the single missing is at
    pos = 0
    missing = 0
    i = 0
    for c in L:
        if (c < 0):
            missing += 1
            pos = i
        i += 1
    # print 'MisingandPos list ' + str(L) + ' missing ' + str(missing) + ' pos ' + str(pos)
    return missing, pos


def FillMissingInHorizBox(box, num, rowList):
    # check if num is single in this row of the box
    global Possible
    # get col missing
    #       print 'FillMisHOR box ' + str(box) + ' ' + str(rowList)
    col, row = GetBoxStartPos(box)
    s = set(range(row, row + 3))
    rowSet = set(rowList) - set([-1])
    row = list(s - rowSet)[0]
    colsLeft = 3
    # if we can eliminiate 2 cols, the third col is where we fill in num
    for c in range(col, col + 3):
        L = GetColList(c)
        s = set([num]) - set(L)
        if (len(Possible[row][c]) == 1) or (len(s) == 0):
            colsLeft -= 1
        else:
            colCandidate = c  # could be the col we want
    if colsLeft == 1:
        print 'horiz box check put ' + str(num) + ' at ' + str(row) + ',' + str(colCandidate)
        Possible[row][colCandidate] = [num]
        return True
        # not found
    return False


def FillMissingInVertBox(box, num, colList):
    # check if num is single in this col of the box
    global Possible
    # get col missing
    #       print 'FillMisVER box ' + str(box) + ' ' + str(colList)
    col, row = GetBoxStartPos(box)
    s = set(range(col, col + 3))
    colSet = set(colList) - set([-1])
    col = list(s - colSet)[0]
    rowsLeft = 3
    # if we can eliminiate 2 rows, the third row is where we fill in num
    for r in range(row, row + 3):
        L = GetRowList(r)
        s = set([num]) - set(L)
        #               print 'set ' + str(s) + ' L ' + str(L)
        if (len(Possible[r][col]) == 1) or (len(s) == 0):
            rowsLeft -= 1
        else:
            rowCandidate = r  # could be the row we want
    if rowsLeft == 1:
        print 'vert box check put ' + str(num) + 'at ' + str(rowCandidate) + ',' + str(col)
        Possible[rowCandidate][col] = [num]
        return True
        # not found
    return False


def CheckNumbersInBoxes():
    for num in range(1, 10):
        #       for num in range(4,5):
        # horizontal boxes check, value 1
        for box in range(0, 9, 3):
            boxList = range(box, box + 3)
            # print 'CheckNIB boxlist ' + str(boxList)
            L = GetBoxListPosForNum(boxList, num, True)
            nbrMissing, position = MissingAndPosInBoxList(L)
            if nbrMissing == 1:
                if FillMissingInHorizBox(boxList[position], num, L) == True:
                    return True
        # vertical boxes check value 1
        for box in range(3):
            boxList = [box, box + 3, box + 6]
            L = GetBoxListPosForNum(boxList, num, False)
            nbrMissing, position = MissingAndPosInBoxList(L)
            if nbrMissing == 1:
                if FillMissingInVertBox(boxList[position], num, L) == True:
                    return True
    # more than 1 missing in row boxes, can't find position for num
    return False


def EliminateListFromRow(row, l):
    global Possible
    rlist = GetEntireRowList(row)
    for col in range(9):
        s2 = set(rlist[col]) - set(l)
        old = Possible[row][col]
        if len(s2) > 0:
            Possible[row][col] = list(s2)
            if set(old) != set(Possible[row][col]):
                print 'EliminateListFromRow=' + str(row) + ' ' + str(rlist[col]) + '-' + str(l) + '=' + str(
                    Possible[row][col])


def EliminateListFromCol(col, l):
    global Possible
    clist = GetEntireColList(col)
    for row in range(9):
        s2 = set(clist[row]) - set(l)
        old = Possible[row][col]
        if len(s2) > 0:
            Possible[row][col] = list(s2)
            if set(old) != set(Possible[row][col]):
                print 'EliminateListFromCol=' + str(col) + ' ' + str(clist[row]) + '-' + str(l) + '=' + str(
                    Possible[row][col])


def EliminateListFromBox(box, l):
    global Possible
    col, row = GetBoxStartPos(box)
    for r in range(row, row + 3):
        for c in range(col, col + 3):
            old = set(Possible[r][c])
            s2 = old - set(l)
            if len(s2) > 0:
                Possible[r][c] = list(s2)
                if set(old) != s2:
                    print 'EliminateListFromBox=' + str(box) + ' ' + str(old) + '-' + str(l) + '=' + str(Possible[r][c])


def GetMatchedForOrder(l, order):
    # order is 2,3 or 4 to find doubles, tripes and quads
    none = []
    common = []
    added = 0
    for i in range(0, len(l) - order + 1):
        common = set(l[i])
        added = 1
        for j in range(i + 1, len(l)):
            s2 = common | set(l[j])
            if len(s2) <= order:
                common = s2
                added += 1
            if (added >= order) and (len(common) == order):
                return common
    return none


def RemoveDoublesTriplesQuads(order):
    # if 2,3 or 4 possible match another 2 possible in row,col or box, elimimate from row,col.box
    for row in range(9):
        l = []
        rlist = GetEntireRowList(row)
        # print 'rlist is ' + str(rlist)
        for c in rlist:
            # print str(c)
            if (len(c) > 1) and (len(c) <= order):
                l.append(c)
        if len(l) > 0:
            matchedSet = GetMatchedForOrder(l, order)
            if len(matchedSet) > 0:
                EliminateListFromRow(row, matchedSet)
    for col in range(9):
        l = []
        clist = GetEntireColList(col)
        for c in clist:
            if (len(c) > 1) and (len(c) <= order):
                l.append(c)
        if len(l) > 0:
            matchedSet = GetMatchedForOrder(l, order)
            if len(matchedSet) > 0:
                EliminateListFromCol(col, matchedSet)
    for box in range(9):
        l = []
        blist = GetEntireBoxList(box)
        for c in blist:
            if (len(c) > 1) and (len(c) <= order):
                l.append(c)
        if len(l) > 0:
            matchedSet = GetMatchedForOrder(l, order)
            if len(matchedSet) > 0:
                EliminateListFromBox(box, matchedSet)


def Solved():
    # check if solved
    global Possible
    for col in range(9):
        for row in range(9):
            if len(Possible[col][row]) > 1:
                return False
    # did not return it is solved
    print 'Solved Puzzle!'
    return True


def Conflict():
    # return true if violoation in duplicates in row, column or box
    for row in range(9):
        rlist = GetRowList(row)
        if len(rlist) != len(set(rlist)):  # there is a duplicate
            print 'Conflict in row ' + str(row)
            return True
    for col in range(9):
        clist = GetColList(col)
        if len(clist) != len(set(clist)):  # there is a duplicate
            print 'Conflict in col ' + str(col)
            return True
    for box in range(9):
        blist = GetBoxList(box)
        if len(blist) != len(set(blist)):  # there is a duplicate
            print 'Conflict in box ' + str(box)
            return True
    return False  # no conflict


def SetUp():
    # set up game
    RemoveGivenFromPossible(lines)  # fill in known cells - cells given to us by user
    EliminateSinglesInBox()  # eliminate singles from box possiblities
    print 'ORGINAL PUZZLE:'
    PrintGrid()

def Solve():
    # main loop - runs through known solvers to try to solve
    # RESULT_SOLVED = 1
    # RESULT_CONFLICT = 2
    # RESULT_UNSOLVED = 3


    round = 0
    solved = False
    while (solved == False) and (round < 100):
        EliminateRowColMatches()
        FillMissingInBox()
        CheckNumbersInBoxes()
        EliminateSinglesInBox()
        # PrintPossible()
        RemoveDoublesTriplesQuads(2)
        RemoveDoublesTriplesQuads(3)
        RemoveDoublesTriplesQuads(4)
        if Solved() == True:
            return RESULT_SOLVED
        if Conflict() == True:
            return RESULT_CONFLICT
        round += 1
    # PrintPossible()
    print 'PUZZLE: - ' + str(round) + ' rounds'
    PrintGrid()
    return RESULT_UNSOLVED


def get_next_of_order(r, c, order):
    none = []
    for row in range(r, 9):
        for col in range(c, 9):
            if len(Possible[row][col]) == order:
                return row, col, Possible[row][col]
    return row, col, none


def GuessCell(row, col, num):
    # save possible, guess cell, try to solve, report results
    global old_possible
    global Possible
    print '** GUESS ' + str(num) + ' at [' + str(row) + ',' + str(col) + ']'
    # old_possible = Possible
    # print 'OLD POSSIBLE:'
    # PrintOldPossible()
    Possible[row][col] = [num]
    result = Solve()
    return result


def Revert():
    global Possible
    print '**** Revert'
    for row in range(9):
        for col in range(9):
            Possible[row][col] = old_possible[row][col]


def SaveOldPossible():
    global old_possible
    print '**** SaveOldPossible'
    for row in range(9):
        for col in range(9):
            old_possible[row][col] = Possible[row][col]


def Guess():
    # start wiht possible cells of size 2, guess values until solved
    global old_possible
    none = []
    order = 2
    row = col = 0
    SaveOldPossible()
    print 'GUESS OLD POSSIBLE:'
    PrintOldPossible()
    while (row < 8) and (col < 8):
        row, col, p = get_next_of_order(row, col, order)
        print '** next cell to guess ' + str(p) + ' at [' + str(row) + ',' + str(col) + ']'
        if p != none:
            for c in p:
                result = GuessCell(row, col, c)
                if result == RESULT_SOLVED:
                    return RESULT_SOLVED
                if result == RESULT_CONFLICT:
                    print 'POSSIBLE:'
                    PrintPossible()
                    print 'OLD POSSIBLE:'
                    PrintOldPossible()
                    Revert()
                    print 'AFTER REVERT:'
                    PrintPossible()
                if result == RESULT_UNSOLVED:
                    print 'Result unsolved'
                    SaveOldPossible()
                    print 'OLD POSSIBLE:'
                    PrintOldPossible()
                    break
    return RESULT_UNSOLVED


def DisplayResult(result):
    if result == RESULT_SOLVED:
        print 'SOLVED!'
        PrintGrid()
    if result == RESULT_UNSOLVED:
        print 'Could Not Solve Puzzle!'
        PrintPossible()

def GetSolvedLines():
    global Possible
    solved = []
    line = ''
    for y in range(9):
        for x in range(9):
            if len(Possible[y][x]) == 1:
                line += str(Possible[y][x][0])
            else:
                line += '-'
        solved.append(line)
        line = ''
    return solved


def SolvePuzzle():
    result = Solve()
    DisplayResult(result)
    if result != RESULT_SOLVED:
        result = Guess()
        return GetSolvedLines()
    DisplayResult(result)
    return GetSolvedLines()


def LoadGameLogicWithLines(clientLines):
    global lines
    print 'LoadgameLogicWithLines ' + str(clientLines)
    InitGame()
    lines = []
    for i in range(9):
        lines.append(clientLines[i])

if __name__ == "__main__":
    InitGame()
    l = LoadGame(1)
    SetUp()
    SolvePuzzle()

