import tkinter as tk
import tkinter.ttk as tkk
from Player import Player
from StaticBoard import StaticBoard
from PlayingBoard import PlayingBoard
from Game import Game
from functools import partial

# TO DO now when clicked I need to make sure the tile is revealed.
# I can do so by comparing the row and column tile with the playing board which will be just a list
def play(name):
    initial_frm.destroy()
    init_player(name)
    init_game_frm()
    init_boards()

# initilaise the player class with player name from input
def init_player(name):
    player = Player(name)
    print("initialised player:", player.name)

# create the game frame and move to the game frame
def init_game_frm():
    main_frm.pack()
    board_frm.pack()

def init_boards():
    game.display_grid()
    static_board.display_grid()


loop = True
while loop:
    window = tk.Tk()
    # Getting input from user to put in Player name class

    initial_frm = tk.Frame()
    initial_frm.pack(fill=tk.BOTH)

    lbl_input = tk.Label(master=initial_frm,text="Enter Player Name")
    ent_name = tk.Entry(master=initial_frm)

    lbl_input.pack(fill=tk.BOTH)
    ent_name.pack(fill=tk.BOTH)

    player = None
    ent_button = tk.Button(master=initial_frm, text="Submit", command=partial(play,ent_name.get()))
    ent_button.pack(fill=tk.BOTH)

    main_frm = tk.Frame()
    board_frm = tk.Frame(master=main_frm)

    x = 12
    y = 12
    static_board = StaticBoard(x,y)
    playing_board = PlayingBoard(x,y,board_frm,static_board)
    game = Game(player,playing_board)

# TO DO: When name is submit move to the next frame which is the game, use a new submit button and after submitting move to new frame

    window.mainloop()
