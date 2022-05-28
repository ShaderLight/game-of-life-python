import logging
import os
from time import sleep

from modules import board


# https://stackoverflow.com/a/684344
cls = lambda: os.system('cls' if os.name=='nt' else 'clear')

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

board_data = board.Board(20, 10)


board_data.toggle_cell_at(5, 5)
board_data.toggle_cell_at(5, 6)
board_data.toggle_cell_at(5, 7)

board_data.toggle_cell_at(15, 5)
board_data.toggle_cell_at(15, 6)
board_data.toggle_cell_at(15, 7)
board_data.toggle_cell_at(16, 6)
board_data.toggle_cell_at(16, 5)
board_data.toggle_cell_at(16, 4)

print(board_data)

# Simple oscillators
# https://upload.wikimedia.org/wikipedia/commons/c/c2/2-3_O1.gif
# and
# https://upload.wikimedia.org/wikipedia/commons/a/ac/2-3_unruhe.gif

for i in range(10):
    cls()
    print("Oscillators")
    board_data.calculate_next_state_all()
    board_data.switch_to_next_state_all()
    print(board_data)
    sleep(0.5)

cls()

print('Before saving')
print(board_data)
board_data.save_to_file('out/saved_oscillators.json')
board_data.reset_all()

print('Cleared')
print(board_data)

print('Loaded')
board_data.load_from_file('out/saved_oscillators.json')
print(board_data)