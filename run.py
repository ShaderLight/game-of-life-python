import logging
import tkinter as tk

from modules import gui

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('882x728')

    main_frame = gui.App(root)
    main_frame.pack(side="top", fill="both", expand=1)

    root.mainloop()