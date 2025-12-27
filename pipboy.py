import pygame
pygame.init()

class PipBoy:
    def __init__(self, width=800, height=480, framerate=60):
        self.width = width
        self.height = height
        self.font= pygame.font.Font("monofonto.ttf", 18) 
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.framerate = framerate
        self.clock = pygame.time.Clock()
        self.run_loop() #Initializes the main loop of the PipBoy

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    def bootup_sequence(self):
        self.screen.fill('black')

        boot_text = ["******************************* PIP-OS (R) V7 .1.0.8 ********************************",
                    "",
                    "",
                    "",
                    "COPYRIGHT 2075 ROBCO(R)",
                    "LOADER V1.1",
                    "EXEC VERSION 41.10",
                    "264k RAM SYSTEM",
                    "253k BYTES FREE",
                    "NO HOLOTAPE FOUND"
                    "LOAD ROM(1): DEITRIX 303"]
        
        for i, line in enumerate(boot_text):
            pos = 0
            for char in line:
                self.event_handler()
                char_text = self.font.render(char, True, (2, 255, 2))
                char_x = 15 + pos
                char_y = 10 + i * (pygame.font.Font.size(self.font, char)[1] + 4)
                self.screen.blit(char_text, (char_x, char_y))
                pygame.display.flip()
                pygame.time.delay(40)
                pos += pygame.font.Font.size(self.font, char)[0]
                self.clock.tick(self.framerate)
    

    #Main loop of the PipBoy    
    def run_loop(self):
        running = True
        bootup_done = False
    
        if not bootup_done:
            self.bootup_sequence()
            bootup_done = True
            pygame.time.delay(2000)
            self.screen.fill('black')

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.display_update()  
            self.clock.tick(self.framerate)
    

        pygame.quit()

    #Updates the entire screen with the current state of the PipBoy
    def display_update(self):
        pygame.display.flip()
    
boi = PipBoy()

