# DISPLAY=10.146.122.56:1 python EXAMPLES/a.py

import tkinter as tk
from tkinter import simpledialog

root = tk.Tk() # Create an instance of tkinter

start_date = simpledialog.askstring(title = "Test Title",
                                    prompt = "Entire Start Date in MM/DD/YYYY format:")
print(start_date)
