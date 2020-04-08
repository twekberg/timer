"""
Displays a simpmle menu and a label below it.
"""

import tkinter as tk

root = tk.Tk()

def hello():
    print("hello!")

frame = tk.Frame(root)
frame.pack()

menubar = tk.Menu(frame)
menubar.add_command(label="Hello!", command=hello)
menubar.add_command(label="Quit!", command=lambda: root.quit() or root.destroy())
root.config(menu=menubar)

l = tk.Label(frame, text='Hi Tom!')
l.pack( side = tk.LEFT)

root.mainloop()
