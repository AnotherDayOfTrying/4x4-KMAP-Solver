import sys
import pygame
import util

class InputBox():
    activeColor = (250, 250, 250)
    passiveColor = (20, 20, 20)
    errorColor = (255, 20, 20)
    def __init__(self, x, y, width, height, text = ''):
        self.rect = pygame.Rect(x, y, width ,height)
        self.text = text
        self.color = self.passiveColor
        self.font = pygame.font.Font(pygame.font.match_font('trebuchetms'), 20)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def typing(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.activeColor if self.active else self.passiveColor
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.width = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def error(self):
        self.color = self.errorColor


class TruthTable():
    x = 100
    y = 20
    def __init__(self):
        self.positon = (0,0)
        self.input = []
        self.cols = 1
        self.font = pygame.font.Font(pygame.font.match_font('trebuchetms'), 40)
        list = []
        for i in range(16):
            self.y += 30
            list.append(InputBox(self.x, self.y, 30, 30))
        self.input.append(list)
        self.y = 50

    def addcol(self):
        list = []
        self.cols += 1
        self.x += 30
        for i in range(16):
            list.append(InputBox(self.x, self.y, 30, 30))
            self.y += 30
        self.y = 50
        self.input.append(list)

    def draw(self, screen):
        function_name = 65
        pygame.draw.line(screen, (250, 250, 250), (100, 50), (30 + self.x, 50), 3)
        pygame.draw.line(screen, (250, 250, 250), (100, 50), (100, 50 + 30 * 16), 3)
        for i in range(self.cols):

            screen.blit(self.font.render(chr(function_name), 1, (250,250,250)), (100 + 30 * i, 10))
            function_name += 1
        for input in self.input:
            for inp in input:
                inp.draw(screen)

    def typing(self, event):
        for input in self.input:
            for inp in input:
                inp.typing(event)

    def read(self):
        list = []
        for input in self.input:
            indiv_list = []
            for inp in input:
                indiv_list.append(int(inp.text))
            list.append(indiv_list)
        return list


class K_MAP(object):
    # Karnaugh Map
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
    # Object to draw around selected positions
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
    # Contain several encapsuals to create terms
    def __init__(self, color, EncapList):
        self.color = color
        self.term = EncapList
        self.overlapSet = set()

    def drawTerm(self):
        for Encapsual in self.term:
            Encapsual.color = self.color
            Encapsual.EncapDraw([i for i in self.term if Encapsual is not i])


class One(object):
    # Used to create the ones level order tree
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
