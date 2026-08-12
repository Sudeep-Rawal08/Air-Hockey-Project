from cmu_graphics import *
from cmu_cpcs_utils import almostEqual, testFunction
import math
'''
Author: Sudeep, Rawal
Creation Date: 11/18/2024
Last Modified: 12/9/2024
Project Description:
    This project is a game of air hockey. The program moves two
    players with 'wasd' and arrow keys. You score points by 
    getting the puck in the middle to the opponent's goal. It is possible to
    change the velocity of the puck by clicking on the bottom arrows
instructions:
    Use "wasd" to move the left player and the arrow keys to move the right.
    The goal of the game is to enter the puck, which starts in the middle, to
    the opposing goal. The game goes on indefinitely and can be paused by
    pressing "p". By holding the mouse down, the players will slowly speed up.
    when the mouse is released, they will immediately return to their base
    speed.
Credits: Brian Son
Updates: gave inspiration for how players should move and
how puck should be considered scored.
Rubric Items:
    Constant: 51
    Variable: 56
    Operator: 118
    Built-In Function: 190
    Helper Function:149
    if-elif-else: 157 to 165
    Nested Conditional: 167
    For Loop: 117
    While Loop: 185
    Break/Continue: 188
    f string: 99
    String Method: 97
    Shape 1: 120
    Shape 2: 122
    Shape 3: 143
    Key Event 1: 393
    Key Event 2: 447
    Mouse Event 1: 368
    Mouse Event 2: 388
    Timer Event: 474
    Motion 1: 224 to 260
    Motion 2: 262 to 269
'''
# start app(app.properties)
def onAppStart(app):
    #initializes the apps variables
    #important board stuff
    app.mouseIsHeld = False
    app.boardSizeX = 500
    app.boardSizeY = app.width/2
    app.gapDistance = 50
    app.arcRadiusX = 100
    app.arcRadiusY = 100
    app.player1Score = 0
    app.player2Score = 0
    app.paused = False
    app.arrowColor1 = 'black'
    app.arrowColor2 = 'black'
    app.maxMoveSpeed = 30
    #player 1 data fields
    app.moveSpeed1 = 10
    app.player1X = 80
    app.player1Y = app.height/2
    app.player1N = ' '
    app.player1NPlaceholder = ''
    app.player1R = 30
    app.movingUp1 = False
    app.movingDown1 = False
    app.movingLeft1 = False
    app.movingRight1 = False
    #player 2 data fields:
    app.moveSpeed2 = 10
    app.player2X = 520
    app.player2Y = app.height/2
    app.player2N = ' '
    app.player2NPlaceholder = ''
    app.player2R = 30
    app.movingUp2 = False
    app.movingDown2 = False
    app.movingLeft2 = False
    app.movingRight2 = False
    #puck Data Fields:
    app.puckX = app.width/2
    app.puckY = app.height/2
    app.puckRadius = 30
    app.angleHit = 0
    app.inMotion = False
    app.puckVelocityX = 0
    app.puckVelocityY = 0
    app.puckVelocityMult = 15
    app.lastHitBy = "None"
