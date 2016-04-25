"""
John Parreno and Seth Stoudenmier
---------------------------------
The code below is intended to produce a slight twist on the traditional Snake game.
It utilizes multple different classes in the main and also classes from other .py
files in order to make the entire game. All audio files used are documented in
_sound-details.txt and all sprite images that were not handmade are documented in
_sprite-details.txt. The file used for the background is background.txt.
"""
# import statements
import pygame

from OurSprite import *
from OurSpriteInventory import *
from SpriteTileMap import *

from random import randrange

# constants used throughout the code
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SPRITE_SIZE = 25
WIDTH = 800
HEIGHT = 600

"""
class Mongoose

properties:
x - x coordinate of the Mongoose
y - y coordinate of the Mongoose
screen - pygame screen used by the Mongoose
sprite - sprite that represents the Mongoose
barrierList - list of points that the mongoose is not able to pass through

behaviors:
init - initialize the characteristics of the Mongoose
getX - returns the x value for the Mongoose
getY - retuns the y value for the Mongoose
boundaryHit - determines if a boundary has been hit
directionToMove - determines direction to move the Mongoose
move - moves the mongoose to new location
draw - draws the mongoose on the screen
"""
class Mongoose:

    def __init__(self, x, y, screen, sprite, barrierList):
        self.x = x
        self.y = y
        self.screen = screen
        self.sprite = sprite
        self.directions = ["LEFT", "RIGHT", "UP", "DOWN"]
        self.barrierList = barrierList

    """
    Returns the x value of the mongoose.
    @return: x value of the mongoose
    """
    def getX(self):
        return self.x

    """
    Returns the y value of the mongoose.
    @return: y value of the mongoose
    """
    def getY(self):
        return self.y

    """
    Determines whether or not the adjusted x and y value cause a collision with
    a boundary.
    @param: change_x - the change in the x value
            change_y - the change in the y value
    @return: true if there is a collision; false otherwise
    """
    def boundaryHit(self, change_x, change_y):
        p = Point(self.x + change_x, self.y + change_y)
        if p in self.barrierList:
            return True
        return False

    """
    Determines a random direction to move the mongoose.
    @param: snake - the snake head so that the mongoose moves towards the snake
    @return: which direction the mongoose should move towards
    """
    def directionToMove(self, snake):
        directionChoices = []
        snakeX = snake.get_x()
        snakeY = snake.get_y()
        rand = randrange(0,2)
        if self.x < snakeX:
            directionChoices.append("RIGHT")
        elif self.x >= snakeX:
            directionChoices.append("LEFT")
        if self.y < snakeY:
            directionChoices.append("DOWN")
        elif self.y >= snakeY:
            directionChoices.append("UP")

        return directionChoices[rand]

    """
    Moves the mongoose to a new location.
    @param: snake - the head of the snake
    """
    def move(self, snake):
        direction = self.directionToMove(snake)
        x_change = 0
        y_change = 0
        while True:
            if direction == "LEFT":
                x_change = -25
                y_change = 0
            elif direction == "RIGHT":
                x_change = 25
                y_change = 0
            elif direction == "UP":
                x_change = 0
                y_change = -25
            elif direction == "DOWN":
                x_change = 0
                y_change = 25
            if not self.boundaryHit(x_change, y_change):
                self.x+= x_change
                self.y+= y_change
                break
            else:
                direction = self.directionToMove(snake)

    """
    Draws the mongoose onto the screen.
    """
    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))

