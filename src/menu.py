import customtkinter as ctk
import sys
import os

from properties import COLOR

from board import Board

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Menu(ctk.CTkFrame):
    def __init__(self, master, bombs_amount: int, win_func) -> None:
        super().__init__(master, fg_color=COLOR.ACCENT_1)
        self.pack(side='top', padx=5, pady=5, ipadx=10, ipady=10, fill=ctk.X, expand=True)
        self.font = ctk.FontManager.windows_load_font(resource_path('fonts\\PressStart2P-Regular.ttf'))
        self.flag_amount: int = bombs_amount
        self.win_func = win_func
        self.next = None
        self.paused = False
        self.minutes: int = 0
        self.seconds: int = 0
        self.time_label()
        self.flag_counter()

    def time_label(self) -> None:
        self.timer_label = ctk.CTkLabel(self, font=ctk.CTkFont('Press Start 2P', 34),
                                        text_color=COLOR.WHITE, anchor=ctk.S, 
                                        text=f'{str(self.minutes).zfill(2)}:{str(self.seconds).zfill(2)}')
        self.timer_label.pack(side=ctk.LEFT, padx=10, pady=5)
        self.timer()

    def timer(self) -> None:
        self.next = self.master.after(1000, self.timer)
        self.seconds += 1
        if self.seconds == 60:
            self.seconds = 0
            self.minutes += 1
        self.timer_label.configure(text=f'{str(self.minutes).zfill(2)}:{str(self.seconds).zfill(2)}')

    def flag_counter(self):
        self.flag_counter_label = ctk.CTkLabel(self, font=ctk.CTkFont('Press Start 2P', 34),
                                                text_color=COLOR.WHITE, anchor=ctk.S,
                                                text=f'Flags:{str(self.flag_amount).zfill(2)}')
        self.flag_counter_label.pack(side=ctk.RIGHT, padx=10, pady=10)

    def update_counter(self, type_: str) -> None:
        if type_ == 'inc':
            self.flag_amount += 1
        elif type_ == 'dec':
            self.flag_amount -= 1
        self.flag_counter_label.configure(text=f'Flags:{str(self.flag_amount).zfill(2)}')
        if self.flag_amount == 0:
            self.win_func

    def reset_timer(self):
        self.minutes = 0
        self.seconds = 0
        self.timer_label.configure(text='00:00')
        self.master.after_cancel(self.next)
        self.timer()

    def pause_timer(self):
        if not self.paused and self.next:
            self.master.after_cancel(self.next)
            self.paused = True
        elif self.paused:
            self.master.after_cancel(self.next)
            self.seconds = 0
            self.minutes = 0
            self.timer()
            self.paused = False
