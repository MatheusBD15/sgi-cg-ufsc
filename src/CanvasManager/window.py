from CanvasManager.transformations import rotate_direction_vector
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
