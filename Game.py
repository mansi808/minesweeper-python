import tkinter as tk
from functools import partial
# from tkinter import ttk
from Player import Player
from Timer import Timer
from PlayingBoard import PlayingBoard
from StaticBoard import StaticBoard
import threading

"""Classes: 
Player
Board 
StaticBoard - board with all the placed bombs and numbers
Game - performs actions for that game

# In game, the size of playing board must be equal to the main board otherwise it would give an error, to remedy this
 a playing grid is initialised when creating an object of Class StaticBoard
"""

# TO DO: Implement ability to play again after end (Play again feature)
# TO DO: Graphics: Make a top bar with flags decreasing slowly,
# TO DO: Make buttons prettier
# TO DO: Make the windows responsive

class Game():

    def __init__(self,x,y,database):
        self.window = tk.Tk()
        self.set_window_properties()
        # Getting input from user to put in Player name class
        self.frm = tk.Frame(master = self.window)
        self.frm.pack(expand=True)

        self.initial_frm = tk.Frame(master=self.frm)
        self.main_frm = tk.Frame(master=self.frm)
        self.topbar_frm = tk.Frame(master=self.main_frm,width=3)
        self.board_frm = tk.Frame(master=self.main_frm)
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
        # flag set at 0 initially, increases if a flag is placed on the board
        self.flags = 0

        self.database = database
        self.database.create_db()
        self.timer = Timer(self.topbar_frm)

    def set_initial_frm(self):
        lbl_input = tk.Label(master=self.initial_frm, text="Enter Player Name")
        ent_name = tk.Entry(master=self.initial_frm)

        lbl_input.pack(expand=True,fill=tk.BOTH)
        ent_name.pack(expand=True,fill=tk.BOTH)
        ent_button = tk.Button(master=self.initial_frm, text="Submit", command=partial(self.start, ent_name))
        ent_button.pack(expand=True,fill=tk.BOTH)

    def set_window_properties(self):
        self.window.title("Minesweeper")
        self.window.config(bg="navy")
        self.window.geometry("600x400")
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.resizable(True, True)

    def display_grid(self):
        self.board_frm.pack(expand=True,fill="both")
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
                self.playing_board.grid[r][c] = tk.Button(master=frame, text=""
                                            ,command= partial(self.make_curr_move,r,c))
                # self.playing_board.grid[r][c].bind('<Button-2>', lambda event: self.key_handler(event))
                self.playing_board.grid[r][c].bind('<Button-2>', partial(self.set_flag,r,c),add="+")
                self.playing_board.grid[r][c].pack(expand=True,fill="both")

    def set_curr_move(self,r,c):
        self.curr_move = (r,c)

    def set_flag(self,r,c,event):
        if self.flags<self.playing_board.bombs_count:
            if not self.playing_board.is_played(r,c):
                if self.playing_board.grid[r][c]['text'] != "f":
                    self.playing_board.set_grid_box(r, c, "f")
                    self.flags += 1
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
            self.database.add_score(self.database.get_curr_playr_id(),self.timer.getSecond())
            self.display_result()

    def set_topbar(self):
        self.topbar_frm.pack(expand=True,fill="both")
        self.timer.display()

    def display_result(self):
        label = "Won" if self.win else "Lost"
        result_lbl = tk.Label(master=self.end_frm, text="You "+label + "!")
        self.end_frm.tkraise()
        self.display_leaderboard()
        result_lbl.pack(expand=True,fill="both")

    def display_leaderboard(self):
        leaderboard_frm = tk.Frame(master=self.end_frm)
        leaderboard_frm.pack()
        leaderboard = self.database.get_leaderboard()
        for r in range(len(leaderboard)):
            for c in range(2):
                frame = tk.Frame(
                    borderwidth=1,
                    relief=tk.RAISED,
                    master=leaderboard_frm
                )
                frame.grid(row=r, column=c)
                frame.grid_columnconfigure(1, weight=1)
                frame.grid_rowconfigure(1, weight=1)
                lbl = tk.Label(master=frame)
                lbl.grid(row=r, column=c)
                lbl['text'] = leaderboard[r][c]

    # start the game by initialising the player and moving onto the next frame
    def start(self,ent_name):
        # if initial frame is destroyed before initialising name, the name is empty
        self.init_player(name=ent_name.get())
        self.initial_frm.destroy()
        self.raise_main_frm()
        # set the frames in the main frame
        self.set_topbar()
        self.init_boards()

    # initialise the player class with player name from input
    def init_player(self,name):
        player = Player(name)
        print("initialised player:", player.name)
        #add player to the databse
        self.database.add_player(player.name)

    # raise the next frame to display it
    def raise_main_frm(self):
        self.main_frm.tkraise()

    # display the grid in terminal and UI version
    def init_boards(self):
        self.display_grid()
        self.static_board.display_grid()

    def start_timer_thread(self):
        work1 = threading.Thread(target=self.timer.work, daemon=True)
        work1.start()

