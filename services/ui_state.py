class UIState:
    """
    Контролирует что сейчас открыто в интерфейсе
    (чтобы не дублировать меню)
    """

    def __init__(self):
        self.current_menu = None

    def is_menu_open(self, name: str) -> bool:
        return self.current_menu == name

    def set_menu(self, name: str):
        self.current_menu = name

    def reset(self):
        self.current_menu = None


ui_state = UIState()