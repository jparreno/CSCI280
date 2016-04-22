import pygame

from SpriteTileMap import *

from random import randrange

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SPRITE_SIZE = 25
WIDTH = 800
HEIGHT = 600

# start with 2 mongooses
# get_x and get_y
class Mongoose:

    def __init__(self, x, y, screen, sprite):
        self.x = x
        self.y = y
        self.screen = screen
        self.sprite = sprite
        self.directions = ["LEFT", "RIGHT", "UP", "DOWN"]

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def boundaryHit(self, x, y):
        if (self.x + x < SPRITE_SIZE or self.x + x >= WIDTH - SPRITE_SIZE or
            self.y + y < SPRITE_SIZE or self.y + y >= HEIGHT - SPRITE_SIZE):
            return True
        return False

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

    def move(self, snake):
        direction = self.directionToMove(snake)
        x_change = 0
        y_change = 0
        while True:
            print("In Loop")
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

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))


class Snake:
    global SPRITE_SIZE
    global WIDTH
    global HEIGHT

    def __init__(self,x,y,numSegments,screen,headspriteList,bodysprite):
        self.x = x
        self.y = y
        self.numSegments = numSegments
        self.screen = screen
        self.headspriteList = headspriteList
        self.bodysprite = bodysprite
        self.bodyList = [SnakeBody(x,y)]
        for i in range(1,self.numSegments-1):
            self.bodyList.append(SnakeBody(x-i*SPRITE_SIZE,y))

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

    def get_bodyList(self):
        return self.bodyList

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_headObj(self):
        return self.bodyList[0]

    def check_collision(self, mongooseList):
        for i in range(1,len(self.bodyList)):
            if (self.bodyList[i].get_x() == self.x and self.bodyList[i].get_y() == self.y):
                return True
        if self.x < SPRITE_SIZE or self.x >= WIDTH - SPRITE_SIZE or self.y < SPRITE_SIZE or self.y >= HEIGHT - SPRITE_SIZE:
            return True
        for m in mongooseList:
            if m.getX() == self.x and m.getY() == self.y:
                return True
        return False

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

class SnakeBody:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __eq__(self,other):
        return self.x == other.get_x() and self.y == other.get_y()

class Foods:
    global SPRITE_SIZE
    def __init__(self,screen,sprite):
        self.screen = screen
        self.sprite = sprite
        self.foodList = []

    def generate_food(self,amount):
        for i in range(amount):
            x = randrange(0 + SPRITE_SIZE, WIDTH - SPRITE_SIZE, SPRITE_SIZE)
            y = randrange(0 + SPRITE_SIZE, HEIGHT - SPRITE_SIZE, SPRITE_SIZE)
            self.foodList.append(Food(x,y))

    def get_numFoods(self):
        return len(self.foodList)

    def check_eat(self,snakeHead):
        for i in range(len(self.foodList)):
            if (self.foodList[i].get_x() == snakeHead.get_x() and self.foodList[i].get_y() == snakeHead.get_y() ):
                self.foodList.pop(i)
                return True
        return False

    def draw_food(self):
        for i in range(len(self.foodList)):
            self.screen.blit(self.sprite,(self.foodList[i].get_x(),self.foodList[i].get_y()))

class Food:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __eq__(self,other):
        return self.x == other.get_x() and self.y == other.get_y()

def main():
    pygame.init()

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
    background.drawMap(screen)

    #screen.fill(WHITE)

    snake = Snake(400,300,7,screen,headSpriteList,bodySprite)
    snake.draw_snake("RIGHT")

    mongooseList = []
    mongooseList.append(Mongoose(25, 25, screen, enemySprite))
    mongooseList.append(Mongoose((WIDTH) - 50, (HEIGHT) - 50, screen, enemySprite))
    for m in mongooseList:
        m.draw()
    mongoose_move = True

    food = Foods(screen,foodSprite)
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
        for m in mongooseList:
            m.draw()
        food.draw_food()
        if food.get_numFoods() < 1:
            food.generate_food(3)
            level += 1
        pygame.display.flip()
        clock.tick(5 + level)
    pygame.quit()

main()
