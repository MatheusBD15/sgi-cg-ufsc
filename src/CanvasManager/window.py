import numpy as np


class Window:
    def __init__(self, xMin, yMin, xMax, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.rotationAngle = 0

        self.center = [(self.xMin + self.xMax) / 2, (self.yMax + self.yMin) / 2]
        self.view_up_vector = [0, 1]
