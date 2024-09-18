from tkinter import *
from tkinter import ttk
from vars import *
from Sketchpad.sketchpad import Sketchpad
from Dialog.addObjDialog import AddObjDialog


def main():
    root = Tk()
    root.title("SGI-UFSC")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe = ttk.Frame(root, padding="50 50 50 50")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=3)
    mainframe.rowconfigure(0, weight=1, pad=20)
    mainframe.rowconfigure(1, weight=0)

    menu = ttk.LabelFrame(mainframe, text="Menu", width=200, padding="20")
    menu.grid(column=0, row=0, sticky=(N, W, S))

    objectsListTitle = ttk.Label(menu, text="Objetos")
    objectsListTitle.grid(column=0, row=0, sticky=(N, W))

    sketch = Sketchpad(
        mainframe,
        menu=menu,
        background="black",
        height=CANVAS_HEIGHT,
        width=CANVAS_WIDTH,
        borderwidth=5,
        relief="sunken",
    )
    sketch.grid(column=1, row=0, rowspan=2)
    sketch.focus()

    objectsList = Listbox(menu, listvariable=sketch.getObjectsList())
    objectsList.grid(column=0, row=1, sticky=(N, W, E))

    sketch.set_objects_list(objectsList)  # Set the objectsList in Sketchpad

    scrollBar = ttk.Scrollbar(menu, orient=VERTICAL, command=objectsList.yview)
    objectsList["yscrollcommand"] = scrollBar.set
    scrollBar.grid(column=1, row=1, sticky=(N, S))

    addNewObjBtn = ttk.Button(
        menu, text="+", width=5, command=lambda: AddObjDialog(root, sketch)
    )
    addNewObjBtn.grid(column=0, row=0, sticky=(E))

    root.mainloop()


main()
