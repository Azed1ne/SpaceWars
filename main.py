import pygame
import os # path for images
pygame.font.init() # initialise font
pygame.mixer.init() # intialise the sound thing

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceWars || my Pygame Hello World")
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # border in the middle

# Settings
FPS = 60
VEL = 5 # Velocity of players
BULLET_VEL = 7 # Velocity of bullet
MAX_BULLETS = 3
PLAYER_HEALTH = 10
HEALTH_FONT = pygame.font.SysFont('Segoe UI', 30, bold=True)
WINNER_FONT = pygame.font.SysFont('Segoe UI', 80, bold=True)

# creating events for players health
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# colors
WHITE = (255, 255, 255)
LGREY = (235, 235, 235)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# SPACESHIP size
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 80, 35

# Loading spaceship images, and fixing their sizes
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'Ship44.png')) # os path join to ensure it works for different OSs
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, 40)), 0)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'Ship33.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)
RED_SPACESHIP = pygame.transform.flip(RED_SPACESHIP, False, True)

# Loading bullet images
YEL_BULLET_IMAGE = pygame.image.load(os.path.join('Assets','shot4.png'))
RED_BULLET_IMAGE = pygame.transform.rotate(pygame.image.load(os.path.join('Assets','shot3.png')), 180)

# Loading the BG
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','bg5.jpg')), (WIDTH, HEIGHT))

# Loading the sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_HIT_SOUND.set_volume(0.1)
BULLET_FIRE_SOUND.set_volume(0.1)


def draw_window(red, yellow, red_bullets, yel_bullets, red_health, yel_health):
    # blit for surfaces, images count as surfaces, we also use blit for text
    WINDOW.blit(SPACE, (0,0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: "+ str(red_health), 1, WHITE)
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    yel_health_text = HEALTH_FONT.render("Health: "+ str(yel_health), 1, WHITE)
    WINDOW.blit(yel_health_text, (10, 10))

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    # Applying skin to bullets
    for bullet in red_bullets:
        # pygame.draw.rect(WINDOW, RED, bullet) # <- this if we want coloured
        WINDOW.blit(RED_BULLET_IMAGE, (bullet.x, bullet.y))
    for bullet in yel_bullets:
        WINDOW.blit(YEL_BULLET_IMAGE, (bullet.x, bullet.y))

    pygame.display.update()

def handle_yellow_movement(keys_pressed, yellow): # function to handle yellow movment [ zqsd ]
    if keys_pressed[pygame.K_z] and yellow.y - VEL > 0:   # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_q] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10:  # DOWN
        yellow.y += VEL

def handle_red_movement(keys_pressed, red): # function to handle red movment [ arrows ]
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10:  # DOWN
        red.y += VEL

def handle_bullets(yel_bullets, red_bullets, yellow, red):
    for bullet in yel_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yel_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yel_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, LGREY)
    WINDOW.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2500) # 2.5 sec pause after someone wins
    pygame.event.clear(eventtype=pygame.KEYDOWN)  # ignore key presses when the game has ended

def main_game():
    # Players hitbox
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # Empty lists to keep track of current bullets being fired ( since we have a cooldown )
    red_bullets = []
    yel_bullets = []

    # Giving players starter Health
    red_health = PLAYER_HEALTH
    yel_health = PLAYER_HEALTH


    clock = pygame.time.Clock() # creating a clock object to fix the fps later
    run = True
    while run:
        clock.tick(FPS) # Capping the FPS at 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() # quit the game

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yel_bullets) < MAX_BULLETS:
                    # -10 in x to fix bullet spawn position
                    bullet = pygame.Rect(yellow.x + yellow.width - 10, yellow.y + yellow.height // 2 , 10, 5)
                    yel_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    # -10 in x to fix bullet spawn position
                    bullet = pygame.Rect(red.x - 10, red.y + red.height//2 , 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yel_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Player 1 wins!"

        if yel_health <= 0:
            winner_text = "Player 2 wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break


        keys_pressed = pygame.key.get_pressed() # get the key being pressed

        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        handle_bullets(yel_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yel_bullets, red_health, yel_health)

    main_game() # auto restart the game

if __name__ == "__main__":
    main_game()