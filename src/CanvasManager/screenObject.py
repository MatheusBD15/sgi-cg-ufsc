from Math.transformations import normalized_coordinate_transform

class ScreenObject:
    def __init__(
            self, name: str, type: str, coords: list[tuple[float, float]], color: str
    ) -> None:
        self.name = name
        self.type = type
        self.world_coords = coords  # List of (x, y) tuples
        self.normalized_coords = coords
        self.color = color
        self.selected = False

    def apply_transformation(self, transformation_func, *args):
        self.world_coords = transformation_func(self.world_coords, *args)

    def normalize_coords(self, window):
        self.normalized_coords = normalized_coordinate_transform(
            self.world_coords, window
        )