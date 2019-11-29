import K_Map


def mixColor(colors):
    outColor = [0,0,0]
    for i in range(3):
        for j in range(len(colors)):
            outColor[i] += colors[j][i]
        outColor[i] = outColor[i]//len(colors)
    return outColor


def screenDim(KMAPs):
    y = (len(KMAPs)//5 +1) * 350
    if len(KMAPs) > 4:
        x = 4 * 350
    else:
        x = len(KMAPs) * 350
    return x, y

def makeKMAP(truthTables):
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

def solveKMAP(KMAP):
    cols = KMAP.cols
    somethinglist = []
    for row in range(4):
        for col in range(4):
            if cols[col][row] == 1:
                refCol = col
                refRow = row
                somethinglist.append(SideChecker(cols, refCol, refRow, {(refCol, refRow)}))
    for term in somethinglist:
        somethinglist[0] = somethinglist[0].union(term)
    # print( somethinglist[0])
    return somethinglist[0]

def SideChecker(cols, x, y, visited):
    if (x % 4, (y-1) % 4) not in visited and cols[x % 4][(y-1) % 4] == 1:
        visited.add((x %4, (y-1) %4))
        visited.union(SideChecker(cols, x % 4, (y-1 % 4), visited))
    if (x % 4, (y+1) % 4) not in visited and cols[x % 4][(y+1) % 4] == 1:
        visited.add((x %4, (y+1) %4))
        visited.union(SideChecker(cols, x % 4, (y+1 % 4), visited))
    if ((x+1) % 4, y % 4) not in visited and cols[(x+1) % 4][y % 4] == 1:
        visited.add(((x+1) %4, y %4))
        visited.union(SideChecker(cols, (x+1) % 4, (y % 4), visited))
    if ((x-1) % 4, y % 4) not in visited and cols[(x+1) % 4][y % 4] == 1:
        visited.add(((x+1) %4, y %4))
        visited.union(SideChecker(cols, (x+1) % 4, (y % 4), visited))
    return visited

def makeOnesTree(transOnes):
    trees = []
    for position in transOnes:
        tree = K_Map.One(position)
        trees.append(recursiveSoln(position, transOnes, tree, (position, )))
    return trees


def recursiveSoln(position, nextposition, starting, visited):
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
    # print(wraparoundX, wraparoundY, X, Y)
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
    minimizedlist = []
    for length in [16, 8, 4, 2, 1]:
        print(length)
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
                        print(ones)
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
    overlappintlist = []
    checkingList = [position for term in minimizedOnes for position in term]
    for position in checkingList:
        if position not in overlappintlist:
            if checkingList.count(position) > 1:
                 overlappintlist.append([position, checkingList.count(position)])

    return overlappintlist

def createEquations(minimizedOnes):
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

        print(collist)
        print(rowlist)
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

if __name__ == "__main__":
    K_Map.pygame.init()
    table = [1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0]
    # table = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    # table = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    tables = [table]
    KMAP = makeKMAP(tables)
    foo = solveKMAP(KMAP[0])
    foo = list(foo)
    trees = makeOnesTree(foo)
    someset = set()
    for tree in trees:
        lit = []
        levelOrder(tree, lit, (tree.pos, ))
        # print(lit)
        someset = someset.union(set(lit))
    the_list = list(someset)
    the_list.sort(key = len, reverse = True)
    print(the_list)
    the_list = (list(map(ispossible, the_list)))
    print(the_list)

    ok = minimize(foo,the_list)
    print(createEquations(ok))
    print(ok)
    # print(overlap(ok))

    # print(ispossible(((0, 3), (0, 0), (3, 0), (3, 3))))