#draw graphics (redrawAll)
def redrawAll(app):
    #renders all the game elements: players, puck, the board, etc.
    if(app.player1N.isspace()):
        drawLabel('Select player one name: ', app.width/2, 100, size = 20)
        drawLabel(f'player one: {app.player1NPlaceholder}', app.width/2, 200, 
                                                                    size= 20)
        drawLabel('Press p to pause', app.width/2, 300, size = 20)
    elif(app.player2N.isspace()):
        drawLabel('Select player two name: ', app.width/2, 100, size = 20)
        drawLabel(f'player two: {app.player2NPlaceholder}', app.width/2, 200, 
                                                                    size= 20)
        drawLabel('Press p to pause', app.width/2, 300, size = 20)
    else:
        drawRect(0, 100, app.width, app.height/2, fill = None, border = 'black')
        drawRect(50,50,app.boardSizeX, app.boardSizeY, fill = 'white',
                                                               border = 'black')
        drawLine(50, 100, 50, 300, fill = 'red', lineWidth = 3)
        drawLine(550, 100, 550, 300, fill = 'red', lineWidth = 3)
        drawLabel(f'{app.player1N}: {app.player1Score}', (app.width)/2 - 
                                app.gapDistance, app.gapDistance/2, size = 20)
        drawLabel(f'{app.player2N}: {app.player2Score}', (app.width)/2 + 
                                app.gapDistance, app.gapDistance/2, size = 20)
        for i in range(3):
            x = 150 + (150 * i)
            drawLine(x, 50, x, 350, fill = 'blue')
        drawCircle(app.width/2, app.height/2, app.puckRadius, fill = 'white', 
                                                            border = 'black')
        drawArc(app.gapDistance, app.height/2, app.arcRadiusX, app.arcRadiusY, 
                                        -90, 180, fill = None, border = 'red')
        drawArc(app.width - app.gapDistance, app.height/2, app.arcRadiusX, 
                         app.arcRadiusY, 90, 180, fill = None, border = 'red')
        #player 1 drawing
        for i in range(1,4):
            radius1 = app.player1R/i
            drawCircle(app.player1X, app.player1Y, radius1, fill = 'red', 
                                                            border = 'black')
        #player 2 drawing
        for i in range(1,4):
            radius2 = app.player2R/i
            drawCircle(app.player2X, app.player2Y, radius2, fill = 'blue', 
                                                            border = 'black')
        #puck drawing
        drawCircle(app.puckX, app.puckY, app.puckRadius, fill = 'lavender', 
                                                            border = 'black')
        #puck Movement Speed Slider:
        drawRect(200, 360, 200, 40, border = 'black', fill = 'pink')
        drawRect(200, 360, 50, 40, fill = 'white', border = 'black')
        drawRect(350, 360, 50, 40, fill = 'white', border = 'black')
        drawRegularPolygon(225, 380, 14, 3, fill = app.arrowColor1,
                                                            rotateAngle = -90)
        drawRegularPolygon(375, 380, 14, 3, fill = app.arrowColor2, 
                                                             rotateAngle = 90)
        drawLabel(f'Puck Speed', 300, 380, size = 16)
#helper functions
def wherePuckHit(playerX, playerY, puckX, puckY):
    #calculates the angle at which the puck is hit based on its position
    #relative to the player using trig, then uses a while loop to get the exact
    #angle.
    quadrant1 = False
    quadrant2 = False
    quadrant3 = False
    quadrant4 = False
    if (playerY == puckY) and (playerX < puckX):
        return 0
    elif (playerY == puckY) and (playerX > puckX):
        return -math.pi
    elif (playerX == puckX) and (playerY < puckY):
        return -math.pi/2
    elif (playerX == puckX) and (playerY > puckY):
        return (math.pi/2)
    else:
        #quadrant 1
        if(puckY < playerY and puckX > playerX):
            tangentAngle = abs((puckY - playerY)/(puckX - playerX))
            quadrant1 = True
        #quadrant 2
        elif(puckY < playerY and puckX < playerX):
            tangentAngle = -abs((puckY - playerY)/(puckX - playerX))
            quadrant2 = True
        #quadrant 3
        elif(puckY > playerY and puckX < playerX):
            tangentAngle = abs((puckY - playerY)/(puckX - playerX))
            quadrant3 = True
        #quadrant 4
        elif(puckY > playerY and puckX > playerX):
            tangentAngle = -abs((puckY - playerY)/(puckX - playerX))
            quadrant4 = True
        guessAngle = 0
        #top right and bottom left quadrants
        if(quadrant1 or quadrant2):
         while guessAngle < 180:
            guessAngle += 0.1
            if guessAngle == 0 or guessAngle == 90 or guessAngle == 180:
                continue
            else:
                if(abs(tangentAngle - math.tan(guessAngle * math.pi / 180))
                                                                    <= 0.01):
                    print(f'GuessAngle: {guessAngle}')
                    print(tangentAngle)
                    print(f'quadrant1:{quadrant1}')
                    print(f'quadrant2:{quadrant2}')
                    print(f'quadrant3:{quadrant3}')
                    print(f'quadrant4:{quadrant4}')
                    return guessAngle * math.pi /180
        if(quadrant3 or quadrant4):
            while guessAngle > -180:
                guessAngle -= 0.1
                if guessAngle == 0 or guessAngle == -90 or guessAngle == 180:
                    continue
                else:
                    if(abs(tangentAngle - math.tan(guessAngle * math.pi / 180))
                                                                    <= 0.01):
                        print(f'GuessAngle: {guessAngle}')
                        print(tangentAngle)
                        print(f'quadrant1:{quadrant1}')
                        print(f'quadrant2:{quadrant2}')
                        print(f'quadrant3:{quadrant3}')
                        print(f'quadrant4:{quadrant4}')
                        return guessAngle * math.pi /180
    return guessAngle
            
