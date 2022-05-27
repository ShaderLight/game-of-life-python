import tkinter as tk
import logging
from turtle import width

from .board import*


class App(tk.Frame):
    def __init__(self, parent, grid_width = 40, grid_height = 30, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.board = Board(self.grid_width, self.grid_height)
        self.last_painted = None
        parent.bind('<B1-Motion>', self.toggle_gui_cell_handler)
        parent.bind('<ButtonRelease-1>', self.reset_last_painted_handler)
        parent.bind('<Button-1>', self.toggle_gui_cell_handler)


        self.set_up_button_frame()
        self.set_up_cell_frame()

    def set_up_button_frame(self) -> None:
        button_frame = tk.Frame(self)

        reset_button = tk.Button(button_frame, text='Reset')
        reset_button.grid(row=0, column=0)

        next_state = tk.Button(button_frame, text='Next state')
        next_state.grid(row=0, column=1)

        button_frame.grid_columnconfigure((0,1), weight=1, uniform="column")

        button_frame.pack(side="top", fill="x", pady=20)

    def set_up_cell_frame(self) -> None:
        self.cell_window = tk.Frame(self)

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                new_cell = tk.Frame(self.cell_window, width=20, height=20)
                new_cell.configure({"background": "White"})
                new_cell.paintable = True
                new_cell.grid(row=y, column=x, padx=1, pady=1)
                new_cell.bind('<FocusIn>', self.toggle_gui_cell_handler)
        self.cell_window.pack(side="top", fill="x")

    def update_gui_cells(self) -> None:
        for key, value in self.cell_window.children.items():
            pass
    
    def reset_last_painted_handler(self, event) -> None:
        self.last_painted = None

    def toggle_gui_cell_handler(self, event) -> None:
        widget = event.widget.winfo_containing(event.x_root, event.y_root)

        if not hasattr(widget, 'paintable'):
            return

        x = widget.grid_info()['column']
        y = widget.grid_info()['row']

        if self.last_painted == (x, y):
            return

        new_state = self.board.toggle_cell_at(x, y)

        if new_state == 1:
            widget.configure({"background": "Black"})
        else:
            widget.configure({"background": "White"})

        self.last_painted = (x, y)