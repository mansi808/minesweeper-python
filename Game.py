import tkinter as tk
from functools import partial
from tkinter import ttk


from Player import Player
from PlayingBoard import PlayingBoard
from StaticBoard import StaticBoard
import time
import threading



"""Classes: 
Player
Board 
StaticBoard - board with all the placed bombs and numbers
Game - performs actions for that game

# In game, the size of playing board must be equal to the main board otherwise it would give an error, to remedy this
 a playing grid is initialised when creating an object of Class StaticBoard
"""

# The next important thing is to make sure the player can put flags on the tiles
# DONE: Test the game show you won! and you lost!
# TO DO: Make buttons prettier
# TO DO: Make the windows responsive
# TO DO: Make database which scores the scores and plaher names
# TO DO: Display highest score in the end and ability to play 
# TO DO: Make a top bar with flags decreasing slowly, limit number of flags according to number of bombs


# Database - SQLite
class Game():

    def __init__(self,x,y):
        self.window = tk.Tk()
        self.set_window_properties()
        # Getting input from user to put in Player name class
        self.frm = tk.Frame(self.window)
        self.frm.pack(expand=True)

        self.initial_frm = tk.Frame(master=self.frm)
        self.main_frm = tk.Frame(master=self.frm)
        self.board_frm = tk.Frame(master=self.main_frm)
        self.board_frm.pack(expand=True,fill="both")
        self.end_frm = tk.Frame(master=self.frm)

        for frm in (self.initial_frm,self.main_frm,self.end_frm):
            frm.grid(row=0, column=0, sticky='NEWS',padx=10, pady=10)
            self.frm.grid_columnconfigure(1, weight=1)
            self.frm.grid_rowconfigure(1, weight=1)

        self.set_initial_frm()
        self.initial_frm.tkraise()

        self.win = False
        self.static_board = StaticBoard(x, y)
        self.playing_board = PlayingBoard(x,y,self.board_frm,self.static_board)
        self.curr_move = None

    def set_initial_frm(self):
        lbl_input = tk.Label(master=self.initial_frm, text="Enter Player Name")
        ent_name = tk.Entry(master=self.initial_frm)

        lbl_input.pack(expand=True,fill=tk.BOTH)
        ent_name.pack(expand=True,fill=tk.BOTH)

        ent_button = tk.Button(master=self.initial_frm, text="Submit", command=partial(self.start, ent_name.get()))
        ent_button.pack(expand=True,fill=tk.BOTH)

    def set_window_properties(self):
        self.window.title("Minesweeper")
        self.window.config(bg="navy")
        self.window.geometry("600x400")
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.resizable(True, True)

    def display_grid(self):
        for r in range(self.playing_board.y):
            for c in range(self.playing_board.x):
                frame = tk.Frame(
                    borderwidth=1,
                    relief=tk.RAISED,
                    master=self.playing_board.frm
                )
                frame.grid(row=r, column=c)
                frame.grid_columnconfigure(1, weight=1)
                frame.grid_rowconfigure(1, weight=1)
                self.playing_board.grid[r][c] = ttk.Button(master=frame, text=""
                                            ,command= partial(self.make_curr_move,r,c))
                # self.playing_board.grid[r][c].bind('<Button-2>', lambda event: self.key_handler(event))
                self.playing_board.grid[r][c].bind('<Button-2>', partial(self.set_flag,r,c),add="+")
                self.playing_board.grid[r][c].pack(expand=True,fill="both")

    def set_curr_move(self,r,c):
        self.curr_move = (r,c)

    # TO DO: place a flag if valid position
    def set_flag(self,r,c,event):
        if not self.playing_board.is_played(r,c):
            if self.playing_board.grid[r][c]['text'] != "f":
                self.playing_board.set_grid_box(r, c, "f") #ERROR: error here cannot change values
        elif self.playing_board.grid[r][c]['text'] == "f":
            self.playing_board.set_grid_box(r, c, "")

    # def key_handler(self,event):
        # print("clicked at",event)

        # when a tile is clicked it can either be for placing flag or for opening
    def make_curr_move(self,r ,c):

        self.set_curr_move(r ,c)
        safe = self.playing_board.static_board.is_safe(self.curr_move[0], self.curr_move[1])
        # player makes a move and then if safe proceeds, if not loses
        if safe:

            original_grid_value = int(self.playing_board.static_board.grid[self.curr_move[0]][self.curr_move[1]])
            # reassign current block in playing_grid to new value
            self.playing_board.increment_played_squares()
            if self.playing_board.played_squares == 1:
                self.start_timer_thread()
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

    def display_topbar(self):
        topbar_frm = tk.Frame(master=self.main_frm)
        topbar_frm.pack()
        topbar_frm.tkraise()


    def display_result(self):
        label = "Won" if self.win else "Lost"
        result_lbl = tk.Label(master=self.end_frm, text="You "+label + "!")
        self.end_frm.tkraise()
        result_lbl.pack(expand=True,fill="both")

    def start(self,name):
        self.initial_frm.destroy()
        self.init_player(name=name)
        self.raise_main_frm()
        self.init_boards()

    # initialise the player class with player name from input
    @staticmethod
    def init_player(name):
        player = Player(name)
        print("initialised player:", player.name)

    # create the game frame and move to the game frame
    def raise_main_frm(self):
        self.main_frm.tkraise()

    def init_boards(self):
        self.display_grid()
        self.static_board.display_grid()
        self.display_topbar()

    def start_timer_thread(self):
        thread1 = Parallel()

        # thread1.work(self.window)

        work1 = threading.Thread(target=thread1.work, daemon=True, args=(self.window,))

        work1.start()
        # print("hello")


class Parallel:

    def work(self,window):
        name = self.__repr__()
        second = tk.IntVar()
        second.set(000)
        secondEntry = tk.Entry(window, width=3, font=("Arial", 18, ""),
                               textvariable=second)
        secondEntry.place(x=180, y=20)
        while True:

            time.sleep(1)
            second.set(second.get() + 1)
            secondEntry.update()

        print(name, " is complete after ", " seconds")    