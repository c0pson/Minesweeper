import customtkinter as ctk
import random

from properties import COLOR

from tile import Tile

class Board(ctk.CTkFrame):
    def __init__(self, master, size: int, difficulty: str) -> None:
        super().__init__(master, fg_color=COLOR.BACKGROUND)
        self.pack(padx=5, pady=5, expand=True)
        self.size = size
        self.difficulty = self.set_difficulty(difficulty)
        self.board: list[list[Tile]] = self.create_board()
        self.place_bombs()
        self.count_all_bombs()
        self.display_board()

    def create_board(self) -> list[list[Tile]]:
        board: list[list[Tile]] = [[_ for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            frame = ctk.CTkFrame(self, fg_color=COLOR.BACKGROUND,
                                    corner_radius=0)
            frame.pack(side='top', padx=0, pady=0, expand=True)
            for j in range(self.size):
                board[i][j] = Tile(frame, i, j, self.master.reveal_cells)
        return board

    def set_difficulty(self, difficulty) -> float:
        if difficulty == 'easy':
            return .1
        elif difficulty == 'normal':
            return .15
        elif difficulty == 'medium':
            return .2
        elif difficulty == 'hard':
            return .3
        else: 
            raise ValueError(f'Improper string passed: {difficulty}')

    def place_bombs(self) -> None:
        bombs_amount: int = int(self.size * self.size * self.difficulty)
        already_used: list[tuple[int, int]] = []
        while bombs_amount:
            x: int = random.randrange(0, self.size)
            y: int = random.randrange(0, self.size)
            if (x,y) not in already_used:
                self.board[x][y].mark_as_bomb()
                already_used.append((x,y))
                bombs_amount -= 1

    def display_board(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                    self.board[i][j].pack(side='left', padx=2, pady=2, expand=True)

    def count_all_bombs(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                    self.count_bombs_around_cell(i, j)

    def count_bombs_around_cell(self, x, y) -> None:
        count = 0
        for i in range(max(0, x-1), min(self.size, x+2)):
            for j in range(max(0, y-1), min(self.size, y+2)):
                if self.board[i][j].is_bomb and (i, j) != (x, y):
                    count += 1
        self.board[x][y].bombs_around = count
        self.board[x][y].update_cell()

    def reveal_around(self, x, y) -> None:
        if self.board[x][y].is_bomb:
            print('bomb')
            return
        if self.board[x][y].bombs_around > 0 and not self.board[x][y].is_bomb:
            self.board[x][y].is_revealed = True
            self.board[x][y].update_cell()
            return
        for i in range(max(0, x - 1), min(x + 2, self.size)):
            for j in range(max(0, y - 1), min(y + 2, self.size)):
                if not self.board[i][j].is_revealed and not self.board[i][j].is_bomb:
                    self.board[i][j].is_revealed = True
                    self.board[i][j].update_cell()
                    if not self.board[i][j].bombs_around:
                        self.reveal_around(i, j)
