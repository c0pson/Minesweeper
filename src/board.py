from concurrent.futures import ThreadPoolExecutor
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
        self.bombs_amount: int = int(self.size * self.size * self.difficulty)
        self.board: list[list[Tile]] = self.create_board()
        self.first_move: bool = True
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

    def place_bombs(self, x, y) -> None:
        bombs_amount: int = self.bombs_amount
        already_used: list[tuple[int, int]] = [ (x-1,y+1), (x,y+1), (x+1,y+1),
                                                (x-1,y)  , (x , y), (x+1,y)  ,
                                                (x-1,y-1), (x,y-1), (x+1,y-1) ]
        while bombs_amount:
            x_coord: int = random.randrange(0, self.size)
            y_coord: int = random.randrange(0, self.size)
            if (x_coord,y_coord) not in already_used:
                self.board[x_coord][y_coord].mark_as_bomb()
                already_used.append((x_coord,y_coord))
                bombs_amount -= 1

    def display_board(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j].pack(side='left', padx=2, pady=2, expand=True)

    def count_all_bombs(self) -> None:
        def count_bombs_task(i, j):
            self.count_bombs_around_cell(i, j)

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(self.size):
                for j in range(self.size):
                    futures.append(executor.submit(count_bombs_task, i, j))
            for future in futures:
                future.result()

    def count_bombs_around_cell(self, x, y) -> None:
        count = 0
        for i in range(max(0, x-1), min(self.size, x+2)):
            for j in range(max(0, y-1), min(self.size, y+2)):
                if self.board[i][j].is_bomb and (i, j) != (x, y):
                    count += 1
        self.board[x][y].bombs_around = count
        self.board[x][y].update_cell()

    def reveal_around(self, x, y) -> None:
        if self.first_move:
            self.first_move = False
            self.place_bombs(x, y)
            self.count_all_bombs()
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
