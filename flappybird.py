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
data_path = str(current_dir + '\data.jsonl')

# Initialize Pygame
pygame.init()

# Khởi tạo âm thanh
pygame.mixer.init()  # Bắt đầu hệ thống âm thanh

# Load nhạc nền
pygame.mixer.music.load(texture_path + r"\background_music2.mp3")  # đặt file nhạc vào Assets
pygame.mixer.music.set_volume(0.3)  # âm lượng nhạc nền
pygame.mixer.music.play(-1)  # -1 để loop vô hạn

# Window settings
WIDTH, HEIGHT = 1000, 1000
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird!")
# ===== BLUR OVERLAY (MEDIUM EFFECT) =====
blurOverlay = pygame.Surface((WIDTH, HEIGHT))
blurOverlay.set_alpha(120)   # 0 = trong suốt, 255 = đen đặc
blurOverlay.fill((50, 50, 50))

# Load background texturea
background = pygame.image.load(texture_path + r"\background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

gameover = pygame.image.load(texture_path + r"\gameover.png")

yellowbirdTexture = pygame.image.load(texture_path + r"\bird.png")
pipeTexture = pygame.image.load(texture_path + r"\pipe.png")


pointerTexture = pygame.image.load(texture_path + r"\pointer.png")
easyTexture = pygame.image.load(texture_path + r"\easy.png")
mediumTexture = pygame.image.load(texture_path + r"\medium.png")
hardTexture = pygame.image.load(texture_path + r"\hard.png")

bookTexture = pygame.image.load(texture_path + r"\book.png")
shopTexture = pygame.image.load(texture_path + r"\shop.png")
coinTexture = pygame.image.load(texture_path + r"\coin.png")


loginUI = pygame.image.load(texture_path + r"\loginUI.png")
placeHolder = pygame.image.load(texture_path + r"\nameinputplaceholder.png")
fcursor = pygame.image.load(texture_path + r"\cursor.png")
okbuttonTexture = pygame.image.load(texture_path + r"\okbutton.png")
createUserTexture = pygame.image.load(texture_path + r"\createusernamebutton.png")
enterUserTexture = pygame.image.load(texture_path + r"\enterexistingusernamebutton.png")


returnButtonTexture = pygame.image.load(texture_path + r"\returnButton.png")




banner = pygame.image.load(texture_path + r"\gamebanner.png")

tutorialTexture = pygame.image.load(texture_path + r"\tutorial.png")

stallTexture = pygame.image.load(texture_path + r"\stall.png")
bluebirdTexture = pygame.image.load(texture_path + r"\bluebird.png")
pinkbirdTexture = pygame.image.load(texture_path + r"\pinkbird.png")
redbirdTexture = pygame.image.load(texture_path + r"\redbird.png")
itemContainerTexture = pygame.image.load(texture_path + r"\itemContainer.png")
shopPointerTexture = pygame.image.load(texture_path + r"\shopPointer.png")
lockedSymbol = pygame.image.load(texture_path + r"\lock.png")
tickedSymbol = pygame.image.load(texture_path + r"\unlocked.png")

heartTexture = pygame.image.load(texture_path + r"\heart.png")
heartTexture = pygame.transform.scale(heartTexture, (32, 32))
enemyTexture = pygame.image.load(texture_path + r"\enemy.png")
enemyTexture = pygame.transform.scale(enemyTexture, (40, 40))
enemyBulletTexture = pygame.image.load(texture_path + r"\enemy_bullet.png")
enemyBulletTexture = pygame.transform.scale(enemyBulletTexture, (23, 11))


scoreboardTexture = pygame.image.load(texture_path + r"\scoreboard.png")

font = pygame.font.Font(str(current_dir+"\Fonts\Minecraft.ttf"), 36)
cmsFont = pygame.font.Font(str(current_dir+"\Fonts\COMIC.TTF"),58)
ScmsFont = pygame.font.Font(str(current_dir+"\Fonts\COMIC.TTF"),36)
VScmsFont = pygame.font.Font(str(current_dir+"\Fonts\COMIC.TTF"),22)




score_position_x = WIDTH/2
score_position_y = HEIGHT/6

# Clock to control framerate
clock = pygame.time.Clock()

# Sprite class for the Bird
class Bird(pygame.sprite.Sprite):
    def __init__(this):
        super().__init__()

        # Load bird texture
        this.texture = yellowbirdTexture
        this.rect = this.texture.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        this.rect.x = WIDTH // 2 - 300                                        # đặt bird lệch về góc trái so với tâm window

        # Bird physics
        this.gravityForce = 7
        this.isJumping = False
        this.isFalling = False
        this.jumpForce = -800
        this.jumpForceCap = -10
        this.jumpedHeight = 0
        this.jumpHeightCap = 75
        this.fallVelocity = 0.33333
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

        this.originalTexture = this.texture

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
        this.texture = pygame.transform.rotate(this.originalTexture, this.rotateAngle)
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
        this.texture = yellowbirdTexture
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
        this.fallVelocity = 0.66667
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
        this.enemyChecked = False

        this.distance = 175
        this.t = Pipe()
        this.b = Pipe()

        this.b.rect.x = WIDTH + this.iniPos
        this.t.rect.x = WIDTH + this.iniPos
        this.b.rect.y = this.iniPhase
        # Attri moving Pipe
        this.base_b_y = this.b.rect.y  # baseline Y cho dao động Medium
        this.medium_vertical_amplitude = 40.0  # pixel lên/xuống
        this.medium_vertical_speed = 1.5       # tốc độ dao động (rad/s)

        this.t.texture = pygame.transform.flip(this.t.texture, False, True) #flip the top pipe


        this.deltaTime = 0
        this.timeCounter = 0
        this.velocity = 125

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
        # Dao động trơn lên xuống - ống di chuyển theo sin wave
        this.b.rect.y = int(this.base_b_y + this.medium_vertical_amplitude * math.sin(this.timeCounter * this.medium_vertical_speed))
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
        this.enemyChecked = False
        this.b.rect.x = WIDTH 
        this.t.rect.x = WIDTH
        this.b.rect.y = iniPhase 
        this.base_b_y = this.b.rect.y  # reset baseline

        this.placeTheMatchingTopPipe()
    
    def placeTheMatchingTopPipe(this):
        this.t.rect.y = this.b.rect.y
        this.t.rect.y = this.t.rect.y - this.t.texture.get_height() - this.distance


# Main game class
def applyEasyLogic(game, keys, deltaTime):
    game.bird.gravityForce = 4.5
    game.bird.jumpForceCap = -8
    game.bird.fallVelocityCap = 14

    for pipe in game.pops:
        pipe.distance = 260
        pipe.velocity = 95

    if game.invincibleTime > 0:
        game.invincibleTime -= deltaTime

    if game.invincibleTime <= 0 and game.birdCollided():
            game.hp -= 1
            game.invincibleTime = 2
            if game.hp <= 0:
                game.State = State.isOver
# ===== EASY ENEMY SPAWN 
    for i, pipe in enumerate(game.pops):
        if not hasattr(pipe, "enemyChecked"):
            pipe.enemyChecked = False
        # chỉ đếm khi ống vừa xuất hiện ở mép phải
        if WIDTH - 5 < pipe.t.rect.x < WIDTH and not pipe.enemyChecked:
            pipe.enemyChecked = True
            game.pipeCounter += 1

            # Random xác suất spawn Enemy (70%)
            if random.random() < 0.6:
            # Tìm Enemy inactive đầu tiên để spawn
                for enemy in game.enemies:
                    if not enemy.active:
                        enemy.spawn(pipe)
                        break
def applyMediumLogic(game, keys, deltaTime):
    """Logic độ khó Medium: ống dao động, enemy, coin gắn ống"""
    # Attri
    MED_VERTICAL_AMPLITUDE = 40.0  # pixel lên/xuống (tăng = khó hơn)
    MED_VERTICAL_SPEED = 1.5       # tốc độ dao động rad/s
    MED_PIPE_VELOCITY = 110        # tốc độ ngang ống
    MED_PIPE_DISTANCE = 240        # khoảng cách giữa ống
    MED_ENEMY_SPAWN_CHANCE = 0.5   # xác suất spawn enemy

    # Bird Attri
    game.bird.gravityForce = 6.5
    game.bird.jumpForceCap = -12
    game.bird.fallVelocityCap = 16

    # Pipe attri
    for pipe in game.pops:
        pipe.distance = MED_PIPE_DISTANCE
        pipe.velocity = MED_PIPE_VELOCITY
        pipe.medium_vertical_amplitude = getattr(pipe, "medium_vertical_amplitude", MED_VERTICAL_AMPLITUDE)
        pipe.medium_vertical_speed = getattr(pipe, "medium_vertical_speed", MED_VERTICAL_SPEED)

    # invc
    if game.invincibleTime > 0:
        game.invincibleTime -= deltaTime

   

    # Enemy spawn
    for i, pipe in enumerate(game.pops):
        if not hasattr(pipe, "enemyChecked"):
            pipe.enemyChecked = False
        if WIDTH - 5 < pipe.t.rect.x < WIDTH and not pipe.enemyChecked:
            pipe.enemyChecked = True
            game.pipeCounter += 1
            if random.random() < MED_ENEMY_SPAWN_CHANCE:
                for enemy in game.enemies:
                    if not enemy.active:
                        enemy.spawn(pipe)  # truyền pipe để enemy gắn vào
                        break

    # ===== ENEMY UPDATE + COLLISION (MEDIUM) =====
    for enemy in game.enemies:
        enemy.update(game.pops[0].velocity, deltaTime)

        # Chim đụng enemy → KHÔNG MẤT MÁU, CHỈ RUNG MÀN
        if enemy.collide(game.bird):
            enemy.active = False

            game.screenShakeTimer = 0.6
            game.screenShakeIntensity = 18

        # Bullet vẫn gây damage
        if enemy.bullet.collide(game.bird) and game.invincibleTime <= 0:
            game.hp -= 1
            game.invincibleTime = 2
            enemy.bullet.active = False

            if game.hp <= 0:
                game.State = State.isOver
  
class MainGame():
    def __init__(this):
        this.State = State.isRunning
        this.playerData = {
            "username": "",
            "score": 0,
            "coins": 0,
            "skins" :{
                "bluebird" : False,
                "redbird" : False,
                "pinkbird" : False,
                "yellowbird":True
            }
        }
        this.restart() # tai tao attributes
        this.collectedCoins = 0
        
#Game loop
    def update(this, keys, deltaTime):

        #super super super vital 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        this.keys = keys
        this.deltaTime = deltaTime

    #Select Difficulty
    #Running
        if(this.State == State.isRunning):
            this.timeElapsed += deltaTime
            if(int(this.timeElapsed) > this.themomentThatCoinsCanAppear):
                    if(int(this.timeElapsed) % this.coinAppearPeriod ==0):
                        if(this.coin.isCollected or this.coin.rect.x<0):
                            this.coin.refresh()
                        this.coin.trigger()      
            this.coin.update(this.bird, this.deltaTime)
        #Easy 
            if(this.selectedButton == Buttons.Easy):
                this.bird.easyHitbox = True
                for pipe in this.pops:
                    pipe.EasyUpdate(keys,this.deltaTime)                   #Nếu muốn có thể thay đổi logic các ống ở hàm này
                # this.p3.update(keys, deltaTime)

                this.bird.update(keys, this.deltaTime)
     #EASYYY           # thêm logic game bên dưới
                        # hàm update() phải có biến:
                        # keys: list các phím ấn từ bàn phím
                        #this.deltaTime: là thời gian trôi qua của mỗi vòng lặp
                applyEasyLogic(this, keys, this.deltaTime)
                # ===== ENEMY UPDATE + COLLISION =====
                for enemy in this.enemies:
                    enemy.update(this.pops[0].velocity, this.deltaTime)

                    if enemy.collide(this.bird) and this.invincibleTime <= 0:
                        this.hp -= 1
                        this.invincibleTime = 2
                        enemy.active = False

                        if this.hp <= 0:
                            this.State = State.isOver
                    # ===== BULLET COLLISION (EASY ONLY) =====
                    if enemy.bullet.collide(this.bird) and this.invincibleTime <= 0:
                        this.hp -= 1
                        this.invincibleTime = 2
                        enemy.bullet.active = False

                        if this.hp <= 0:
                            this.State = State.isOver
                # ===== COIN LOGIC =====
                if(int(this.timeElapsed) > this.themomentThatCoinsCanAppear):
                    if(int(this.timeElapsed) % this.coinAppearPeriod ==0):
                        if(this.coin.isCollected):
                            this.coin.refresh()
                        this.coin.trigger()
                        
                this.coin.update(this.bird, this.deltaTime)
                if(not this.coin.isCollected and not this.coin.isDrawable):
                    this.collectedCoins +=1
                    this.coin.isCollected = True
                this.checkScore()
                this.score_text = font.render(str(this.score), True, (255, 255, 255))
       
        #Medium
            if(this.selectedButton == Buttons.Medium):
                this.bird.easyHitbox = False
                
                # Set HP cho Medium lần đầu tiên (2 mạng)
                if not hasattr(this, 'mediumHpSet'):
                    this.hp = 2 
                    this.mediumHpSet = True
                
                for pipe in this.pops:
                    pipe.MediumUpdate(keys,this.deltaTime)
                # this.p3.update(keys, deltaTime)

                this.bird.update(keys, this.deltaTime)
                 # Áp dụng logic Medium (ống dao động lên/xuống, enemy, coin gắn ống)
                applyMediumLogic(this, keys, this.deltaTime)
                if this.birdCollided() and this.invincibleTime <= 0:
                    this.hp -= 2
                    this.invincibleTime = 2

                    this.screenShakeTimer = 1
                    this.screenShakeIntensity = 55

                    if this.hp <= 0:
                        this.State = State.isOver

                this.checkScore()
                this.score_text = font.render(str(this.score), True, (255, 255, 255))

            if(int(this.timeElapsed) > this.themomentThatCoinsCanAppear):
                    if(int(this.timeElapsed) % this.coinAppearPeriod ==0):
                        if(this.coin.isCollected):
                            this.coin.refresh()
                        this.coin.trigger()
                        
            this.coin.update(this.bird, this.deltaTime)
            if(not this.coin.isCollected and not this.coin.isDrawable):
                    this.collectedCoins +=1
                    this.coin.isCollected = True    
            # ===== SCREEN SHAKE UPDATE (MEDIUM ONLY) =====
            shake_x = 0
            shake_y = 0

            if this.selectedButton == Buttons.Medium and this.screenShakeTimer > 0:
                this.screenShakeTimer -= this.deltaTime
                shake_x = random.randint(-this.screenShakeIntensity, this.screenShakeIntensity)
                shake_y = random.randint(-this.screenShakeIntensity, this.screenShakeIntensity)

            # Draw background (with shake)
            window.blit(background, (shake_x, shake_y))

            # Draw pipes and bird
            for pipe in this.pops:
                pipe.draw(window)
            for enemy in this.enemies:
                enemy.draw(window)
            # this.p3.draw(window)
            window.blit(this.score_text,(score_position_x,score_position_y))
            if this.selectedButton == Buttons.Easy or this.selectedButton == Buttons.Medium:
                for i in range(this.hp):
                    window.blit(heartTexture, (30 + i * 40, 30))
            #window.blit(this.bird.texture, (this.bird.rect.x, this.bird.rect.y))
            if this.selectedButton == Buttons.Easy or this.selectedButton == Buttons.Medium:
                if this.invincibleTime > 0:
                    if int(pygame.time.get_ticks() / 100) % 2 == 0:
                        window.blit(this.bird.texture, this.bird.rect)
                else:
                        window.blit(this.bird.texture, this.bird.rect)
            else:
                window.blit(this.bird.texture, this.bird.rect)
            # ===== COIN DRAWING =====
            if(this.coin.isDrawable):
                window.blit(this.coin.Texture,(this.coin.rect.x,this.coin.rect.y))
        #Hard
            if(this.selectedButton == Buttons.Hard):
                this.bird.easyHitbox = False
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
                window.blit(tutorialTexture,(0,0))

            if(this.selectedButton == Buttons.Shop):
                this.Stall.getData(this.playerData)
                
                this.Stall.update(this.keys,this.playerData)
                if(this.keys[pygame.K_ESCAPE]):
                    this.selectedButton =Buttons.Nonee
            if(this.selectedButton == Buttons.Nonee):
                this.selectButtons()
    #Game over    
        if(this.State == State.isOver):
            window.blit(this.overTexture,(WIDTH/2-225/2,20))
            
            if(this.DataSaved == False):
                this.saveData()
            this.scoreboard.update(data_path,this.score)

            if(this.keys[pygame.K_r] and not this.preKeys[pygame.K_r]):
                this.restart()
        this.preKeys = this.keys

        # print(this.coins)

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
        this.scoreboard = ScoreBoard(scoreboardTexture)
        this.collectedCoins = 0
        this.State = State.isRunning
        this.popGap = (WIDTH - 4*pipeTexture.get_width())/(4-1)
#Game set up
        this.selectedButton = Buttons.Nonee  
#Game sprites
        # Reset flag Medium HP
        this.mediumHpSet = False  
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
#Coin
        this.coin = Coin()
        this.themomentThatCoinsCanAppear = 1
        this.coinAppearPeriod = 3
        
        # this.coin.refresh()

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

        this.timeElapsed = 0
        this.savedData = False

#Game logic attributes
        this.keys = []
        this.preKeys = []
        this.deltaTime = 0

        this.started = False
        # ===== EASY ONLY =====
        this.hp = 3
        this.invincibleTime = 0
        # ===== MEDIUM SCREEN SHAKE =====
        this.screenShakeTimer = 0
        this.screenShakeIntensity = 0
        # ===== EASY ENEMY =====
        this.enemies = [Enemy() for _ in range(4)]
         # ===== EASY ENEMY SPAWN CONTROL =====
        this.pipeCounter = 0
        this.nextEnemySpawn = random.choice([1, 3, 5])
        this.DataSaved = False

        this.Stall = Stall(stallTexture)

#Game logic attributes
        this.keys = pygame.key.get_pressed()
        this.preKeys = this.keys
        this.deltaTime = 0

        this.started = False

         # ===== EASY ONLY =====
        this.hp = 3
        this.invincibleTime = 0
        # ===== EASY ENEMY =====
        this.enemies = [Enemy() for _ in range(4)]
         # ===== EASY ENEMY SPAWN CONTROL =====
        this.pipeCounter = 0
        this.nextEnemySpawn = random.choice([1, 3, 5])
    def selectButtons(this):
        window.blit(background, (0, 0))
        this.pointerTexture = this.bird.texture

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
            this.pointer.rect.x = this.EasyButton.rect.x - this.pointerTexture.get_width() - 10
            this.pointer.rect.y = this.EasyButton.rect.y + this.EasyButton.Texture.get_height()/2 - this.pointerTexture.get_height()/2 - 10 + 125*this.pointerIndex            #125 la offset giua 3 buttons || 84 la height cua buttons
    def joinButton(this):
        this.selectedButton = this.pointerIndex
    def saveData(this):
        # 1. Read the existing data into memory
        updated_lines = []
        found_player = False

        try:
            with open(data_path, 'r', encoding="utf-8") as f:
                for line in f:
                    if not line.strip(): # Skip empty lines
                        continue
                        
                    playerData = json.loads(line) # Use loads() for strings
                    
                    # 2. Check and update the specific player
                    if playerData["username"] == this.playerData["username"]:
                        playerData["coins"] += this.collectedCoins
                        this.playerData["coins"] += this.collectedCoins
                        if(this.score > playerData["score"]):
                            playerData["score"] = this.score
                        found_player = True
                        this.DataSaved = True
                    updated_lines.append(playerData)
        except FileNotFoundError:
            print("File not found, starting fresh.")

        # 3. Write everything back to the file
        with open(data_path, 'w', encoding="utf-8") as f:
            for data in updated_lines:
                f.write(json.dumps(data) + '\n')

        # 4. Trigger restart if the player was updated
        if found_player:
            return True
        return False
    
class Button(pygame.sprite.Sprite):
        def __init__(this, Texture,offset):
            this.Texture = Texture
            this.rect = this.Texture.get_rect()
            this.rect.x = WIDTH / 2 - 200/2
            this.rect.y = HEIGHT/4 - 100 + offset
            this.value =-1
        def setPosition(this,x,y):
            this.rect.x = x
            this.rect.y = y
        def isClicked(this,event):
            
            if event.button == 1: # 1 is Left Click
                if(this.rect.collidepoint(event.pos)):
                    return True
                else:
                    return False
        def respondToMouseHover(this,event):
            if (event.type == pygame.MOUSEMOTION):
                if(this.rect.collidepoint(event.pos)):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                # To change it back to a normal arrow:
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
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
            this.subUsername = ""
            this.char =''
            this.displacement = 0
            this.keys =[]
            this.preKeys = []
            this.isActing = False
            this.maxLength = 12
            this.fcursor = flickeringCursor()
            this.currentLength_text = ScmsFont.render(str(this.maxLength-len(this.username)), True, (28, 25, 16))

            this.outcome =""
            this.confirmButton = Button(okbuttonTexture,0)
            this.confirmButton.setPosition(container.rect.x + container.Texture.get_width()/2 - this.confirmButton.Texture.get_width()/2,650)
            this.finished = False
            this.submitted = False

            
        def update(this, keys):
            this.keys = keys

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #to act is to be clicked
                this.confirmButton.respondToMouseHover(event)
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    this.isActing = this.isClicked(event)
                    if(this.confirmButton.isClicked(event) and not this.submitted == True):
                        this.submitted = True
                #acting 
                if(this.isActing):
                    if event.type == pygame.KEYDOWN:
                        this.read_key(event)
                       

            if(this.isActing):    
                this.delete_key()
                this.move_fcursor()
                this.update_fcursor()          
                if(this.keys[pygame.K_RETURN] and not this.preKeys[pygame.K_RETURN] and not this.submitted == True):
                    this.submitted = True
                
                
            this.sequence = cmsFont.render(str(this.username), True, (28, 25, 16))
            this.currentLength_text = ScmsFont.render(str(this.maxLength-len(this.username)), True, (28, 25, 16))

            window.blit(this.sequence,(this.rect.x + 30,this.rect.y+5))

            text_width, text_height = ScmsFont.size(str(len(this.username))) 
            window.blit(this.currentLength_text,(this.rect.x +this.Texture.get_width() - 50,this.rect.y+text_height/2))
            window.blit(this.confirmButton.Texture,(this.confirmButton.rect.x,this.confirmButton.rect.y))


            
            
            if(this.fcursor.drawable and this.isActing):
                window.blit(this.fcursor.Texture,(this.fcursor.rect.x,this.fcursor.rect.y))
            
            this.preKeys = this.keys
            # print(this.isActing)
        def isClicked(this,event):
            if event.button == 1: # 1 is Left Click
                if(this.rect.collidepoint(event.pos)):
                    return True
                else:
                    return False
        def read_key(this,event):
            this.submitted = False
            if(len(this.username) < this.maxLength):
                if((event.unicode).isnumeric() or (event.unicode).isalpha()):     
                    this.char = event.unicode
                    this.username = this.username[:len(this.username)-this.displacement] + this.char + this.username[len(this.username)-1-this.displacement+1:]
        def delete_key(this):

            if(this.keys[pygame.K_BACKSPACE] and not this.preKeys[pygame.K_BACKSPACE]):
                this.submitted = False
                if len(this.username) >0 and this.displacement != len(this.username):
                    this.username = this.username[:(len(this.username)-1-this.displacement)] + this.username[len(this.username)-1-this.displacement+1:] #xoa 1 ki tu tai vi tri fcursor 
        def move_fcursor(this):
            if(this.keys[pygame.K_LEFT] and not this.preKeys[pygame.K_LEFT]):
                this.submitted = False
                this.displacement +=1
                if(this.displacement > len(this.username)):
                    this.displacement = len(this.username)
            if(this.keys[pygame.K_RIGHT] and not this.preKeys[pygame.K_RIGHT]):
                this.submitted = False
                this.displacement +=-1
                if(this.displacement <0):
                    this.displacement = 0
        def update_fcursor(this):
            if(this.displacement != 0):
                this.fcursor.update(this.rect,this.username[:-this.displacement])
            else: 
                this.fcursor.update(this.rect,this.username[:])

        def usernameExists(this):
            with open(data_path, "r") as f:
                for line in f:
                    user = json.loads(line)
                    if(this.username == user["username"]):
                        return True
            return False
class message():
    def __init__(this,text,font,colour = (0,0,0)):
        this.text = text
        this.font = font
        this.colour = colour 
        this.drawableMessage = this.font.render(this.text,True,colour)
    def draw(this,pos):
        window.blit(this.drawableMessage,(pos))
                                  
class Login():
    def __init__(this):

        this.restart()
        
    def update(this,keys,deltaTime,game):
        this.keys = keys
        this.deltaTime = deltaTime
        if(this.State == loginState.choosingloggingOptions):
            this.loadLoginOptions()
        if(this.State == loginState.enteringUsername):
            this.login(this.keys,game)
        this.preKeys = this.keys
    #Game button
    def restart(this):
        this.playerData = {
            "username": "",
            "score": 0,
            "coins": 0,
            "skins" :{
                "bluebird" : False,
                "redbird" : False,
                "pinkbird" : False,
                "yellowbird":True
            }
        }
        this.chosenOptions = LoginOptions.Nonee
        this.State = loginState.choosingloggingOptions
        this.LoginUI = LoginUI()
        this.UserNamePlaceHolder = userNamePlaceHolder(this.LoginUI)

        this.timeElapsed = 0
        this.savedData = False

#Game logic attributes
        this.keys = []
        this.preKeys = []
        this.deltaTime = 0

        this.started = False
        this.creater = Button(createUserTexture,0)
        this.creater.rect.x = WIDTH/2 - this.creater.Texture.get_width()/2
        this.creater.rect.y = 300
        this.creater.value = 0
        this.enterer = Button(enterUserTexture,0)
        this.enterer.rect.x = WIDTH/2 - this.enterer.Texture.get_width()/2
        this.enterer.rect.y = 500
        this.enterer.value = 1

        this.logginOptions = [this.enterer,this.creater]
        this.blankLeftAlert = message("Please enter your name",VScmsFont,(207, 28, 28))
        this.usernameExistingAlert = message("Username must be unique",VScmsFont,(207, 28, 28))
            #40 149 10
        this.usernameAcceptedAnnouncement =message("Username Accepted!",VScmsFont,(40,149,10))
        this.usernameRecognizedAnnouncement =message("Username Recognized! Welcome back",VScmsFont,(40,149,10))
        this.undefinedUsernameAnnouncement = message("Couldn't recognize you, please create a new one",VScmsFont,(207, 28, 28))
        this.noMessage = message("",VScmsFont,(0,0,0))
        this.drawableAlert = this.noMessage

        this.returnButton = Button(returnButtonTexture,0)
        this.returnButton.setPosition(5,5)

        this.dataLoaded = False
        # print (this.selectedButton)
    def login(this,events,game):
        global Event
        
        window.blit(background,(0,0))
        
        window.blit(this.LoginUI.Texture,(0,0))
        window.blit(this.UserNamePlaceHolder.Texture,(this.UserNamePlaceHolder.rect.x,this.UserNamePlaceHolder.rect.y))
        this.UserNamePlaceHolder.update(events)
        if(this.keys[pygame.K_ESCAPE]):
            this.restart()
        #Create
        if(this.chosenOptions == LoginOptions.Create):
            if(this.UserNamePlaceHolder.submitted):
                if(len(this.UserNamePlaceHolder.username)==0):
                    this.drawableAlert = this.blankLeftAlert
                elif(this.UserNamePlaceHolder.usernameExists()):
                    this.drawableAlert = this.usernameExistingAlert
                else:
                    this.UserNamePlaceHolder.finished = True
            if(this.UserNamePlaceHolder.finished):
                # print("hi")
                this.UserNamePlaceHolder.outcome = this.UserNamePlaceHolder.username
                this.addNewPlayer()
                this.loadData(this.UserNamePlaceHolder.outcome,game)
                Event = GlobalEvent.Loggedin
                this.UserNamePlaceHolder.outcome = ""
                this.UserNamePlaceHolder.finished = False
                this.UserNamePlaceHolder.submitted = False
                this.drawableAlert = this.usernameAcceptedAnnouncement

        #Reuse
        if(this.chosenOptions == LoginOptions.EnterExisting):
            if(this.UserNamePlaceHolder.submitted):
                if(len(this.UserNamePlaceHolder.username)==0):
                    this.drawableAlert = this.blankLeftAlert
                elif(this.UserNamePlaceHolder.usernameExists()):
                    this.drawableAlert = this.usernameRecognizedAnnouncement
                    this.UserNamePlaceHolder.finished = True
                else:
                    this.drawableAlert = this.undefinedUsernameAnnouncement
            if(this.UserNamePlaceHolder.finished):
                # print("hi")
                this.UserNamePlaceHolder.outcome = this.UserNamePlaceHolder.username
                this.loadData(this.UserNamePlaceHolder.outcome,game)
                
                Event = GlobalEvent.Loggedin
                this.UserNamePlaceHolder.outcome = ""
                this.UserNamePlaceHolder.finished = False
        text_width, text_height = VScmsFont.size(this.drawableAlert.text) 
        this.drawableAlert.draw((this.UserNamePlaceHolder.rect.x + this.UserNamePlaceHolder.Texture.get_width()/2 - text_width/2,this.UserNamePlaceHolder.rect.y + this.UserNamePlaceHolder.Texture.get_height() + 10))

    def addNewPlayer(this):
        print(data_path)
        newPlayer = {
            "username": this.UserNamePlaceHolder.outcome,
            "score": 0,
            "coins": 0,
            "skins" :{
                "bluebird" : False,
                "redbird" : False,
                "pinkbird" : False,
                "yellowbird":True
            }
        }

        with open(data_path,'a') as json_file:
            json_file.write(json.dumps(newPlayer)+ "\n")
    
    def loadData(this,username,game):
        with open(data_path, "r") as f:
            for line in f:
                    player = json.loads(line)
                    if(player["username"] == username):
                        this.playerData = player
                        game.restart()
                        game.playerData = this.playerData
                        this.dataLoaded = True
                        return True
        print("Fail to load player's datas")

        return False 
    def loadLoginOptions(this):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            for button in this.logginOptions:
                button.respondToMouseHover(event)
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if(button.isClicked(event)):
                        this.State = loginState.enteringUsername
                        this.chosenOptions = button.value
                        # print(this.chosenOptions)
                        
        
        window.blit(background,(0,0))
        for button in this.logginOptions:
            window.blit(button.Texture,(button.rect.x,button.rect.y))       
                 

class flickeringCursor(pygame.sprite.Sprite):
    def __init__(this):
        this.Texture = fcursor
        this.rect = fcursor.get_rect()
        this.drawable = True
    def update(this,owners_rect,owners_sequence):
        text_width, text_height = cmsFont.size(owners_sequence)   # tra ve 1 tuple :kich thuoc (w,h) cua string voi font cms
        this.rect.y = owners_rect.y + 15
        this.rect.x = owners_rect.x + 30 + text_width
        #logic cho cursor nhap nhay
        this.flicker()
    def flicker(this):
        #for every 0.5s
        timeElapsed = float(pygame.time.get_ticks()/1000) #tra ve thoi gian ke tu pygame.init() doi ms -> s
        if(2*(math.floor(timeElapsed*2)/2)  == math.floor(timeElapsed)*2 + 1):
            this.drawable = True
        else:
            this.drawable = False

class Coin(pygame.sprite.Sprite):
    def __init__(this):
        this.Texture = coinTexture
        this.rect = this.Texture.get_rect()
        this.isCollected = False
        this.isDrawable = True
        this.velocity = 100
        this.deltaTime = 0
        this.iniPos_y = 0
        this.rect.x = WIDTH + 100
        this.defineDir = False
        this.isActing = False
    def update(this,bird,deltaTime):
        if(this.isActing):
            if(not this.defineDir):
                this.setIniPos_y()
            this.deltaTime = deltaTime
            this.move()
            this.Collide(bird)


# Initialize the game
    def Collide(this,bird):
        if(bird.rect.colliderect(this.rect)):
            this.isDrawable = False
    def move(this):
        this.rect.y = this.iniPos_y
        this.rect.x -= this.velocity*this.deltaTime
    def refresh(this):
        this.rect.x = WIDTH + 100
        this.isCollected = False
        this.isDrawable = True
        this.defineDir = False
        this.isActing = False
    def setIniPos_y(this):
        this.iniPos_y = random.randint(4,7)*100 + random.randint(2,3)*10 + random.randint(-2,2)*20
        this.defineDir = True
    def trigger(this):
        if(not this.isActing):
            this.isActing = True
class Enemy(pygame.sprite.Sprite):
    def __init__(this):
        this.Texture = enemyTexture
        this.rect = this.Texture.get_rect()

        this.active = False
        this.hitbox = pygame.Rect(0, 0, 18, 18)  # HITBOX NHỎ
        this.bullet = Bullet()
        this.shootCooldown = random.uniform(1.2, 2.2)
        this.shootTimer = 0
        
        # Support gắn vào ống (Medium difficulty)
        this.attached_pipe = None
        this.initial_y_offset = 0

    def spawn(this, pipe):
        this.active = True
        this.attached_pipe = pipe
        this.rect.centerx = pipe.b.rect.x + pipe.b.texture.get_width() // 2
        # random sát ống trên hoặc dưới
        if random.choice([True, False]):
            # sát miệng ống trên
            this.initial_y_offset = pipe.t.rect.bottom + 6 - pipe.b.rect.y
        else:
            # sát miệng ống dưới
            this.initial_y_offset = pipe.b.rect.top - this.rect.height - 6 - pipe.b.rect.y
        this.rect.y = pipe.b.rect.y + this.initial_y_offset
    def update(this, velocity, deltaTime):
        if not this.active:
            return

        this.rect.x -= velocity * deltaTime
        
        # Nếu enemy gắn vào ống, theo dõi Y của ống (oscillation)
        if this.attached_pipe is not None:
            this.rect.y = this.attached_pipe.b.rect.y + this.initial_y_offset
            # Khi ống ra ngoài màn hình, deactivate enemy
            if this.attached_pipe.b.rect.x + this.attached_pipe.b.texture.get_width() <= 0:
                this.active = False
        
        this.hitbox.center = this.rect.center

        # ===== SHOOT BULLET =====
        this.shootTimer += deltaTime
        if this.shootTimer >= this.shootCooldown:
            this.shootTimer = 0
            this.shootCooldown = random.uniform(1.2, 2.2)
            this.bullet.spawn(this.rect.left, this.rect.centery)

        this.bullet.update(deltaTime)

        if this.rect.right < 0:
             this.active = False


    def draw(this, window):
        if this.active:
            window.blit(this.Texture, this.rect)
            this.bullet.draw(window)
    def collide(this, bird):
        return this.active and this.hitbox.colliderect(bird.rect)
class Bullet(pygame.sprite.Sprite):
    def __init__(this):
        this.Texture = enemyBulletTexture
        this.rect = this.Texture.get_rect()
        this.rect = pygame.Rect(0, 0, 10, 4)
        this.speed = 400
        this.active = False

    def spawn(this, x, y):
        this.rect.x = x
        this.rect.y = y
        this.active = True

    def update(this, deltaTime):
        if not this.active:
            return
        this.rect.x -= this.speed * deltaTime
        if this.rect.right < 0:
            this.active = False

    def draw(this, window):
        if this.active:
            window.blit(this.Texture, this.rect)
    def collide(this, bird):
        return this.active and this.rect.colliderect(bird.rect)
class Item(pygame.sprite.Sprite):
    def __init__(this,Texture,name,price):
            this.Texture = Texture
            this.rect = this.Texture.get_rect()
            this.rect.x = 0
            this.rect.y = 0
            this.isOwned = False
            this.symbol = pygame.sprite.Sprite
            this.symbolTextures = [lockedSymbol,tickedSymbol]
            this.symbol.rect = this.symbolTextures[0].get_rect()
            this.name = name
            this.price = price
            # this.symbol.rect.x = this.rect.x + this.Texture.get_width()/2 - this.symbolTextures[0].get_width()/2
            # this.symbol.rect.y = this.rect.y + this.Texture.get_height()
    def placeSymbol(this):
            this.symbol.rect.x = this.rect.x + this.Texture.get_width()/2 - this.symbolTextures[0].get_width()/2
            this.symbol.rect.y = this.rect.y + this.Texture.get_height()
    


class ItemContainer(pygame.sprite.Sprite):
    def __init__(this,Texture,item):
            this.Texture = Texture
            this.rect = this.Texture.get_rect()
            this.rect.x = 0
            this.rect.y = 0
            this.item = item
        
    def placeItem(this):
        this.item.rect.x = this.rect.x + this.Texture.get_width()/2 - this.item.Texture.get_width()/2
        this.item.rect.y = this.rect.y + this.Texture.get_height()/2 - this.item.Texture.get_height()/2
    def draw(this):
        window.blit(this.Texture,this.rect)
        window.blit(this.item.Texture,this.item.rect)
        window.blit(this.item.symbolTextures[this.item.isOwned],this.item.symbol.rect)
        window.blit(coinTexture,(this.rect.x + 30 ,this.rect.y + this.Texture.get_height() + 20))
        window.blit(VScmsFont.render('x' +str(this.item.price),True,(0,0,0)),(this.rect.x  + coinTexture.get_width() + 10,this.rect.y + this.Texture.get_height() + 50 ))
    def update(this):
        this.item.placeSymbol()
        this.draw()
class pointer(pygame.sprite.Sprite):
        def __init__(this,Texture):
            this.Texture = Texture
            this.rect = pointerTexture.get_rect()
        def update(this,pointee):
            this.rect.y = pointee.rect.y - 10 - this.Texture.get_height() 
            this.rect.x = pointee.rect.x + pointee.Texture.get_height()/2 - this.Texture.get_height()/2

            window.blit(this.Texture,this.rect)
class Stall(pygame.sprite.Sprite):
        def __init__(this,Texture):
            this.Texture = Texture
            this.rect = this.Texture.get_rect()
            this.item0 = Item(yellowbirdTexture,"yellowbird",0)
            this.item1 = Item(redbirdTexture,"redbird",1)
            this.item2 = Item(bluebirdTexture,"bluebird",10)
            this.item3 = Item(pinkbirdTexture,"pinkbird",100)

            this.Items = [this.item0,this.item1,this.item2,this.item3]
            this.ItemContainers = []
            this.keys = pygame.key.get_pressed()
            this.preKeys = this.keys
            this.iniPos = [125,550]
            this.displacement = 0
            this.placeItems()

            this.pointer = pointer(yellowbirdTexture)
            this.pointerIndex = 0

            this.numberOfCoins =0
            this.drawableCoins =  ScmsFont.render(str(this.numberOfCoins),True,(0,0,0))

        def getData(this,playerData):
                for itemContainer in this.ItemContainers:
                       itemContainer.item.isOwned = playerData["skins"][itemContainer.item.name]    
        def placeItems(this):
            for item in this.Items:
                itemContainer = ItemContainer(itemContainerTexture,item)
                this.ItemContainers.append(itemContainer)
            for container in this.ItemContainers:
                container.rect.y = this.iniPos[1]
                container.rect.x = this.iniPos[0] + this.displacement
                container.placeItem()
                this.displacement += 200
                
            
        def display(this):
            window.blit(this.Texture,(0,0))
            for container in this.ItemContainers:
                container.update()
            window.blit(coinTexture,(10,10))
            window.blit(this.drawableCoins,(70,10))

        def update(this,keys,playerData):
            this.numberOfCoins = playerData["coins"]
            this.drawableCoins =  ScmsFont.render('X' + str(this.numberOfCoins),True,(0,0,0))
            this.keys = keys

            if(this.keys[pygame.K_RIGHT] and not this.preKeys[pygame.K_RIGHT]):
                this.pointerIndex += 1
                if(this.pointerIndex >= len(this.ItemContainers)):
                    this.pointerIndex = 0
            if(this.keys[pygame.K_LEFT] and not this.preKeys[pygame.K_LEFT]):
                this.pointerIndex -= 1
                if(this.pointerIndex < 0):
                    this.pointerIndex = len(this.ItemContainers) -1
            this.purchase()
            this.display()
            this.pointer.update(this.ItemContainers[this.pointerIndex])

            this.preKeys = this.keys
        def purchase(this):
                if(this.keys[pygame.K_RETURN] and not this.preKeys[pygame.K_RETURN]):
                    if(this.ItemContainers[this.pointerIndex].item.isOwned == True):
                        this.pointer.Texture = this.ItemContainers[this.pointerIndex].item.Texture
                        game.bird.texture = this.ItemContainers[this.pointerIndex].item.Texture
                        game.bird.originalTexture = this.ItemContainers[this.pointerIndex].item.Texture

                    if(this.ItemContainers[this.pointerIndex].item.isOwned == False and game.playerData["coins"] >= this.ItemContainers[this.pointerIndex].item.price):
                        this.ItemContainers[this.pointerIndex].item.isOwned = True
                        updated_lines = []
                        found_player = False
                        try:
                            with open(data_path, 'r', encoding="utf-8") as f:
                                for line in f:
                                    if not line.strip(): # Skip empty lines
                                        continue
                                        
                                    playerData = json.loads(line) # Use loads() for strings
                                    
                                    # 2. Check and update the specific player
                                    if playerData["username"] == game.playerData["username"]:
                                        playerData["coins"] -= this.ItemContainers[this.pointerIndex].item.price
                                        game.playerData["coins"] = playerData["coins"]
                                        game.playerData["skins"][this.ItemContainers[this.pointerIndex].item.name] = True
                                        playerData["skins"][this.ItemContainers[this.pointerIndex].item.name] = True
                                        found_player = True
                                        this.DataSaved = True
                                    updated_lines.append(playerData)
                        except FileNotFoundError:
                            print("File not found, starting fresh.")

                        # 3. Write everything back to the file
                        with open(data_path, 'w', encoding="utf-8") as f:
                            for data in updated_lines:
                                f.write(json.dumps(data) + '\n')

                        # 4. Trigger restart if the player was updated
                        if found_player:
                            return True
                        return False

import pygame, json

import pygame, json

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(this, Texture):
        super().__init__()

        this.Texture = Texture
        this.rect = this.Texture.get_rect()
        this.rect.x = WIDTH // 2 - this.Texture.get_width() // 2
        this.rect.y = HEIGHT // 2 - this.Texture.get_height() // 2

        # ===== DATA =====
        this.top_3_players = []
        this.gottop3 = False

        # ===== PLAYER SCORE ANIMATION =====
        this.scoreCounter = 0
        this.frameCounter = 0

        # ===== TOP 3 CASCADE ANIMATION =====
        this.revealRank = 0          # đang hiển thị tới rank nào (0-2)
        this.rankScoreCounter = 0    # score đang đếm của rank hiện tại
        this.rankFrameCounter = 0

    def update(this, playerData, score):
        # =======================
        # BACKGROUND
        # =======================
        window.blit(this.Texture, this.rect)

        # =======================
        # ĐẾM SCORE PLAYER
        # =======================
        this.frameCounter += 1
        if this.frameCounter % 20 == 0:
            if this.scoreCounter < score:
                this.scoreCounter += 1

        window.blit(
            font.render(str(this.scoreCounter), True, (255, 255, 255)),
            (this.rect.x + 470, this.rect.y + 100)
        )

        # =======================
        # LOAD TOP 3 (1 LẦN)
        # =======================
        if not this.gottop3:
            this.gettop3()

        # =======================
        # CASCADE TOP 3
        # =======================
        if this.scoreCounter == score and this.gottop3:

            start_y = this.rect.y + 440

            # ----- vẽ những rank đã hoàn thành -----
            for i in range(this.revealRank):
                player = this.top_3_players[i]

                window.blit(
                    font.render(f"{i+1}. {player['username']}", True, (255,255,255)),
                    (this.rect.x + 110, start_y + i * 40)
                )

                window.blit(
                    font.render(str(player['score']), True, (255,255,255)),
                    (this.rect.x + 420, start_y + i * 40)
                )

            # ----- xử lý rank hiện tại -----
            if this.revealRank < len(this.top_3_players):

                player = this.top_3_players[this.revealRank]

                this.rankFrameCounter += 1
                if this.rankFrameCounter % 10 == 0:
                    if this.rankScoreCounter < player["score"]:
                        this.rankScoreCounter += 1

                # vẽ username
                window.blit(
                    font.render(
                        f"{this.revealRank+1}. {player['username']}",
                        True,
                        (255,255,255)
                    ),
                    (this.rect.x + 110, start_y + this.revealRank * 40)
                )
                # vẽ score đang đếm
                window.blit(
                    font.render(
                        str(this.rankScoreCounter),
                        True,
                        (255,255,255)
                    ),
                    (this.rect.x + 420, start_y + this.revealRank * 40)
                )

                # ----- xong rank này → sang rank tiếp -----
                if this.rankScoreCounter >= player["score"]:
                    this.revealRank += 1
                    this.rankScoreCounter = 0
                    this.rankFrameCounter = 0

    def gettop3(this):
        players = []

        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                players.append(json.loads(line))

        this.top_3_players = sorted(
            players,
            key=lambda x: x["score"],
            reverse=True
        )[:3]

        this.gottop3 = True



# Initialize the game   
class State(Enum):
    isRunning = 1
    isOver = 2
    mainMenu = 3
class loginState(Enum):
    Nonee = -1
    choosingloggingOptions = 0
    enteringUsername = 1
class GlobalEvent(Enum):
    Loggingin = 0
    Loggedin = 1
class Buttons(IntEnum):
    Easy = 0
    Medium = 1
    Hard = 2
    Tutorial = 3
    Shop = 4 
    Nonee = 5
class LoginOptions(IntEnum):
    Nonee = -1
    Create = 0
    EnterExisting = 1

Event = GlobalEvent.Loggingin
 
game = MainGame()
Login = Login()
# Game loop
def main():
    # print(texture_path)
    

    deltaTime = clock.tick(60) / 1000.0

    while True:
        clock.tick(120)  # 120 FPS\

        # Update sprites
        if(Event == GlobalEvent.Loggingin):
            Login.update(pygame.key.get_pressed(),deltaTime,game)
        if(Event == GlobalEvent.Loggedin):
            game.update(pygame.key.get_pressed(),deltaTime)

        # Refresh the screen
        pygame.display.flip() 

if __name__ == "__main__":
    main()