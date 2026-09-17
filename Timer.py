import tkinter as tk
import time


class Timer:

    def __init__(self,master_frm):
        self.second = tk.IntVar()
        self.second.set(000)
        self.frm = tk.Frame(master_frm)
        self.secondEntry = tk.Label(self.frm, width=3, font=("Arial", 18, ""),
                               textvariable=self.second)

    def display(self):
        self.frm.pack()
        self.secondEntry.pack()

    def work(self):
        while True:
            time.sleep(1)
            self.second.set(self.second.get() + 1)
            self.secondEntry.update()

    def getSecond(self):
        return self.second.get()