# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 10:26:13 2022

@author: Rjjam
"""
import pygame
import pytmx
from stages import Stages
    
#print(layer.data)`


class Obstacle(pygame.sprite.Sprite):
    
    def __init__ (self, game, x, y, w, h):
        self.groups = game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Hole(pygame.sprite.Sprite):
    
    def __init__ (self, game, x, y, w, h):
        self.groups = game.holes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        
class TiledMap:
    
    
    
    def __init__(self):
        self.stage = Stages().stage
        tile_map = pytmx.load_pygame(self.stage, pixelalpha = True)
        self.width = tile_map.width * tile_map.tilewidth
        self.height = tile_map.height * tile_map.tileheight
        self.tmx_data = tile_map
        self.platforms = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        self.map_image = self.make_map()
        
        
        
        
    def render(self, surface):
        
        self.make_platforms()
        self.make_holes()
        tile_image = self.tmx_data.get_tile_image_by_gid
        
        for layer in self.tmx_data.visible_layers:
            
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tile_image(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth, 
                                            y * self.tmx_data.tileheight))
                        
    def make_map(self):
        
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
    
    
    def spawn_players(self):
        
        player1 = []
        player2 = []
        
        for tile_object in self.tmx_data.objects:
            if tile_object.name == "player1":
                player1.append(tile_object.x)
                player1.append(tile_object.y)
            elif tile_object.name == "player2":
                player2.append(tile_object.x)
                player2.append(tile_object.y)
                
        return (player1, player2)
                
    def make_platforms(self):
        for tile_object in self.tmx_data.objects:
            if tile_object.name == "platform":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                
    def make_holes(self):
        for tile_object in self.tmx_data.objects:
            if tile_object.name == "hole":
                Hole(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                print("found hole")
 
                
    
        

            

            