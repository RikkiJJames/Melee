# -*- coding: utf-8 -*-
import os
import random
import pygame

class Stages:
    
    def __init__(self, screen_w, screen_h):
        
        
        self.file_root = "images/background/"
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.stages = []
        self.list = [1,2,3,4,5]
        self.load_stages()
        self.stage = None
        self.image = pygame.image.load("images/background/misty.jpg")
        self.tile_size = 10
        self.rect = self.image.get_rect()
        self.tile_list = []
        
        
        
    def load_stages(self):
        
        for image in os.listdir(self.file_root):
            if image.endswith(".jpg"):
                self.stages.append(os.path.join(self.file_root, image))
                
    def select_stage(self):
        
        self.stage = random.choice(self.stages)
        self.stages.remove(self.stage)
        
        return self.stage
    '''
    def tiles(self, data):
        
        
        back_ground = pygame.transform.scale(self.image, (sile_size, tile_size))
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    self.rect.x =col_count * self.tile_size
                    self.rect.y = row_count * self.tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
            col_count += 1
        row_count += 1
    '''
    
    def draw_grid(self, screen, screen_w, screen_h):
        
        for line in range(int(screen_w/self.tile_size)):
            pygame.draw.line(screen, (255,255,255), (0, line * self.tile_size),(screen_w, line * self.tile_size))
            pygame.draw.line(screen, (255,255,255), (line * self.tile_size, 0),(line * self.tile_size, screen_h))

        
        

#class Platform(s)
        
        
        
