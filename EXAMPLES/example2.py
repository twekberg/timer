from tkinter import Tk, Label

window = Tk()

window.title("Welcome to LikeGeeks app")

lbl = Label(window, text="Hello")

lbl.grid(column=0, row=0)

window.mainloop()
