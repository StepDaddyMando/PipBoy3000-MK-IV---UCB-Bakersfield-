import pygame
import submenus


class MenuTab:
    def __init__(self, name):
        self.name = name
        self.tabs_list = None

    def display_tab(self):
        return self.name

    def subtabs(self):
        return self.tabs_list

    def subtab_names(self):
        return [name.display_name() for name in self.subtabs()]

    def display_subtabs(self, index):
        return self.subtabs()[index]
    
    def update_selected_submenu(self, submenu_index):
        self.tabs_list[submenu_index].input_handler()

    def draw_menu(
        self, screen, tabs, menu_index, submenu_index, color, menu_font, submenu_font
    ):
        screen.fill("black")
        menu_tab_x_pos = 20
        submenu_tab_x_pos = 20
        y_pos = 10
        menu_tab_names = [i.display_tab() for i in tabs]
        submenu_tab_names = self.subtab_names()
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
        y_pos += submenu_font.get_linesize()
        self.subtabs()[submenu_index].draw_submenu(screen, y_pos, color)


class StatusTab(MenuTab):
    def __init__(self):
        super().__init__("STAT")
        self.tabs_list = [
            submenus.StatusMenu(),
            submenus.SpecialMenu(),
            submenus.PerksMenu(),
        ]


class InventoryTab(MenuTab):
    def __init__(self):
        super().__init__("INV")
        self.tabs_list = [
            submenus.ItemsMenu(),
            submenus.WeaponsMenu(),
            submenus.ApparelMenu(),
            submenus.AidMenu(),
            submenus.MiscMenu(),
        ]


class DataTab(MenuTab):
    def __init__(self):
        super().__init__("DATA")
        self.tabs_list = [submenus.QuestsMenu(), submenus.NotesMenu()]


class MapTab(MenuTab):
    def __init__(self):
        super().__init__("MAP")
        self.tabs_list = [submenus.WorldMapMenu(), submenus.LocalMapMenu()]


class RadioTab(MenuTab):
    def __init__(self):
        super().__init__("RADIO")
        self.tabs_list = [submenus.StationsMenu(), submenus.TuningMenu()]
