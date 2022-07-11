# -*- coding: utf-8 -*-

#load spritesheets

skeleton_file_root = "images/characters/Skeleton/"
goblin_file_root = "images/characters/Goblin/"

skeleton_animation_steps = {"idle":4, "move": 4, "attack": 8, "damage": 4, "die": 4}
goblin_animation_steps = {"idle":4, "move": 8, "attack": 8, "damage": 4, "die": 4}

#define fighter variables
skeleton_size = 150
skeleton_scale = 2
skeleton_offset = [72, 56]
skeleton_data = [skeleton_file_root, skeleton_size, skeleton_animation_steps, skeleton_scale, skeleton_offset]
goblin_size = 150
goblin_scale = 2
goblin_offset = [72, 56]
goblin_data = [goblin_file_root, goblin_size, goblin_animation_steps, goblin_scale, goblin_offset]