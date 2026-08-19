from math import *
import random

"""Classes: 
Player
Board 
StaticBoard - board with all the placed bombs and numbers
PlayingBoard - displayed board where the game is played on
Game - performs actions for that game

# In game, the size of playing board must be equal to the main board otherwise it would give an error, to remedy this
 a playing grid is initialised when creating an object of Class StaticBoard
"""


class Board:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = self.set_grid()
        self.set_bombs_count()
        self.bombs_count = self.get_bombs_count()

    def set_grid(self):
        return list([["-" for _ in range(self.x)] for _ in range(self.y)])

    def display_grid(self):
        for row in self.grid:
            for val in row:
                print(val, end=" ")
            print("")

    def get_dimensions(self):
        return [self.x, self.y]

    def set_bombs_count(self):
        self.bombs_count = ceil((self.x * self.y) / 6)

    def get_bombs_count(self):
        return self.bombs_count


class PlayingBoard(Board):

    # used to change values in playing grid if a move is made, does not check if the move made is valid
    def set_grid_box(self, i, j, new_value):
        self.grid[j][i] = new_value


class StaticBoard(Board):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.bombs_index = []
        self.playing_board = PlayingBoard(self.x, self.y)
        self.played_squares = 0
        # static_grid will have all 0s initially before placing bombs and placing numbers
        self.place_bombs()
        self.place_numbers()

    # overwrote to place 0s instead of "-"
    def set_grid(self):
        return list([["0" for _ in range(self.x)] for _ in range(self.y)])

    def place_bombs(self):
        for i in range(self.bombs_count):
            x = random.randint(0, self.x - 1)
            y = random.randint(0, self.y - 1)
            self.bombs_index.append(list([x, y]))
            self.grid[y][x] = '*'

    # places how many bombs are near for each square
    def place_numbers(self):
        for x, y in self.bombs_index:
            for m in range(-1, 2):
                for n in range(-1, 2):
                    if ((y + m) >= self.y) or ((x + n) >= self.x) or ((x + n) < 0) or ((y + m) < 0) or (
                            self.grid[y + m][x + n] == "*"):
                        pass
                    else:
                        self.grid[y + m][x + n] = str(int(self.grid[y + m][x + n]) + 1)

    # check if this single grid box is safe ie has no bombs, parameters x,y
    def is_safe(self, i, j):
        return self.grid[j][i] != "*"

    # compute the surrounding safe blocks by recursions and calling the same function again each time a 0 is found
    # change values in playing_grid
    def compute_safe_blocks(self, x, y):
        for m in range(-1, 2):
            for n in range(-1, 2):
                if (n == 0 and m == 0) or (y + m) >= self.y or (x + n) >= self.x or (x + n) < 0 or (y + m) < 0:
                    continue
                elif self.is_safe(x + n, y + m):
                    if self.playing_board.grid[y + m][x + n] == '-':
                        self.playing_board.set_grid_box(x + n, y + m, self.grid[y + m][x + n])
                        self.increment_played_squares()
                        if self.grid[y + m][x + n] == "0":
                            self.compute_safe_blocks((x + n), (y + m))

    def increment_played_squares(self):
        self.played_squares += 1


class Player:

    def __init__(self, name):
        self.score = 0
        self.name = name

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score

    def increment_score(self):
        self.score += 1


class Game:

    def __init__(self, player: Player, static_board: StaticBoard):
        self.player = player
        self.static_board = static_board
        self.win = False

    def set_move(self):
        try:
            player_move = list(map(int, list(input("Enter as x y: ").strip().split(" "))))
            if (player_move[0] >= self.static_board.x or player_move[1] >= self.static_board.y) or (
                    player_move[0] < 0 or player_move[1] < 0):
                print("Invalid index value!")
                return self.set_move()
            # TO DO: look at the possibility if there are double spaces in the middle and if the values are even valid

            elif self.static_board.playing_board.grid[player_move[1]][player_move[0]] != '-':
                print("You already made move on that box!")
                return self.set_move()
        except ValueError:
            print(ValueError("Invalid value: Enter numbers in format x y"))
            return self.set_move()
        return player_move

    # TO DO: change the set_move method and use a separate isvalidmove method
    def valid_move(self, x, y):
        pass

    def play(self):
        safe = True
        while not self.win and safe:
            self.static_board.playing_board.display_grid()
            # entered as x y
            print("The board is", self.static_board.x, "long(y) and", self.static_board.y,
                  "in width(x). The index starts from 0.")

            # the move of the player returned in x y format (index starting at 0)
            player_move = self.set_move()
            safe = self.static_board.is_safe(player_move[0], player_move[1])

            # player makes a move and then if safe proceeds, if not loses
            if safe:
                original_grid_value = int(self.static_board.grid[player_move[1]][player_move[0]])
                # reassign current block in playing_grid to new value
                self.static_board.increment_played_squares()
                self.static_board.playing_board.set_grid_box(player_move[0], player_move[1], original_grid_value)
                # if 0 is present on that block, find safe blocks around it until you get a bomb or a number greater than 0
                if original_grid_value == 0:
                    self.static_board.compute_safe_blocks(player_move[0], player_move[1])

            else:
                for x, y in self.static_board.bombs_index:
                    self.static_board.playing_board.set_grid_box(x, y, self.static_board.grid[y][x])
                self.static_board.playing_board.display_grid()
                print("You Lost!")
            if self.static_board.played_squares == (
                    (self.static_board.x * self.static_board.y) - self.static_board.bombs_count):
                self.win = True
                print("You Won!")


p = Player("")
static_board = StaticBoard(5, 5)
game = Game(p, static_board)
game.play()
