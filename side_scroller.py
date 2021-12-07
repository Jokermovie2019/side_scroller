#imports
import pygame, sys
from pygame.locals import *
import random, time

#initializing
pygame.init()

#setting up FPS
FPS = 60
FramesPerSec = pygame.time.Clock()

#creating colors
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

#other variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("cloudsky.jpg")
 
#create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Booster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boosto.png")
        self.rect = self.image.get_rect()
        self.rect.center = (1000, random.randint(40, SCREEN_HEIGHT - 40))
        self.wait = 0

    def move(self):
        if self.wait ==0:
            self.rect.move_ip(-10, 0)
            if (self.rect.left < 0):
                self.wait += 10
                self.rect.left = 1000
                self.rect.center = (1000, random.randint(40, SCREEN_HEIGHT - 40))
    def hide(self):
        if self.wait > 0:
            self.rect.left = 1000
            self.rect.center = (1000, random.randint(40, SCREEN_HEIGHT - 40))
            self.wait -= 1

class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("roboto_rough.png")
        self.rect = self.image.get_rect()
    def move(self):
        pass

    
class Lilbot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("tomat2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (1000, random.randint(40, SCREEN_HEIGHT - 40))
        self.wait = 40
        self.speed = -7

    def move(self):
        self.rect.move_ip(self.speed, 0)
        if (self.rect.left < 0):
            self.wait += 20
            self.rect.left = 1000
            self.rect.center = (1000, random.randint(40, SCREEN_HEIGHT - 40))
            self.speed = (random.randint(-12, -5))
    
        
        



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("superpig.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 520)
        self.fall_speed = 1
        self.boost = 0
    def speed_up(self, speedy):
        if speedy > 6 and speedy <= 20:
            self. fall_speed = 2
        if speedy>12:
            self.fall_speed = 3


    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top < (SCREEN_HEIGHT-5):
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -7)
        if self.rect.bottom > 5:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,7)
         
        if self.boost > 0:
            if self.rect.right < (SCREEN_WIDTH-75):        
                if pressed_keys[K_RIGHT]:
                    self.rect.move_ip(10, 0)
                    self.boost -= 1

        if self.rect.left > (0):        
                if pressed_keys[K_LEFT]:
                    self.rect.move_ip(-5, 0)

        self.rect.move_ip(-self.fall_speed, 0)

#setting up sprites
P1 = Player()
E1 = Booster()
R1 = Robot()
B1 = Lilbot()
B2 = Lilbot()

#creating sprites group
enemies = pygame.sprite.Group()
enemies.add(R1)
enemies.add(B1)
enemies.add(B2)
boosters = pygame.sprite.Group()
boosters.add(E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(R1)
all_sprites.add(B1)
all_sprites.add(B2)

 
#adding a new user event
INC_SPEED = pygame.USEREVENT + 1 
pygame.time.set_timer(INC_SPEED, 1000)

#variable to help increase speed slowly
speedy = 0


#game loop
while True:     
    #Cycles through all events occuring  
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(background, (0,0))
    

    P1.speed_up(speedy)

  

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    if E1.wait == 0:
        DISPLAYSURF.blit(E1.image, E1.rect)
        E1.move()
    else:
        E1.hide()
    



    #To be run if collision occurs between Player and BOOST
    boost_score = P1.boost

    if pygame.sprite.spritecollideany(P1, boosters):
        P1.boost += 25
        E1.wait += 20
        speedy += 1
        

    scores = font_small.render(str(boost_score), True, BLACK)
    DISPLAYSURF.blit(scores, (500,10))
        
        
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
    

        DISPLAYSURF.fill(RED)
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        
         
    pygame.display.update()
    FramesPerSec.tick(FPS)
