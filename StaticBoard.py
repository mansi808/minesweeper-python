import random
from Board import Board

class StaticBoard(Board):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.bombs_index = []
        # static_grid will have all 0s initially before placing bombs and placing numbers
        self.place_bombs()
        self.place_numbers()

    # overwrote to place 0s instead of "-"
    def set_grid(self):
        return list([["0" for _ in range(self.x)] for _ in range(self.y)])

    def place_bombs(self):
        for _ in range(self.bombs_count):
            r = random.randint(0, self.y - 1)
            c = random.randint(0, self.x - 1)
            if [r,c] not in self.bombs_index:
                self.bombs_index.append(list([r, c]))
                self.grid[r][c] = '*'

    def display_grid(self):
        print("   ", end="")
        for i in range(self.x): print(i, end=" ")
        print()
        print("-----------------------------")
        i = 0
        for row in self.grid:
            print(str(i)+"|", end=" ")
            for val in row:
                print(val, end=" ")
            print("")
            i += 1

    # TO DO: bugs in place_numbers potentially around corner value
    # places how many bombs are near for each square
    def place_numbers(self):
        print(self.bombs_index)
        for r, c in self.bombs_index:
            print("row",r,"col",c)
            i = 0
            for m in range(-1, 2):
                for n in range(-1, 2):
                    if ((r + m) >= self.y) or ((c + n) >= self.x) or ((c + n) < 0) or ((r + m) < 0) or (
                            self.grid[r + m][c + n] == "*"):
                        pass
                    else:
                        i += 1
                        print("increased",i,"times","on", "row",r+m, "col",c+n)
                        self.grid[r + m][c + n] = str(int(self.grid[r + m][c + n]) + 1)
            print(i)
    # check if this single grid box is safe ie has no bombs, parameters x,y
    def is_safe(self, r, c):
        return self.grid[r][c] != "*"

