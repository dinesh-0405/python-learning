import pygame, sys
import random
import math
from pygame import mixer


pygame.init()

# creating a SCREEN
SCREEN = pygame.display.set_mode((800, 600))

# title and logo
pygame.display.set_caption("Legendary Space Warriors")
icon = pygame.image.load('001-ufo.png')
pygame.display.set_icon(icon)

# background  ------------------------------------------------------------------------

# game background
background = pygame.image.load('space-background.jpg')
# background music
mixer.music.load('background(1).wav')
mixer.music.play(-1)

# button's background
BG = pygame.image.load("Background.png")

# button's font
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

# game over text
over_font = pygame.font.Font("freesansbold.ttf",64)

# options text
options_font = pygame.font.Font("freesansbold.ttf",32)

# high score text
high_score_font = pygame.font.Font("freesansbold.ttf",32)

# high score
previous_score = 0 
def update_high_score(current_score):
        global previous_score
        with open("high_score.txt","r") as file:
            previous_score = int(file.read())
        if current_score > previous_score:
            with open("high_score.txt","w") as file:
                file.write(str(current_score))
            return True
        else:
            return False


class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


def play():
    #while True:

    # player
    playerimg = pygame.image.load('001-space-invaders.png')
    playerX = 370
    playerY = 480
    playerX_change = 0

    # enemy
    enemyimg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemyimg.append(pygame.image.load('001-space-ship.png'))
        enemyX.append(random.randint(0,736))
        enemyY.append(random.randint(45,145))
        enemyX_change.append(0.4)
        enemyY_change.append(40)

    # bullet

    #ready - you can't see bullet
    #fire - you can see bullet moving
    bulletimg = pygame.image.load('001-bullet.png')
    bulletX = 0
    bulletY = 470
    bulletX_change = 0
    bulletY_change = 1.2
    bullet_state = 'ready'

    # score 
    score_value = 0
    font = pygame.font.Font("freesansbold.ttf",32)
    textX = 10
    textY = 10

    # game over text
    over_font = pygame.font.Font("freesansbold.ttf",64)

    # high score text
    high_score_font = pygame.font.Font("freesansbold.ttf",32)

    def show_score(x,y):
        score = font.render("Score : " + str(score_value), True , (255, 255, 255))
        SCREEN.blit(score, (x, y))

    

    def game_over_text():
        over_text = over_font.render("GAME OVER", True , (255, 255, 255))
        SCREEN.blit(over_text,(220,160))

    def high_score_text():
        high_Score_text = high_score_font.render("High Score : " + str(previous_score), True , (255, 255, 255))
        SCREEN.blit(high_Score_text,(560,10))

    def player(x,y):
        SCREEN.blit(playerimg,(x,y))

    def enemy(x, y, i):
        SCREEN.blit(enemyimg[i],(x,y))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = 'fire'
        SCREEN.blit(bulletimg, (x+16, y+10))

    def iscollision (enemyX,enemyY,bulletX,bulletY):
        distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
        if distance < 28 :
            return True
        else:
            return False

    # game loop 
    running = True
    while running:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill((0,0,0))
        # backgrond image
        SCREEN.blit(background,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if key entered checks right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.6
                if event.key == pygame.K_RIGHT:   
                    playerX_change = 0.6
                if event.key == pygame.K_SPACE: 
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        # get the space ship position and it will assaign to bullet
                        bulletX = playerX  
                        #fire_bullet(bulletX,bulletY)
                        bullet_state = 'fire'
                        SCREEN.blit(bulletimg, (bulletX+16,bulletY+10))


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0


        # checking for boundaries of spaceship so it doesn't go out of bounds
        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # enemy movement
        for i in range(num_of_enemies):

            # game over
            if enemyY[i] > 400 :
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                playerX = 365

                # it will return to main menu or exit the game
                PLAY_BACK = Button(image=None, pos=(400, 290), text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")
                QUIT_BUTTON = Button(image=None, pos=(400, 390), text_input="QUIT", font=get_font(50), base_color="White", hovering_color="Green")

                PLAY_BACK.changeColor(PLAY_MOUSE_POS)
                PLAY_BACK.update(SCREEN)
                QUIT_BUTTON.changeColor(PLAY_MOUSE_POS)
                QUIT_BUTTON.update(SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                            main_menu()
                        if QUIT_BUTTON.checkForInput(PLAY_MOUSE_POS):
                            pygame.quit()
                            sys.exit()
                break
                
            # enemy moment
            enemyX[i] += enemyX_change[i]

            if enemyX[i] <= 0:
                enemyX_change[i] = 0.5  # 0.4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.5   # 0.4
                enemyY[i] += enemyY_change[i]

            # collision
            collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(45, 145)

            enemy(enemyX[i],enemyY[i],i)


        # bullet movement
        if bulletY <= 2:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change



        player(playerX,playerY)
        show_score(textX,textY)
        update_high_score(score_value)
        high_score_text()
        pygame.display.update()


    
def options():
    global previous_score
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        #OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        #OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 260))
        #SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_TEXT = options_font.render(f"HIGH SCORE : {str(previous_score)}",True, "Black")
        SCREEN.blit(OPTIONS_TEXT, (10,10))
        ABOUT_TEXT = options_font.render("ABOUT : This Game Is Developed By Saitama !",True, "Black")
        SCREEN.blit(ABOUT_TEXT, (10,60))
        NOTE_TEXT = options_font.render("NOTE : Join With Us To Make Intresting Gamezzz ",True, "Black")
        SCREEN.blit(NOTE_TEXT, (10,110))
        LINK_TEXT = options_font.render("Contact With My e-mail -> dinesh.g0405",True, "Black")
        SCREEN.blit(LINK_TEXT, (10,160))

        OPTIONS_BACK = Button(image=None, pos=(400, 460), text_input="BACK", font=get_font(55), base_color="Black", hovering_color="Green")

        OPTIONS_LEVELS = Button(image=pygame.image.load("Play Rect.png"), pos=(400, 320), text_input="LEVELS", font=get_font(55), base_color="Black", hovering_color="Green")


        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        OPTIONS_LEVELS.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_LEVELS.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_LEVELS.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(62).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(400, 250), 
                            text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(400, 400), 
                            text_input="OPTIONS", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(400, 550), 
                            text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()



main_menu()