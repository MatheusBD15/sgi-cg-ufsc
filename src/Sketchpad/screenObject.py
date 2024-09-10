class ScreenObject:
    def __init__(
        self, name: str, type: str, coords: tuple[tuple[float]], color: str
    ) -> None:
        self.type = type
        self.coords = coords
        self.name = name
        self.color = color
