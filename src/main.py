import customtkinter as ctk

from properties import COLOR
from board import Board

class MainWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__(fg_color=COLOR.BACKGROUND)
        self.board: Board = Board(self, 7, 'easy')

    def reveal_cells(self, x, y):
        self.board.reveal_around(x, y)

if __name__ == "__main__":
    window = MainWindow()
    window.title('Minesweeper')
    window.geometry('1080x680')
    window.minsize(1080, 760)
    window.mainloop()
