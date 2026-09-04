import tkinter as tk
from functools import partial
from Player import Player

"""Classes: 
Player
Board 
StaticBoard - board with all the placed bombs and numbers
Game - performs actions for that game

# In game, the size of playing board must be equal to the main board otherwise it would give an error, to remedy this
 a playing grid is initialised when creating an object of Class StaticBoard
"""

class Game:

    def __init__(self, player: Player, playing_board):
        self.title = "Minesweeper"
        self.player = player
        self.win = False
        self.playing_board = playing_board
        self.curr_move = None

    def display_grid(self):
        for r in range(self.playing_board.y):
            for c in range(self.playing_board.x):
                frame = tk.Frame(
                    borderwidth=1,
                    relief=tk.RAISED,
                    master=self.playing_board.frm
                )
                frame.grid(row=r, column=c)
                self.playing_board.grid[r][c] = tk.Button(master=frame, text="", background="red"
                                            ,command= partial(self.set_curr_move,r,c))
                self.playing_board.grid[r][c].pack()

    def set_curr_move(self ,r ,c):
        self.curr_move = (r ,c)
        safe = self.playing_board.static_board.is_safe(self.curr_move[0], self.curr_move[1])

        # player makes a move and then if safe proceeds, if not loses
        if safe:
            original_grid_value = int(self.playing_board.static_board.grid[self.curr_move[0]][self.curr_move[1]])
            # reassign current block in playing_grid to new value
            self.playing_board.increment_played_squares()
            self.playing_board.set_grid_box(self.curr_move[0], self.curr_move[1], original_grid_value)
            # if 0 is present on that block, find safe blocks around it until you get a bomb or a number greater than 0
            if original_grid_value == 0:
                self.playing_board.compute_safe_blocks(self.curr_move[0], self.curr_move[1])

        else:
            for r, c in self.playing_board.static_board.bombs_index:
                self.playing_board.set_grid_box(r, c, self.playing_board.static_board.grid[r][c])
            print("You Lost!")
            self.display_result()
        if self.playing_board.played_squares == (
                (self.playing_board.x * self.playing_board.y) - self.playing_board.bombs_count):
            print("You Won!")
            self.win = True
            self.display_result()


    def display_result(self):
        label = "Won" if self.win else "Lost"
        end_frm = tk.Frame()
        result_lbl = tk.Label(master=end_frm, text="You "+label + "!")
        end_frm.pack()
        result_lbl.pack()