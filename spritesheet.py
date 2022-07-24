# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 13:43:24 2022

@author: Rjjam
"""
import pygame

class SpriteSheet:

    def __init__(self, file_name):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(file_name).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {file_name}")
            raise SystemExit(e)

    def get_sprite(self, frame, width, height, scale):
        
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        #sprite.set_colorkey((0,0,0))
        sprite.blit(self.sheet, (0,0),((frame * width) , 0, width, height))
        sprite = pygame.transform.scale(sprite, (width * scale , height * scale))
        
        return sprite
    