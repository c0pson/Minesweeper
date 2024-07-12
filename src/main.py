import customtkinter as ctk

from properties import COLOR
from board import Board
from menu import Menu

class MainWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__(fg_color=COLOR.BACKGROUND)
        self.board: Board = Board(self, 10, 'easy', self.update_flags, self.get_flags, self.stop_timer)
        self.menu = Menu(self, self.board.bombs_amount, self.check_win_conditions)

    def reveal_cells(self, x, y):
        self.board.reveal_around(x, y)

    def update_flags(self, type_: str):
        self.menu.update_counter(type_)

    def check_win_conditions(self):
        self.board.check_win()

    def get_flags(self, restart = False):
        if restart:
            self.menu.flag_amount = self.board.bombs_amount
            self.menu.update_counter('')
            self.menu.reset_timer()
        return self.menu.flag_amount

    def stop_timer(self):
        self.menu.pause_timer()

if __name__ == "__main__":
    window = MainWindow()
    window.title('Minesweeper')
    window.geometry(f'750x900+{(window.winfo_screenwidth()-750)//2}+{(window.winfo_screenheight()-1000)//2}')
    window.minsize(750, 900)
    window.mainloop()
