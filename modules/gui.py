import tkinter as tk

from .board import*


class App(tk.Frame):
    def __init__(self, parent, grid_width = 20, grid_height = 10, *args, **kwargs):
        super.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.board = Board(self.grid_width, self.grid_height)

    def create_cell_window(self):
        pass