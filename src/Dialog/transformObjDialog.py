from tkinter import *
from tkinter import ttk

class TransformObjDialog(Toplevel):
    def __init__(self, parent, sketchpad, **kwargs):
        super().__init__(parent, **kwargs)
        self.sketchpad = sketchpad
        self.title("Transform Object")
        self.geometry("300x200")
        self.resizable(False, False)

        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Translation buttons
        ttk.Button(mainframe, text="↑", command=lambda: self.translate(0, -10)).grid(column=1, row=0)
        ttk.Button(mainframe, text="↓", command=lambda: self.translate(0, 10)).grid(column=1, row=2)
        ttk.Button(mainframe, text="←", command=lambda: self.translate(-10, 0)).grid(column=0, row=1)
        ttk.Button(mainframe, text="→", command=lambda: self.translate(10, 0)).grid(column=2, row=1)

        # Scaling buttons
        ttk.Button(mainframe, text="+", command=lambda: self.scale(1.1, 1.1)).grid(column=4, row=0)
        ttk.Button(mainframe, text="-", command=lambda: self.scale(0.9, 0.9)).grid(column=4, row=2)

        # Rotation buttons
        ttk.Button(mainframe, text="↺ 15°", command=lambda: self.rotate(-15)).grid(column=0, row=4)
        ttk.Button(mainframe, text="↻ 15°", command=lambda: self.rotate(15)).grid(column=2, row=4)

        # Labels
        ttk.Label(mainframe, text="Translation").grid(column=1, row=3)
        ttk.Label(mainframe, text="Scale").grid(column=4, row=3)
        ttk.Label(mainframe, text="Rotation").grid(column=1, row=5)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def translate(self, dx, dy):
        self.sketchpad.translate_selected(dx, dy)

    def scale(self, sx, sy):
        self.sketchpad.scale_selected(sx, sy)

    def rotate(self, angle):
        self.sketchpad.rotate_selected(angle)