# Allows one to insert multiple lines.
# Needs to resize when the list gets too long.python

import tkinter as tk
from datetime import datetime


class App(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.label_frame = tk.Frame(self.master)
        self.label_frame.grid()

        self.label_list = []

        for i in range(2):
            self.label_list.append(tk.Label(self.label_frame, text="Some Data"))
            self.label_list[i].grid(row=i)

        self.label_list.append(tk.Button(self.label_frame, text="Add new data", command=self.add_new_data))
        self.label_list[2].grid(row=2)

    def add_new_data(self):
        self.label_list.insert(1, tk.Label(self.label_frame, text=str(datetime.now().strftime('%H:%M:%S'))))

        for widget in self.label_frame.children.values():
            widget.grid_forget() 

        for ndex, i in enumerate(self.label_list):
            i.grid(row=ndex)


if __name__ == "__main__":
    root = tk.Tk() 
    root.geometry('200x300')
    my_app = App(root)
    root.mainloop()
