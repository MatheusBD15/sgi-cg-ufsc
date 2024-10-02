from CanvasManager.screenObject import ScreenObject

CANVAS_HEIGHT = 900
CANVAS_WIDTH = 900
VIEWPORT_OFFSET = 50
CANVAS_BORDER = 6

# POINT, LINE OU WIREFRAME
OBJECT_TYPES = ["point", "line", "wireframe"]
STARTING_DISPLAY_FILE = [
    ScreenObject("ponto1", "point", ((500, 900),), "white"),
    ScreenObject("linha1", "line", ((200, 350), (250, 500)), "red"),
    ScreenObject(
        "poligono1", "wireframe", ((50, 50), (200, 200), (40, 800), (50, 50)), "blue"
    ),
]
COLORS = ["white", "red", "blue", "orange", "grey", "cyan", "purple", "pink", "yellow"]
