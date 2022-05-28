import logging
import json

from .cell import*

class Board:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells = []

        self.generate_cells()
        self.assign_neighbours()
    
    def generate_cells(self):
        for y in range(self.height):
            temporary_row = []
            for x in range(self.width):
                temporary_row.append(Cell(x,y))
            self.cells.append(temporary_row.copy())

    def assign_neighbours(self):
        for y in range(self.height):
            for x in range(self.width):
                for pair in self.get_neighbouring_coords(x, y):
                    self.cells[y][x].adjacent_cells.append (self.cells[pair[1]][pair[0]])
                logging.debug(f"Cell ({x},{y}) received references to neighbours")

    def get_neighbouring_coords(self, x: int, y: int) -> list[tuple[int]]:
        possible_coords = [(x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1), (x, y-1), (x-1, y-1), (x-1, y), (x-1, y+1)]
        actual_coords = []

        for pair in possible_coords:
            if pair[0] < self.width and pair[1] < self.height:
                actual_coords.append(pair)

        return actual_coords.copy()
    
    def calculate_next_state_all(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.calculate_next_state()

    def switch_to_next_state_all(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.switch_to_next_state()

    def state_at(self, x: int, y: int) -> int:
        return self.cells[y][x].state

    def __repr__(self) -> str:
        output = ""
        for y in range(self.height):
            temp_row = ""
            for x in range(self.width):
                temp_row += f"{self.cells[y][x].state} "
            output += temp_row[:-1] + "\n"
        
        return output

    def __str__(self) -> str:
        output = ""
        for y in range(self.height):
            temp_row = ""
            for x in range(self.width):
                temp_row += f"{self.cells[y][x].state} "
            output += temp_row[:-1] + "\n"
        
        return output

    def toggle_cell_at(self, x: int, y: int) -> int:
        selected_cell = self.cells[y][x]

        if selected_cell.state == 0:
            selected_cell.state = 1
            return 1
        else:
            selected_cell.state = 0
            return 0

    def reset_all(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.reset()

    def get_serialized_cells(self) -> list[int]:
        serialized = []

        for row in self.cells:
            for cell in row:
                serialized.append(int(cell))

        return serialized

    def save_to_file(self, filename: str) -> None:
        with open(filename, mode='w') as f:
            to_dump = {'width': self.width, 'height': self.height, 'cells': self.get_serialized_cells()}
            json.dump(to_dump, f, indent=4)

    def load_serialized_cells(self, cells: list[int]) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].state = cells[y*self.width + x]

    def load_from_file(self, filename: str) -> int:
        with open(filename, mode='r') as f:
            content = json.load(f)
        
        if content['width'] == self.width and content['height'] == self.height:
            self.load_serialized_cells(content['cells'])
            return 0
        else:
            logging.warning(f'Incorrect save file dimensions {content["width"]}x{content["height"]}, expected {self.width}x{self.height}')
            return -1