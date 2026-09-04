import tkinter as tk
from math import ceil


class Board:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = self.set_grid()
        self.set_bombs_count()
        self.bombs_count = self.get_bombs_count()

    def set_grid(self):
        return list([[None for _ in range(self.x)] for _ in range(self.y)])

    def get_dimensions(self):
        return [self.x, self.y]

    def set_bombs_count(self):
        self.bombs_count = ceil((self.x * self.y) / 6)

    def get_bombs_count(self):
        return self.bombs_count
