import pygame
import random
import math
import menus
from moviepy import VideoFileClip


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

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.start_image = pygame.image.load("PipBoyStart (1).png").convert()
        self.start_image = pygame.transform.scale(
            self.start_image, self.screen.get_size()
        )

        self.font_18 = pygame.font.Font("monofonto.ttf", 18)
        self.font_24 = pygame.font.Font("monofonto.ttf", 24)
        self.font_36 = pygame.font.Font("monofonto.ttf", 36)
        self.green_text = (2, 255, 2)

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
                        self.submenu_index, "K_RETURN"
                    )

                elif event.key == pygame.K_q:
                    self.tabs[self.menu_index].update_selected_submenu(
                        self.submenu_index, "K_q"
                    )

                elif event.key == pygame.K_e:
                    self.tabs[self.menu_index].update_selected_submenu(
                        self.submenu_index, "K_e"
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
        value = max(
            0, min(255, value)
        )  # converts brightness to a int, ensuring its from 0-255
        self.flicker_surface.fill((value, value, value, 255))
        self.screen.blit(
            self.flicker_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT
        )

    def show_start_screen(self, duration_ms=2000):
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < duration_ms:
            # keep the window responsive
            self.event_handler()

            # draw the start image
            self.screen.blit(self.start_image, (0, 0))
            self.screen.blit(self.scanline_surface, (0, 0))
            pygame.display.flip()

            # cap FPS so we’re not spinning too fast
            self.clock.tick(self.framerate)

    def play_intro_video(self, path):
        """Play the intro video once between start image and bootup."""
        try:
            clip = VideoFileClip(path)
        except Exception as e:
            print(f"Could not load video {path}: {e}")
            return

        # Match clip FPS to your game or clip fps
        fps = clip.fps if clip.fps else self.framerate

        for frame in clip.iter_frames(fps=fps, dtype="uint8"):
            self.event_handler()

            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            vw, vh = frame_surface.get_size()

            target_w = self.width
            target_h = int(vh * (target_w / vw))

            # if it’s still too tall, fit by height instead
            if target_h > self.height:
                target_h = self.height
                target_w = int(vw * (target_h / vh))

            frame_surface = pygame.transform.smoothscale(
                frame_surface, (target_w, target_h)
            )

            # center on screen
            x = (self.width - target_w) // 2
            y = (self.height - target_h) // 2
            self.screen.blit(frame_surface, (x, y))
            self.screen.blit(frame_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(fps)

        clip.close()

    def scrolling_memory_log(self, duration_s=5.0):
        lines = []
        for cpu in range(0, 16):  # CPU0 .. CPU15 → 16 * 4 = 64 lines
            lines.append(
                "0x0000AA 0x0000000000000000 start memory discovery @ 0x0000AA"
            )
            lines.append(
                f"0x0000AA 0x0000000000000000 CPU{cpu} starting cell relocation"
            )
            lines.append(f"0x0000AA 0x0000000000000000 CPU{cpu} launch EFI0 0x0000AA")
            lines.append(f"0x0000AA 0x0000000000000000 CPU{cpu} starting EFI0 0x0000AA")

        # Pre-render all lines once
        line_surfaces = [
            self.font_18.render(text, True, self.green_text) for text in lines
        ]
        line_height = self.font_18.get_linesize()
        block_height = len(line_surfaces) * line_height

        # Find max line width to center the whole block
        max_line_width = max(surf.get_width() for surf in line_surfaces)

        # Margins
        margin = 20
        x_base = (self.width - max_line_width) // 2

        # Keep margins on both sides
        if x_base < margin:
            x_base = margin
        if x_base + max_line_width > self.width - margin:
            x_base = self.width - margin - max_line_width

        # Start just off the bottom, end fully off the top
        start_y = self.height
        end_y = -block_height
        distance = start_y - end_y  # total pixels to travel

        start_time = pygame.time.get_ticks()

        while True:
            now = pygame.time.get_ticks()
            elapsed_s = (now - start_time) / 1000.0
            t = elapsed_s / duration_s

            if t >= 1.0:
                break

            self.event_handler()

            # Current top Y of the block (lerp)
            current_top = start_y - distance * t

            # Background
            self.screen.fill((0, 6, 0))

            # Draw each line at its offset from current_top
            for i, surf in enumerate(line_surfaces):
                y = current_top + i * line_height
                self.screen.blit(surf, (x_base, y))

            # Scanlines + flicker
            self.screen.blit(self.scanline_surface, (0, 0))
            dt = self.clock.get_time() / 1000.0
            self.apply_frame_flicker(dt)

            pygame.display.flip()
            self.clock.tick(self.framerate)

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

        background_color = (0, 6, 0)
        blink_on_ms = 4  # how long the cursor is visible
        blink_off_ms = 4  # how long it's invisible

        # ---TYPE THE TEXT ---
        for line_index, line in enumerate(boot_text):
            pos_x = 0

            _, char_height = self.font_18.size("A")

            for char in line:
                self.event_handler()

                char_width, _ = self.font_18.size(char)
                char_x = 15 + pos_x
                char_y = 10 + line_index * (char_height + 4)

                cursor_rect = pygame.Rect(char_x, char_y, char_width, char_height)

                # cursor ON
                pygame.draw.rect(self.screen, self.green_text, cursor_rect)
                self.screen.blit(self.scanline_surface, (0, 0))
                pygame.display.flip()
                pygame.time.delay(blink_on_ms)

                # cursor OFF
                pygame.draw.rect(self.screen, background_color, cursor_rect)
                self.screen.blit(self.scanline_surface, (0, 0))
                pygame.display.flip()
                pygame.time.delay(blink_off_ms)

                # draw the character
                char_surface = self.font_18.render(char, True, self.green_text)
                self.screen.blit(char_surface, (char_x, char_y))
                self.screen.blit(self.scanline_surface, (0, 0))
                pygame.display.flip()
                pygame.time.delay(8)

                pos_x += char_width
                self.clock.tick(self.framerate)

        # --- SCROLL ENTIRE SCREEN UP ---

        boot_surface = self.screen.copy()

        duration_s = 2.0  # how long the scroll takes
        start_time = pygame.time.get_ticks()
        h = self.height

        while True:
            now = pygame.time.get_ticks()
            elapsed = (now - start_time) / 1000.0
            t = elapsed / duration_s

            if t >= 1.0:
                break

            self.event_handler()

            y_offset = int(-t * h)

            self.screen.fill(background_color)

            self.screen.blit(boot_surface, (0, y_offset))

            self.screen.blit(self.scanline_surface, (0, 0))
            dt = self.clock.get_time() / 1000.0
            self.apply_frame_flicker(dt)

            pygame.display.flip()
            self.clock.tick(self.framerate)

    def animate_initial_menu_entry(self, total_duration=1.0):
        # Render current menu (STAT / STATUS) once to an off-screen surface
        menu_surface = pygame.Surface((self.width, self.height)).convert()
        self.tabs[self.menu_index].draw_menu(
            menu_surface,
            self.tabs,
            self.menu_index,
            self.submenu_index,
            self.green_text,
            self.font_36,
            self.font_24,
        )

        h = self.height
        overshoot = -40  # pixels above final resting position

        def y_for_t(t):
            """Piecewise y-offset for normalized time t in [0, 1]."""
            if t < 0.25:
                # 1st pass: -h -> +h
                local = t / 0.25
                return -h + (2 * h) * local
            elif t < 0.5:
                # 2nd pass: -h -> +h
                local = (t - 0.25) / 0.25
                return -h + (2 * h) * local
            elif t < 0.75:
                # bounce up: bottom (h) -> overshoot (-40)
                local = (t - 0.5) / 0.25
                return h + (overshoot - h) * local
            else:
                # settle: overshoot -> 0
                local = (t - 0.75) / 0.25
                return overshoot + (0 - overshoot) * local

        def draw_with_offset(y_offset):
            self.screen.fill((0, 6, 0))
            self.screen.blit(menu_surface, (0, int(y_offset)))

            # scanlines + flicker
            self.screen.blit(self.scanline_surface, (0, 0))
            dt = self.clock.get_time() / 1000.0
            self.apply_frame_flicker(dt)

            pygame.display.flip()
            self.clock.tick(self.framerate)

        start_time = pygame.time.get_ticks()
        total_ms = total_duration * 1000.0

        while True:
            self.event_handler()

            now = pygame.time.get_ticks()
            elapsed = now - start_time
            if elapsed >= total_ms:
                break

            t = elapsed / total_ms  # 0 → 1
            y = y_for_t(t)
            draw_with_offset(y)

        # final frame exactly in place
        draw_with_offset(0)

    # Main loop of the PipBoy
    def run_loop(self):
        running = True
        bootup_done = False

        if not bootup_done:
            self.show_start_screen()
            self.scrolling_memory_log()
            self.bootup_sequence()
            self.play_intro_video("Pip.Start 2.mov")
            self.animate_initial_menu_entry()
            bootup_done = True

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
