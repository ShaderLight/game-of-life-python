from turtle import width
from cell import Cell

class Board:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells = []

        self.generate_cells()
    
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
                    self.cells[y][x] = self.cells[pair[1]][pair[0]]

    def get_neighbouring_coords(self, x: int, y: int) -> list[tuple[int]]:
        possible_coords = [(x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1), (x, y-1), (x-1, y-1), (x-1, y), (x-1, y+1)]
        actual_coords = []

        for pair in possible_coords:
            if pair[0] < self.width and pair[1] < self.height:
                actual_coords.append(pair)

        return actual_coords.copy()