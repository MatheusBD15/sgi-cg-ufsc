class ScreenObject:
    def __init__(self, name: str, type: str, coords: tuple[tuple[float]]) -> None:
        self.type = type
        self.coords = coords
        self.name = name
