from tkinter import *
from tkinter import ttk


CANVAS_HEIGHT = 1000
CANVAS_WIDTH = 1000


class ScreenObject:
    def __init__(self, type: str, coords: tuple[tuple[float]]) -> None:
        self.type = type
        self.coords = coords


# POINT, LINE OU WIREFRAME
DISPLAY_FILE = [
    ScreenObject("point", ((500, 900))),
    ScreenObject("line", ((200, 350), (250, 500))),
    ScreenObject("wireframe", ((50, 50), (200, 200), (40, 800), (50, 50))),
]


class Window:
    def __init__(self, xMin, yMin, xMax, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax


class Viewport:
    def __init__(self, xMin, yMin, xMax, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax


class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.movementSpeed = 50
        self.bind_all("<Button-4>", self.handleZoomIn)
        self.bind_all("<Button-5>", self.handleZoomOut)
        self.bind_all("<KeyPress>", self.handleKeyPress)

        ## Representa o canvas em si
        self.viewport = Viewport(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)

        # Representa um recorte do mundo
        self.window = Window(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
        self.displayFile = DISPLAY_FILE

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

    def drawAllObjects(self):
        self.delete("all")

        for obj in self.displayFile:
            self.drawObject(obj)

    def drawObject(self, obj: ScreenObject):
        if obj.type == "point":
            (xvp, yvp) = self.viewportTransform2d(obj.coords)

            # criar oval para representar um ponto
            self.create_oval(xvp, yvp, xvp + 10, yvp + 10, fill="white")
        else:
            print(obj.coords)
            for index, _el in enumerate(obj.coords):
                if index == 0:
                    pass
                else:
                    # print(_el)
                    (xvp1, yvp1) = self.viewportTransform2d(obj.coords[index - 1])
                    (xvp2, yvp2) = self.viewportTransform2d(obj.coords[index])

                    self.create_line(
                        (xvp1, yvp1, xvp2, yvp2),
                        width=2,
                        fill="white",
                    )

    def zoom(self, percentage: float = 0.1):
        self.window.xMax = self.window.xMax * (1.0 + percentage)
        self.window.yMax = self.window.yMax * (1.0 + percentage)
        self.drawAllObjects()


def main():

    root = Tk()
    # root.minsize(width=1920, height=1080)
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

    menu = ttk.LabelFrame(mainframe, text="Menu", width=400, padding="20")
    menu.grid(column=0, row=0, sticky=(N, W, S), rowspan=3)

    menu.columnconfigure(0, weight=1)
    menu.columnconfigure(1, weight=1)
    menu.columnconfigure(2, weight=1)
    menu.rowconfigure(0, weight=0, pad=20)
    menu.rowconfigure(1, weight=1)

    objectsListTitle = ttk.Label(menu, text="Objetos")
    objectsListTitle.grid(column=0, row=0, sticky=(N, W))

    addNewObjBtn = ttk.Button(menu, text="+", width=5)
    addNewObjBtn.grid(column=2, row=0, sticky=(N, E))

    objects = StringVar(value=["item 1", "item 2"])
    objectsList = Listbox(menu, listvariable=objects)
    objectsList.grid(column=0, row=1, sticky=(N, W, E))

    scrollBar = ttk.Scrollbar(menu, orient=VERTICAL, command=objectsList.yview)
    objectsList["yscrollcommand"] = scrollBar.set
    scrollBar.grid(column=1, row=1, sticky=(N, W, E))

    sketch = Sketchpad(
        mainframe, background="black", height=CANVAS_HEIGHT, width=CANVAS_WIDTH
    )
    sketch.grid(column=2, row=1)
    sketch.focus()

    root.mainloop()


main()
