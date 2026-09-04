import tkinter as tk
from functools import partial
from Board import Board

"""PlayingBoard - displayed board where the game is played on
has the buttons list
"""

class PlayingBoard(Board):
    def __init__(self, x, y ,frm, static_board):
        super().__init__(x, y)
        self.frm = frm
        self.move = None
        self.static_board = static_board
        self.played_squares = 0

    def set_grid(self):
        return list([[None for _ in range(self.x)] for _ in range(self.y)])

    # used to change values in playing grid if a move is made, does not check if the move made is valid
    def set_grid_box(self, r, c, new_value):
        self.grid[r][c].config(text=new_value)

    def is_played(self, r, c):
        return self.grid[r][c]['text'] != ""

    # compute the surrounding safe blocks by recursions and calling the same function again each time a 0 is found
    # change values in playing_grid
    def compute_safe_blocks(self, r, c):
        for m in range(-1, 2):
            for n in range(-1, 2):
                if (n == 0 and m == 0) or (r + m) >= self.y or (c + n) >= self.x or (c + n) < 0 or (r + m) < 0:
                    continue
                elif self.static_board.is_safe(r + m,c+n):
                    if not self.is_played(r+m,c+n):
                        self.set_grid_box(r + m, c + n, self.static_board.grid[r + m][c + n])
                        self.increment_played_squares()
                        if self.static_board.grid[r + m][c + n] == "0":
                            self.compute_safe_blocks((r + m), (c + n))

    def increment_played_squares(self):
        self.played_squares += 1