import K_Map


def screenDim(KMAPs):
    """ screenDim(KMAPs)
    Args - KMAPs : list of KMAPs
    Returns - the screen dimensions for rendering (x, y)
    """
    y = (len(KMAPs)//5 +1) * 350
    if len(KMAPs) > 4:
        x = 4 * 350
    else:
        x = len(KMAPs) * 350
    return x, y


def makeKMAP(truthTables):
    """ makeKMAP(truthTables)
    Args - truthTables : truthtable columns in list form
    Returns - KMAPs : list of KMAP objects
    """
    x = 0
    y = 0
    funcName = 65
    counter = 0
    KMAPs = []
    for table in truthTables:
        KMAPs.append(K_Map.K_MAP(table,chr(funcName), (x, y)))
        funcName += 1
        x += 350
        counter += 1
        if counter % 4 == 0:
            y += 350
            x = 0
    return KMAPs


def findOnes(KMAP):
    """ solveKMAP(KMAP)
    Args - KMAP: the KMAP class
    Returns - List of the position of all ones (row, col)
    """
    oneslist = []
    cols = KMAP.cols
    for row in range(4):
        for col in range(4):
            if cols[row][col] == 1:
                oneslist.append((row, col))
    return oneslist


def makeOnesTree(transOnes):
    """ makeOnesTree(transOnes)
    Args - the ones positions
    Returns - the tree
    """
    trees = []
    for position in transOnes:
        tree = K_Map.One(position)
        trees.append(recursiveSoln(position, transOnes, tree, (position, ))) # tuple, so that each branch has it's unique visited
    return trees


def recursiveSoln(position, nextposition, starting, visited):
    """ recursiveSoln(position, nextpostion, starting, visited)
    Args: - position: current position (row, col)
            nextpostion: the next position (row, col)
            starting: Ones Tree
            visited: tuple of visited ones
    Returns:
    """
    pos = ((position[0] - 1)%4, position[1])
    if pos in nextposition and pos not in visited:

        starting.left = K_Map.One(pos)
        starting.left.level = starting.level + 1
        starting.left = recursiveSoln(pos, nextposition, starting.left, visited + (pos, ))

    pos = ((position[0] + 1)%4, position[1])
    if pos in nextposition and pos not in visited:
        starting.right = K_Map.One(pos)

        starting.right.level =  starting.level + 1
        starting.right = recursiveSoln(pos, nextposition, starting.right, visited + (pos, ))

    pos = (position[0], (position[1] + 1) % 4)
    if pos in nextposition and pos not in visited:
        starting.down = K_Map.One(pos)

        starting.down.level  =  starting.level + 1
        starting.down = recursiveSoln(pos, nextposition, starting.down, visited + (pos, ))


    pos = (position[0], (position[1]- 1) % 4)
    if pos in nextposition and pos not in visited:
        starting.up = K_Map.One(pos)

        starting.up.level =  starting.level + 1
        starting.up = recursiveSoln(pos, nextposition, starting.up, visited + (pos, ))

    return starting

def levelOrder(tree, possible, path):
    """ levelOrder(tree, possible, path):
    Traverses the tree by level order
    """
    levels = [1,2,4,8,16]
    if tree.down is not None:
        levelOrder(tree.down, possible, path + ((tree.down.pos , )))
    if tree.up is not None:
        levelOrder(tree.up, possible, path + ((tree.up.pos , )))
    if tree.right is not None:
        levelOrder(tree.right, possible, path + (tree.right.pos , ))
    if tree.left is not None:
        levelOrder(tree.left, possible, path + (tree.left.pos , ))

    if tree.level in levels:
        possible.append(path)

def ispossible(possibility):
    """ ispossible(possibility)
    Args - possibility : a single term
    Returns - possibility : determines if the term is possible
    """
    minX = 3
    maxX = 0
    minY = 3
    maxY = 0
    wraparoundX = True
    wraparoundY = True
    for position in possibility:
        if position[0] < minX:
            minX = position[0]
        if position[0] > maxX:
            maxX = position[0]
        if position[1] < minY:
            minY = position[1]
        if position[1] > maxY:
            maxY = position[1]
        if position[0] == 1 or position[0] == 2:
            wraparoundX = False
        if position[1] == 1 or position[1] == 2:
            wraparoundY = False
    X = abs(minX - maxX) + 1
    Y = abs(minY - maxY) + 1
    if wraparoundX is True and wraparoundY is False and X % 3 != 0 and Y % 3 != 0:
        for y in range(Y):
            if (minX, minY+y) not in possibility:
                return None
        return possibility
    if wraparoundY is True and wraparoundX is False and X % 3 != 0 and Y % 3 != 0:
        for x in range(X):
            if (minX + x, minY) not in possibility:
                return None
        return possibility
    if wraparoundX is True and wraparoundY is True:
        if (2,2)  not in possibility:
            return possibility
    else:
        for x in range(X):
            for y in range(Y):
                if (minX + x,minY + y) not in possibility:
                    return None
    return possibility


def minimize(ones, possibleTerms):
    """ minimize(ones, possibleTerms)
    Args - ones : posiition of ones
           possibleTerms : list of all possible terms
    Returns - minimizedlist : Gives the solution terms
    """
    minimizedlist = []
    for length in [16, 8, 4, 2, 1]:
        for term in possibleTerms:
            if term is None:
                continue
            minTerm = True
            for position in term:
                if position not in ones:
                    minTerm = False
            # Go through 5 times, prefering the largest, first Essential prime implicants
            if minTerm is True and len(term) == length:
                minimizedlist.append(term)
                for position in term:
                    if position in ones:
                        ones.remove(position)
            # If some ones left over, find the biggest prime implicant until solved
            minTerm = False
            for position in term:
                if position in ones:
                    minTerm = True
            if minTerm is True and len(term) == length:
                minimizedlist.append(term)
                for position in term:
                    if position in ones:
                        ones.remove(position)

    return minimizedlist


def overlap(minimizedOnes):
    """ overlap(minimizedOnes)
    Args - minimizedOnes : The solution to the Karnaugh map
    Returns - overlappinglist : List of the coords that overlap (row, col)
    """
    overlappintlist = []
    checkingList = [position for term in minimizedOnes for position in term]
    for position in checkingList:
        if position not in overlappintlist:
            if checkingList.count(position) > 1:
                 overlappintlist.append([position, checkingList.count(position)])

    return overlappintlist


def createEquations(minimizedOnes):
    """ createEquations(minimizedOnes)
    Args - minimizedOnes: The solution to the Karnaugh Map
    Returns - equations: a tuple of equations, the equations are a string
    """
    equations = []

    for term in minimizedOnes:
        equation = ""
        rowlist = []
        collist = []
        for position in term:
            if position[0] not in collist:
                collist.append(position[0])
            if position[1] not in rowlist:
                rowlist.append(position[1])

        if len(collist) == 2:
            if 0 in collist and 1 in collist and 2 not in collist and 3 not in collist:
                equation += "a'"
            if 2 in collist and 3 in collist and 1 not in collist and 0 not in collist:
                equation += "a"
            if 1 in collist and 2 in collist and 0 not in collist and 3 not in collist:
                equation += "b"
            if 0 in collist and 3 in collist and 1 not in collist and 2 not in collist:
                equation += "b'"
        if len(collist) == 1:
            if 0 in collist and 1 not in collist and 2 not in collist and 3 not in collist:
                equation += "a'b'"
            if 1 in collist and 0 not in collist and 2 not in collist and 3 not in collist:
                equation += "a'b"
            if 2 in collist and 0 not in collist and 1 not in collist and 3 not in collist:
                equation += "ab"
            if 3 in collist and 0 not in collist and 1 not in collist and 2 not in collist:
                equation += "ab'"

        if len(rowlist) == 2:
            if 0 in rowlist and 1 in rowlist and 2 not in rowlist and 3 not in rowlist:
                equation += "c'"
            if 2 in rowlist and 3 in rowlist and 1 not in rowlist and 0 not in rowlist:
                equation += "c"
            if 1 in rowlist and 2 in rowlist and 0 not in rowlist and 3 not in rowlist:
                equation += "d"
            if 0 in rowlist and 3 in rowlist and 1 not in rowlist and 2 not in rowlist:
                equation += "d'"
        if len(rowlist) == 1:
            if 0 in rowlist and 1 not in rowlist and 2 not in rowlist and 3 not in rowlist:
                equation += "c'd'"
            if 1 in rowlist and 0 not in rowlist and 2 not in rowlist and 3 not in rowlist:
                equation += "c'd"
            if 2 in rowlist and 0 not in rowlist and 1 not in rowlist and 3 not in rowlist:
                equation += "cd"
            if 3 in rowlist and 0 not in rowlist and 1 not in rowlist and 2 not in rowlist:
                equation += "cd'"

        equations.append(equation)

    return equations


# if __name__ == "__main__":
#     K_Map.pygame.init()
#     table = [1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0]
#     # table = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#     # table = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#     tables = [table]
#     KMAP = makeKMAP(tables)
#     foo = findOnes(KMAP[0])
#     foo = list(foo)
#     trees = makeOnesTree(foo)
#     someset = set()
#     for tree in trees:
#         lit = []
#         levelOrder(tree, lit, (tree.pos, ))
#
#         someset = someset.union(set(lit))
#     the_list = list(someset)
#     the_list.sort(key = len, reverse = True)
#
#     the_list = (list(map(ispossible, the_list)))
#
#
#     ok = minimize(foo,the_list)
#     print(ok)
