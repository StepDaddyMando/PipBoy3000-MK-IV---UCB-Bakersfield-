import pygame
import datetime

pygame.init()


class SubMenu:
    def __init__(self, name=None, submenu_index=None):
        self.name = name
        self.submenu_index = submenu_index

    def display_name(self):
        return self.name

    def draw_submenu(self):
        raise NotImplementedError


class StatusMenu(SubMenu):
    def __init__(self, name="STATUS", submenu_index=0):
        super().__init__(name, submenu_index)
        self.current_time = datetime.datetime.now()
        self.military_time = False

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


class SpecialMenu(SubMenu):
    def __init__(self, name="SPECIAL", submenu_index=1):
        super().__init__(name, submenu_index)


class PerksMenu(SubMenu):
    def __init__(self, name="PERKS", submenu_index=2):
        super().__init__(name, submenu_index)


class ItemsMenu(SubMenu):
    def __init__(self, name="ITEMS", submenu_index=0):
        super().__init__(name, submenu_index)


class WeaponsMenu(SubMenu):
    def __init__(self, name="WEAPONS", submenu_index=1):
        super().__init__(name, submenu_index)


class ApparelMenu(SubMenu):
    def __init__(self, name="APPAREL", submenu_index=2):
        super().__init__(name, submenu_index)


class AidMenu(SubMenu):
    def __init__(self, name="AID", submenu_index=3):
        super().__init__(name, submenu_index)


class MiscMenu(SubMenu):
    def __init__(self, name="MISC", submenu_index=4):
        super().__init__(name, submenu_index)


class QuestsMenu(SubMenu):
    def __init__(self, name="QUESTS", submenu_index=0):
        super().__init__(name, submenu_index)


class NotesMenu(SubMenu):
    def __init__(self, name="NOTES", submenu_index=1):
        super().__init__(name, submenu_index)


class WorldMapMenu(SubMenu):
    def __init__(self, name="World Map", submenu_index=0):
        super().__init__(name, submenu_index)


class LocalMapMenu(SubMenu):
    def __init__(self, name="LOCAL MAP", submenu_index=1):
        super().__init__(name, submenu_index)


class StationsMenu(SubMenu):
    def __init__(self, name="STATIONS", submenu_index=0):
        super().__init__(name, submenu_index)


class TuningMenu(SubMenu):
    def __init__(self, name="Tuning", submenu_index=1):
        super().__init__(name, submenu_index)
