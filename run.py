import logging
import tkinter as tk

from modules import gui

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('882x728')
    root.title('The game of life')
    root.iconbitmap('glider.ico') 

    main_frame = gui.App(root, 60, 40)
    main_frame.pack(side="top", fill="both", expand=1)
    root.eval('tk::PlaceWindow . center')

    root.mainloop()