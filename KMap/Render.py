import pygame, sys
from pygame import *
from util import *
from K_Map import *
from random import randint

pygame.init()


truthtable = TruthTable()

def KMAPcalc(tables, KMAPs, screen):

    termlists = []
    equations = []
    for i in KMAPs:
        foo = findOnes(i)
        foo = list(foo)
        trees = makeOnesTree(foo)
        someset = set()
        for tree in trees:
            lit = []
            levelOrder(tree, lit, (tree.pos, ))
            someset = someset.union(set(lit))
        the_list = list(someset)
        the_list.sort(key = len, reverse = True)
        the_list = (list(map(ispossible, the_list)))

        printableTerms = minimize(foo,the_list)
        overlapingList = overlap(printableTerms)
        equations.append(createEquations(printableTerms))
        for turm in printableTerms:
            newcirclelist = []
            for thing in turm:
                thickness = 0
                for overlaps in overlapingList:
                    if thing == overlaps[0]:
                        thickness = overlaps[1]
                        overlaps[1] -= 1

                newcirclelist.append(Encapsulate(screen, i, thing[0], thing[1], line = thickness))
            a = randint(50, 255)
            b = randint(50, 255)
            c = randint(50, 255)
            alpha = 255
            termlists.append(Term(Color(a ,b ,c, 55), newcirclelist))
    return termlists, equations


equationFont = pygame.font.Font(pygame.font.match_font('trebuchetms'), 40)
otherFont =  pygame.font.Font(pygame.font.match_font('trebuchetms'), 20)
counter = 0
status = False
setup = False

screen = pygame.display.set_mode((100, 100))

while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if pygame.key.get_pressed()[K_SPACE]:
            counter += 1
            counter %= 3
            status = False

        if pygame.key.get_pressed()[K_a]:
            print("Added Table")
            truthtable.addcol()


        if counter == 1 and status is False:
            tables = truthtable.read()
            KMAPs = makeKMAP(tables)
            screenx, screeny = screenDim(KMAPs)
            screen = pygame.display.set_mode((screenx,screeny))
            termlists, equations = KMAPcalc(tables, KMAPs, screen)
            screen.fill((20,20,20))
            screen.blit(otherFont.render("Spacebar to display Equations", 1, (250,250,250)), (screen.get_width()-300, screen.get_height()-40))
            for i in range(len(KMAPs)):
                KMAPs[i].K_MAPdraw(screen)
                KMAPs[i].K_MAPfill(screen)

            for i in termlists:
                i.drawTerm()
            status = True

        elif counter == 2:
            y = 20
            funcName = 65
            screen.fill((20,20,20))
            for equation in equations:
                screen.blit(equationFont.render(chr(funcName) + " = " + " + ".join(equation), 1, (250,250,250)), (20, 40 + y))
                y += 60
                funcName += 1
        elif counter == 0:
            screen = pygame.display.set_mode((600, 600))
            screen.fill((20,20,20))
            truthtable.draw(screen)
            truthtable.typing(event)
        pygame.display.flip()
