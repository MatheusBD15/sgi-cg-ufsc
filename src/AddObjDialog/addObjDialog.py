from tkinter import *
from tkinter import ttk
from vars import *


class AddObjDialog(Toplevel):
    def __init__(self, parent, sketchpad, **kwargs):
        super().__init__(parent, **kwargs)
        self.sketchpad = sketchpad
        self.title("Adicionar objeto")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        mainframe = ttk.Frame(self, padding="50 50 50 50")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1, pad=40)
        mainframe.columnconfigure(1, weight=1, pad=40)
        mainframe.columnconfigure(2, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.rowconfigure(1, weight=1, pad=100)
        mainframe.rowconfigure(2, weight=1)

        ttk.Button(mainframe, text="Cancelar", command=self.dismiss).grid(
            row=2, column=0
        )

        objTypeComboboxLabel = ttk.Label(mainframe, text="Tipo")
        objTypeComboboxLabel.grid(row=0, column=0)

        self.objTypeCombobox = ttk.Combobox(
            mainframe,
        )
        self.objTypeCombobox["values"] = objTypes
        self.objTypeCombobox.state(["readonly"])
        self.objTypeCombobox.set(objTypes[0])
        self.objTypeCombobox.grid(row=1, column=0)

        nameEntryLabel = ttk.Label(mainframe, text="Nome")
        nameEntryLabel.grid(row=0, column=1)

        name = StringVar()
        self.nameEntry = ttk.Entry(mainframe, textvariable=name, width=50)
        self.nameEntry.grid(row=1, column=1)

        coordEntryLabel = ttk.Label(
            mainframe, text="Coordenadas, no padrão (x1, y1),(x2, y2),..."
        )
        coordEntryLabel.grid(row=0, column=2)

        coords = StringVar()

        self.coordEntry = ttk.Entry(
            mainframe,
            textvariable=coords,
            width=50,
        )
        self.coordEntry.grid(row=1, column=2)

        ttk.Button(mainframe, text="Confirmar", command=self.confirm).grid(
            row=2, column=2
        )

    def dismiss(self):
        self.grab_release()
        self.destroy()

    def confirm(self):
        try:
            type = self.objTypeCombobox.get()
            name = self.nameEntry.get()
            rawCoords = self.coordEntry.get()

            if name == "":
                return

            coords = list(eval((rawCoords)))
            newObj = ScreenObject(name, type, coords)
            self.sketchpad.addObject(newObj)
            self.dismiss()
        except:
            return
