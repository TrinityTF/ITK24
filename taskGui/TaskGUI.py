from tkinter import Frame, Text, Button, Label, Entry, messagebox
from tkinter.ttk import Combobox

from Circle import Circle
from Rectangle import Rectangle
from Cone import Cone


class TaskGUI:
    def __init__(self, main):
        self.main = main
        main.title("Task GUI")
        self.main.geometry("1280x720")

        # Frame
        self.frame = Frame(self.main, background="gray24")
        self.frame.pack(fill="both", expand=True)

        # Create Combobox
        self.cmb= Combobox(self.frame, values=("Vali kujund", "Ring", "Ristkülik", "Koonus", "Silinder", "Täisnurkne kolmnurk"))
        self.cmb.current(0) # vali kujund
        self.cmb["state"] = "readonly"
        self.cmb.grid(row=0, column=0,padx=5, pady=5, columnspan=2,sticky="ew")

        # "Ujuvad" Vidinad
        self.lblCircle, self.txtCircle = self.createCircleWidget()
        self.lblA, self.lblB, self.txtA, self.txtB = self.createRectangleWidget()
        self.lblConeR, self.lblConeH, self.txtConeR, self.txtConeH = self.createConeWidget()

        # Create button
        self.btnSubmit = self.createButton()

        # Create result Text
        self.result = self.createResult()

        # Peidame kujundidte "asjad"
        self.forgetCircle()
        self.forgetRectangle()
        self.forgetCone()

        # Kuula Comboboxi muutusi
        self.cmb.bind("<<ComboboxSelected>>", self.changed)
        self.main.bind("<Return>", lambda event=None: self.calculate())



    def createButton(self):
        button = Button(self.frame, text="Näita", command=lambda: self.calculate())
        button["state"] = "disabled"
        button.grid(row=3, column=0, padx=5, pady=5,columnspan=2, sticky="ew")
        return button

    def createResult(self):
        result = Text(self.frame, height=5, width=25)
        result.grid(row=4, column=0, padx=5, pady=5, columnspan=2, sticky="ew")
        result["state"] = "disabled"
        return result

    def createCircleWidget(self):
        label = Label(self.frame, text="Raadius")
        label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        text = Entry(self.frame, width=12)
        text.focus()
        text.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        return label, text

    def createRectangleWidget(self):
        labelA = Label(self.frame, text="Külg A")
        labelA.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        textA = Entry(self.frame, width=12)
        textA.focus()
        textA.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        labelB = Label(self.frame, text="Külg B")
        labelB.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        textB = Entry(self.frame, width=12)
        textB.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        return labelA, labelB, textA, textB
    
    def createConeWidget(self):
        labelR = Label(self.frame, text="Raadius")
        labelR.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        textR = Entry(self.frame, width=12)
        textR.focus()
        textR.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        labelH = Label(self.frame, text="Raadius")
        labelH.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        textH = Entry(self.frame, width=12)
        textH.focus()
        textH.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        return labelR, labelH, textR, textH
        
    def forgetCircle(self):
        self.lblCircle.grid_forget()
        self.txtCircle.grid_forget()
        self.btnSubmit["state"] = "disabled"

    def forgetRectangle(self):
        self.lblA.grid_forget()
        self.lblB.grid_forget()
        self.txtA.grid_forget()
        self.txtB.grid_forget()
        self.btnSubmit["state"] = "disabled"
        
    def forgetCone(self):
        self.lblConeR.grid_forget()
        self.lblConeH.grid_forget()
        self.txtConeR.grid_forget()
        self.txtConeH.grid_forget()
        self.btnSubmit["state"] = "disabled"

    def changed(self, event=None):
        comboIndex = self.cmb.current()
        #print(comboIndex)
        if comboIndex == 0:
            self.forgetCircle()
            self.forgetRectangle()
            self.btnSubmit["state"] = "disabled"

        elif comboIndex == 1:
            self.lblCircle, self.txtCircle = self.createCircleWidget()
            self.forgetRectangle()
            self.btnSubmit["state"] = "normal"

        elif comboIndex == 2:
            self.lblA, self.lblB, self.txtA, self.txtB = self.createRectangleWidget()
            self.forgetCircle()
            self.btnSubmit["state"] = "normal"
            
        elif comboIndex == 3:
            self.lblConeR, self.lblConeR, self.txtConeR, self.txtConeH = self.createConeWidget()
            self.forgetCone()
            self.btnSubmit["state"] = "normal"

        self.clearResult()

    def clearResult(self):
        self.result.config(state="normal")
        self.result.delete("1.0", "end")
        self.result.config(state="disabled")

    def calculate(self):
        cmbIndex = self.cmb.current()
        if cmbIndex == 1:
            try :
                radius = float(self.txtCircle.get().strip())
                circle = Circle(radius)
                self.clearResult()
                self.result.config(state="normal")
                self.result.insert("1.0", str(circle))
                self.result.config(state="disabled")

            except ValueError:
                messagebox.showerror("Viga", "Raadius peab olema number.")

            self.txtCircle.delete(0, "end")
            self.txtCircle.focus()

        elif cmbIndex == 2:
            try:
                a = float(self.txtA.get().strip())
                b = float(self.txtB.get().strip())
                rectangle = Rectangle(a, b)
                self.clearResult()
                self.result.config(state="normal")
                self.result.insert("1.0", str(rectangle))
                self.result.config(state="disabled")

            except ValueError:
                messagebox.showerror("Viga", "Küljed peavad olema numbrid.")
                
        elif cmbIndex == 3:
            try:
                r = float(self.txtConeR.get().strip())
                h = float(self.txtConeH.get().strip())
                cone = Cone(r, h)
                self.clearResult()
                self.result.config(state="normal")
                self.result.insert("1.0", str(cone))
                self.result.config(state="disabled")
                
            except ValueError:
                messagebox.showerror("Viga", "Raadius ja kõrgus peavad olema numbrid.")

            self.txtA.delete(0, "end")
            self.txtB.delete(0, "end")
            self.txtA.focus()
