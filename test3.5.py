import pygame

from OurSprite import *
from OurSpriteInventory import *
from SpriteTileMap import *

from random import randrange

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SPRITE_SIZE = 25
WIDTH = 800
HEIGHT = 600


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

    def get_headObj(self):
        return self.bodyList[0]

    def check_collision(self):
        for i in range(1,len(self.bodyList)):
            if (self.bodyList[i].get_x() == self.x and self.bodyList[i].get_y() == self.y):
                return True

        for i in range(len(self.barrierList)):
            if (self.barrierList[i].get_x() == self.x and self.barrierList[i].get_y() == self.y):
                return True
        
##        if self.x < SPRITE_SIZE or self.x >= WIDTH - SPRITE_SIZE or self.y < SPRITE_SIZE or self.y >= HEIGHT - SPRITE_SIZE:
##            return True
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
    def __init__(self,screen,sprite,barrierList):
        self.screen = screen
        self.sprite = sprite
        self.barrierList = barrierList
        self.foodList = []

    def generate_food(self,amount):
        while(len(self.foodList) < amount):
            x = randrange(0, WIDTH, SPRITE_SIZE)
            y = randrange(0, HEIGHT, SPRITE_SIZE)
            for i in range(len(self.barrierList)):
                while (self.barrierList[i].get_x() == x and self.barrierList[i].get_y() == y):
                    x = randrange(0, WIDTH, SPRITE_SIZE)
                    y = randrange(0, HEIGHT, SPRITE_SIZE)
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
    barrierList = background.getBarriers(['l'],25)
    background.drawMap(screen)

    #screen.fill(WHITE)

    snake = Snake(400,300,7,screen,headSpriteList,bodySprite,barrierList)
    snake.draw_snake("RIGHT")

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
        if(snake.check_collision()):
            done = True
        background.drawMap(screen)
        #screen.fill(WHITE)
        snake.draw_snake(curr_dir)
        food.draw_food()
        if food.get_numFoods() < 1:
            food.generate_food(3)
            level += 1
        pygame.display.flip()
        clock.tick(5 + level)
    pygame.quit()

main()
