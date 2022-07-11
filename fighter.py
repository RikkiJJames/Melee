# -*- coding: utf-8 -*-
import pygame
from spritesheet import SpriteSheet

class Fighter():
    
    def __init__(self,player, x, y, flip, data, sound):
        self.player = player
        self.size = data[1]
        self.scale = data[3]
        self.offset = data[4]
        self.flip = flip
        self.rect = pygame.Rect((x, y, 50, 80))
        self.vel_y = 0
        self.jump = False
        self.moving = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.action = "idle"
        self.health = 10
        self.death = False
        self.frame_index = 0
        self.states = {"idle":{"url":f"{data[0]}Idle.png",
                               "animation_properties":{"steps":data[2]["idle"],"width":self.size,"height":self.size},
                               "images": []},
                       "move":{"url":f"{data[0]}Move.png",
                              "animation_properties":{"steps":data[2]["move"],"width":self.size,"height":self.size},
                              "images": []},
                       "jump":{"url":f"{data[0]}Jump.png",
                              "animation_properties":{"steps":data[2]["jump"],"width":self.size,"height":self.size},
                              "images": []},
                       "fall":{"url":f"{data[0]}Fall.png",
                              "animation_properties":{"steps":data[2]["jump"],"width":self.size,"height":self.size},
                              "images": []},
                       "attack":{"url":f"{data[0]}Attack.png",
                                 "animation_properties":{"steps":data[2]["attack"],"width":self.size,"height":self.size},
                                 "images": []},
                       "damage":{"url":f"{data[0]}Damage.png",
                               "animation_properties":{"steps": data[2]["damage"],"width":self.size,"height":self.size},
                               "images": []},
                       "die":{"url":f"{data[0]}Death.png",
                            "animation_properties":{"steps":data[2]["die"],"width":self.size,"height":self.size},
                           "images": []}
                           }
        self.load_images()
        self.image = self.states[self.action]["images"][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        
        
    def load_images (self):
        
        states = self.states.keys()
        
        for state in states :
            file_name = self.states[state]["url"]
            print(f" FILENAME IS: {file_name}")
            sprite_sheet = SpriteSheet(file_name)

            for step in range(self.states[state]["animation_properties"]["steps"]):
                self.states[state]["images"].append(sprite_sheet.get_sprite(step, self.states[state]["animation_properties"]["width"],self.states[state]["animation_properties"]["height"] , self.scale))
        
    
            
    def move(self, screen_width, screen_height, surface, target):
        
        SPEED = 5
        GRAVITY = 2
        dx = 0
        dy = 0
        self.moving = False
        
        #key presses
        key = pygame.key.get_pressed()
        
        #can only perform other actions if not currently attacking
        #movement
        if self.attacking == False and self.death == False:
            #checkplayer 1 controls
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.moving = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.moving = True
                #jump
                
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y= -30
                    self.jump = True
                
                #attacks
                
                if key[pygame.K_SPACE]:
                    self.attack(surface, target)
                    
            
            if self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.moving = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.moving = True
                #jump
                
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y= -30
                    self.jump = True
                
                #attacks
                
                if key[pygame.K_l]:
                    self.attack(surface, target)
                    
        
        #apply gravity  
        self.vel_y += GRAVITY
        dy += self.vel_y
            
        # ensure player stays on screen
        
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
              dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 500:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 500 - self.rect.bottom
            
            
        #ensure players face each other
        
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
              
            
        #apply attack cooldown
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        #update position 
        
        self.rect.x += dx
        self.rect.y += dy
        
    # handle animation updates
    def update(self):
        
        #check what action player is performing
        if self.health <= 0:
            self.health = 0
            self.death = True
            self.update_action("die")
        elif self.hit == True:
            self.update_action("damage")
        elif self.attacking == True:
            self.update_action("attack")
        elif self.jump == True:
            self.update_action("jump")
        elif self.moving == True:
            self.update_action("move")
        else:
            self.update_action("idle")
            
        animation_cooldown = 50
        
        #update image
        self.image = self.states[self.action]["images"][self.frame_index]
        
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        #check if animation is finished
        if self.frame_index >= self.states[self.action]["animation_properties"]["steps"]:
            #if player is dead. End animation
            if self.death == True:
                self.frame_index = self.states[self.action]["animation_properties"]["steps"] - 1
            else:
                self.frame_index = 0
            
            #check if attack was executed
            
            if self.action == "attack":
                self.attacking = False
                self.attack_cooldown = 20
            
            #check if damage was taken
            
            if self.action == "damage":
                self.hit = False
                
            #if player was in the middle of attack then it's stopped
                self.attacking = False
                self.attack_cooldown = 20
                
            #if player dies
            
            
    
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attack_sound.play()
            self.attacking = True    
            attacking_rect = pygame.Rect(self.rect.centerx - (1.5 * self.rect.width * self.flip), self.rect.y, 1.5 * self.rect.width, self.rect.height)
            
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            
            #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
        
    def update_action(self, new_action):
        #check if new action is different to previous
        
        if new_action != self.action:
            self.action = new_action
            #update animtion settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def draw(self, surface):
        
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255,0,0) , self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.scale), self.rect.y - (self.offset[1] * self.scale)))        
        