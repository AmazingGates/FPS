import pygame as pg

class Sound: # This is where we create our class for sound. In the class itslef, we need to initialize the sound mixer
    #and load the file we need
    def __init__(self,game):
        self.game = game
        pg.mixer.init()
        self.path = "Resources/Sound/"
        self.Weapon = pg.mixer.Sound(self.path + "Shotgun Shot.mp3")
        self.npc_pain = pg.mixer.Sound(self.path + "Zombie Pain Sound.mp3")
        self.npc_death = pg.mixer.Sound(self.path + "Zombie Pain Sound.mp3")
        self.npc_shot = pg.mixer.Sound(self.path + "Zombie Shot Sound.mp3")
        self.npc_attack = pg.mixer.Sound(self.path + "Zombie Attack Sound.mp3")
        self.player_pain = pg.mixer.Sound(self.path + "Player Hit Sound.mp3")
        self.theme = pg.mixer.music.load(self.path + "Background Music.mp3")