import tkinter as tk
from tkinter import filedialog as fd
import os

from .board import*

class App(tk.Frame):
    """
    Represents the whole app, itended to be put into a root window in order to run it.

    Has a set of buttons to control the cells, and allows "painting" the board
    by clicking and dragging the cursor. Loading and saving the state of the board
    to .json files is possible by using the menu bar.

    Attributes:
        parent: References the root window containing the app.
        grid_width: How wide should board be, measured in cells. The default value is 40.
            Change with caution, as differences in grid dimensions will lead to
            errors in loading the state from file.
        grid_height: The same as above, but with height. The default value is 30.
        board: A data structure organising the cells and managaging their states.
        last_painted: Coordinates of the last cell painted. Fixes the problem
            of cells flickering when hovering cursor above one cell while holding LMB.
        is_ticking: A boolean indicating if automatic clock is turned on, used to
            automatically switch to next state without the need to manually click the
            next state button.
        cell_widgets: A list containing frames. Each frame is a graphical representation
            of one cell. Indicating the state is achieved by switching their background color,
            with black meaning alive and white meaning dead.
    """

    def __init__(self, parent, grid_width = 40, grid_height = 30, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.board = Board(self.grid_width, self.grid_height)
        self.last_painted = None
        self.is_ticking = False
        self.cell_widgets = []
        parent.bind('<B1-Motion>', self.toggle_gui_cell_handler)
        parent.bind('<ButtonRelease-1>', self.reset_last_painted_handler)
        parent.bind('<Button-1>', self.toggle_gui_cell_handler)

        # Creating necessary buttons, frames, and menu bar cascades, moved to methods to improve readibility
        self.set_up_menu_bar()
        self.set_up_button_frame()
        self.set_up_cell_frame()
        
    def set_up_menu_bar(self) -> None:
        """Configures the menu bar and it's cascades"""
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar)
        self.about_menu = tk.Menu(self.menu_bar)
        self.file_menu.add_command(label='Open...', command=self.load_board_handler)
        self.file_menu.add_command(label='Save as...', command=self.save_board_handler)
        self.about_menu.add_command(label='GitHub repo', command=self.open_gh_page)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.menu_bar.add_cascade(label='Help', menu=self.about_menu)
        self.parent.config(menu=self.menu_bar)

    def set_up_button_frame(self) -> None:
        """Configures the buttons and packs the frames containing them"""
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
        """Creates the cell frame and packs the cells in a grid layout"""
        self.cell_frame_container = tk.Frame(self)
        self.cell_frame = tk.Frame(self.cell_frame_container)

        for y in range(self.grid_height):
            temp_row = []
            for x in range(self.grid_width):
                new_cell = tk.Frame(self.cell_frame, width=20, height=20)
                new_cell.configure({"background": "White"})
                new_cell.paintable = True
                new_cell.grid(row=y, column=x, padx=1, pady=1)
                new_cell.bind('<FocusIn>', self.toggle_gui_cell_handler)
                temp_row.append(new_cell)
            self.cell_widgets.append(temp_row)
        self.cell_frame.pack(side='top')
        self.cell_frame_container.pack(side='top', fill='x')

    def update_gui_cells(self) -> None:
        """
        For every cell that has changed state, update the background color
        of the corresponding widget in cell grid.
        """
        for cell in self.board.changed_cells:
            curr_widget = self.cell_widgets[cell.y][cell.x]

            if cell.state == 1:
                curr_widget.configure({"background": "Black"})
            else:
                curr_widget.configure({"background": "White"})

        self.board.clear_changed_cells_mem()

    def force_update_all_cells(self) -> None:
        """
        Forces the update of all widgets regardless if they are present
        in the changed_cells list. Used to load board from state.
        """
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                curr_widget = self.cell_widgets[y][x]
                if self.board.state_at(x, y) == 1:
                    curr_widget.configure({"background": "Black"})
                else:
                    curr_widget.configure({"background": "White"})

        self.board.clear_changed_cells_mem()

    def reset_last_painted_handler(self, event) -> None:
        """Clears the last_painted cell reference when releasing LMB."""
        self.last_painted = None

    def toggle_gui_cell_handler(self, event) -> None:
        """
        Handles the clicking and dragging with mouse.
        Allows painting the cells.
        """
        widget = event.widget.winfo_containing(event.x_root, event.y_root)

        # In case user tries to "paint" other widgets than cell frames
        if not hasattr(widget, 'paintable'):
            return

        # Get the grid x,y relative coordinates of the cell user wants to paint
        x = widget.grid_info()['column']
        y = widget.grid_info()['row']

        # In order to avoid the flickering of hovered cell
        if self.last_painted == (x, y):
            return

        new_state = self.board.toggle_cell_at(x, y)

        if new_state == 1:
            widget.configure({"background": "Black"})
        else:
            widget.configure({"background": "White"})

        self.last_painted = (x, y)

    def reset_all_handler(self, event) -> None:
        """Clear all cell widgets and board"""
        for widget in self.cell_frame.grid_slaves():
            widget.configure({"background": "White"})

        self.board.reset_all()
    
    def next_state_handler(self, event) -> None:
        """Handles clicking the next_state button"""
        self.board.calculate_next_state_all()
        self.board.switch_to_next_state_all()
        self.update_gui_cells()

    def save_board_handler(self) -> None:
        """Shows a prompt to choose a file path and name to save the state, then saves the state of the board"""
        filename = fd.asksaveasfilename(initialfile = 'saved.json', defaultextension=".json", filetypes=[("All Files","*.*"),("JSON File","*.json")])
        self.board.save_to_file(filename)

    def load_board_handler(self) -> None:
        """Asks for a file to load, then loads it"""
        filename = fd.askopenfilename(defaultextension=".json", filetypes=[("All Files","*.*"),("JSON File","*.json")])
        status = self.board.load_from_file(filename)

        if status == -1:
            tk.messagebox.showerror(title='Error loading data', message='Save file dimensions don\'t match window dimensions!')
        else:
            self.force_update_all_cells()
    
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