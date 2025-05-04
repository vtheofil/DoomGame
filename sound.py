import pygame as pg

class Sound:
    def __init__(self,game):
        self.game = game 
        pg.mixer.init()
        
        self.shotgun = pg.mixer.Sound(r"AssetsGame\sound\shotgun.wav")
        self.npc_pain = pg.mixer.Sound(r"AssetsGame\sound\npc_pain.wav")
        self.npc_death = pg.mixer.Sound(r"AssetsGame\sound\npc_death.wav")
        self.npc_shot = pg.mixer.Sound(r"AssetsGame\sound\npc_attack.wav")
        self.player_pain = pg.mixer.Sound(r"AssetsGame\sound\player_pain.wav")
        self.theme = pg.mixer.music.load(r"AssetsGame\sound\theme.mp3")
        pg.mixer.music.set_volume(0.3)
        