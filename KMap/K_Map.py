import sys
import pygame
import util

class K_MAP(object):
    def __init__(self, truthCol, funcName, Pos):
        self.cols = [truthCol[0:4], truthCol[4:8], truthCol[12:16], truthCol[8:12]]
        self.__func = funcName
        self._color = (250, 250, 250)
        self.innerfont = pygame.font.Font(pygame.font.match_font('trebuchetms'), 40)
        self.outerfont = pygame.font.Font(pygame.font.match_font('trebuchetms'), 20)
        self.x_pos = Pos[0]
        self.y_pos = Pos[1]

        for col in self.cols:
            col[2], col[3] = col[3], col [2]

    def K_MAPdraw(self, screen):
        pygame.draw.line(screen, (250, 250, 250), (self.x_pos + 40, self.y_pos + 40), (self.x_pos + 90, self.y_pos + 90), 3)
        pygame.draw.line(screen, (250, 250 , 250), (self.x_pos +90, self.y_pos + 90), (self.x_pos + 290, self.y_pos + 90), 3)
        pygame.draw.line(screen, (250, 250 , 250), (self.x_pos +90, self.y_pos + 90), (self.x_pos + 90, self.y_pos + 290), 3)
        screen.blit(self.innerfont.render(self.__func, 1, (250, 250, 250)) , (self.x_pos + 5, self.y_pos + 5))
        screen.blit(self.outerfont.render("cd", 1, (250, 250, 250)) , (self.x_pos + 40, self.y_pos + 65))
        screen.blit(self.outerfont.render("ab", 1, (250, 250, 250)) , (self.x_pos + 65, self.y_pos + 40))
        x_pos = self.x_pos + 80
        y_pos = self.y_pos + 80
        counter = -1

        for i in range(4):
            x_pos += 45
            counter += 1
            coltext = self.outerfont.render("{0:02b}".format(counter ^ (counter >> 1)), 1, (250, 250, 250))
            coltextpos = coltext.get_rect(centerx = x_pos, centery =  y_pos)
            screen.blit(coltext, coltextpos)
        x_pos = self.x_pos + 70
        y_pos = self.y_pos + 90
        counter = -1
        for i in range(4):
            y_pos += 45
            counter += 1
            rowtext = self.outerfont.render("{0:02b}".format(counter ^ (counter >> 1)), 1, (250, 250, 250))
            rowtextpos = rowtext.get_rect(centerx = x_pos, centery = y_pos)
            screen.blit(rowtext, rowtextpos)

    def K_MAPfill(self, screen):
        x_pos = self.x_pos + 80
        for col in self.cols:
            x_pos += 45
            y_pos = self.y_pos + 80
            for row in col:
                y_pos += 45
                state = self.innerfont.render(str(row), 1, (250, 250, 250))
                statepos = state.get_rect(centerx = x_pos, centery = y_pos)
                screen.blit(state, statepos)

    def K_MAPget(self, x, y):
        return self.cols[x][y]

class Encapsulate(object):
    def __init__(self, screen, K_MAP, col, row, line = 2):
        self.K_MAP = K_MAP
        self.row = row
        self.col = col
        self.lineThickness = 2 +  line
        self.screen = screen
        self.color = (250, 250, 250)
        self.cols = [125, 170, 215, 260]
        self.rows = [125, 170, 215, 260]

    def EncapCheck(self, Encapsulate):
        besideSet = set()
        for encap in Encapsulate:
            y_check = encap.row
            x_check = encap.col
            if (self.row - y_check == -1) and self.col == x_check:
                besideSet.add("down")
            elif (self.row - y_check == 1) and self.col == x_check:
                besideSet.add("up")
            elif (self.col - x_check == -1) and self.row == y_check:
                besideSet.add("right")
            elif (self.col - x_check == 1)  and self.row == y_check:
                besideSet.add("left")
        for encap in Encapsulate:
            y_check = encap.row
            x_check = encap.col
            if self.row - y_check == 3 and self.col == x_check and "up" not in besideSet:
                besideSet.add("down")
            elif self.row - y_check == -3 and self.col == x_check and "down" not in besideSet:
                besideSet.add("up")
            elif self.col - x_check == 3 and self.row == y_check and "left" not in besideSet:
                besideSet.add("right")
            elif self.col - x_check == -3 and self.row == y_check and "right" not in besideSet:
                besideSet.add("left")
        return (besideSet)

    def EncapDraw(self, Encapsulate):
        drawingSet= {"up", "down", "left", "right"}
        encaplist = []
        ref_x = self.K_MAP.x_pos
        ref_y = self.K_MAP.y_pos
        # change to surfaces to allow for transparency

        drawingSet = drawingSet.intersection(self.EncapCheck(Encapsulate))
        if "up" not in drawingSet:
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]-20, ref_y + self.rows[self.row]-20), (ref_x + self.cols[self.col]+20, ref_y + self.rows[self.row]-20), self.lineThickness)
        else:
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]-20, ref_y + self.rows[self.row]-20), (ref_x + self.cols[self.col]-20, ref_y + self.rows[self.row]-25), self.lineThickness)
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]+20, ref_y + self.rows[self.row]-20), (ref_x + self.cols[self.col]+20, ref_y + self.rows[self.row]-25), self.lineThickness)

        if "left" not in drawingSet:
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]-20, ref_y + self.rows[self.row]+20), (ref_x + self.cols[self.col]-20, ref_y + self.rows[self.row]-20), self.lineThickness)
        else:
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]-20, ref_y + self.rows[self.row]-20), (ref_x + self.cols[self.col]-25, ref_y + self.rows[self.row]-20), self.lineThickness)
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]-20, ref_y + self.rows[self.row]+20), (ref_x + self.cols[self.col]-25, ref_y + self.rows[self.row]+20), self.lineThickness)

        if "down" not in drawingSet:
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]-20, ref_y + self.rows[self.row]+20), (ref_x + self.cols[self.col]+20, ref_y + self.rows[self.row]+20), self.lineThickness)
        else:
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]-20, ref_y + self.rows[self.row]+20), (ref_x + self.cols[self.col]-20, ref_y + self.rows[self.row]+25), self.lineThickness)
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]+20, ref_y + self.rows[self.row]+20), (ref_x + self.cols[self.col]+20, ref_y + self.rows[self.row]+25), self.lineThickness)


        if "right" not in drawingSet:
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]+20, ref_y + self.rows[self.row]+20), (ref_x + self.cols[self.col]+20, ref_y + self.rows[self.row]-20), self.lineThickness)
        else:
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]+20, ref_y + self.rows[self.row]+20), (ref_x + self.cols[self.col]+25, ref_y + self.rows[self.row]+20), self.lineThickness)
            pygame.draw.line(self.screen, self.color, (ref_x + self.cols[self.col]+20, ref_y + self.rows[self.row]-20), (ref_x + self.cols[self.col]+25, ref_y + self.rows[self.row]-20), self.lineThickness)


class Term(object):
    def __init__(self, color, EncapList):
        self.color = color
        self.term = EncapList
        self.overlapSet = set()

    def drawTerm(self):
        for Encapsual in self.term:
            Encapsual.color = self.color
            Encapsual.EncapDraw([i for i in self.term if Encapsual is not i])




class One(object):
    def __init__(self, pos):
        self.pos = pos
        self.down = None
        self.up = None
        self.right = None
        self.left = None
        self.level = 1
    def get_down(self):
        return self.down
    def get_up(self):
        return self.up
    def get_right(self):
        return self.right
    def get_left(self):
        return self.left
    def get_position(self):
        return self.pos
