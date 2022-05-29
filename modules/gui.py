import tkinter as tk
from tkinter import filedialog as fd
import os
from PIL import Image as ImagePIL, ImageTk

from .board import*


class App(tk.Frame):
    def __init__(self, parent, grid_width = 40, grid_height = 30, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.board = Board(self.grid_width, self.grid_height)
        self.last_painted = None
        self.is_ticking = False

        self.images = {}

        self.images['alive'] = ImageTk.PhotoImage(ImagePIL.open('modules/images/alive_border.png'), name='alive')
        self.images['dead'] = ImageTk.PhotoImage(ImagePIL.open('modules/images/dead_border.png'), name='dead')

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
        outer_button_frame = tk.Frame(self)
        button_frame = tk.Frame(outer_button_frame)

        self.reset_button = tk.Button(button_frame, text='Reset')
        self.reset_button.bind('<Button>', self.reset_all_handler)
        self.reset_button.grid(row=1, column=0, padx=5)

        self.tick_rate = tk.DoubleVar()
        slider = tk.Scale(button_frame, from_=1, to=20, orient='horizontal', variable=self.tick_rate)
        slider.grid(row=1, column=1, padx=5)

        slider_label = tk.Label(button_frame, text='Tick frequency [Hz]')
        slider_label.grid(row=0, column=1, padx=5)

        auto_ticking_button = tk.Button(button_frame, text='Start/stop')
        auto_ticking_button.bind('<Button>', self.auto_ticking_handler)
        auto_ticking_button.grid(row=1, column=2, padx=5)

        self.next_state = tk.Button(button_frame, text='Next state')
        self.next_state.bind('<Button>', self.next_state_handler)
        self.next_state.grid(row=1, column=3, padx=5)

        button_frame.grid_columnconfigure((0,1), weight=1, uniform="column")
        button_frame.pack()


        outer_button_frame.pack(side="top", fill="x", pady=20)

    def set_up_cell_frame(self) -> None:
        cell_frame_container = tk.Frame(self)
        self.cell_frame = tk.Canvas(cell_frame_container, height=20*self.grid_height, width=20*self.grid_width)

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                self.set_cell((x, y), 0)


        self.cell_frame.pack(side='top')
        cell_frame_container.pack(side='top', fill='x')

    def set_cell(self, coords: tuple[float], state: int) -> None:
        x, y = ((p + 0.5) * 20 for p in coords)

        if state:
            self.cell_frame.create_image(x, y, image=self.images['alive'])
        else:
            self.cell_frame.create_image(x, y, image=self.images['dead'])

    


    def update_gui_cells(self) -> None:
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                self.set_cell((x, y), self.board.state_at(x, y))
    
    def reset_last_painted_handler(self, event) -> None:
        self.last_painted = None

    def toggle_gui_cell_handler(self, event) -> None:
        pass

    def reset_all_handler(self, event) -> None:
        pass
    
    def next_state_handler(self, event) -> None:
        self.board.calculate_next_state_all()
        self.board.switch_to_next_state_all()
        self.update_gui_cells()

    def save_board_handler(self) -> None:
        filename = fd.asksaveasfilename(initialfile = 'saved.json', defaultextension=".json", filetypes=[("All Files","*.*"),("JSON File","*.json")])
        self.board.save_to_file(filename)

    def load_board_handler(self) -> None:
        filename = fd.askopenfilename(defaultextension=".json", filetypes=[("All Files","*.*"),("JSON File","*.json")])
        status = self.board.load_from_file(filename)

        if status == -1:
            tk.messagebox.showerror(title='Error loading data', message='Save file dimensions don\'t match window dimensions!')
        else:
            self.update_gui_cells()
    
    def open_gh_page(self) -> None:
        os.system("start \"\" https://github.com/ShaderLight/game-of-life-python")

    def auto_ticking_handler(self, event) -> None:
        if self.is_ticking:
            self.is_ticking = False
            self.enable_buttons()
        else:
            self.is_ticking = True
            self.disable_buttons()
            self.ticking_loop()

    def disable_buttons(self) -> None:
        self.reset_button.configure(state='disabled')
        self.next_state.configure(state='disabled')

    def enable_buttons(self) -> None:
        self.reset_button.configure(state='normal')
        self.next_state.configure(state='normal')

    def ticking_loop(self) -> None:
        self.board.calculate_next_state_all()
        self.board.switch_to_next_state_all()
        self.update_gui_cells()
        if self.is_ticking:
            self.parent.after(int(1000/self.tick_rate.get()), self.ticking_loop)