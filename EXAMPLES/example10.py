# Only inserts 1 new row.

from tkinter import *
from tkinter.ttk import *
root = Tk()

def add_new_data():
    Label(root, text="<<New Data>>").grid(row=1)

Label(root, text="Some Data").grid(row=0)
Label(root, text="Some Data").grid(row=2)

Button(root, text="Add New Data", command=add_new_data).grid(row=3)

root.mainloop()