def distance(x1, y1, x2, y2):
    #gets distance from one point to another
    return math.sqrt((x2 -x1) ** 2 + (y2 - y1) ** 2)
#functions
def boundaries(app):
    #makes sure the puck cant go through board walls but can go through goal
    #confines the players to left and right space respectively.
    #also handles scoring for the puck
    if app.puckX - app.puckRadius <=app.gapDistance and (app.puckY + 
                app.puckRadius> app.width/2 or app.puckY - app.puckRadius< 100):
        app.puckVelocityX = -app.puckVelocityX
        app.puckX =app.gapDistance+ app.puckRadius
    if app.puckX - app.puckRadius < app.gapDistance and not (app.puckY + 
                app.puckRadius> app.width/2 or app.puckY - app.puckRadius< 100):
        app.player2Score += 1
        app.puckVelocityX = 0
        app.puckVelocityY = 0
        app.puckX = app.width/2
        app.puckY = app.height/2
        app.player1X = 80
        app.player1Y = app.height/2
        app.player2X = 520
        app.player2Y = app.height/2
    if app.puckX + app.puckRadius >= app.width -app.gapDistance and (app.puckY + 
                app.puckRadius> app.width/2 or app.puckY - app.puckRadius< 100):
        app.puckVelocityX = -app.puckVelocityX
        app.puckX = app.width - app.gapDistance - app.puckRadius
    if app.puckX + app.puckRadius > app.width - app.gapDistance and not (
                        app.puckY + app.puckRadius> app.width/2 or app.puckY - 
                                                        app.puckRadius< 100):
        app.player1Score += 1
        app.puckVelocityX = 0
        app.puckVelocityY = 0
        app.puckX = app.width/2
        app.puckY = app.height/2
        app.player1X = 80
        app.player1Y = app.height/2
        app.player2X = 520
        app.player2Y = app.height/2
    if app.puckY - app.puckRadius <=app.gapDistance:
        app.puckVelocityY = -app.puckVelocityY
        app.puckY = app.gapDistance + app.puckRadius
    if app.puckY + app.puckRadius >= app.boardSizeY +app.gapDistance:
        app.puckVelocityY = -app.puckVelocityY
        app.puckY = app.boardSizeY + app.gapDistance - app.puckRadius
    #player 1
    if app.player1X - app.player1R <=app.gapDistance:
        app.movingLeft1 = False 
    if app.player1X + app.player1R >=app.gapDistance+ app.boardSizeX/2:
        app.movingRight1 = False
    if app.player1Y - app.player1R <=app.gapDistance:
        app.movingUp1 = False
    if app.player1Y + app.player1R >= app.boardSizeY +app.gapDistance:
        app.movingDown1 = False
    
    #player2
    if app.player2X - app.player2R <= app.width/2:
        app.movingLeft2 = False 
    if app.player2X + app.player2R >= app.width -app.gapDistance:
        app.movingRight2 = False
    if app.player2Y - app.player2R <=app.gapDistance:
        app.movingUp2 = False
    if app.player2Y + app.player2R >= app.boardSizeY +app.gapDistance:
        app.movingDown2 = False
    
