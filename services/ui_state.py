
class UIState:
    def __init__(self):
        self.current_menu = None

    def is_menu_open(self, name):
        return self.current_menu == name

    def set_menu(self, name):
        self.current_menu = name

    def reset(self):
        self.current_menu = None

ui_state = UIState()
