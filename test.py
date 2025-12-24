import pygame

class PipBoy:
    def __init__(self, width=800, height=480):
        pygame.init()
        self.screen = pygame.display.set_mode(width, height)
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)  # Position the PipBoy at the top-left corner

    def display(self):
        self.screen.blit(self.image, self.rect)
        

pipboy = PipBoy()
pipboy.display()