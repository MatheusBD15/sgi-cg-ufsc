from tkinter import *
from tkinter import ttk
from vars import *
from Sketchpad.sketchpad import Sketchpad
from AddObjDialog.addObjDialog import AddObjDialog


def openAddObjDialog(root: Tk, sketchpad: Sketchpad):
    AddObjDialog(root, sketchpad)


def main():

    root = Tk()
    root.title("SGI-UFSC")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe = ttk.Frame(root, padding="50 50 50 50")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1, pad=40)
    mainframe.columnconfigure(1, weight=1)
    mainframe.columnconfigure(2, weight=0)
    mainframe.rowconfigure(0, weight=1)
    mainframe.rowconfigure(1, weight=0)
    mainframe.rowconfigure(2, weight=1)

    menu = ttk.LabelFrame(mainframe, text="Menu", width=600, padding="20")
    menu.grid(column=0, row=0, sticky=(N, W, S), rowspan=3)

    menu.columnconfigure(0, weight=1, minsize=500)
    menu.columnconfigure(1, weight=1)
    menu.columnconfigure(2, weight=1)
    menu.rowconfigure(0, weight=0, pad=20)
    menu.rowconfigure(1, weight=1)

    objectsListTitle = ttk.Label(menu, text="Objetos")
    objectsListTitle.grid(column=0, row=0, sticky=(N, W))

    # A classe Sketchpad contém toda a lógica de renderização
    sketch = Sketchpad(
        mainframe,
        background="black",
        height=CANVAS_HEIGHT,
        width=CANVAS_WIDTH,
        borderwidth=5,
        relief="sunken",
    )
    sketch.grid(column=2, row=1)
    sketch.focus()

    objectsList = Listbox(menu, listvariable=sketch.getObjectsList())
    objectsList.grid(column=0, row=1, sticky=(N, W, E))

    scrollBar = ttk.Scrollbar(menu, orient=VERTICAL, command=objectsList.yview)
    objectsList["yscrollcommand"] = scrollBar.set
    scrollBar.grid(column=1, row=1, sticky=(N, W, E))

    addNewObjBtn = ttk.Button(
        menu, text="+", width=5, command=lambda: openAddObjDialog(root, sketch)
    )
    addNewObjBtn.grid(column=2, row=0, sticky=(N, E))

    root.mainloop()


main()
