# -*- coding: utf-8 -*-

import csv

class Character_Data:
    
    def __init__(self, class_name):
        
        self.class_name = class_name
        self.file_root = f"images/characters/{self.class_name}"
        self.idle_steps = self.get_data(class_name, "idle")
        self.move_steps = self.get_data(class_name, "move")
        self.jump_steps = self.get_data(class_name, "jump")
        self.fall_steps = self.get_data(class_name, "fall")
        self.attack_steps = self.get_data(class_name, "attack")
        self.damage_steps = self.get_data(class_name, "damage")
        self.die_steps = self.get_data(class_name, "die")
        self.size = self.get_data(class_name, "size")
        self.scale = self.get_data(class_name, "scale")
        self.offset_x = self.get_data(class_name, "offset_x")
        self.offset_y = self.get_data(class_name, "offset_y")
        
    def get_data(self, class_name, header):
        with open("characters.csv", newline="") as file:
            reader = csv.reader(file, delimiter = ",")
            
            
            headers = []
            headers = next(reader)
            
            if header in headers:
                index_pos = headers.index(header)
            else:
                print(f"{header} not found in headings")
            
            rows = []
            
            for row in reader:
                rows.append(row)
                
            row_index = None
            for row_number in range(len(rows)):
                if class_name in rows[row_number]:
                    row_index = row_number
                    break
            
            file.close()
            
            if header == "scale":   
                return float(rows[row_index][index_pos])
            else:
                return int(rows[row_index][index_pos])
        
class Character():
    
    def __init__(self, class_name, name):
        self.name = name
        self.character_data = Character_Data(class_name)
        self.animation_steps = {"idle": self.character_data.idle_steps, "move": self.character_data.move_steps, 
                                "jump":self.character_data.jump_steps, "fall": self.character_data.fall_steps, 
                                "attack": self.character_data.attack_steps, "damage": self.character_data.damage_steps, 
                                "die": self.character_data.die_steps}
        self.size = self.character_data.size
        self.scale = self.character_data.scale
        self.offset = [self.character_data.offset_x, self.character_data.offset_y]
        self.data = [self.character_data.file_root, self.size, self.animation_steps, self.scale, self.offset]
    
    def new_character(self):
        
        return self.data

k = Character("Wizard","Rikki")

print(k.new_character())