"""
class Snake

properties:
x - x coordinate of the Snake
y - y coordinate of the Snake
numSegments - number of body parts
screen - pygame screen used by the Snake
headSpriteList - the sprites used to represent the different directions of the head
bodySprite - the sprite used to represent the body of the snake
barrierList - list of points that the mongoose is not able to pass through

behaviors:
init - initialize the characteristics of the Snake
move - moves the snake to a new location
get_bodyList - returns the list of body parts
get_headObj - returns the head of the snake
check_collision - checks to see if the snake has collided with any obstacles
draw_snake - draws the snake onto the screen
get_x - returns the x coordinate of the snake
get_y - returns the y coordinate of the snake
"""
class Snake:
    global SPRITE_SIZE
    global WIDTH
    global HEIGHT

    def __init__(self,x,y,numSegments,screen,headspriteList,bodysprite,barrierList):
        self.x = x
        self.y = y
        self.numSegments = numSegments
        self.screen = screen
        self.headspriteList = headspriteList
        self.bodysprite = bodysprite
        self.barrierList = barrierList
        self.bodyList = [SnakeBody(x,y)]
        for i in range(1,self.numSegments-1):
            self.bodyList.append(SnakeBody(x-i*SPRITE_SIZE,y))
    """
    Moves the snake.
    @param: direction - direction to move the snake
            grow - whether or not the snake should grow
    """
    def move(self,direction,grow):
        if (direction == "LEFT"):
            if not grow:
                self.bodyList.pop()
            self.bodyList.insert(0, SnakeBody((self.x-SPRITE_SIZE)%WIDTH,self.y))
            self.x = (self.x - SPRITE_SIZE) % WIDTH

        elif (direction == "RIGHT"):
            if not grow:
                self.bodyList.pop()
            self.bodyList.insert(0, SnakeBody((self.x+SPRITE_SIZE)%WIDTH,self.y))
            self.x = (self.x + SPRITE_SIZE) % WIDTH

        elif (direction == "UP"):
            if not grow:
                self.bodyList.pop()
            self.bodyList.insert(0, SnakeBody(self.x,(self.y-SPRITE_SIZE)%HEIGHT))
            self.y = (self.y - SPRITE_SIZE) % HEIGHT

        elif (direction == "DOWN"):
            if not grow:
                self.bodyList.pop()
            self.bodyList.insert(0, SnakeBody(self.x,(self.y+SPRITE_SIZE)%HEIGHT))
            self.y = (self.y + SPRITE_SIZE) % HEIGHT

    """
    Returns the list of snake body parts.
    @return: the list of body parts of the snake
    """
    def get_bodyList(self):
        return self.bodyList

    """
    Returns the head of the snake.
    @return: the head of the snake
    """
    def get_headObj(self):
        return self.bodyList[0]

    """
    Checks to see if the snake has collided with any of the obstacles (i.e. mongoose,
    lava, body).
    @param: mongooseList - list of existing mongooses
    @return: true if there is a collision; false otherwise
    """
    def check_collision(self, mongooseList):
        for i in range(1,len(self.bodyList)):
            if (self.bodyList[i].get_x() == self.x and self.bodyList[i].get_y() == self.y):
                return True

        for i in range(len(self.barrierList)):
            if (self.barrierList[i].get_x() == self.x and self.barrierList[i].get_y() == self.y):
                return True

        for m in mongooseList:
            if m.getX() == self.x and m.getY() == self.y:
                return True
##        if self.x < SPRITE_SIZE or self.x >= WIDTH - SPRITE_SIZE or self.y < SPRITE_SIZE or self.y >= HEIGHT - SPRITE_SIZE:
##            return True
        return False

    """
    Draw the snake onto the screen.
    @param: headDir - direction the head is moving
    """
    def draw_snake(self,headDir):
        if headDir == "UP":
            head = self.headspriteList[0]
        elif headDir == "DOWN":
            head = self.headspriteList[1]
        elif headDir == "LEFT":
            head = self.headspriteList[2]
        elif headDir == "RIGHT":
            head = self.headspriteList[3]
        self.screen.blit(head,(self.x,self.y))
        for i in range(1,len(self.bodyList)):
            self.screen.blit(self.bodysprite,(self.bodyList[i].get_x(),self.bodyList[i].get_y()))

    """
    Returns the x value of the snake.
    @return: x coordinate of the snake
    """
    def get_x(self):
        return self.x

    """
    Returns the y value of the snake.
    @return: y coordinate of the snake
    """
    def get_y(self):
        return self.y

"""
class SnakeBody

properties:
x - x coordinate of the Snake
y - y coordinate of the Snake

behaviors:
init - initialize the characteristics of the Snake
get_x - returns the x coordinate of the snake
get_y - returns the y coordinate of the snake
eq - override for the eq method
"""
class SnakeBody:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    """
    Returns the x value of the snakebody.
    @return: x coordinate of the snakebody
    """
    def get_x(self):
        return self.x

    """
    Returns the y value of the snakebody.
    @return: y coordinate of the snakebody
    """
    def get_y(self):
        return self.y

    """
    Override the eq method to accomadate for the snakebody.
    @param: other - value to compare against self
    @return: true if they are equal; false otherwise
    """
    def __eq__(self,other):
        return self.x == other.get_x() and self.y == other.get_y()