def puckMovement(app):
    #checks if either player hits the puck, then adds speed to the puck in the
    #corresponding angle by calling the method wherePuckHit.Also, while the puck
    #is moving, it slowly decreases its speed until it is no longer moving
    #player 1:
    distancePlayer1 = distance(app.player1X, app.player1Y, app.puckX, app.puckY)
    if distancePlayer1 <= app.puckRadius + app.player1R:
        app.inMotion = True
        angleHit = wherePuckHit(app.player1X,app.player1Y, app.puckX,app.puckY)
        app.puckVelocityX = math.cos(angleHit) * app.puckVelocityMult
        app.puckVelocityY = math.sin(angleHit) * app.puckVelocityMult
    #player 2:
    distancePlayer2 = distance(app.player2X, app.player2Y, app.puckX, app.puckY)
    if distancePlayer2 <= app.puckRadius + app.player2R:
        app.inMotion = True
        angleHit2=wherePuckHit(app.player2X, app.player2Y, app.puckX, app.puckY)
        app.puckVelocityX = math.cos(angleHit2) * app.puckVelocityMult
        app.puckVelocityY = math.sin(angleHit2) * app.puckVelocityMult
    if(app.inMotion):
        app.puckX += app.puckVelocityX
        app.puckY -= app.puckVelocityY
        app.puckVelocityX /= 1.01
        app.puckVelocityY /= 1.01
    if abs(app.puckVelocityY) < 0.6:
        app.puckVelocityY = 0
    if abs(app.puckVelocityX) < 0.6:
        app.puckVelocity = 0
    
def playerMovement(app):
    #uses wasd and arrow keys to control the players as well as updating the
    #puck's location when the player gets too close so that they do not
    #intersect
    #player 1
    distancePlayer1 = distance(app.player1X, app.player1Y, app.puckX,app.puckY)
    if(app.movingUp1):
        if (distancePlayer1 <= app.puckRadius + app.player1R) and (app.puckY < 
                                                                app.player1Y):
            app.puckY = app.player1Y - app.player1R - app.puckRadius
        else:
            app.player1Y -= app.moveSpeed1
    if(app.movingLeft1):
        if (distancePlayer1 <= app.puckRadius + app.player1R) and (app.puckX < 
                                                                app.player1X):
            app.puckX = app.player1X - app.player1R - app.puckRadius
        else:
            app.player1X -= app.moveSpeed1
    if(app.movingDown1):
        if (distancePlayer1 <= app.puckRadius + app.player1R) and (app.puckY > 
                                                                app.player1Y):
            app.puckY = app.player1Y + app.player1R + app.puckRadius
        app.player1Y += app.moveSpeed1
    if(app.movingRight1):
        if (distancePlayer1 <= app.puckRadius + app.player1R) and (app.puckX > 
                                                                app.player1X):
            app.puckX= app.player1X + app.puckRadius + app.player1R
        else:
            app.player1X += app.moveSpeed1
    #player 2
    distancePlayer2 = distance(app.player2X, app.player2Y, app.puckX,app.puckY)
    if(app.movingUp2):
        if (distancePlayer2 <= app.puckRadius + app.player2R) and (app.puckY < 
                                                                app.player2Y):
            app.puckY = app.player2Y - app.player2R - app.puckRadius
        else:
            app.player2Y -= app.moveSpeed2
    if(app.movingLeft2):
        if (distancePlayer2 <= app.puckRadius + app.player2R) and (app.puckX < 
                                                                app.player2X):
            app.puckX = app.player2X - app.player2R - app.puckRadius
        else:
            app.player2X -= app.moveSpeed2
    if(app.movingDown2):
        if (distancePlayer2 <= app.puckRadius + app.player2R) and (app.puckY > 
                                                                app.player2Y):
            app.puckY = app.player2Y + app.player2R + app.puckRadius
        app.player2Y += app.moveSpeed2
    if(app.movingRight2):
        if (distancePlayer2 <= app.puckRadius + app.player2R) and (app.puckX > 
                                                                app.player2X):
            app.puckX= app.player2X + app.puckRadius + app.player2R
        else:
            app.player2X += app.moveSpeed2
#main function
def main():
    #initializes and runs the app
    runApp(height = 400, width = 600)
