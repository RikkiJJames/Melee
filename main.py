# -*- coding: utf-8 -*-

import pygame, sys
from fighter import Fighter
from pygame import mixer
from settings import Settings
from characters import Characters
from stages import Stages

mixer.init()
settings = Settings()
pygame.init()

#define coloursaz

YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = settings.intro_count
last_count_update = pygame.time.get_ticks()
score = [0,0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#set screen
screen_dimensions = pygame.display.Info()
screen_w = screen_dimensions.current_w
screen_h = screen_dimensions.current_h

screen = pygame.display.set_mode((screen_w, screen_h))

pygame.display.set_caption("Melee")

#load music and sounds
pygame.mixer.music.load("images/Music/menu.mp3")
pygame.mixer.music.set_volume(settings.volume)
pygame.mixer.music.play(-1, 0.0, 5000)

sword_fx = pygame.mixer.Sound("images/characters/Warrior/sword_attack.wav")
pygame.mixer.music.set_volume(settings.volume)

magic_fx = pygame.mixer.Sound("images/characters/Wizard/fire_attack.wav")
pygame.mixer.music.set_volume(settings.volume)

#load random background image
stages = Stages(screen_w, screen_h)
bg_image = pygame.image.load("images/background/misty.jpg").convert_alpha()


clock = pygame.time.Clock()
FPS = settings.fps

#define font

count_font = pygame.font.Font("images/Fonts/Turok.ttf", 80)
score_font = pygame.font.Font("images/Fonts/Turok.ttf", 30)


#character select

characters = ["king", "ninja", "samurai", "warrior", "wizard"]

p1 = Characters("wizard","Player 1")
p2 = Characters("samurai","Player 2")

def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img,(x,y))

# fucntion for drawing background

def draw_bg():
    
    scaled_bg = pygame.transform.scale(bg_image, (screen_w,screen_h))
    screen.blit(scaled_bg, (0, 0))

# function for drawing fighter health bars

def draw_health_bar(health, x, y):
    ratio = health / 100  
    pygame.draw.rect(screen, settings.colours["WHITE"], (x - 2, y - 2, (screen_w/3) + 4, 34))
    pygame.draw.rect(screen, settings.colours["RED"], (x, y, screen_w/3, 30))
    pygame.draw.rect(screen, settings.colours["YELLOW"], (x, y, screen_w/3 * ratio, 30))
    
    
# create fighter instances

fighter_1 = Fighter(1, 20, 300, False, p1.new_character(), sword_fx)
fighter_2 = Fighter(2, 1200, 310, True, p2.new_character(), magic_fx)


run = True

while run:
    
    #quit game
    pygame.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            run = False        

    clock.tick(settings.fps)
    # draw background
    draw_bg()
    
    #show player stats
    
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, -20 + (screen_w/3) * 2, 20)
    draw_text(f"{p1.name}: " + str(score[0]), score_font, RED, 20, 60)
    draw_text(f"{p2.name}: " + str(score[1]), score_font, RED, (screen_w/3) * 2, 60)
    stages.draw_grid(screen, screen_w, screen_h)
    
    
    #update countdown
    
    if intro_count <= 0:
        #move players
        fighter_1.move(screen_w, screen_h, screen, fighter_2)
        fighter_2.move(screen_w, screen_h, screen, fighter_1)

    else:
        #display count timer
        draw_text(str(intro_count), count_font, RED, screen_w / 2, screen_h/ 3)
        
        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            
    
    #update fighters
    
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    
    #check for player defeat
    if round_over == False:
        if fighter_1.death == True:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.death == True:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        draw_text("VICTORY", count_font, RED, screen_w / 2 - 120, screen_h/ 3)
        if pygame.time.get_ticks() - round_over_time > settings.round_over_cooldown:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 100, 300, False, p1.new_character(), sword_fx)
            fighter_2 = Fighter(2, 700, 310, True, p2.new_character(), magic_fx)
            bg_image = pygame.image.load(stages.select_stage()).convert_alpha()

    
                
    
    #update display
    pygame.display.update()
            
pygame.quit()

    