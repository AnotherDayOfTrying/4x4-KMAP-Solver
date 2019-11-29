import pygame, sys
from pygame import *
import K_Map
import util
from K_Map import Encapsulate, Term
from random import randint

pygame.init()


KMAPs = []
table = [0,1,1,1,0,0,0,1,0,1,1,0,1,1,0,0]
table1 = [1,1,1,1,1,0,0,1,1,1,1,0,0,1,0,0]
table2 = [1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0]
table3 = [1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0]
table4 = [1,0,1,0,0,0,1,0,1,0,1,1,1,1,1,1]
table5 = [1,0,0,0,1,1,1,0,1,1,1,1,1,0,1,1]
table6 = [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0]
# table7 = [1,1,0,0,1,1,0,0,0,0,0,0,0,1,1,1]

tables = [table, table1, table2, table3, table4, table5, table6]

KMAPs = util.makeKMAP(tables)

screenx, screeny = util.screenDim(KMAPs)
screen = pygame.display.set_mode((screenx,screeny))


termlists = []
equations = []
for i in KMAPs:
    foo = util.solveKMAP(i)
    foo = list(foo)
    trees = util.makeOnesTree(foo)
    someset = set()
    for tree in trees:
        lit = []
        util.levelOrder(tree, lit, (tree.pos, ))
        someset = someset.union(set(lit))
    the_list = list(someset)
    the_list.sort(key = len, reverse = True)
    the_list = (list(map(util.ispossible, the_list)))

    printableTerms = util.minimize(foo,the_list)
    overlapingList = util.overlap(printableTerms)
    equations.append(util.createEquations(printableTerms))
    for turm in printableTerms:
        newcirclelist = []
        for thing in turm:
            for overlap in overlapingList:
                if thing == overlap[0]:
                    thickness = overlap[1]
                    overlap[1] -= 1

            newcirclelist.append(Encapsulate(screen, i, thing[0], thing[1], line = thickness))
        a = randint(50, 255)
        b = randint(50, 255)
        c = randint(50, 255)
        alpha = 255
        termlists.append(Term(Color(a ,b ,c, 55), newcirclelist))


equationFont = pygame.font.Font(pygame.font.match_font('trebuchetms'), 40)
otherFont =  pygame.font.Font(pygame.font.match_font('trebuchetms'), 20)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not pygame.key.get_pressed()[K_SPACE]:
            screen.fill((20,20,20))
            screen.blit(otherFont.render("Spacebar to display Equations", 1, (250,250,250)), (screen.get_width()-300, screen.get_height()-40))
            for i in range(len(KMAPs)):
                KMAPs[i].K_MAPdraw(screen)
                KMAPs[i].K_MAPfill(screen)

            for i in termlists:
                i.drawTerm()
            status = True
        else:
            y = 20
            funcName = 65
            screen.fill((20,20,20))
            for equation in equations:
                screen.blit(equationFont.render(chr(funcName) + " = " + " + ".join(equation), 1, (250,250,250)), (20, 40 + y))
                y += 60
                funcName += 1
    pygame.display.flip()
