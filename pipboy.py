import pygame
import random
import math
import menus


class PipBoy:
    def __init__(
        self,
        width=800,
        height=480,
        framerate=60,
        menu_tabs=[
            menus.StatusTab(),
            menus.InventoryTab(),
            menus.DataTab(),
            menus.MapTab(),
            menus.RadioTab(),
        ],
    ):
        self.width = width
        self.height = height
        self.font_18 = pygame.font.Font("monofonto.ttf", 18)
        self.font_24 = pygame.font.Font("monofonto.ttf", 24)
        self.font_36 = pygame.font.Font("monofonto.ttf", 36)
        self.green_text = (2, 255, 2)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.scanline_surface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        self.flicker_surface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        self.flicker_phase = 0.0
        self.flicker_speed = 0.6
        self.flicker_strength = 0.03
        self.create_scanlines()
        self.framerate = framerate
        self.clock = pygame.time.Clock()
        self.tabs = menu_tabs
        self.menu_index = 0  # Tracks which menu is currently active
        self.submenu_index = 0  # Tracks which submenu is currently active

    def event_handler(self):
        for event in pygame.event.get():
            # Handle quitting the application
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Handle key presses for menu navigation
            if event.type == pygame.KEYDOWN:
                # Left and Right arrow keys are used to switch between main menu tabs
                if event.key == pygame.K_LEFT:
                    if self.menu_index > 0:
                        self.menu_index -= 1
                        self.submenu_index = 0

                elif event.key == pygame.K_RIGHT:
                    if self.menu_index < len(self.tabs) - 1:
                        self.menu_index += 1
                        self.submenu_index = 0

                # Up and Down arrow keys are used to navigate the submenus within the current tab
                elif event.key == pygame.K_UP:
                    if self.submenu_index > 0:
                        self.submenu_index -= 1

                elif event.key == pygame.K_DOWN:
                    if (
                        self.submenu_index
                        < len(self.tabs[self.menu_index].subtabs()) - 1
                    ):
                        self.submenu_index += 1

                elif event.key == pygame.K_RETURN:
                    self.tabs[self.menu_index].update_selected_submenu(
                        self.submenu_index
                    )

    def create_scanlines(self):
        self.scanline_surface.fill((0, 0, 0, 0))
        line_spacing = 2
        alpha_value = 40

        for y in range(0, self.height, line_spacing):
            pygame.draw.line(
                self.scanline_surface, (0, 0, 0, alpha_value), (0, y), (self.width, y)
            )

    def apply_frame_flicker(self, dt):
        # Uses sin function to create a smooth flicker effect
        self.flicker_phase += self.flicker_speed * dt
        flicker = math.sin(self.flicker_phase)
        brightness = 1.0 + (flicker * self.flicker_strength)
        brightness = max(0.97, min(1.03, brightness))
        value = int(255 * brightness)  
        value = max(0, min(255, value))# converts brightness to a int, ensuring its from 0-255
        self.flicker_surface.fill((value, value, value, 255))
        self.screen.blit(
            self.flicker_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT
        )

    def bootup_sequence(self):
        self.screen.fill((0, 6, 0))

        boot_text = [
            "******************************* PIP-OS (R) V7 .1.0.8 ********************************",
            "",
            "",
            "",
            "COPYRIGHT 2075 ROBCO(R)",
            "LOADER V1.1",
            "EXEC VERSION 41.10",
            "264k RAM SYSTEM",
            "253k BYTES FREE",
            "NO HOLOTAPE FOUNDLOAD ROM(1): DEITRIX 303",
        ]

        for i, line in enumerate(boot_text):
            pos = 0
            for char in line:
                self.event_handler()
                char_text = self.font_18.render(char, True, self.green_text)
                char_x = 15 + pos
                char_y = 10 + i * (pygame.font.Font.size(self.font_18, char)[1] + 4)
                self.screen.blit(
                    char_text, (char_x, char_y)
                )  # adds character to the frame for a typewriter effect
                self.screen.blit(
                    self.scanline_surface, (0, 0)
                )  # adds scanlines to the bootup frame
                pygame.display.flip()  # renders the completed bootup frame
                pygame.time.delay(40)
                pos += pygame.font.Font.size(self.font_18, char)[0]
                self.clock.tick(self.framerate)

    # Main loop of the PipBoy
    def run_loop(self):
        running = True
        bootup_done = False

        if not bootup_done:
            self.bootup_sequence()
            bootup_done = True
            pygame.time.delay(2000)
            self.screen.fill("black")

        while running:
            self.event_handler()
            dt = self.clock.get_time() / 1000.0
            self.tabs[self.menu_index].draw_menu(
                self.screen,
                self.tabs,
                self.menu_index,
                self.submenu_index,
                self.green_text,
                self.font_36,
                self.font_24,
            )

            self.screen.blit(
                self.scanline_surface, (0, 0)
            )  # adds scanlines after all frame elements are added to the frame
            self.apply_frame_flicker(dt)  # applys flicker before frame is rendered

            pygame.display.flip()  # renders the completed frame
            self.clock.tick(self.framerate)

        pygame.quit()

    # Updates the entire screen with the current state of the PipBoy
    def display_update(self):
        pygame.display.flip()
