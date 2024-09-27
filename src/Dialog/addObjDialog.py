from tkinter import *
from tkinter import ttk
from vars import *


class AddObjDialog(Toplevel):
    def __init__(self, parent, canvas_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas_manager = canvas_manager
        self.title("Adicionar objeto")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_frame = ttk.Frame(self, padding="50 50 50 50")
        main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        main_frame.columnconfigure(0, weight=1, pad=40)
        main_frame.columnconfigure(1, weight=1, pad=40)
        main_frame.columnconfigure(2, weight=1, pad=40)
        main_frame.columnconfigure(3, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1, pad=100)
        main_frame.rowconfigure(2, weight=1)

        ttk.Button(main_frame, text="Cancelar", command=self.dismiss).grid(
            row=2, column=0
        )

        obj_type_combobox_label = ttk.Label(main_frame, text="Tipo")
        obj_type_combobox_label.grid(row=0, column=0)

        self.obj_type_combobox = ttk.Combobox(main_frame)
        self.obj_type_combobox["values"] = obj_types
        self.obj_type_combobox.state(["readonly"])
        self.obj_type_combobox.set(obj_types[0])
        self.obj_type_combobox.grid(row=1, column=0)

        color_combobox_label = ttk.Label(main_frame, text="Cor")
        color_combobox_label.grid(row=0, column=3)

        self.color_combobox = ttk.Combobox(main_frame)
        self.color_combobox["values"] = COLORS
        self.color_combobox.state(["readonly"])
        self.color_combobox.set(COLORS[0])
        self.color_combobox.grid(row=1, column=3)

        name_entry_label = ttk.Label(main_frame, text="Nome")
        name_entry_label.grid(row=0, column=1)

        name = StringVar()
        self.name_entry = ttk.Entry(main_frame, textvariable=name, width=50)
        self.name_entry.grid(row=1, column=1)

        coord_entry_label = ttk.Label(
            main_frame, text="Coordenadas, no padrão (x1, y1),(x2, y2),..."
        )
        coord_entry_label.grid(row=0, column=2)

        coords = StringVar()
        self.coord_entry = ttk.Entry(main_frame, textvariable=coords, width=50)
        self.coord_entry.grid(row=1, column=2)

        ttk.Button(main_frame, text="Confirmar", command=self.confirm).grid(
            row=2, column=3
        )

    def dismiss(self):
        self.grab_release()
        self.destroy()

    def confirm(self):
        try:
            obj_type = self.obj_type_combobox.get()
            name = self.name_entry.get()
            raw_coords = self.coord_entry.get()
            color = self.color_combobox.get()

            if name == "":
                return

            coords = list(eval(raw_coords))
            new_obj = ScreenObject(name, obj_type, coords, color)
            self.canvas_manager.add_object(new_obj)
            self.dismiss()
        except:
            return
