import logging

from modules import board

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

board_data = board.Board(20, 10)


board_data.toggle_cell_at(5, 5)
board_data.toggle_cell_at(5, 6)
board_data.toggle_cell_at(5, 7)

print(board_data)

for i in range(3):
    board_data.calculate_next_state_all()
    board_data.switch_to_next_state_all()
    print(board_data)