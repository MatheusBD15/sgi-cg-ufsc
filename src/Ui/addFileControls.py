from tkinter import *
from tkinter import ttk
from CanvasManager.canvasManager import CanvasManager

def add_file_controls(canvasManager: CanvasManager, main_frame: Frame):
    control_frame = ttk.LabelFrame(main_frame, text="Arquivos")
    control_frame.grid(column=1, row=1, sticky=(N, W, E, S))
    control_frame.rowconfigure(0, pad=30)
    control_frame.columnconfigure(0, pad=30)
    control_frame.columnconfigure(1, pad=30)

    ttk.Button(
        control_frame, text="Exportar .obj", command=canvasManager.export_obj_file
    ).grid(column=0, row=0)
    # ttk.Button(
    #     control_frame, text="Importar .obj", command=canvasManager.import_obj_file
    # ).grid(column=1, row=0)