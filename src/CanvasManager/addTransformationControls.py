from tkinter import *
from tkinter import ttk


def add_transformation_controls(canvasManager, menu: LabelFrame):
    control_frame = ttk.LabelFrame(menu, text="Transformações")
    control_frame.grid(column=0, row=2, sticky=(W, E))
    control_frame.rowconfigure(0, pad=20, weight=1)
    control_frame.columnconfigure(0, pad=20, weight=1)
    control_frame.columnconfigure(1, pad=20, weight=1)

    translation_frame = ttk.LabelFrame(control_frame, text="Translação")
    translation_frame.grid(column=0, row=0, sticky=(W, E))
    translation_frame.rowconfigure(0, pad=10)
    translation_frame.rowconfigure(1, pad=10)
    translation_frame.rowconfigure(2, pad=10)
    translation_frame.columnconfigure(0, pad=10)

    ttk.Label(translation_frame, text="Magnitude:").grid(column=0, row=0)

    translation_magnitude = StringVar()
    canvasManager.translation_entry = ttk.Entry(
        translation_frame, textvariable=translation_magnitude, width=20
    )
    canvasManager.translation_entry.grid(row=0, column=1)

    ttk.Button(
        translation_frame,
        text="←",
        command=lambda: canvasManager.transform_selected(
            "translate", -1 * float(canvasManager.translation_entry.get() or 10), 0
        ),
    ).grid(row=1, column=0)
    ttk.Button(
        translation_frame,
        text="→",
        command=lambda: canvasManager.transform_selected(
            "translate", float(canvasManager.translation_entry.get() or 10), 0
        ),
    ).grid(row=1, column=1)
    ttk.Button(
        translation_frame,
        text="↑",
        command=lambda: canvasManager.transform_selected(
            "translate", 0, -1 * float(canvasManager.translation_entry.get() or 10)
        ),
    ).grid(row=2, column=0)
    ttk.Button(
        translation_frame,
        text="↓",
        command=lambda: canvasManager.transform_selected(
            "translate", 0, float(canvasManager.translation_entry.get() or 10)
        ),
    ).grid(row=2, column=1)

    scale_frame = ttk.LabelFrame(control_frame, text="Escalonamento")
    scale_frame.grid(column=1, row=0, sticky=(N, W, E, S))
    scale_frame.rowconfigure(0, pad=10)
    scale_frame.rowconfigure(1, pad=10)
    scale_frame.columnconfigure(0, pad=10)

    ttk.Label(scale_frame, text="Magnitude em %:").grid(column=0, row=0)

    scale_magnitude = StringVar()
    canvasManager.scale_entry = ttk.Entry(
        scale_frame, textvariable=scale_magnitude, width=20
    )
    canvasManager.scale_entry.grid(row=0, column=1)

    ttk.Button(
        scale_frame,
        text="+",
        command=lambda: canvasManager.scale_selected(
            1 + (float(canvasManager.scale_entry.get() or 10)) / 100,
        ),
    ).grid(row=1, column=0)
    ttk.Button(
        scale_frame,
        text="-",
        command=lambda: canvasManager.scale_selected(
            1 - (float(canvasManager.scale_entry.get() or 10)) / 100,
        ),
    ).grid(row=1, column=1)

    rotate_frame = ttk.LabelFrame(control_frame, text="Rotação")
    rotate_frame.grid(column=0, row=1, sticky=(N, W, E, S), columnspan=2)
    rotate_frame.rowconfigure(0, pad=10)
    rotate_frame.rowconfigure(1, pad=10)
    rotate_frame.columnconfigure(0, pad=10)
    rotate_frame.columnconfigure(1, pad=10)
    rotate_frame.columnconfigure(2, pad=10)

    ttk.Label(rotate_frame, text="Rotação em graus:").grid(column=0, row=0)

    rotate_magnitude = StringVar()
    canvasManager.rotate_entry = ttk.Entry(
        rotate_frame, textvariable=rotate_magnitude, width=20
    )
    canvasManager.rotate_entry.grid(row=0, column=1)

    rotate_type_frame = ttk.Frame(rotate_frame)
    rotate_type_frame.grid(row=0, column=2)

    canvasManager.rotate_type = StringVar()
    canvasManager.rotate_type.set("object")
    ttk.Radiobutton(
        rotate_type_frame,
        text="Em torno do centro do mundo",
        variable=canvasManager.rotate_type,
        value="world",
    ).grid(row=0, column=0)
    ttk.Radiobutton(
        rotate_type_frame,
        text="Em torno do centro do objeto",
        variable=canvasManager.rotate_type,
        value="object",
    ).grid(row=1, column=0)
    ttk.Radiobutton(
        rotate_type_frame,
        text="Em torno de ponto arbitrário",
        variable=canvasManager.rotate_type,
        value="arbitrary_point",
    ).grid(row=2, column=0)

    ttk.Label(
        rotate_type_frame, text="Ponto arbitrário para rotação, formato x, y:"
    ).grid(row=3, column=0)

    rotate_point = StringVar()
    canvasManager.rotate_point_entry = ttk.Entry(
        rotate_frame, textvariable=rotate_point, width=10
    )
    canvasManager.rotate_point_entry.grid(row=1, column=2)

    ttk.Button(
        rotate_frame,
        text="↺",
        command=lambda: canvasManager.rotate_selected("counterclockwise"),
    ).grid(row=1, column=0)
    ttk.Button(
        rotate_frame,
        text="↻",
        command=lambda: canvasManager.rotate_selected("clockwise"),
    ).grid(row=1, column=1)
