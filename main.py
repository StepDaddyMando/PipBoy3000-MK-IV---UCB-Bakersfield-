import pygame
import pipboy as pip

pygame.init()
pipboy = pip.PipBoy()

if __name__ == "__main__":
    pipboy.run_loop()