"""
class Foods

properties:
screen - pygame screen used by the Snake
sprite - the sprite that represents the foodList
barrierList - list containing the barriers the food cannot spawn on

behaviors:
init - initialize the characteristics of the Snake
generate_food - generate the food items in the food list
get_numFoods - returns the number of food items
check_eat - checks if the snake is over the food
draw_food - draws the food onto the screen
"""
class Foods:
    global SPRITE_SIZE
    def __init__(self,screen,sprite,barrierList):
        self.screen = screen
        self.sprite = sprite
        self.barrierList = barrierList
        self.foodList = []

    """
    Generate the food items that will be placed in the map.
    @param: amount - number of food items to generate
    """
    def generate_food(self,amount):
        while(len(self.foodList) < amount):
            x = randrange(0, WIDTH, SPRITE_SIZE)
            y = randrange(0, HEIGHT, SPRITE_SIZE)
            testPoint = Point(x, y)
            while testPoint in self.barrierList:
                x = randrange(0, WIDTH, SPRITE_SIZE)
                y = randrange(0, HEIGHT, SPRITE_SIZE)
                testPoint = Point(x, y)
            self.foodList.append(Food(x,y))

    """
    Return the number of off objects left.
    @return: number of food items left in foodList
    """
    def get_numFoods(self):
        return len(self.foodList)

    """
    Check to see if the snake is eating the food.
    @param: snakeHead - the head of the snake
    @return: true if the snake is eating food; false otherwise
    """
    def check_eat(self,snakeHead):
        for i in range(len(self.foodList)):
            if (self.foodList[i].get_x() == snakeHead.get_x() and self.foodList[i].get_y() == snakeHead.get_y() ):
                self.foodList.pop(i)
                return True
        return False

    """
    Draws the food.
    """
    def draw_food(self):
        for i in range(len(self.foodList)):
            self.screen.blit(self.sprite,(self.foodList[i].get_x(),self.foodList[i].get_y()))

"""
class Food

properties:
x - x coordinate of the Food
y - y coordinate of the Food

behaviors:
init - initialize the characteristics of the Food
get_x - returns the x coordinate of the Food
get_y - returns the y coordinate of the Food
eq - override for the eq method
"""
class Food:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    """
    Returns the x value of the snakebody.
    @return: x coordinate of the snakebody
    """
    def get_x(self):
        return self.x

    """
    Returns the y value of the snakebody.
    @return: y coordinate of the snakebody
    """
    def get_y(self):
        return self.y

    """
    Override the eq method to accomadate for the food.
    @param: other - value to compare against self
    @return: true if they are equal; false otherwise
    """
    def __eq__(self,other):
        return self.x == other.get_x() and self.y == other.get_y()

"""
Main method for running the game.
"""
def main():
    pygame.init()
    pygame.mixer.init()

    bite_sound = pygame.mixer.Sound("bite.wav")
    bite_sound.set_volume(.5)
    background_sound = pygame.mixer.Sound("background.wav")
    #bbackground_sound.set_volume(.25)
    background_sound.play(-1)

    screen = pygame.display.set_mode([WIDTH,HEIGHT])

    bodySprite = pygame.image.load("snakebody.png")
    headup = pygame.image.load("headup.png")
    headdown = pygame.image.load("headdown.png")
    headleft = pygame.image.load("headleft.png")
    headright = pygame.image.load("headright.png")
    headSpriteList = [headup, headdown,headleft,headright]
    foodSprite = pygame.image.load("food.png")
    enemySprite = pygame.image.load("enemy.png")

    pygame.display.set_caption("Snake Test")
    done = False
    clock = pygame.time.Clock()

    background = SpriteTileMap("backgroundMap.txt")
    barrierList = background.getBarriers(['l'],SPRITE_SIZE)
    background.drawMap(screen)

    #screen.fill(WHITE)

    snake = Snake(400,300,7,screen,headSpriteList,bodySprite,barrierList)
    snake.draw_snake("RIGHT")

    mongooseList = []
    mongooseList.append(Mongoose(25, 25, screen, enemySprite, barrierList))
    #mongooseList.append(Mongoose((WIDTH) - 50, (HEIGHT) - 50, screen, enemySprite, barrierList))
    for m in mongooseList:
        m.draw()
    mongoose_move = True

    food = Foods(screen,foodSprite,barrierList)
    food.generate_food(3)
    food.draw_food()

    curr_dir = "RIGHT"
    level = 1
    while not done:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and curr_dir != "RIGHT":
                    curr_dir = "LEFT"
                elif event.key == pygame.K_RIGHT and curr_dir != "LEFT":
                    curr_dir = "RIGHT"
                elif event.key == pygame.K_UP and curr_dir != "DOWN":
                    curr_dir = "UP"
                elif event.key == pygame.K_DOWN and curr_dir != "UP":
                    curr_dir = "DOWN"

        snake.move(curr_dir,food.check_eat(snake.get_headObj()))
        if food.check_eat(snake.get_headObj()):
            bite_sound.play()
        if mongoose_move:
            for m in mongooseList:
                m.move(snake)
            mongoose_move = False
        else:
            mongoose_move = True

        if(snake.check_collision(mongooseList)):
            done = True
        background.drawMap(screen)
        #screen.fill(WHITE)
        snake.draw_snake(curr_dir)
        food.draw_food()
        for m in mongooseList:
            m.draw()
        if food.get_numFoods() < 1:
            food.generate_food(3)
            level += 1
        pygame.display.flip()
        clock.tick(5 + level)
    pygame.quit()

main()
