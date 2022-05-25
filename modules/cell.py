class Cell:
    def __init__(self) -> None:
        self.state = 0 # 0 - dead, 1 - alive
        self.state_next = None
        self.adjacentCells = None

    def calculateNextState(self) -> None:
        sum = 0
        for cell in self.adjacentCells:
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