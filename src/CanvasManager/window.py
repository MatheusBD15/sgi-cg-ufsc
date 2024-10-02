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
        self.rotationAngle = angle
        self.view_up_vector = rotate_direction_vector(self.view_up_vector, angle)

    def scale_window(self, percentage):
        magnitude = percentage + 1.0
        [xCenter, yCenter] = self.center
        [(xMax, yMax), (xMin, yMin)] = scale(
            [(self.xMax, self.yMax), (self.xMin, self.yMin)],
            magnitude,
            magnitude,
            xCenter,
            yCenter,
        )
        self.xMax = xMax
        self.yMax = yMax
        self.yMin = yMin
        self.xMin = xMin

        self.center = [(self.xMin + self.xMax) / 2, (self.yMax + self.yMin) / 2]
