import pygame
import datetime

pygame.init()


class SubMenu:
    def __init__(self, name=None, submenu_index=0):
        self.name = name
        self.submenu_index = submenu_index
        self.submenu_list = []

    def display_name(self):
        return self.name

    def submenu_index_range(self):
        return len(self.submenu_list) - 1

    def increase_submenu_index(self):
        if not self.submenu_index < self.submenu_index_range():
            self.submenu_index += 1

    def decrease_submenu_index(self):
        if not self.submenu_index == 0:
            self.submenu_index -= 1

    def draw_submenu(self, screen, y_pos, color):
        raise NotImplementedError

    def input_handler(self):
        raise NotImplementedError


class StatusMenu(SubMenu):
    def __init__(self, name="STATUS", submenu_index=0):
        super().__init__(name, submenu_index)
        self.current_time = datetime.datetime.now()
        self.military_time = False

    def update_time_format(self):
        self.military_time = not self.military_time

    def update_time(self):
        self.current_time = datetime.datetime.now()

    def formatted_time(self):
        if self.military_time:
            formatted_time = self.current_time.strftime("%H:%M:%S")
        else:
            formatted_time = self.current_time.strftime("%I:%M:%S%p")
        return formatted_time

    def formatted_date(self):
        return self.current_time.strftime("%m/%d/%Y")

    def draw_submenu(
        self,
        screen,
        y_pos,
        color,
        time_font=pygame.font.Font("monofonto.ttf", 90),
        date_font=pygame.font.Font("monofonto.ttf", 24),
    ):
        x_pos = 20
        remaining_space = 460 - y_pos
        self.update_time()

        time_text = self.formatted_time()
        rendered_time_text = time_font.render(time_text, True, color)
        time_text_size = pygame.font.Font.size(time_font, time_text)

        date_text = self.formatted_date()
        rendered_date_text = date_font.render(date_text, True, color)
        date_text_size = pygame.font.Font.size(date_font, date_text)

        centered_time_text_x = x_pos + ((760 - time_text_size[0]) // 2)
        centered_time_text_y = y_pos + (
            (remaining_space - time_text_size[1] - date_text_size[1]) // 2
        )
        screen.blit(rendered_time_text, (centered_time_text_x, centered_time_text_y))
        y_pos = centered_time_text_y + time_font.get_linesize()
        centered_date_text_x = x_pos + ((760 - date_text_size[0]) // 2)
        screen.blit(rendered_date_text, (centered_date_text_x, y_pos))

    def input_handler(self):
        if self.submenu_index == 0:
            self.update_time_format()


class SpecialMenu(SubMenu):
    def __init__(self, name="SPECIAL", submenu_index=0):
        super().__init__(name, submenu_index)

        # (name, value, description)
        self.stats = [
            (
                "STRENGTH",
                5,
                "Strength is a measure of your raw physical power. It affects how much you can carry and the damage of all melee attacks.",
            ),
            (
                "PERCEPTION",
                5,
                "Perception is your environmental awareness and 'sixth sense,' and affects weapon accuracy in V.A.T.S.",
            ),
            (
                "ENDURANCE",
                5,
                "Endurance is the measure of your physical fitness. It affects your total Health and the action point drain from sprinting.",
            ),
            (
                "CHARISMA",
                5,
                "Charisma is the ability to charm and convice others. It affects your chance to persuade in dialogue and prices when you barter.",
            ),
            (
                "INTELLIGENCE",
                5,
                "Intelligence is a measure of your overall mental acuity, and affects the number of Experience Points earned.",
            ),
            (
                "AGILITY",
                5,
                "Agility is the measurement of your overall fitness and reflexes. It affects the number of Action Points in V.A.T.S. and your ability to sneak.",
            ),
            (
                "LUCK",
                5,
                "Luck is a measurement of your general good fortune, and affects the recharge rate of Critical Hits.",
            ),
        ]

        self.selected_index = 0

    def wrap_text(self, font, text, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = (current_line + " " + word).strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def draw_submenu(
        self,
        screen,
        y_pos,
        color,
        stat_font=pygame.font.Font("monofonto.ttf", 18),
        desc_font=pygame.font.Font("monofonto.ttf", 18),
    ):
        left_margin = 60
        top = y_pos + 20
        line_spacing = stat_font.get_linesize() + 8

        # fixed value column (aligned by longest name + 3 "tabs")
        tab_width = stat_font.size("    ")[0]
        max_name_width = max(stat_font.size(name)[0] for name, _, _ in self.stats)
        value_column_x = left_margin + max_name_width + 3 * tab_width

        # left list: name + aligned value
        for i, (name, value, desc) in enumerate(self.stats):
            y = top + i * line_spacing

            if i == self.selected_index:
                pointer_surface = stat_font.render(">", True, color)
                pointer_rect = pointer_surface.get_rect()
                pointer_rect.midright = (
                    left_margin - 10,
                    y + stat_font.get_height() // 2,
                )
                screen.blit(pointer_surface, pointer_rect.topleft)

            name_surface = stat_font.render(name, True, color)
            screen.blit(name_surface, (left_margin, y))

            value_surface = stat_font.render(str(value), True, color)
            screen.blit(value_surface, (value_column_x, y))

        # description for selected stat, bottom-right
        _, value, desc = self.stats[self.selected_index]

        desc_x = left_margin + 260
        bottom_start_y = top + line_spacing * len(self.stats) + 20

        screen_width = screen.get_width()
        max_width = screen_width - desc_x - 20

        lines = self.wrap_text(desc_font, desc, max_width)

        for i, line in enumerate(lines):
            text_surface = desc_font.render(line, True, color)
            line_y = bottom_start_y + i * line_spacing
            screen.blit(text_surface, (desc_x, line_y))



    def input_handler(self):
        """
        Called when the user presses ENTER on the SPECIAL submenu.

        For now, we'll simply cycle through S -> P -> E -> C -> I -> A -> L.
        """
        self.selected_index = (self.selected_index + 1) % len(self.stats)



class PerksMenu(SubMenu):
    def __init__(self, name="PERKS", submenu_index=0):
        super().__init__(name, submenu_index)


class ItemsMenu(SubMenu):
    def __init__(self, name="ITEMS", submenu_index=0):
        super().__init__(name, submenu_index)


class WeaponsMenu(SubMenu):
    def __init__(self, name="WEAPONS", submenu_index=0):
        super().__init__(name, submenu_index)


class ApparelMenu(SubMenu):
    def __init__(self, name="APPAREL", submenu_index=0):
        super().__init__(name, submenu_index)


class AidMenu(SubMenu):
    def __init__(self, name="AID", submenu_index=0):
        super().__init__(name, submenu_index)


class MiscMenu(SubMenu):
    def __init__(self, name="MISC", submenu_index=0):
        super().__init__(name, submenu_index)


class QuestsMenu(SubMenu):
    def __init__(self, name="QUESTS", submenu_index=0):
        super().__init__(name, submenu_index)


class NotesMenu(SubMenu):
    def __init__(self, name="NOTES", submenu_index=0):
        super().__init__(name, submenu_index)


class WorldMapMenu(SubMenu):
    def __init__(self, name="World Map", submenu_index=0):
        super().__init__(name, submenu_index)


class LocalMapMenu(SubMenu):
    def __init__(self, name="LOCAL MAP", submenu_index=0):
        super().__init__(name, submenu_index)


class StationsMenu(SubMenu):
    def __init__(self, name="STATIONS", submenu_index=0):
        super().__init__(name, submenu_index)


class TuningMenu(SubMenu):
    def __init__(self, name="Tuning", submenu_index=0):
        super().__init__(name, submenu_index)
