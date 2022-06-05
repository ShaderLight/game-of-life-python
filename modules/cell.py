class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.state = 0 # 0 - dead, 1 - alive
        self.state_next = None
        self.adjacent_cells = []
        self.x = x
        self.y = y

    def calculate_next_state(self) -> bool:
        sum = 0
        for cell in self.adjacent_cells:
            sum += int(cell)

        if sum == 3:
            self.state_next = 1
            return self.state_next != self.state
        
        if sum == 2 and self.state == 1:
            self.state_next = 1
            return self.state_next != self.state

        self.state_next = 0

        # Has the cell changed state?
        # Allows to avoid further iterations through all board cells
        # by remembering which cells changed their state
        return self.state_next != self.state

    def switch_to_next_state(self) -> None:
        if self.state_next == None:
            raise NextStateNotCalculatedError

        self.state = self.state_next
        self.state_next = None

    def reset(self) -> None:
        self.state = 0
        self.state_next = None

    # For simple next state calculation
    def __int__(self) -> int:
        return self.state

    def __str__(self) -> str:
        return f"Cell at ({self.x}, {self.y}), with state {self.state}"


class NextStateNotCalculatedError(Exception):
    pass