import tkinter as tk
from tkinter import filedialog as fd
import os

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

        # Menu bar
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar)
        self.about_menu = tk.Menu(self.menu_bar)

        self.file_menu.add_command(label='Open...', command=self.load_board_handler)
        self.file_menu.add_command(label='Save as...', command=self.save_board_handler)

        self.about_menu.add_command(label='GitHub repo', command=self.open_gh_page)

        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.menu_bar.add_cascade(label='Help', menu=self.about_menu)

        
        
        self.parent.config(menu=self.menu_bar)

        self.set_up_button_frame()
        self.set_up_cell_frame()

    def set_up_button_frame(self) -> None:
        button_frame = tk.Frame(self)

        reset_button = tk.Button(button_frame, text='Reset')
        reset_button.bind('<Button>', self.reset_all_handler)
        reset_button.grid(row=0, column=0)

        next_state = tk.Button(button_frame, text='Next state')
        next_state.bind('<Button>', self.next_state_handler)
        next_state.grid(row=0, column=1)

        button_frame.grid_columnconfigure((0,1), weight=1, uniform="column")

        button_frame.pack(side="top", fill="x", pady=20)

    def set_up_cell_frame(self) -> None:
        self.cell_frame_container = tk.Frame(self)
        self.cell_frame = tk.Frame(self.cell_frame_container)

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                new_cell = tk.Frame(self.cell_frame, width=20, height=20)
                new_cell.configure({"background": "White"})
                new_cell.paintable = True
                new_cell.grid(row=y, column=x, padx=1, pady=1)
                new_cell.bind('<FocusIn>', self.toggle_gui_cell_handler)
        self.cell_frame.pack(side='top')
        self.cell_frame_container.pack(side='top', fill='x')

    def update_gui_cells(self) -> None:
        for key, value in self.cell_frame.children.items():
            x = value.grid_info()['column']
            y = value.grid_info()['row']
            if self.board.state_at(x, y) == 1:
                value.configure({"background": "Black"})
            else:
                value.configure({"background": "White"})
    
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

    def reset_all_handler(self, event) -> None:
        for widget in self.cell_frame.grid_slaves():
            widget.configure({"background": "White"})

        self.board.reset_all()
    
    def next_state_handler(self, event) -> None:
        self.board.calculate_next_state_all()
        self.board.switch_to_next_state_all()
        self.update_gui_cells()

    def save_board_handler(self):
        filename = fd.asksaveasfilename(initialfile = 'saved.json', defaultextension=".json", filetypes=[("All Files","*.*"),("JSON File","*.json")])
        self.board.save_to_file(filename)

    def load_board_handler(self):
        filename = fd.askopenfilename(defaultextension=".json", filetypes=[("All Files","*.*"),("JSON File","*.json")])
        status = self.board.load_from_file(filename)

        if status == -1:
            tk.messagebox.showerror(title='Error loading data', message='Save file dimensions don\'t match window dimensions!')
        else:
            self.update_gui_cells()
    
    def open_gh_page(self):
        os.system("start \"\" https://github.com/ShaderLight/game-of-life-python")