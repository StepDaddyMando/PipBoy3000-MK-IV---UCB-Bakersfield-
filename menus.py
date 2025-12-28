
class Menu_Tab():
    def __init__(self, name):
        self.name = name
    
    def display_text(self):
        return self.name
    
    def subtabs(self):
        return []
    
    def display_subtabs(self, index):
        return self.subtabs()[index]

class Status_Tab(Menu_Tab):
    def __init__(self):
        super().__init__("STAT")
    def subtabs(self):
        return ["STATUS", "SPECIAL", "PERKS"]

class Inventory_Tab(Menu_Tab):
    def __init__(self):
        super().__init__("INV")
    def subtabs(self):
        return ["ITEMS", "WEAPONS", "APPAREL", "AID", "MISC"]

class Data_Tab(Menu_Tab):
    def __init__(self):
        super().__init__("DATA")
    def subtabs(self):
        return ["QUESTS", "MAP", "LOG"]

class Map_Tab(Menu_Tab):
    def __init__(self):
        super().__init__("MAP")
    def subtabs(self):
        return ["WORLD MAP", "LOCAL MAP"]

class Radio_Tab(Menu_Tab):
    def __init__(self):
        super().__init__("RADIO")
    def subtabs(self):
        return ["STATIONS"]