import pygame,sys,random,time
from pygame.locals import (KEYDOWN,K_UP,K_SPACE,QUIT)

pygame.init()
SCREEN_X = 800
SCREEN_Y = 300
SCREEN_SIZE = [SCREEN_X,SCREEN_Y]

screen = pygame.display.set_mode(SCREEN_SIZE)

#Adding Title and Icon

pygame.display.set_caption("DinoRun")
icon = pygame.image.load("./assets/footprint.png")
pygame.display.set_icon(icon)

def eventListener(event):
    global isJumping
    if event.type == QUIT:
        sys.exit(0)
    if event.type == KEYDOWN:
        if event.key == K_SPACE:
            isJumping = True
    pass

#ground Variables
G_SpeedX = 10
G_SpeedY = 0
G_X1 = 0
G_Y1 = 0
G_X2 = SCREEN_X
G_Y2 = 0


def background():
    global G_X1,G_X2,G_Y1,G_Y2,G_SpeedX,G_SpeedY
    screen.fill((255,255,255))
    backgroundImg = pygame.image.load("./assets/background.jpg")
    backgroundImg = pygame.transform.scale(backgroundImg,SCREEN_SIZE)
    screen.blit(backgroundImg,[G_X1,G_Y1])
    screen.blit(backgroundImg,[G_X2,G_Y2])
    G_X1=G_X1-G_SpeedX
    G_X2=G_X2-G_SpeedX
    if G_X2 == 0:
        G_X1 = SCREEN_X
    
    if G_X1 == 0:
        G_X2 = SCREEN_X
    pass





#Dino Variables
P_X =120
P_Y = 175
isJumping = False

def Player():
    global P_X,P_Y,isJumping
    
    Dino = pygame.image.load("./assets/pterosaurus.png")
    Dino = pygame.transform.scale(Dino,[60,60])
    screen.blit(Dino,[P_X,P_Y])
    if isJumping:
        P_Y = jump(P_Y)
    
    

def jumpValidation(P_Y):
    global isJumping,gravityFlag
    if isJumping and P_Y>=175:
        isJumping = False
        gravityFlag = False
        return

gravityFlag = False;
gravity = 10

def jump(P_Y):
    global gravityFlag,gravity
    if P_Y <= 70:
        gravityFlag = True
    
    if gravityFlag:
        P_Y+=gravity
    else:
        P_Y-=gravity
    
    jumpValidation(P_Y)
    if not isJumping:
        P_Y=175 
    return P_Y
    pass

#Obstancle Variables
nextFlag = True
AllObstacles = list()


def obstacleA(O_X,O_Y,G_SpeedX):
    global nextFlag
    Obs = pygame.image.load("./assets/cactus.png")
    Obs = pygame.transform.scale(Obs,[60,60])
    screen.blit(Obs,[O_X,O_Y])
    O_X = O_X - G_SpeedX
    if O_X  <= 0:
        nextFlag = True
    return O_X
    
def obstacleB(O_X,O_Y,G_SpeedX):
    global nextFlag
    Obs = pygame.image.load("./assets/tree.png")
    Obs = pygame.transform.scale(Obs,[60,60])
    screen.blit(Obs,[O_X,O_Y])
    
    O_X = O_X - G_SpeedX
    if O_X <= 0:
        nextFlag = True
    
    return O_X

O_XA = SCREEN_X
O_XB = SCREEN_X
O_Y = 175

i=0

class Obstancle:
    current = 0
    X = 0
    Y = 0 
    Speed =0
    choice = 0
    def __init__(self,O_X,O_Y,Speed):
        
        self.X= O_X
        self.Y= O_Y
        self.Speed = Speed
        random.seed(time.time())
        self.choice = random.choice([1,2])
    
    def setCurrent(self,value):
        self.current = value

    def call(self):
        
        if self.choice == 1:
            self.X=obstacleA(self.X,self.Y,self.Speed)
            pass
       
        else:
            self.X=obstacleB(self.X,self.Y,self.Speed)
        


def callAll(callInt):
    global AllObstacles
    AllObstacles[callInt].call()
    
def makeNewObstacle():
    global G_SpeedX,O_XA,O_Y,AllObstacles,currentObs,nextFlag
    print([O_XA,O_Y,G_SpeedX])
    obs = Obstancle(800,175,G_SpeedX)
    AllObstacles.append(obs)
    currentObs = len(AllObstacles) -1
    nextFlag = False


def CheckCollision():
    global currentObs,P_X,P_Y,AllObstacles,gravity,G_SpeedX,CollisonFlag,running,gameFlag

    obs = AllObstacles[currentObs]
    print("1 :",(obs.X < P_X+62 < obs.X+62))
    print("2 :",(obs.Y , P_Y+62 , obs.Y + 62))
    if (obs.X < P_X+62 < obs.X+62) and (obs.Y ==P_Y):
        G_SpeedX=0
        gravity =0
        gameFlag =False
        
        CollisonFlag = True

def Score(score):
    txt = pygame.font.SysFont('Arial',20)
    text = txt.render(f"Score : {score}",True,(0,0,0))
    screen.blit(text,[10,10])


def GameOver():
    txt = pygame.font.SysFont('Arial',60)
    text = txt.render(f"Game Over!",True,(0,0,0))
    screen.blit(text,[400,200])
#game variable

currentObs = -1;
score = 0
gameFlag = True
CollisonFlag = False
def gameloop():
    global currentObs,nextFlag,running,score,CollisonFlag,G_SpeedX,gravity
    running = True

    while running:
        if gameFlag:
            score+=1

        
        for event in pygame.event.get():
           eventListener(event)

        background()
        
        Player()
        
       
        if nextFlag:
            makeNewObstacle()
        
        if currentObs>-1:
            callAll(currentObs)

        Score(score)
        CheckCollision()
        if CollisonFlag:
            GameOver()
        
        pygame.display.update()


if __name__ == '__main__':
    gameloop()


           

