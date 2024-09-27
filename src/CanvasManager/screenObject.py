class ScreenObject:
    def __init__(
        self, name: str, type: str, coords: list[tuple[float, float]], color: str
    ) -> None:
        self.name = name
        self.type = type
        self.coords = coords  # List of (x, y) tuples
        self.color = color
        self.selected = False

    def apply_transformation(self, transformation_func, *args):
        self.coords = transformation_func(self.coords, *args)
