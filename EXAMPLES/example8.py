from tkinter import Tk, Label, Button, Entry

lbl = None
txt = None

def clicked():
    global lbl, txt
    res = "Welcome to " + txt.get()
    lbl.configure(text=res)

def main():
    global lbl,txt
    window = Tk()

    window.title("Welcome to LikeGeeks app")
    window.geometry('350x200')

    #lbl = Label(window, text="Hello", font=("Arial Bold", 50))
    lbl = Label(window, text="Hello")
    lbl.grid(column=0, row=0)

    txt = Entry(window,width=10)
    txt.grid(column=1, row=0)

    #btn = Button(window, text="Click Me")
    btn = Button(window, text="Click Me", command=clicked)
    btn.grid(column=2, row=0)

    window.mainloop()


if __name__ == '__main__':
    main()
