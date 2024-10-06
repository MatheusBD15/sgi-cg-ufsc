from CanvasManager.screenObject import ScreenObject

CANVAS_HEIGHT = 900
CANVAS_WIDTH = 900
VIEWPORT_OFFSET = 100
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

# Cohen-Sutherland clipping constants
COHEN_SUTHERLAND = {
    "INSIDE": 0,  # 0000
    "LEFT": 1,    # 0001
    "RIGHT": 2,   # 0010
    "BOTTOM": 4,  # 0100
    "TOP": 8,     # 1000
    "WINDOW_MIN_X": -1,
    "WINDOW_MIN_Y": -1,
    "WINDOW_MAX_X": 1,
    "WINDOW_MAX_Y": 1
}