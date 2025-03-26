import pygame

class Sound:
    def __init__(self, path:str):
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        self.sound.play()