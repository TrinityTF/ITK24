import tkinter as tk
from tkinter import messagebox


def mouseMotion(event):
    x,y = event.x, event.y
    lblMouse.config(text=f"x = {x} y = {y}")

def welcome(event=None):
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
#tk.Label(frame, text="Nimi", background="gray57").place(x=5, y=5, width=55)
tk.Label(frame, text="Nimi", background="gray57").grid(row=0, column=0)

# Entry Sisestuskaust
txtName = tk.Entry(frame)
txtName.focus()
#txtName.place(x=70, y=5)
txtName.grid(row=0, column=1, padx=5, pady=5)

# Button Nupp Näita
btnSubmit = tk.Button(frame, text="Näita", command=lambda:welcome())
#btnSubmit.place(x=200, y=5, height=20)
btnSubmit.grid(row=0, column=2,padx=5, pady=5)

# Label Mouse
lblMouse = tk.Label(frame,text="x = 0, y = 0")
#lblMouse.place(x=245, y=5, height=19)
lblMouse.grid(row=0, column=3,padx=5, pady=5)

# Label Previous
lblPrevious = tk.Label(frame,text="Eelimne sõna: POLE")
#lblPrevious.place(x=335, y=5, height=19)
lblPrevious.grid(row=0, column=4,padx=5, pady=5)

window.bind("<Motion>", mouseMotion)
window.bind("<Return>", welcome)

window.mainloop() # Viimane rida