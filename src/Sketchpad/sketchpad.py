from tkinter import *
from tkinter import ttk
from vars import *
from Sketchpad.viewport import Viewport
from Sketchpad.window import Window


class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.movementSpeed = 50
        self.bind("<Button-4>", self.handleZoomIn)
        self.bind("<Button-5>", self.handleZoomOut)
        self.bind_all("<KeyPress>", self.handleKeyPress)

        ## Representa o canvas em si
        self.viewport = Viewport(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)

        # Representa um recorte do mundo
        self.window = Window(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
        self.displayFile = STARTING_DISPLAY_FILE
        self.objectsVar = StringVar(value=self.getAllObjectNames())

        self.drawAllObjects()

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

        self.drawAllObjects()

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
        self.drawAllObjects()

    def drawAllObjects(self):
        self.delete("all")

        for obj in self.displayFile:
            self.drawObject(obj)

    def drawObject(self, obj: ScreenObject):
        if obj.type == "point":
            (xw, yw) = obj.coords
            (xvp1, yvp1) = self.viewportTransform2d(obj.coords)
            (xvp2, yvp2) = self.viewportTransform2d((xw + 10, yw + 10))

            # criar oval para representar um ponto
            self.create_oval(xvp1, yvp1, xvp2, yvp2, fill=obj.color)
        else:
            for index, _el in enumerate(obj.coords):
                if index == 0:
                    pass
                else:
                    (xvp1, yvp1) = self.viewportTransform2d(obj.coords[index - 1])
                    (xvp2, yvp2) = self.viewportTransform2d(obj.coords[index])

                    self.create_line(
                        (xvp1, yvp1, xvp2, yvp2),
                        width=2,
                        fill=obj.color,
                    )

    def zoom(self, percentage: float = 0.1):
        self.window.xMax = self.window.xMax * (1.0 + percentage)
        self.window.yMax = self.window.yMax * (1.0 + percentage)
        self.drawAllObjects()

    def getObjectsList(self):
        return self.objectsVar

    def getAllObjectNames(self):
        acc = []
        for obj in self.displayFile:
            acc.append(obj.name + " - " + obj.type)
        return acc
