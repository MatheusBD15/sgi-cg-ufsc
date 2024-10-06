from Math.transformations import rotate_direction_vector, scale
import numpy as np

class Window:
    def __init__(self, xMin, yMin, xMax, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.rotationAngle = 0

        self.center = [(self.xMin + self.xMax) / 2, (self.yMax + self.yMin) / 2]
        self.view_up_vector = np.array([0, 1])

    def set_rotation(self, angle: float):
        self.rotationAngle += angle

    def scale_window(self, percentage):
        magnitude = percentage + 1.0
        [wcx, wcy] = self.center
        [(xMax, yMax), (xMin, yMin)] = scale(
            [(self.xMax, self.yMax), (self.xMin, self.yMin)],
            magnitude,
            magnitude,
            wcx,
            wcy,
        )
        self.xMax = xMax
        self.yMax = yMax
        self.yMin = yMin
        self.xMin = xMin
        self.center = [(self.xMin + self.xMax) / 2, (self.yMax + self.yMin) / 2]

    def move(self, dx, dy):
        self.xMin += dx
        self.xMax += dx
        self.yMin += dy
        self.yMax += dy
        self.center[0] = (self.xMin + self.xMax) / 2
        self.center[1] = (self.yMin + self.yMax) / 2