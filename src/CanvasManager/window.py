import numpy as np

class Window:
    def __init__(self, xMin, yMin, xMax, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.center = [(self.xMin + self.xMax) / 2, (self.yMin + self.yMax) / 2]
        self.world_rotation_angle = 0  # This is the rotation of the world, not the window
        self.view_up_vector = np.array([0, 1])

    def set_world_rotation(self, angle: float):
        self.world_rotation_angle += angle

    def move(self, dx, dy):
        self.xMin += dx
        self.xMax += dx
        self.yMin += dy
        self.yMax += dy
        self.center[0] = (self.xMin + self.xMax) / 2
        self.center[1] = (self.yMin + self.yMax) / 2

    def scale_window(self, percentage):
        magnitude = percentage + 1.0
        [wcx, wcy] = self.center
        new_width = (self.xMax - self.xMin) * magnitude
        new_height = (self.yMax - self.yMin) * magnitude

        self.xMin = wcx - new_width / 2
        self.xMax = wcx + new_width / 2
        self.yMin = wcy - new_height / 2
        self.yMax = wcy + new_height / 2
        self.center = [(self.xMin + self.xMax) / 2, (self.yMin + self.yMax) / 2]

    def move(self, dx, dy):
        self.xMin += dx
        self.xMax += dx
        self.yMin += dy
        self.yMax += dy
        self.center[0] = (self.xMin + self.xMax) / 2
        self.center[1] = (self.yMin + self.yMax) / 2