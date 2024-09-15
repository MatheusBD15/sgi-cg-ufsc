from tkinter import *
from tkinter import ttk
from vars import *
from Sketchpad.viewport import Viewport
from Sketchpad.window import Window
from Sketchpad.transformations import translate, scale, rotate


class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.movementSpeed = 50
        self.bind("<Button-4>", self.handleZoomIn)
        self.bind("<Button-5>", self.handleZoomOut)
        self.bind_all("<KeyPress>", self.handleKeyPress)
        self.bind("<Motion>", self.handleMouseMovement)
        self.mouseXw = 0
        self.mouseYw = 0

        ## Representa o canvas em si
        self.viewport = Viewport(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)

        # Representa um recorte do mundo
        self.window = Window(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
        self.displayFile = STARTING_DISPLAY_FILE
        self.objectsVar = StringVar(value=self.getAllObjectNames())

        self.selected_object = None
        self.objectsList = None  # We'll set this later from main.py

        # Add transformation controls
        self.add_transformation_controls(parent)

        self.repaint()

    def add_transformation_controls(self, parent):
        control_frame = ttk.Frame(parent)
        control_frame.grid(column=0, row=1, sticky=(W, E))

        ttk.Button(
            control_frame,
            text="←",
            command=lambda: self.transform_selected("translate", -3, 0),
        ).grid(row=0, column=0)
        ttk.Button(
            control_frame,
            text="→",
            command=lambda: self.transform_selected("translate", 3, 0),
        ).grid(row=0, column=1)
        ttk.Button(
            control_frame,
            text="↑",
            command=lambda: self.transform_selected("translate", 0, -3),
        ).grid(row=0, column=2)
        ttk.Button(
            control_frame,
            text="↓",
            command=lambda: self.transform_selected("translate", 0, 3),
        ).grid(row=0, column=3)

        ttk.Button(
            control_frame,
            text="+",
            command=lambda: self.transform_selected("scale", 1.05, 1.05),
        ).grid(row=1, column=0)
        ttk.Button(
            control_frame,
            text="-",
            command=lambda: self.transform_selected("scale", 0.95, 0.95),
        ).grid(row=1, column=1)

        ttk.Button(
            control_frame,
            text="↺",
            command=lambda: self.transform_selected("rotate", -1),
        ).grid(row=1, column=2)
        ttk.Button(
            control_frame,
            text="↻",
            command=lambda: self.transform_selected("rotate", 1),
        ).grid(row=1, column=3)

    def set_objects_list(self, listbox):
        self.objectsList = listbox
        self.objectsList.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, event):
        if self.objectsList.curselection():
            index = self.objectsList.curselection()[0]
            self.selected_object = self.displayFile[index]
            self.selected_object.selected = True
            self.repaint()
        else:
            self.clearSelected()

    def clearSelected(self):
        if self.selected_object:
            self.selected_object.selected = False
            self.selected_object = None
            self.repaint()

    def transform_selected(self, transformation, *args):
        if self.selected_object:
            if transformation == "translate":
                self.selected_object.apply_transformation(translate, *args)
            elif transformation == "scale":
                self.selected_object.apply_transformation(scale, *args)
            elif transformation == "rotate":
                self.selected_object.apply_transformation(rotate, *args)
            self.repaint()

    def handleMouseMovement(self, event: Event):
        (xw, yw) = self.viewportTransform2d((event.x, event.y))
        self.mouseXw = xw
        self.mouseYw = yw

        self.repaint()

    def handleZoomIn(self, event: Event):
        self.zoom(-0.1)

    def handleZoomOut(self, event: Event):
        self.zoom(0.1)

    def handleKeyPress(self, event: Event):
        movementSpeed = self.movementSpeed

        if event.keysym == "Right":
            self.window.xMax += movementSpeed
            self.window.xMin += movementSpeed
        if event.keysym == "Left":
            self.window.xMax -= movementSpeed
            self.window.xMin -= movementSpeed
        if event.keysym == "Down":
            self.window.yMax -= movementSpeed
            self.window.yMin -= movementSpeed
        if event.keysym == "Up":
            self.window.yMax += movementSpeed
            self.window.yMin += movementSpeed

        self.repaint()

    def viewportTransform2d(self, coords: tuple[float]):
        (xw, yw) = coords
        window = self.window
        viewport = self.viewport
        xvp = ((xw - window.xMin) / (window.xMax - window.xMin)) * (
            viewport.xMax - viewport.xMin
        )
        yvp = (1 - ((yw - window.yMin) / (window.yMax - window.yMin))) * (
            viewport.yMax - viewport.yMin
        )
        return (xvp, yvp)

    def addObject(self, obj: ScreenObject):
        self.displayFile.append(obj)
        self.objectsVar.set(self.getAllObjectNames())
        self.repaint()

    def repaint(self):
        self.delete("all")
        self.drawAllObjects()
        self.drawText()

    def drawAllObjects(self):
        for obj in self.displayFile:
            self.drawObject(obj)

    def drawText(self):
        self.create_text(
            10,
            10,
            text="Controle com scroll do mouse e setas do teclado",
            fill="white",
            anchor="nw",
        )

        self.create_text(
            950,
            980,
            anchor="se",
            text="Xwmin: "
            + str(round(self.window.xMin, 2))
            + "\n"
            + "Xwmax: "
            + str(round(self.window.xMax, 2))
            + "\n"
            + "Ywmin: "
            + str(round(self.window.yMin, 2))
            + "\n"
            + "Ywmax: "
            + str(round(self.window.yMax, 2)),
            fill="white",
        )

        self.create_text(
            960,
            10,
            anchor="ne",
            fill="white",
            text="Mouse xw: "
            + str(round(self.mouseXw, 2))
            + "\n"
            + "Mouse yw: "
            + str(round(self.mouseYw, 2)),
        )

    def drawObject(self, obj: ScreenObject):
        if obj.type == "point":
            width = 5
            if self.selected_object and self.selected_object.name == obj.name:
                width = 10

            [(xw, yw)] = obj.coords
            (xvp1, yvp1) = self.viewportTransform2d((xw - width, yw - width))
            (xvp2, yvp2) = self.viewportTransform2d((xw + width, yw + width))

            # criar oval para representar um ponto
            self.create_oval(xvp1, yvp1, xvp2, yvp2, fill=obj.color)
        else:
            for index, _el in enumerate(obj.coords):
                if index == 0:
                    pass
                else:
                    (xvp1, yvp1) = self.viewportTransform2d(obj.coords[index - 1])
                    (xvp2, yvp2) = self.viewportTransform2d(obj.coords[index])

                    width = 2
                    if self.selected_object and self.selected_object.name == obj.name:
                        width = 10

                    self.create_line(
                        (xvp1, yvp1, xvp2, yvp2),
                        width=width,
                        fill=obj.color,
                    )

    def zoom(self, percentage: float = 0.1):
        self.window.xMax = self.window.xMax * (1.0 + percentage)
        self.window.yMax = self.window.yMax * (1.0 + percentage)
        self.repaint()

    def getObjectsList(self):
        return self.objectsVar

    def getAllObjectNames(self):
        acc = []
        for obj in self.displayFile:
            acc.append(obj.name + " - " + obj.type)
        return acc

    def transform_selected_object(self, transformation, *args):
        selected_index = self.objectsList.curselection()
        if selected_index:
            obj = self.displayFile[selected_index[0]]
            getattr(obj, transformation)(*args)
            self.repaint()

    def translate_selected(self, tx, ty):
        self.transform_selected_object("translate", tx, ty)

    def scale_selected(self, sx, sy):
        self.transform_selected_object("scale", sx, sy)

    def rotate_selected(self, angle):
        self.transform_selected_object("rotate", angle)
