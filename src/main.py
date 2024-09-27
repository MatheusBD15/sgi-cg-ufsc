from tkinter import *
from tkinter import ttk
from vars import *
from CanvasManager.canvasManager import CanvasManager
from CanvasManager.addTransformationControls import add_transformation_controls
from Dialog.addObjDialog import AddObjDialog


def main():
    root = Tk()
    root.title("SGI-UFSC")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main_frame = ttk.Frame(root, padding="50 50 50 50")
    main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=3)
    main_frame.rowconfigure(0, weight=1, pad=20)
    main_frame.rowconfigure(1, weight=0)

    menu = ttk.LabelFrame(main_frame, text="Menu", width=200, padding="20")
    menu.grid(column=0, row=0, sticky=(N, W, S))

    objects_list_title = ttk.Label(menu, text="Objetos")
    objects_list_title.grid(column=0, row=0, sticky=(N, W))

    canvas = Canvas(
        main_frame,
        background="black",
        height=CANVAS_HEIGHT,
        width=CANVAS_WIDTH,
        borderwidth=5,
        relief="sunken",
    )
    canvas.grid(column=1, row=0, rowspan=2)
    canvas.focus()

    canvas_manager = CanvasManager(canvas=canvas)
    add_transformation_controls(canvas_manager, menu)

    objects_list = Listbox(menu, listvariable=canvas_manager.get_objects_list())
    objects_list.grid(column=0, row=1, sticky=(N, W, E))

    canvas_manager.set_objects_list(objects_list)

    scroll_bar = ttk.Scrollbar(menu, orient=VERTICAL, command=objects_list.yview)
    objects_list["yscrollcommand"] = scroll_bar.set
    scroll_bar.grid(column=1, row=1, sticky=(N, S))

    add_new_obj_btn = ttk.Button(
        menu, text="+", width=5, command=lambda: AddObjDialog(root, canvas_manager)
    )
    add_new_obj_btn.grid(column=0, row=0, sticky=(E))

    root.mainloop()


main()
