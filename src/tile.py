import customtkinter as ctk
import sys
import os

from properties import COLOR

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Tile(ctk.CTkLabel):
    def __init__(self, master, x_pos: int, y_pos: int, reveal_func) -> None:
        self.reveal_func = reveal_func
        self.position: tuple[int, int] = (x_pos, y_pos)
        self.font = ctk.FontManager.windows_load_font(resource_path('fonts\\Poppins-Black.ttf'))
        super().__init__(master, fg_color=COLOR.TILE_1, text='',
                        width=70, height=70, text_color=COLOR.WHITE,
                        font=ctk.CTkFont('Poppins', 34))
        self.bind('<Any-Button>', lambda e: self.on_click(e))
        self.is_bomb: bool = False
        self.bombs_around: int = 0
        self.is_revealed: bool = False
        self.is_marked: bool = False

    def mark_as_bomb(self) -> None:
        self.is_bomb = True

    def on_click(self, event) -> None:
        if event.num == 1:
            self.reveal_func(self.position[0], self.position[1])
        elif event.num == 3:
            self.mark_bomb()

    def mark_bomb(self) -> None:
        if self.is_marked and not self.is_revealed:
            self.configure(text='')
            self.configure(text_color=COLOR.TILE_1)
            self.is_marked = False
        elif not self.is_marked and not self.is_revealed:
            self.is_marked = True
            self.configure(text='🚩')
            self.configure(text_color=COLOR.ACCENT_2)

    def update_cell(self) -> None:
        if self.is_revealed and not self.bombs_around and not self.is_bomb:
            self.configure(text='')
            self.configure(fg_color=COLOR.ACCENT_1)
        elif self.is_revealed and not self.is_bomb:
            self.configure(text=self.bombs_around)
            self.configure(fg_color=COLOR.TILE_2)
            self.configure(text_color=COLOR.WHITE)
