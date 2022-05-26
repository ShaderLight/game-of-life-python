class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.state = 0 # 0 - dead, 1 - alive
        self.state_next = None
        self.adjacent_cells = None
        self.x = x
        self.y = y

    def calculate_next_state(self) -> None:
        sum = 0
        for cell in self.adjacent_cells:
            sum += int(cell)

        if sum == 3:
            self.state_next = 1
            return
        
        if sum == 2 and self.state == 1:
            self.state_next = 1
            return

        self.state_next = 0

    # For simple next state calculation
    def __int__(self):
        return self.state

    def __str__(self) -> str:
        return f"Cell at ({self.x}, {self.y}), with state {self.state}"