#events
def onMousePress(app, mouseX, mouseY):
    #changes the velocity of the ball depending on which arrow is clicked
    #when the velocity is at its maximum or minimum, the corresponding arrow
    #turns gray
    #also triggers app.mouseIsHeld which works in onstep to slowly increase the
    #speed of each player until it reaches its given maxSpeed.
    app.mouseIsHeld = True
    if(mouseY <= app.height and mouseY >= 360):
        if(mouseX >= 200 and mouseX <= 250 and app.arrowColor1 == 'black'):
            app.puckVelocityMult -= 5
        if(mouseX >= 350 and mouseX <= 400 and app.arrowColor2 == 'black'):
            app.puckVelocityMult += 5
    if app.puckVelocityMult <= 5:
        app.arrowColor1 = 'gray'
    else:
        app.arrowColor1 = 'black'
    if app.puckVelocityMult >= 30:
        app.arrowColor2 = 'gray'
    else:
        app.arrowColor2 = 'black'
def onMouseRelease(app, mouseX, mouseY):
    #resets the effects of app.mouseIsHeld
    app.mouseIsHeld = False
    app.moveSpeed1 = 10
    app.moveSpeed2 = 10
def onKeyPress(app, key):
    key.lower()
    #pauses the game
    if key == 'p':
        app.paused = not app.paused
    #for player One: this sequence selects the players name without numbers or
    #symbols
    if(app.player1N.isspace()):
        if key.isalpha() and len(key) == 1:
            app.player1NPlaceholder += key
        if key == 'space':
            app.player1NPlaceholder += ' '
        if key == 'backspace':
            app.player1NPlaceholder = app.player1NPlaceholder[:-1:]
        elif key == 'enter' and len(app.player1NPlaceholder) > 0:
            app.player1N = app.player1NPlaceholder
    #player Two: works the same as sequence above but this time for player two
    elif(app.player2N.isspace()):
        if key.isalpha() and len(key) == 1:
            app.player2NPlaceholder += key
        if key == 'space':
            app.player2NPlaceholder += ' '
        if key == 'backspace':
            app.player2NPlaceholder = app.player2NPlaceholder[:-1:]
        elif key == 'enter' and len(app.player2NPlaceholder) > 0:
            app.player2N = app.player2NPlaceholder
    else:
        #player One: moving with reinforced boundaries
        if key == 'w':
            if (app.player1Y - app.player1R >app.gapDistance):
                app.movingUp1 = True
        if key == 'a':
            if(app.player1X - app.player1R >app.gapDistance):
                app.movingLeft1 = True
        if key == 's':
            if(app.player1Y + app.player1R < app.height -app.gapDistance):
                app.movingDown1 = True
        if key == 'd':
            if(app.player1X + app.player1R < app.width/2):
                app.movingRight1 = True
        #for player Two: moving with reinforced boundaries
        if key == 'up':
            if (app.player2Y - app.player2R >app.gapDistance):
                app.movingUp2 = True
        if key == 'left':
            if(app.player2X - app.player2R > app.width/2):
                app.movingLeft2 = True
        if key == 'down':
            if(app.player2Y + app.player2R < app.height -app.gapDistance):
                app.movingDown2 = True
        if key == 'right':
            if(app.player2X + app.player2R < app.width -app.gapDistance):
                app.movingRight2 = True

def onKeyRelease(app, key):
    #this allows for the player to hold the key to move more smoothly rather
    #than having to individually tap each key everytime.
    #for player One
    if key == 'w':
        app.movingUp1 = False
    if key == 'a':
        app.movingLeft1 = False
    if key == 's':
        app.movingDown1 = False
    if key == 'd':
        app.movingRight1 = False
    #for player two
    if key == 'up':
        app.movingUp2 = False
    if key == 'left':
        app.movingLeft2 = False
    if key == 'down':
        app.movingDown2 = False
    if key == 'right':
        app.movingRight2 = False

def onStep(app):
    if app.mouseIsHeld and app.moveSpeed1 < app.maxMoveSpeed:
        app.moveSpeed1 += 0.1
        app.moveSpeed2 += 0.1
    if not app.paused:
        playerMovement(app)
        boundaries(app)
        puckMovement(app)
main()
