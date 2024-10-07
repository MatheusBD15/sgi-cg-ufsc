from CanvasManager.screenObject import ScreenObject

CANVAS_HEIGHT = 900
CANVAS_WIDTH = 900
VIEWPORT_OFFSET = 100
CANVAS_BORDER = 6

# POINT, LINE OU WIREFRAME
OBJECT_TYPES = ["point", "line", "wireframe"]

STARTING_DISPLAY_FILE = [
    # Red point at the center
    ScreenObject("center_point", "point", [(450, 450)], "red"),

    # Diagonal lines
    ScreenObject("diagonal_line1", "line", [(100, 100), (800, 800)], "white"),
    ScreenObject("diagonal_line2", "line", [(800, 100), (100, 800)], "white"),

    # Small polygon (triangle)
    ScreenObject("small_polygon", "wireframe", [(400, 400), (500, 400), (450, 300), (400, 400)], "green"),

    # Medium polygon (square)
    ScreenObject("medium_polygon", "wireframe", [(250, 250), (650, 250), (650, 650), (250, 650), (250, 250)], "blue"),

    # Large polygon (pentagon) - only one edge visible in the initial window
    ScreenObject("large_polygon", "wireframe", [
        (450, -400),   # Top point (outside the window)
        (-400, 200),   # Upper left (outside the window)
        (0, 1300),     # Lower left (far outside the window)
        (900, 1300),   # Lower right (far outside the window)
        (1300, 200),   # Upper right (outside the window)
        (450, -400)    # Back to top point to close the shape
    ], "yellow"),
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