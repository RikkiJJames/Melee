# -*- coding: utf-8 -*-
import os
import random
import pygame
import csv

class Stages:
    
    def __init__(self, ):
        
        
        self.file_root = "images/background/tmx"
        self.stages = []
        self.load_stages()
        self.stage = None
        self.select_stage()

        
        
    def load_stages(self):
        
        for stage in os.listdir(self.file_root):
            if stage.endswith(".tmx"):
                self.stages.append(os.path.join(self.file_root, stage))
                

    def select_stage(self):
        
        #self.stage = random.choice(self.stages)
        self.stage = self.stages[0]
        self.stages.remove(self.stage)
        
        return self.stage
    
    

    
    '''
    def draw_grid(self, screen, screen_w, screen_h):
        
        for line in range(int(screen_w/self.tile_size)):
            pygame.draw.line(screen, (255,255,255), (0, line * self.tile_size),(screen_w, line * self.tile_size))
            pygame.draw.line(screen, (255,255,255), (line * self.tile_size, 0),(line * self.tile_size, screen_h))
            
    
    def draw(self, surface):
        
        for tile in self.tile_list:
            pass
            #surface.blit(tile[0], tile[1])
            #pygame.draw.rect(surface, (255,255,255), tile[1])
            #pygame.draw.rect(surface, (255,0,0), (0,0,10,10))
            
    
        
s = Stages(100,200)

        '''
        
