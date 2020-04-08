from tkinter import Tk, Label

window = Tk()

window.title("Welcome to LikeGeeks app")
window.geometry('350x200')

lbl = Label(window, text="Hello", font=("Arial Bold", 50))

lbl.grid(column=0, row=0)

window.mainloop()
