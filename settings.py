score = [0,0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

class Settings:
    
    def __init__(self):

        self.screen_width = 960
        self.screen_height = 640
        self.intro_count = 3
        self.round_over_cooldown = 2000
        self.fps = 60
        self.volume = 0.1
        self.colours = {"YELLOW": (255, 255, 0), "RED":(255, 0, 0), "WHITE":(255, 255, 255)}
        self.count_font = "images/Fonts/Turok.ttf"
        self.count_font_size = 80
        self.score_font = "images/Fonts/Turok.ttf"
        self.score_font_size = 30
    #define colours

    
    