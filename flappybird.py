import pygame
import sys
import os
import random
import math
import json

from enum import Enum
from enum import IntEnum



# Define the texture path
current_dir = os.path.dirname(__file__)
texture_path = str(current_dir + "\\Assets")

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 1000, 1000
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird!")


# Load background texture
background = pygame.image.load(texture_path + r"\background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

gameover = pygame.image.load(texture_path + r"\gameover.png")

birdTexture = pygame.image.load(texture_path + r"\bird.png")
pipeTexture = pygame.image.load(texture_path + r"\pipe.png")


pointerTexture = pygame.image.load(texture_path + r"\pointer.png")
easyTexture = pygame.image.load(texture_path + r"\easy.png")
mediumTexture = pygame.image.load(texture_path + r"\medium.png")
hardTexture = pygame.image.load(texture_path + r"\hard.png")

bookTexture = pygame.image.load(texture_path + r"\book.png")
shopTexture = pygame.image.load(texture_path + r"\shop.png")

loginUI = pygame.image.load(texture_path + r"\loginUI.png")
placeHolder = pygame.image.load(texture_path + r"\nameinputplaceholder.png")





banner = pygame.image.load(texture_path + r"\gamebanner.png")

tutorialTexture = pygame.image.load(texture_path + r"\tutorial.png")

font = pygame.font.Font(str(current_dir+"\Fonts\Minecraft.ttf"), 36)
cmsFont = pygame.font.Font(str(current_dir+"\Fonts\COMIC.TTF"),58)


score_position_x = WIDTH/2
score_position_y = HEIGHT/6

# Clock to control framerate
clock = pygame.time.Clock()

# Sprite class for the Bird
class Bird(pygame.sprite.Sprite):
    def __init__(this):
        super().__init__()

        # Load bird texture
        this.texture = birdTexture
        this.rect = this.texture.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        this.rect.x = WIDTH // 2 - 300                                        # đặt bird lệch về góc trái so với tâm window

        # Bird physics
        this.gravityForce = 9.9
    
        this.isJumping = False
        this.isFalling = False
        this.jumpForce = -800
        this.jumpForceCap = -50
        this.jumpedHeight = 0
        this.jumpHeightCap = 75
        this.fallVelocity = 0.66667
        this.fallVelocityCap = 20

        this.isHovering = False
        this.hoverVelocity = 1
        this.hoverTimeCounter = 0
        this.hoverCooldownCounter =0
        this.deltaTime = 0

        this.counter = 0

        this.keys = []
        this.preKeys = []

        this.rotateAngle = 0

    def update(this, keys, deltaTime):
        this.deltaTime = deltaTime
        
        this.keys = keys 
        this.jump()
        this.hover()
        this.applyGravity()

        # Update rotation based on velocity
        current_velocity = this.fallVelocity if not this.isJumping else this.jumpForce
        this.rotateAngle = min(0, max(-90, -current_velocity * 4))
        
        # Rotate the texture
        this.texture = pygame.transform.rotate(birdTexture, this.rotateAngle)
        # Adjust rect to keep center
        old_center = this.rect.center
        this.rect = this.texture.get_rect()
        this.rect.center = old_center

        # Keep the bird inside the window
        this.rect.clamp_ip(window.get_rect())

        this.preKeys = this.keys

    def applyGravity(this):
        if not this.isJumping:
            if not this.isHovering: 
                if this.fallVelocity >= this.fallVelocityCap:
                    this.fallVelocity = this.fallVelocityCap
                this.fallVelocity += this.gravityForce * this.deltaTime
            this.rect.y += float(this.fallVelocity)

    def jump(this):
        if (this.jumpable()==True) and (this.isJumping==False) :
            this.isJumping = True
            this.jumpedHeight = 0

        if this.isJumping:
            
            if this.jumpForce >= this.jumpForceCap:
                this.jumpForce = this.jumpForceCap
            this.jumpForce -= -this.gravityForce * this.deltaTime
            this.rect.y += float(this.jumpForce * this.deltaTime)
            this.jumpedHeight += abs(this.jumpForce) * this.deltaTime

            if this.jumpedHeight >= this.jumpHeightCap:
                this.isJumping = False
                this.jumpForce = -800
                this.fallVelocity = 0.66667
    def jumpable(this):
        if(this.keys[pygame.K_SPACE] and not this.preKeys[pygame.K_SPACE]): #Đảm bảo phím space phải được ấn liên tục không giữ
            return True
        return False
    def hover(this):
        this.hoverCooldownCounter += this.deltaTime
        if(this.keys[pygame.K_RETURN] and this.hoverCooldownCounter >= 6):
            this.isHovering = True
            this.fallVelocity = this.hoverVelocity
            this.hoverTimeCounter += this.deltaTime
            if(this.hoverTimeCounter >= 4):
                this.hoverTimeCounter = 0
                this.hoverCooldownCounter = 0
        else:
            this.isHovering = False
    def refresh(this):
        this.texture = birdTexture
        this.rect = this.texture.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        this.rect.x = WIDTH // 2 - 300                                        # đặt bird lệch về góc trái so với tâm window

        # Bird physics
        this.gravityForce = 9.8
        this.isJumping = False
        this.isFalling = False
        this.jumpForce = -800/2
        this.jumpForceCap = -50
        this.jumpedHeight = 0
        this.jumpHeightCap = 75
        this.fallVelocity = 0.66667/8
        this.fallVelocityCap = 20
        this.deltaTime = 0

        this.counter = 0

        this.keys = []
        this.preKeys = []

        this.rotateAngle = 0

# Sprite class for the Pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(this):
        super().__init__()

        # Load pipe texture
        this.texture = pipeTexture
        this.rect = this.texture.get_rect(center=(0,0))

# Class for the pair of pipes
class PairOfPipes():
    def __init__(this,iniPos):
        super().__init__()

        this.center = 0
        this.iniPos = iniPos
        this.iniPhase = random.randint(4,7)*100 + random.randint(2,3)*10 + random.randint(-2,2)*20
        this.appliedScore = False

        this.distance = 150
        this.t = Pipe()
        this.b = Pipe()

        this.b.rect.x = WIDTH + this.iniPos
        this.t.rect.x = WIDTH + this.iniPos
        this.b.rect.y = this.iniPhase

        this.t.texture = pygame.transform.flip(this.t.texture, False, True) #flip the top pipe


        this.deltaTime = 0
        this.timeCounter = 0
        this.velocity = 125/2

        this.placeTheMatchingTopPipe()
        
    def EasyUpdate(this, keys, deltaTime):
        this.timeCounter+=this.deltaTime
        if(this.t.rect.x + this.t.texture.get_width() <= 0):
            this.displacement = random.randint(4,7)*100 + random.randint(2,3)*10 + random.randint(-2,2)*20
            this.refresh(this.displacement)
        this.keys = keys
        this.deltaTime = deltaTime
        this.EasyMove()

    def MediumUpdate(this, keys, deltaTime):
        this.timeCounter+=this.deltaTime
        if(this.t.rect.x + this.t.texture.get_width() <= 0):
            this.displacement = random.randint(4,7)*100 + random.randint(2,3)*10 + random.randint(-2,2)*20
            this.refresh(this.displacement)
        this.keys = keys
        this.deltaTime = deltaTime
        this.MediumMove()

    def HardUpdate(this, keys, deltaTime):
        this.timeCounter+=this.deltaTime
        if(this.t.rect.x + this.t.texture.get_width() <= 0):
            this.displacement = random.randint(4,7)*100 + random.randint(2,3)*10 + random.randint(-2,2)*20
            this.refresh(this.displacement)
        this.keys = keys
        this.deltaTime = deltaTime
        this.HardMove()

    def EasyMove(this):
        this.t.rect.x -= float(this.velocity * this.deltaTime)
        this.b.rect.x -= float(this.velocity * this.deltaTime)
        this.placeTheMatchingTopPipe()
    def MediumMove(this):
        this.t.rect.x -= float(this.velocity * this.deltaTime)
        this.b.rect.x -= float(this.velocity * this.deltaTime)
        this.placeTheMatchingTopPipe()
    def HardMove(this):
        this.t.rect.x -= float(this.velocity * this.deltaTime)
        this.b.rect.x -= float(this.velocity * this.deltaTime)

        this.b.rect.y =  this.iniPhase + 250*math.sin(0.0066*this.b.rect.x)  # y = Acos(wx + o)
        this.placeTheMatchingTopPipe()

    def draw(this, window):
        # Draw top and bottom pipes
        window.blit(this.t.texture, this.t.rect)
        window.blit(this.b.texture, this.b.rect)
    def refresh(this,iniPhase):
        this.appliedScore = False
        
        this.b.rect.x = WIDTH 
        this.t.rect.x = WIDTH
        this.b.rect.y = iniPhase 

        this.placeTheMatchingTopPipe()
    
    def placeTheMatchingTopPipe(this):
        this.t.rect.y = this.b.rect.y
        this.t.rect.y = this.t.rect.y - this.t.texture.get_height() - this.distance

# Main game class

class State(Enum):
    isRunning = 1
    isOver = 2
    isIdling = 3
    selectingButtons = 4
    isLoggingin = 5 
class Buttons(IntEnum):
    Easy = 0
    Medium = 1
    Hard = 2
    Tutorial = 3
    Shop = 4
    Nonee = 5

class MainGame():
    
    def __init__(this):
        this.restart() # tai tao attributes
        this.State = State.selectingButtons
#Game loop
    def update(this, keys, deltaTime,events):
        
        this.keys = keys
        this.deltaTime = deltaTime

    #Select Difficulty
        if(this.State == State.isLoggingin):
            this.login(keys)
        if(this.State == State.selectingButtons):
            this.selectButtons()
    #Running
        if(this.State == State.isRunning):
        #Easy 
            if(this.selectedButton == Buttons.Easy):
                for pipe in this.pops:
                    pipe.EasyUpdate(keys,this.deltaTime)                   #Nếu muốn có thể thay đổi logic các ống ở hàm này
                # this.p3.update(keys, deltaTime)

                this.bird.update(keys, this.deltaTime)
     #EASYYY           # thêm logic game bên dưới
                        # hàm update() phải có biến:
                        # keys: list các phím ấn từ bàn phím
                        #this.deltaTime: là thời gian trôi qua của mỗi vòng lặp












                this.checkScore()
                #SCORE HERE ------------------------------------------
                #SCORE HERE ------------------------------------------
                #SCORE HERE ------------------------------------------
                this.score_text = font.render(str(this.score), True, (255, 255, 255)) #SCORE HERE ------------------------------------------
                #SCORE HERE ------------------------------------------
                #SCORE HERE ------------------------------------------
                #SCORE HERE ------------------------------------------
                if(this.birdCollided()):
                    this.State = State.isOver       
                
            # Draw background
            window.blit(background, (0, 0))

            # Draw pipes and bird
            for pipe in this.pops:
                pipe.draw(window)
            # this.p3.draw(window)
            window.blit(this.score_text,(score_position_x,score_position_y))
            window.blit(this.bird.texture, (this.bird.rect.x, this.bird.rect.y))

        #Medium
            if(this.selectedButton == Buttons.Medium):
                for pipe in this.pops:
                    pipe.MediumUpdate(keys,this.deltaTime)
                # this.p3.update(keys, deltaTime)

                this.bird.update(keys, this.deltaTime)
                 # thêm logic game bên dưới
                        # hàm update() phải có biến:
                        # keys: list các phím ấn từ bàn phím
                        #this.deltaTime: là thời gian trôi qua của mỗi vòng lặp












                this.checkScore()
                this.score_text = font.render(str(this.score), True, (255, 255, 255))

                if(this.birdCollided()):
                    this.State = State.isOver

        #Hard
            if(this.selectedButton == Buttons.Hard):
                for pipe in this.pops:
                    pipe.HardUpdate(keys,this.deltaTime)
                # this.p3.update(keys, deltaTime)

                this.bird.update(keys, this.deltaTime)
                this.checkScore()
                this.score_text = font.render(str(this.score), True, (255, 255, 255))

                if(this.birdCollided()):
                    this.State = State.isOver
                
            if(this.selectedButton == Buttons.Tutorial):
                if(this.keys[pygame.K_ESCAPE] and not this.preKeys[pygame.K_ESCAPE]):
                    this.pointerIndex = this.selectedButton
                    this.selectedButton = Buttons.Nonee
                    this.State = State.selectingButtons
                window.blit(tutorialTexture,(0,0))

            if(this.selectedButton == Buttons.Shop):
                pass
    #Game over    
        if(this.State == State.isOver):
            window.blit(this.overTexture,(WIDTH/2-225/2,HEIGHT/4))
            if(this.keys[pygame.K_SPACE] and not this.preKeys[pygame.K_SPACE]):
                print("restarted!")
                this.restart()

        this.preKeys = keys

    def birdCollided(this):
        # Check collision with pipes
        for pipe in this.pops:
            if(this.bird.rect.colliderect(pipe.t.rect) or this.bird.rect.colliderect(pipe.b.rect)):
                return True

        # Check if bird hits the top or bottom of the window
        if this.bird.rect.top <= 0 or this.bird.rect.bottom >= HEIGHT:
            return True
        return False
        
    def checkScore(this):
        for pipe in this.pops:
            if(this.bird.rect.x >= pipe.t.rect.x + pipe.t.texture.get_width() and pipe.appliedScore == False):
                this.score += 1
                pipe.appliedScore = True
        
#Refresh the game's attributes  
    def restart(this):
        this.popGap = 300
#Game set up
        this.State = State.selectingButtons# 1 state at a time
        this.selectedButton = Buttons.Nonee  
#Game sprites
        this.bird = Bird()

        this.p1 = PairOfPipes(50)
        this.p2 = PairOfPipes(50+this.popGap)
        this.p3 = PairOfPipes(50+2*this.popGap)
        this.p4 = PairOfPipes(50+3*this.popGap)
        this.pops = [this.p1,this.p2,this.p3,this.p4] #list cac pair of pipes

#Game decorations
        this.banner = pygame.sprite.Sprite
        this.bannerTexture = banner
        this.banner.rect = this.bannerTexture.get_rect()
        this.banner.rect.x = WIDTH/2 - 450/2
        this.banner.rect.y = HEIGHT/4 - 100

        this.over = pygame.sprite.Sprite
        this.overTexture = gameover
        this.over.rect = this.overTexture.get_rect()
        this.over.rect.x = WIDTH/2 - 225/2
        this.over.rect.y = HEIGHT/4 
#Score
        this.score = 0
        this.score_text = font.render(str(this.score), True, (255, 255, 255))
#Game button
        this.EasyButton = Button(easyTexture,200)
        this.MediumButoon = Button(mediumTexture,325)
        this.HardButton = Button(hardTexture,450)
        this.BookButton = Button(bookTexture,450 + 125*2)
        this.BookButton.rect.x = WIDTH - 84 - 25
        this.ShopButton = Button(shopTexture,450 + 125*2)
        this.ShopButton.rect.x = this.BookButton.rect.x - 150

        this.Buttons = [this.EasyButton,this.MediumButoon,this.HardButton,this.BookButton,this.ShopButton]

        this.pointer = pygame.sprite.Sprite
        this.pointerTexture = pointerTexture
        this.pointer.rect = pointerTexture.get_rect()

        this.pointerIndex = 0

        this.pointer.rect.x = this.EasyButton.rect.x - 30/2
        this.pointer.rect.y = this.EasyButton.rect.y + 84/2 - 10

        this.LoginUI = LoginUI()
        this.UserNamePlaceHolder = userNamePlaceHolder(this.LoginUI)

#Game logic attributes
        this.keys = []
        this.preKeys = []
        this.deltaTime = 0

        this.started = False
    def selectButtons(this):
        window.blit(background, (0, 0))

        if(this.keys[pygame.K_DOWN] and not this.preKeys[pygame.K_DOWN]):
            this.pointerIndex += 1
            if(this.pointerIndex > len(this.Buttons)-1):
                this.pointerIndex = 0
        if(this.keys[pygame.K_UP] and not this.preKeys[pygame.K_UP]):
            this.pointerIndex -= 1
            if(this.pointerIndex <0):
                this.pointerIndex = len(this.Buttons)-1
        this.placePointer() 

        if(this.keys[pygame.K_RETURN] and not this.preKeys[pygame.K_RETURN]):
            this.joinButton()

        window.blit(this.bannerTexture,(WIDTH/2 - 450/2, HEIGHT/4 - 100))
        for button in this.Buttons:
            window.blit(button.Texture,(button.rect.x,button.rect.y))
        window.blit(this.pointerTexture,(this.pointer.rect.x, this.pointer.rect.y))
    def placePointer(this):
        if(this.pointerIndex == 4):
            this.pointer.rect.y = this.ShopButton.rect.y + 84/2
            this.pointer.rect.x = this.ShopButton.rect.x + 91/2 - 100   
        if(this.pointerIndex == 3):
            this.pointer.rect.y = this.BookButton.rect.y + 84/2
            this.pointer.rect.x = this.BookButton.rect.x + 91/2 - 100           
        if(this.pointerIndex in [0,1,2]):
            this.pointer.rect.x = this.EasyButton.rect.x - 30/2
            this.pointer.rect.y = this.EasyButton.rect.y + 84/2 - 10 + 125*this.pointerIndex            #125 la offset giua 3 buttons || 84 la height cua buttons
    def joinButton(this):
        this.selectedButton = this.pointerIndex  # 0-easy , 1-med, 2-hard
        this.State = State.isRunning
        # print (this.selectedButton)
    def login(this,events):
        window.blit(background,(0,0))
        window.blit(this.LoginUI.Texture,(0,0))
        window.blit(this.UserNamePlaceHolder.Texture,(this.UserNamePlaceHolder.rect.x,this.UserNamePlaceHolder.rect.y))

        this.UserNamePlaceHolder.update(events)


class Button(pygame.sprite.Sprite):
        def __init__(this, Texture,offset):
            this.Texture = Texture
            this.rect = this.Texture.get_rect()
            this.rect.x = WIDTH / 2 - 200/2
            this.rect.y = HEIGHT/4 - 100 + offset

class LoginUI(pygame.sprite.Sprite):
        def __init__(this):
            this.Texture = loginUI
            this.rect = this.Texture.get_rect()
            this.rect.x = 0
            this.rect.y = 0

class userNamePlaceHolder(pygame.sprite.Sprite):
        def __init__(this,container):
            this.Texture = placeHolder
            this.rect = this.Texture.get_rect()
            this.rect.x = container.Texture.get_width()/2 - this.Texture.get_width()/2 
            this.rect.y = container.Texture.get_height()/2 - this.Texture.get_height()/2 + 50
            this.username = ""
            this.sequence = ""
            this.char =''
            this.keys =[]
            this.preKeys = []
            this.isActing = False
        def update(this, keys):
            this.keys = keys
            if(this.isClicked(keys)):
                this.isActing = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN: 
                    this.char = event.unicode
                    this.username += this.char
            if(this.keys[pygame.K_BACKSPACE] and not this.preKeys[pygame.K_BACKSPACE]):
                if len(this.username) >0:
                    this.username = this.username[:-1]
                if len(this.username) >0:
                    this.username = this.username[:-1]
                
            this.sequence = cmsFont.render(str(this.username), True, (28, 25, 16))
            window.blit(this.sequence,(this.rect.x + 30,this.rect.y+5))

            this.preKeys = keys
        def isClicked(this,keys):
            return(keys[pygame.K_RETURN] and this.isActing == False)
        
        

# Initialize the game
game = MainGame()

# Game loop
def main():
    # print(texture_path)
    deltaTime = clock.tick(60) / 1000.0

    while True:
        clock.tick(120)  # 120 FPS\

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update sprites
        game.update(pygame.key.get_pressed(), deltaTime,pygame.event.get())

        # Refresh the screen
        pygame.display.flip()

if __name__ == "__main__":
    main()
