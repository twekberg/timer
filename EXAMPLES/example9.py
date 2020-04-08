"""
Open a blank window (the root) and a small dialog box with the
question located elsewhere on the screen.
"""

from tkinter import simpledialog, Tk

root = Tk()
title='New field'
prompt='Enter'
print(simpledialog.askstring(title, prompt) )
