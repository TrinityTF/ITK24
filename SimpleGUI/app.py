import tkinter as tk
from tkinter import messagebox


def mouseMotion(event):
    x,y = event.x, event.y
    lblMouse.config(text=f"x = {x} y = {y}")

def welcome():
    name = txtName.get().strip()
    if name:
        text = f"Tere {name}"
        messagebox.showinfo("Tere", text)
        lblPrevious.config(text=f"Eelmine sõna: {name}")

    else:
        messagebox.showerror("Viga", "Sisesta nimi!")
        lblPrevious.config(text="Eelmine sõna: VIGA")

    txtName.delete(0, tk.END)

window = tk.Tk()
window.title('Lihtne kasutajaliides')
window.geometry('500x250')

# Frame
frame = tk.Frame(window, background="gray20")
frame.pack(fill='both', expand=True)

# Label Name
tk.Label(frame, text="Nimi", background="gray57").place(x=5, y=5, width=55)

# Entry Sisestuskaust
txtName = tk.Entry(frame)
txtName.focus()
txtName.place(x=70, y=5)

# Button Nupp Näita
btnSubmit = tk.Button(frame, text="Näita", command=welcome)
btnSubmit.place(x=200, y=5, height=20)

# Label Mouse
lblMouse = tk.Label(frame,text="x = 0, y = 0")
lblMouse.place(x=245, y=5, height=19)

# Label Previous
lblPrevious = tk.Label(frame,text="Eelimne sõna: POLE")
lblPrevious.place(x=335, y=5, height=19)

window.bind("<Motion>", mouseMotion)

window.mainloop() # Viimane rida