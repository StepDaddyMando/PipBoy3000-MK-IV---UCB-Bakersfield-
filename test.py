import pygame

class PipBoy:
    def __init__(self, width=800, height=480, framerate=60):
        pygame.init()
        self.width = width
        self.height = height
        self.font= pygame.font.Font("monofonto.ttf", 12) 
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.framerate = framerate
        self.clock = pygame.time.Clock()
        self.run_loop()
        
    def run_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.display_update()  
            self.clock.tick(self.framerate)
    

        pygame.quit()

    def display_update(self):
        pygame.display.flip()
    
boi= PipBoy()

