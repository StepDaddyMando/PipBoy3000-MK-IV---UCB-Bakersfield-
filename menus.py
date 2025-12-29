import pygame


class MenuTab:
    def __init__(self, name, font="monofonto.ttf"):
        self.name = name

    def display_tab(self):
        return self.name

    def subtabs(self):
        raise NotImplementedError

    def display_subtabs(self, index):
        return self.subtabs()[index]

    def draw_menu(
        self, screen, tabs, menu_index, submenu_index, color, menu_font, submenu_font
    ):
        screen.fill("black")
        menu_tab_x_pos = 20
        submenu_tab_x_pos = 20
        y_pos = 10
        menu_tab_names = [i.display_tab() for i in tabs]
        submenu_tab_names = self.subtabs()
        amount_of_tabs = len(menu_tab_names)
        amount_of_subtabs = len(submenu_tab_names)
        menu_tab_length = 760 // amount_of_tabs
        submenu_tab_length = 760 // amount_of_subtabs
        
        # Draws the menu tabs at the top of the screen
        for i, name in enumerate(menu_tab_names):
            size = pygame.font.Font.size(menu_font, name)[0]
            center = menu_tab_x_pos + ((menu_tab_length - size) / 2)
            if i == menu_index:
                # Underlines the name of the tab if the tab is selected
                menu_font.set_underline(True)
                text = menu_font.render(name, True, color)
                screen.blit(text, (center, y_pos))
                menu_font.set_underline(False)
            else:
                # Draws the tab normally
                text = menu_font.render(name, True, color)
                screen.blit(text, (center, y_pos))
            menu_tab_x_pos += menu_tab_length
        y_pos += menu_font.get_linesize()

        for i, name in enumerate(submenu_tab_names):
            size = pygame.font.Font.size(submenu_font, name)[0]
            center = submenu_tab_x_pos + ((submenu_tab_length - size) / 2)
            if i == submenu_index:
                # Underlines the name of the subtab if the tab is selected
                submenu_font.set_underline(True)
                text = submenu_font.render(name, True, color)
                screen.blit(text, (center, y_pos))
                submenu_font.set_underline(False)
            else:
                # Draws the subtab normally
                text = submenu_font.render(name, True, color)
                screen.blit(text, (center, y_pos))
            submenu_tab_x_pos += submenu_tab_length


class StatusTab(MenuTab):
    def __init__(self):
        super().__init__("STAT")

    def subtabs(self):
        return ["STATUS", "SPECIAL", "PERKS"]


class InventoryTab(MenuTab):
    def __init__(self):
        super().__init__("INV")

    def subtabs(self):
        return ["ITEMS", "WEAPONS", "APPAREL", "AID", "MISC"]


class DataTab(MenuTab):
    def __init__(self):
        super().__init__("DATA")

    def subtabs(self):
        return ["QUESTS", "MAP", "LOG"]


class MapTab(MenuTab):
    def __init__(self):
        super().__init__("MAP")

    def subtabs(self):
        return ["WORLD MAP", "LOCAL MAP"]


class RadioTab(MenuTab):
    def __init__(self):
        super().__init__("RADIO")

    def subtabs(self):
        return ["STATIONS"]
