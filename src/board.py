from concurrent.futures import ThreadPoolExecutor
import customtkinter as ctk
import random
import sys
import os

from properties import COLOR

from tile import Tile

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Board(ctk.CTkFrame):
    def __init__(self, master, size: int, difficulty: str, update_func, flags_func, stop_timer_func) -> None:
        super().__init__(master, fg_color=COLOR.BACKGROUND)
        self.pack(side=ctk.BOTTOM, padx=5, pady=5, expand=True)
        self.font = ctk.FontManager.windows_load_font(resource_path('fonts\\PressStart2P-Regular.ttf'))
        self.size = size
        self.stop_timer_func = stop_timer_func
        self.flags_func = flags_func
        self.update_func = update_func
        self.difficulty = self.set_difficulty(difficulty)
        self.bombs_amount: int = int(self.size * self.size * self.difficulty)
        self.board: list[list[Tile]] = self.create_board()
        self.first_move: bool = True
        self.top_screen: bool = False
        self.display_board()

    def create_board(self) -> list[list[Tile]]:
        board: list[list[Tile]] = [[_ for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            frame = ctk.CTkFrame(self, fg_color=COLOR.BACKGROUND, corner_radius=0)
            frame.pack(side='top', padx=0, pady=0, expand=True)
            for j in range(self.size):
                board[i][j] = Tile(frame, i, j, self.master.reveal_cells, self.update_func,
                                    self.flags_func, self.check_win)
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
                                                (x-1,  y), (x , y), (x+1,  y),
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

        with ThreadPoolExecutor(max_workers=100) as executor:
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
            self.loss()
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

    def check_win(self) -> None:
        count: int = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].is_bomb and self.board[i][j].is_marked:
                    count += 1
        if count == self.bombs_amount:
            self.win()

    def loss(self):
        if self.top_screen:
            return
        self.top_screen = True
        self.game_over_label = ctk.CTkLabel(self.master, text='GAME OVER', fg_color=COLOR.ACCENT_1, bg_color=COLOR.ACCENT_1,
                                            font=ctk.CTkFont('Press Start 2P', 44), text_color=COLOR.ACCENT_2)
        self.restart_button = ctk.CTkButton(self.game_over_label, command=self.restart_board,
                                            text='RESTART', fg_color=COLOR.TILE_2, anchor=ctk.S,
                                            text_color=COLOR.WHITE, font=ctk.CTkFont('Press Start 2P', 22),
                                            hover=False)
        self.game_over_label.place(relx=0.5, rely=0.5, relwidth =1, relheight=0.2, anchor=ctk.CENTER)
        self.restart_button.grid(padx=10, pady=10, ipadx=0)
        self.reveal_all()
        self.stop_timer_func()

    def win(self):
        if self.top_screen:
            return
        self.top_screen = True
        self.game_over_label = ctk.CTkLabel(self.master, text='YOU WON', fg_color=COLOR.ACCENT_1, bg_color=COLOR.ACCENT_1,
                                            font=ctk.CTkFont('Press Start 2P', 44), text_color=COLOR.ACCENT_2)
        self.restart_button = ctk.CTkButton(self.game_over_label, command=self.restart_board,
                                            text='RESTART', fg_color=COLOR.TILE_2, anchor=ctk.S,
                                            text_color=COLOR.WHITE, font=ctk.CTkFont('Press Start 2P', 22),
                                            hover=False)
        self.game_over_label.place(relx=0.5, rely=0.5, relwidth =1, relheight=0.2, anchor=ctk.CENTER)
        self.restart_button.grid(padx=10, pady=10, ipadx=0)
        self.reveal_all()
        self.stop_timer_func()

    def reveal_all(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j].is_revealed = True
                self.board[i][j].update_cell()

    def restart_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j].restart()
                self.first_move = True
        self.game_over_label.destroy()
        self.top_screen = False
        self.stop_timer_func()
