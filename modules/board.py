from cell import Cell

class Board:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells = []

        self.generate_cells()
    
    def generate_cells(self):
        for y in range(self.height):
            temporary_column = []
            for x in range(self.width):
                temporary_column.append(Cell(x,y))
            self.cells.append(temporary_column.copy())
