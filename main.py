# -*- coding: utf-8 -*-

import pygame, sys
from pygame import mixer
from settings import Settings
from characters import Characters
from tiledmap import TiledMap
from fighter import Fighter

class Game:

    def __init__(self):
        
    #define game variables
        mixer.init()
        pygame.init()
        self.settings = Settings()
        self.intro_count = self.settings.intro_count
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0,0]
        self.round_over = False
        self.ROUND_OVER_COOLDOWN = 2000
        self.characters = ["king", "ninja", "samurai", "warrior", "wizard"]
        self.clock = pygame.time.Clock()
        self.FPS = self.settings.fps
    
        #set screen
        self.screen_dimensions = pygame.display.Info()
        self.screen_w = self.screen_dimensions.current_w
        self.screen_h = self.screen_dimensions.current_h
    
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
    
        pygame.display.set_caption("Melee")
        
        #stage setup
        self.tiled_map = TiledMap()
        
        self.count_font = None
        self.count_font_size = None
        self.score_font = None
        self.score_font_size = None
        self.load_fonts()

    #function for drawing fighter health bars

    def draw_health_bar(self, health, x, y):
        
        ratio = health / 100  
        pygame.draw.rect(self.screen, self.settings.colours["WHITE"], (x - 2, y - 2, (self.screen_w/3) + 4, 34))
        pygame.draw.rect(self.screen, self.settings.colours["RED"], (x, y, self.screen_w/3, 30))
        pygame.draw.rect(self.screen, self.settings.colours["YELLOW"], (x, y, self.screen_w/3 * ratio, 30))
    
    #function for drawing background
    def draw_bg(self):
        
        scaled_bg = pygame.transform.scale(self.tiled_map.map_image, (self.screen_w, self.screen_h))
        self.screen.blit(scaled_bg, (0, 0))
        
    def draw_text(self, text, font, text_colour, x, y):
        img = font.render(text, True, text_colour)
        self.screen.blit(img,(x,y))
        
    def set_music(self):
        pygame.mixer.music.load("images/Music/menu.mp3")
        pygame.mixer.music.set_volume(self.settings.volume)
        pygame.mixer.music.play(-1, 0.0, 5000)

    def load_sfx(self):
        
        sword_fx = pygame.mixer.Sound("images/characters/Warrior/sword_attack.wav")
        pygame.mixer.music.set_volume(self.settings.volume)
        
        magic_fx = pygame.mixer.Sound("images/characters/Wizard/fire_attack.wav")
        pygame.mixer.music.set_volume(self.settings.volume)
        
        return sword_fx, magic_fx
    
    def set_starting_conditions(self):

        #load random background image
        
        map_rect = self.tiled_map.map_image.get_rect()

    def load_fonts(self):
        self.count_font = pygame.font.Font(self.settings.count_font, self.settings.count_font_size)
        self.score_font = pygame.font.Font(self.settings.score_font, self.settings.score_font_size)

        
    def character_select(self):
        p1 = Characters("warrior","Player 1")
        p2 = Characters("ninja","Player 2")
        
        return p1, p2
        
    def create_fighters(self, p1, p2, sound_effect1, sound_effect2):
    
        player1, player2 = self.tiled_map.spawn_players()
        fighter_1 = Fighter(1, player1[0], player1[1], False, p1.new_character(), self.tiled_map, sound_effect1)
        fighter_2 = Fighter(2, player2[0], player2[1], True, p2.new_character(), self.tiled_map, sound_effect2)
        
        return fighter_1, fighter_2
    
    def run(self, fighter_1, fighter_2):
        run = True
        
        while run:
            
            #quit game
            pygame.init()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    run = False        
        
            self.clock.tick(self.settings.fps)
            # draw background
            self.draw_bg()
            sword, magic = self.load_sfx()
            p1 , p2 = self.character_select()
            #pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,315,105,400))
            #stages.draw_grid(screen, screen_w, screen_h)
            #stages.draw(screen)
            
            #show player stats
            self.draw_health_bar(fighter_1.health, 20, 50)
            self.draw_health_bar(fighter_2.health, -20 + (self.screen_w/3) * 2, 50)
            self.draw_text(f"{fighter_1.name}: " + str(self.score[0]), self.score_font, self.settings.colours["RED"], 20, 80)
            self.draw_text(f"{fighter_1.name}: " + str(self.score[1]), self.score_font, self.settings.colours["RED"], (self.screen_w/3) * 2, 80)
            
            #update countdown
            
            if self.intro_count <= 0:
                #move players
                fighter_1.move(self.screen_w, self.screen_h, self.screen, fighter_2, self.tiled_map.map_image)
                fighter_2.move(self.screen_w, self.screen_h, self.screen, fighter_1, self.tiled_map.map_image)

        
            else:
                #display count timer
                self.draw_text(str(self.intro_count), self.count_font, self.settings.colours["RED"], self.screen_w / 2, self.screen_h/ 3)
                
                if pygame.time.get_ticks() - self.last_count_update >= 1000:
                    self.intro_count -= 1
                    self.last_count_update = pygame.time.get_ticks()
                    
            
            #update fighters
            
            fighter_1.update()
            fighter_2.update()
        
            #draw fighters
            
            fighter_1.draw(self.screen)
            fighter_2.draw(self.screen)
        
            
            #check for player defeat
            if self.round_over == False:
                if fighter_1.death == True:
                    self.score[1] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
                elif fighter_2.death == True:
                    self.score[0] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            else:
                self.draw_text("VICTORY", self.count_font, self.settings.colours["RED"], self.screen_w / 2 - 120, self.screen_h/ 3)
                if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    self.intro_count = 3
                    
                    self.create_fighters(p1, p2, sword, sword)
                    
        
        
            #update display
            pygame.display.update()
                    
        pygame.quit()

g = Game()
player1, player2 = g.character_select()
sound1, sound2 = g.load_sfx()
fighter1, fighter2 = g.create_fighters(player1, player2, sound1, sound2)
g.run(fighter1, fighter2)