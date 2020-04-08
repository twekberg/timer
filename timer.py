from tkinter import Tk, Label, Button
from tkinter import simpledialog

lbl = None

def add_field(window):
    #lbl.configure(text="Button was clicked !!")
    field = simpledialog.askstring('Add field', 'Field name')
    print(field)

def main():
    global lbl
    window = Tk()

    window.title("Welcome to timer app")
    window.geometry('350x200')

    #lbl = Label(window, text="Hello", font=("Arial Bold", 50))
    lbl = Label(window, text="Hello")
    lbl.grid(column=0, row=0)

    btn = Button(window, text="Add field", command=lambda: add_field(window))
    btn.grid(column=1, row=0)

    window.mainloop()


if __name__ == '__main__':
    main()
