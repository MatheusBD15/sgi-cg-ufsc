from CanvasManager.screenObject import ScreenObject


def should_draw_point(point: ScreenObject):
    [(x, y)] = point.normalized_coords
    if x >= -1 and x <= 1 and y >= -1 and y <= 1:
        return True
    return False
