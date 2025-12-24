import pygame


pygame.init()
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()