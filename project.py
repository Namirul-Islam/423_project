from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import numpy as np
import time
import math

screen_width = 800
screen_height = 700
coords_board = np.array([[int(screen_width*0.15)], [10], [1]])
radius = 5
startGame = False
circle_coords = np.array([[coords_board[0][0]+60], [coords_board[1][0]+radius], [1]])
translateVector = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
translateBoardLeft = np.array([[1, 0, -8], [0, 1, 0], [0, 0, 1]])
translateBoardRight = np.array([[1, 0, 8], [0, 1, 0], [0, 0, 1]])
reflectXaxis = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
reflectYaxis = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
board_width = 80
blocks = {}
block_width = 40
block_height = 15
paused = False
scaleFactor = 2
pauseScale = np.array([[scaleFactor, 0, 0], [0, scaleFactor, 0], [0, 0, 1]])
pauseBoxLeftUpCoord = np.array([[-5], [1], [1]])
pauseBoxRightUpCoord = np.array([[5], [1], [1]])
pauseBoxRightDownCoord = np.array([[5], [-1], [1]])
pauseBoxLeftDownCoord = np.array([[-5], [-1], [1]])
pauseBoxCoords = [pauseBoxLeftUpCoord, pauseBoxRightUpCoord, pauseBoxRightDownCoord, pauseBoxLeftDownCoord]
translatePauseCoords = np.array([[1, 0, screen_width//2], [0, 1, screen_height//2], [0, 0, 1]])
timesScaled = 5
reversed = True
score = 0
perblockPoint = 10
scoreHeight = 20
scoreWidth = 10
num_coords = (10, screen_height-10)
gameOver = False
gameOverBoxCoords = [((0+screen_width)//10, (screen_height*6)//10), 
                        (screen_width - (0+screen_width)//10, (screen_height*6)//10), 
                        (screen_width - (0+screen_width)//10, (screen_height*4)//10), 
                        ((0+screen_width)//10, (screen_height*4)//10)
                     ]

level = 1
num_blocks = 10
level_coords = (screen_width-10, screen_height-10)

def draw_points(x, y):
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()    

def iterate():
    glViewport(0, 0, screen_width, screen_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, screen_width, 0.0, screen_height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def zone0to1(x, y):
    return y, x

def zone1to0(x, y):
    return y, x
def zone0to2(x, y):
    return -y, x

def zone2to0(x, y):
    return y, -x

def zone0to3(x, y):
    return -x, y

def zone3to0(x, y):
    return -x, y

def zone0to4(x, y):
    return -x, -y

def zone4to0(x, y):
    return -x, -y

def zone0to5(x, y):
    return -y, -x

def zone5to0(x, y):
    return -y, -x

def zone0to6(x, y):
    return y, -x

def zone6to0(x, y):
    return -y, x

def zone0to7(x, y):
    return x, -y

def zone7to0(x, y):
    return x, -y

def zone0(x, y):
    return x, y

def findZone(a, b):
    dy = b[1] - a[1]
    dx = b[0] - a[0]

    if dx >= 0:
        if dy >= 0:
            if abs(dx) >= abs(dy):
                return 0
            else:
                return 1
        else:
            if abs(dx) >= abs(dy):
                return 7
            else:
                return 6
    else:
        if dy >= 0:
            if abs(dx) >= abs(dy):
                return 3
            else:
                return 2
        else:
            if abs(dx) >= abs(dy):
                return 4
            else:
                return 5

def zone1to0(x, y):
    return y, x

def zone1to2(x, y):
    return -x, y

def zone1to3(x, y):
    return -y, x

def zone1to4(x, y):
    return -y, -x

def zone1to5(x, y):
    return -x, -y

def zone1to6(x, y):
    return x, -y

def zone1to7(x, y):
    return y, -x

def draw_circle_in_zone1(r):
    x = 0
    y = r
    d_init = 1 - r
    points = []
    while(x<y):
        if(d_init >= 0):
            d_init = d_init + 2*x - 2*y + 5
            y = y - 1
        else:
            d_init = d_init + 2*x + 3

        points.append((x, y))
        x = x + 1

    return points

def draw_circle(r):
    values = draw_circle_in_zone1(r)
    all_points = values.copy()
    for value in values:
        all_points.append((zone1to0(value[0], value[1])))
        all_points.append((zone1to2(value[0], value[1])))
        all_points.append((zone1to3(value[0], value[1])))
        all_points.append((zone1to4(value[0], value[1])))
        all_points.append((zone1to5(value[0], value[1])))
        all_points.append((zone1to6(value[0], value[1])))
        all_points.append((zone1to7(value[0], value[1])))


    return all_points

def drawLine(x1, y1, x2, y2):
    if y2 < y1:
        x1, y1, x2, y2 = x2, y2, x1, y1
    zone_return = {0: zone0, 1: zone1to0, 2: zone2to0, 3: zone3to0, 4: zone4to0, 5: zone5to0, 6: zone6to0, 7: zone7to0}
    zone_transfer = {0: zone0, 1: zone0to1, 2: zone0to2, 3: zone0to3, 4: zone0to4, 5: zone0to5, 6: zone0to6, 7: zone0to7}
    zone = findZone((x1, y1), (x2, y2))
    new_coords = [zone_transfer[zone](x1, y1), zone_transfer[zone](x2, y2)]
    x1, y1 = new_coords[0]
    x2, y2 = new_coords[1]
    dy = y2 - y1
    dx = x2 - x1
    d_init = 2*dy - dx
    d_ne = 2*dy - 2*dx
    d_e = 2*dy
    while(x1 != x2 or y1 != y2):
        points = zone_return[zone](x1, y1)
        # print(points)
        draw_points(points[0], points[1])
        if(d_init > 0):
            d_init = d_init + d_ne
            y1 = y1 + 1
        else:
            d_init = d_init + d_e

        x1 = x1 + 1

    points = zone_return[zone](x2, y2)
    draw_points(points[0], points[1])
    # print(points)

def drawP(x, y):
    drawLine(x, y, x, y-50)
    drawLine(x, y, x+30, y)
    drawLine(x+30, y, x+30, y-25)
    drawLine(x+30, y-25, x, y-25)

def drawA(x, y):
    drawLine(x, y, x, y-50)
    drawLine(x, y, x+30, y)
    drawLine(x+30, y, x+30, y-50)
    drawLine(x, y-25, x+30, y-25)

def drawU(x, y):
    drawLine(x, y, x, y-50)
    drawLine(x+30, y, x+30, y-50)
    drawLine(x, y-50, x+30, y-50)

def drawS(x, y):
    drawLine(x, y, x+30, y)
    drawLine(x+30, y, x+30, y-15)
    drawLine(x, y, x, y-25)
    drawLine(x, y-25, x+30, y-25)
    drawLine(x+30, y-25, x+30, y-50)
    drawLine(x+30, y-50, x, y-50)
    drawLine(x, y-50, x, y-35)

def drawE(x, y):
    drawLine(x, y, x, y-50)
    drawLine(x, y, x+30, y)
    drawLine(x, y-25, x+30, y-25)
    drawLine(x, y-50, x+30, y-50)

def drawD(x, y):
    drawLine(x, y, x, y-50)
    drawLine(x, y, x+20, y)
    drawLine(x+20, y, x+30, y-10)
    drawLine(x+30, y-10, x+30, y-40)
    drawLine(x+30, y-40, x+20, y-50)
    drawLine(x+20, y-50, x, y-50)

def draw_zero(x, y, scoreWidth = scoreWidth, scoreHeight = scoreHeight):
    drawLine(x, y, x+scoreWidth, y)
    drawLine(x+scoreWidth, y, x+scoreWidth, y-scoreHeight)
    drawLine(x+scoreWidth, y-scoreHeight, x, y-scoreHeight)
    drawLine(x, y-scoreHeight, x, y)

def draw_one(x, y, scoreHeight = scoreHeight):
    drawLine(x, y, x, y-scoreHeight)

def draw_two(x, y, scoreWidth = scoreWidth, scoreHeight = scoreHeight):
    drawLine(x, y, x+scoreWidth, y)
    drawLine(x+scoreWidth, y, x+scoreWidth, y-(scoreHeight//2))
    drawLine(x+scoreWidth, y-(scoreHeight//2), x, y-(scoreHeight//2))
    drawLine(x, y-(scoreHeight//2), x, y-scoreHeight)
    drawLine(x, y-scoreHeight, x+scoreWidth, y-scoreHeight)

def draw_three(x, y, scoreWidth = scoreWidth, scoreHeight = scoreHeight):
    drawLine(x+scoreWidth, y, x+scoreWidth, y-scoreHeight)
    drawLine(x, y, x+scoreWidth, y)
    drawLine(x, y-(scoreHeight//2), x+scoreWidth, y-(scoreHeight//2))   
    drawLine(x, y-scoreHeight, x+scoreWidth, y-scoreHeight)

def draw_four(x, y, scoreWidth = scoreWidth, scoreHeight = scoreHeight):
    drawLine(x, y, x, y-(scoreHeight//2))
    drawLine(x, y-(scoreHeight//2), x+scoreWidth, y-(scoreHeight//2))
    drawLine(x+scoreWidth, y, x+scoreWidth, y-scoreHeight)

def draw_five(x, y, scoreWidth = scoreWidth, scoreHeight = scoreHeight):
    drawLine(x, y, x+scoreWidth, y)
    drawLine(x, y, x, y-(scoreHeight//2))
    drawLine(x+scoreWidth, y-(scoreHeight//2), x, y-(scoreHeight//2))
    drawLine(x+scoreWidth, y-(scoreHeight//2), x+scoreWidth, y-scoreHeight)
    drawLine(x, y-scoreHeight, x+scoreWidth, y-scoreHeight)

def draw_six(x, y, scoreWidth = scoreWidth, scoreHeight = scoreHeight):
    drawLine(x, y, x+scoreWidth, y)
    drawLine(x, y, x, y-scoreHeight)
    drawLine(x+scoreWidth, y-(scoreHeight//2), x, y-(scoreHeight//2))
    drawLine(x+scoreWidth, y-(scoreHeight//2), x+scoreWidth, y-scoreHeight)
    drawLine(x, y-scoreHeight, x+scoreWidth, y-scoreHeight)

def draw_seven(x, y, scoreWidth = scoreWidth, scoreHeight = scoreHeight):
    drawLine(x+scoreWidth, y, x+scoreWidth, y-scoreHeight)
    drawLine(x, y, x+scoreWidth, y)

def draw_eight(x, y, scoreWidth = scoreWidth, scoreHeight = scoreHeight):
    drawLine(x+scoreWidth, y, x+scoreWidth, y-scoreHeight)
    drawLine(x, y, x+scoreWidth, y)
    drawLine(x, y-(scoreHeight//2), x+scoreWidth, y-(scoreHeight//2))   
    drawLine(x, y-scoreHeight, x+scoreWidth, y-scoreHeight)
    drawLine(x, y, x, y-scoreHeight)

def draw_nine(x, y, scoreWidth = scoreWidth, scoreHeight = scoreHeight):
    drawLine(x+scoreWidth, y, x+scoreWidth, y-scoreHeight)
    drawLine(x, y, x+scoreWidth, y)
    drawLine(x, y-(scoreHeight//2), x+scoreWidth, y-(scoreHeight//2))   
    drawLine(x, y-scoreHeight, x+scoreWidth, y-scoreHeight)
    drawLine(x, y, x, y-(scoreHeight//2))

def buttons(key, x, y):
    global window, startGame, paused, pauseBoxCoords, timesScaled, radius, startGame, circle_coords, coords_board, gameOver, score, translateVector, blocks, level
    # print(key)
    if key == b'\x1b':
        glutDestroyWindow(window)
    else:
        if key == b' ' and startGame == False:
            startGame = True
            translateVector[0][2] = 2
            translateVector[1][2] = 1
        if key == b'p':
            paused = not paused
            pauseBoxLeftUpCoord = np.array([[-5], [1], [1]])
            pauseBoxRightUpCoord = np.array([[5], [1], [1]])
            pauseBoxRightDownCoord = np.array([[5], [-1], [1]])
            pauseBoxLeftDownCoord = np.array([[-5], [-1], [1]])
            timesScaled = 5
            pauseBoxCoords = [pauseBoxLeftUpCoord, pauseBoxRightUpCoord, pauseBoxRightDownCoord, pauseBoxLeftDownCoord]
        if key == b'n' and (gameOver==True or paused==True):
            coords_board = np.array([[int(screen_width*0.15)], [10], [1]])
            radius = 5
            startGame = False
            circle_coords = np.array([[coords_board[0][0]+60], [coords_board[1][0]+radius], [1]])
            gameOver = False
            paused = False
            score = 0
            level = 1
            translateVector = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            blocks = {}
            generate_blocks(num_blocks)
# Need to update translation vector

def keys(key, x, y):
    global startGame, coords_board, circle_coords, board_width
    if(paused == False and gameOver == False):
        if (key == GLUT_KEY_LEFT) and (coords_board[0][0] > 0):
            coords_board = np.matmul(translateBoardLeft, coords_board)
        elif key == GLUT_KEY_RIGHT and (coords_board[0][0] + board_width < screen_width):
            coords_board = np.matmul(translateBoardRight, coords_board)

        if(startGame == False):
            circle_coords = np.array([[coords_board[0][0]+60], [coords_board[1][0]+radius], [1]])

    glutPostRedisplay()

def blockScreen():
    global blocks
    for tileList in blocks:
        for tile in blocks[tileList]:
            i = 0
            while(i<block_height):
                drawLine(tileList*block_width, tile*block_height+i, (tileList+1)*block_width, tile*block_height+i)
                i += 1

    # for tileList in blocks:
    #     for tile in blocks[tileList]:
    #         glBegin(GL_QUADS)
    #         glVertex2f(tileList*block_width, tile*block_height)
    #         glVertex2f(tileList*block_width, (tile+1)*block_height)
    #         glVertex2f((tileList+1)*block_width, (tile+1)*block_height)
    #         glVertex2f((tileList+1)*block_width, tile*block_height)
    #         glEnd()

def updateScreen():
    global circle_coords, board_width, blocks, timesScaled, reversed, score, perblockPoint, num_coords, gameOver, num_blocks, radius, translateVector, coords_board, startGame, level
    time.sleep(0.001)
    if(circle_coords[1][0]+radius//2 <= 0):
        gameOver = True
    if(gameOver == True):
        for i in range(len(gameOverBoxCoords)):
            glColor3f(1.0, 0.0, 0.0)
            drawLine(gameOverBoxCoords[i][0], gameOverBoxCoords[i][1], gameOverBoxCoords[(i+1)%len(gameOverBoxCoords)][0], gameOverBoxCoords[(i+1)%len(gameOverBoxCoords)][1])
        
        final_score = str(score)
        total_width = 0
    
        for num in final_score:
            if num != "1":
                total_width += 50
            else:
                total_width += 10
        total_width -= 10
        score_coords = [gameOverBoxCoords[0][0] + (gameOverBoxCoords[1][0] - gameOverBoxCoords[0][0] - total_width)//2, gameOverBoxCoords[0][1]-25]
        numbers = {"0": draw_zero, "1": draw_one, "2": draw_two, "3": draw_three, "4": draw_four, "5": draw_five, "6": draw_six, "7": draw_seven, "8": draw_eight, "9": draw_nine}
        for num in final_score:
            glColor3f(1.0, 0.0, 0.0) 
            if num == "1":
                numbers[num](score_coords[0], score_coords[1], scoreHeight=100)
                score_coords[0] += 10
            else:
                numbers[num](score_coords[0], score_coords[1], scoreWidth=40, scoreHeight=100)
                score_coords[0] += 50

    if paused == True and gameOver == False:
        for i in range(len(pauseBoxCoords)):
            boxCoord1 = np.matmul(translatePauseCoords, pauseBoxCoords[i])
            boxCoord2 = np.matmul(translatePauseCoords, pauseBoxCoords[(i+1)%len(pauseBoxCoords)])
            glColor3f(0.0, 1.0, 0.0) 
            drawLine(boxCoord1[0][0], boxCoord1[1][0], boxCoord2[0][0], boxCoord2[1][0])

        if(timesScaled == 0):
            # width = pauseBoxCoords[1][0][0] - pauseBoxCoords[0][0][0]
            # height = pauseBoxCoords[0][1][0] - pauseBoxCoords[3][1][0]
            coords = np.matmul(translatePauseCoords, pauseBoxCoords[0])
            x_coord = coords[0][0]
            y_coord = coords[1][0] 
            start_coords = [x_coord+40, y_coord-5]
            letters = {"P": drawP, "A": drawA, "U": drawU, "S": drawS, "E": drawE, "D": drawD}
            text ="PAUSED"
            for letter in text:
                letters[letter](start_coords[0], start_coords[1])
                start_coords[0] += 40

        if(timesScaled > 0):
            for i in range(len(pauseBoxCoords)):
                pauseBoxCoords[i] = np.matmul(pauseScale, pauseBoxCoords[i])

            timesScaled -= 1



    numbers = {"0": draw_zero, "1": draw_one, "2": draw_two, "3": draw_three, "4": draw_four, "5": draw_five, "6": draw_six, "7": draw_seven, "8": draw_eight, "9": draw_nine}
    string_score = str(score)
    current_coords = list(num_coords)
    for num in string_score:
        glColor3f(0.0, 1.0, 0.0) 
        numbers[num](current_coords[0], current_coords[1])
        if num == "1":
            current_coords[0] += 10
        else:
            current_coords[0] += scoreWidth+10

    string_level = str(level)
    current_level_coords = list(level_coords)
    for num in string_level:
        if num == "1":
            current_level_coords[0] -= 10
        else:
            current_level_coords[0] -= (scoreWidth+10)

    for num in string_level:
        glColor3f(0.0, 0.0, 1.0) 
        numbers[num](current_level_coords[0], current_level_coords[1])

        if num == "1":
            current_level_coords[0] += 10
        else:
            current_level_coords[0] += (scoreWidth+10)
        

    if( (circle_coords[0][0] + radius >= screen_width) or (circle_coords[0][0] - radius <= 0) ):
        translateVector[:, 2] = np.matmul(reflectYaxis, translateVector[:, 2])
    
    # Reflect along x axis if at screen edge
    if(circle_coords[1][0] + radius >= screen_height):
        translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])

    # print(circle_coords[1][0], coords_board[1][0])
        # elif(circle_coords[0][0] - radius <= coords_board[0][0] + board_width  and circle_coords[0][0] >= coords_board[0][0]):
    glColor3f(0.8, 0.8, 0.8) #konokichur color set (RGB)
    if(paused == False and gameOver == False):
        circle_coords = np.matmul(translateVector, circle_coords)
    for i in range(coords_board[1][0]):
        drawLine(coords_board[0][0], coords_board[1][0]-i-1, coords_board[0]+board_width, coords_board[1]-i-1)
    glColor3f(0.8, 0.8, 0.8) #konokichur color set (RGB) 
    r = radius
    # values = draw_circle(r)
    # for value in values:
    #     draw_points(value[0]+circle_coords[0][0], value[1]+circle_coords[1][0])
    while r>0:
        values = draw_circle(r)
        for value in values:
            draw_points(value[0]+circle_coords[0][0], value[1]+circle_coords[1][0])
        r -= 1

    if(paused == False and gameOver == False):
        if(circle_coords[1][0] - radius <= coords_board[1][0] and startGame == True):
            if(circle_coords[0][0] + radius >= coords_board[0][0]  and circle_coords[0][0] <= coords_board[0][0] + board_width):
                translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])
                translateVector[0, 2] = (circle_coords[0][0] - ( coords_board[0][0] + board_width//2) ) // 10

            elif(circle_coords[0][0] - radius <= coords_board[0][0] + board_width  and circle_coords[0][0] >= coords_board[0][0]):
                translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])
                translateVector[0, 2] = (circle_coords[0][0] - ( coords_board[0][0] + board_width//2) ) // 10            
                

        if(translateVector[0][2] >= 0 and translateVector[1][2] >= 0):
            getx = math.floor(circle_coords[0][0]/block_width)
            nextx = getx + 1
            prevx = getx - 1

            first_y = blocks.get(getx)

            if(first_y != None):
                i = 0
                b = len(first_y)
                while i < b:
                    if(radius+circle_coords[1][0] <= (first_y[i]+1)*block_height and radius+circle_coords[1][0] >= first_y[i]*block_height):
                        first_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1

                if(len(first_y) == 0):
                    blocks.pop(getx)

            second_y = blocks.get(nextx)
            if(second_y != None):            
                i = 0
                b = len(second_y)
                while i < b:
                    if(radius+circle_coords[1][0] <= (second_y[i]+1)*block_height and radius+circle_coords[1][0] >= second_y[i]*block_height and radius+circle_coords[0][0]>=nextx*block_width):
                        second_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectYaxis, translateVector[:, 2])
                            reversed = True
                        score += perblockPoint
                        b -= 1
                    elif(-radius*math.sin(math.radians(135))+circle_coords[1][0] <= (second_y[i]+1)*block_height and -radius*math.sin(math.radians(135))+circle_coords[1][0] >= second_y[i]*block_height and radius+circle_coords[0][0]>=nextx*block_width):
                        second_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectYaxis, translateVector[:, 2])
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1

                if(len(second_y) == 0):
                    blocks.pop(nextx)

            third_y = blocks.get(prevx)
            if(third_y != None):
                i = 0
                b = len(third_y)
                while i < b:
                    if(radius*math.sin(math.radians(45))+circle_coords[1][0] >= third_y[i]*block_height and radius*math.sin(math.radians(45))+circle_coords[1][0] <= (third_y[i]+1)*block_height and -radius+circle_coords[0][0]>=prevx*block_width and -radius+circle_coords[0][0]<=(prevx+1)*block_width):
                        third_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])                    
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1

                if(len(third_y) == 0):
                    blocks.pop(prevx)

        elif(translateVector[0][2] < 0 and translateVector[1][2] >= 0):
            getx = math.floor(circle_coords[0][0]/block_width)
            nextx = getx + 1
            prevx = getx - 1

            first_y = blocks.get(getx)
            if(first_y != None):
                i = 0
                b = len(first_y)
                while i < b:
                    if(radius+circle_coords[1][0] <= (first_y[i]+1)*block_height and radius+circle_coords[1][0] >= first_y[i]*block_height):
                        first_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1

                if(len(first_y) == 0):
                    blocks.pop(getx)

            second_y = blocks.get(prevx)
            if(second_y != None):            
                i = 0
                b = len(second_y)

                while i < b:
                    if(radius+circle_coords[1][0] <= (second_y[i]+1)*block_height and radius+circle_coords[1][0] >= second_y[i]*block_height and circle_coords[0][0]-radius<=(prevx+1)*block_width):
                        second_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectYaxis, translateVector[:, 2])
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    elif(radius*math.sin(math.radians(225))+circle_coords[1][0] <= (second_y[i]+1)*block_height and radius*math.sin(math.radians(225))+circle_coords[1][0] >= (second_y[i])*block_height and circle_coords[0][0]-radius<=(prevx+1)*block_width):
                        second_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectYaxis, translateVector[:, 2])
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1


            third_y = blocks.get(nextx)
            if(third_y != None):
                i = 0
                b = len(third_y)
                while i < b:
                    if(radius*math.sin(math.radians(45))+circle_coords[1][0] >= third_y[i]*block_height and radius*math.sin(math.radians(45))+circle_coords[1][0] <= (third_y[i]+1)*block_height and radius+circle_coords[0][0]>=nextx*block_width and radius+circle_coords[0][0]<=(nextx+1)*block_width):
                        third_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])                    
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1

                if(len(third_y) == 0):
                    blocks.pop(prevx)

        elif(translateVector[0][2] > 0 and translateVector[1][2] <= 0):
            getx = math.floor(circle_coords[0][0]/block_width)
            nextx = getx + 1
            prevx = getx - 1

            first_y = blocks.get(getx)
            if(first_y != None):
                i = 0
                b = len(first_y)
                while i < b:
                    if(-radius+circle_coords[1][0] <= (first_y[i]+1)*block_height and -radius+circle_coords[1][0] >= first_y[i]*block_height):
                        first_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1

                if(len(first_y) == 0):
                    blocks.pop(getx)

            second_y = blocks.get(nextx)
            if(second_y != None):            
                i = 0
                b = len(second_y)
                while i < b:
                    if(-radius+circle_coords[1][0] <= (second_y[i]+1)*block_height and -radius+circle_coords[1][0] >= second_y[i]*block_height and radius+circle_coords[0][0]>=nextx*block_width):
                        second_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectYaxis, translateVector[:, 2])
                            reversed = True
                        score += perblockPoint
                        b -= 1
                    elif(radius*math.sin(math.radians(45))+circle_coords[1][0] <= (second_y[i]+1)*block_height and -radius*math.sin(math.radians(45))+circle_coords[1][0] >= second_y[i]*block_height and radius+circle_coords[0][0]>=nextx*block_width):
                        second_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectYaxis, translateVector[:, 2])
                            reversed = True
                        score += perblockPoint
                        b -= 1
                    else:
                        i += 1

                if(len(second_y) == 0):
                    blocks.pop(nextx)

            third_y = blocks.get(prevx)
            if(third_y != None):
                i = 0
                b = len(third_y)
                while i < b:
                    if(radius*math.sin(math.radians(225))+circle_coords[1][0] >= third_y[i]*block_height and radius*math.sin(math.radians(225))+circle_coords[1][0] <= (third_y[i]+1)*block_height and -radius+circle_coords[0][0]>=prevx*block_width and -radius+circle_coords[0][0]<=(prevx+1)*block_width):
                        third_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])                    
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1

                if(len(third_y) == 0):
                    blocks.pop(prevx)

        elif(translateVector[0][2] < 0 and translateVector[1][2] <= 0):
            getx = math.floor(circle_coords[0][0]/block_width)
            nextx = getx + 1
            prevx = getx - 1

            first_y = blocks.get(getx)
            if(first_y != None):
                i = 0
                b = len(first_y)
                while i < b:
                    if(-radius+circle_coords[1][0] <= (first_y[i]+1)*block_height and -radius+circle_coords[1][0] >= first_y[i]*block_height):
                        first_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1

                if(len(first_y) == 0):
                    blocks.pop(getx)

            second_y = blocks.get(prevx)
            if(second_y != None):            
                i = 0
                b = len(second_y)

                while i < b:
                    if(-radius+circle_coords[1][0] <= (second_y[i]+1)*block_height and -radius+circle_coords[1][0] >= second_y[i]*block_height and circle_coords[0][0]-radius<=(prevx+1)*block_width):
                        second_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectYaxis, translateVector[:, 2])
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    elif(radius*math.sin(math.radians(45))+circle_coords[1][0] <= (second_y[i]+1)*block_height and radius*math.sin(math.radians(45))+circle_coords[1][0] >= (second_y[i])*block_height and circle_coords[0][0]-radius<=(prevx+1)*block_width):
                        second_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectYaxis, translateVector[:, 2])
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1

            third_y = blocks.get(nextx)
            if(third_y != None):
                i = 0
                b = len(third_y)
                while i < b:
                    if(radius*math.sin(math.radians(225))+circle_coords[1][0] >= third_y[i]*block_height and radius*math.sin(math.radians(225))+circle_coords[1][0] <= (third_y[i]+1)*block_height and radius+circle_coords[0][0]>=nextx*block_width and radius+circle_coords[0][0]<=(nextx+1)*block_width):
                        third_y.pop(i)
                        if(reversed == False):
                            translateVector[:, 2] = np.matmul(reflectXaxis, translateVector[:, 2])                    
                            reversed = True
                        b -= 1
                        score += perblockPoint
                    else:
                        i += 1

                if(len(third_y) == 0):
                    blocks.pop(prevx)

    if(len(blocks.keys()) == 0):
        coords_board = np.array([[int(screen_width*0.15)], [10], [1]])
        radius = 5
        startGame = False
        circle_coords = np.array([[coords_board[0][0]+60], [coords_board[1][0]+radius], [1]])
        translateVector = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        num_blocks += 1
        level += 1
        generate_blocks(num_blocks)

    # print(radius)
    reversed = False
    glutPostRedisplay()

def showScreen():
    # global coords_board, radius
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    blockScreen()
    #call the draw methods here
    # Reflect along y axis if at screen edge
    updateScreen()
    glutSwapBuffers()

def generate_blocks(num_blocks):
    i = 0
    while(i < num_blocks):
        key = random.randint(0, (800//block_width)-1)
        temp = screen_height//block_height
        value = random.randint(temp-16, temp-8)
        if key not in blocks:
            blocks[key] = [value]
            i += 1
        else:
            if(value not in blocks[key]):
                blocks[key].append(value)
                i += 1
        
def generate_fixed_blocks(num_blocks):
    i = 0
    key = 0
    while(i < num_blocks):
        temp = screen_height//block_height
        value = random.randint(temp-16, temp-8)
        if key not in blocks:
            blocks[key] = [value]
            i += 1
        else:
            if(value not in blocks[key]):
                blocks[key].append(value)
                i += 1

# generate_fixed_blocks(8)
generate_blocks(num_blocks)
# print(math.sin(math.radians(135)))
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(screen_width, screen_height) #window size
glutInitWindowPosition(0, 0)
window = glutCreateWindow(b"Goriber DX Ball") #window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(buttons)
glutSpecialFunc(keys)
glutMainLoop()