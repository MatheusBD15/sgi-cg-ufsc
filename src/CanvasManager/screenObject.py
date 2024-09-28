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

    def obj_string(self):
        obj_str = f"o {self.name}\n"
        for x, y in self.world_coords:
            obj_str += f"v {x} {y} 0\n"

        if self.type in ["line", "polygon"]:
            num_vertices = len(self.world_coords)
            for i in range(num_vertices):
                next_i = (i + 1) % num_vertices
                obj_str += f"l {i+1} {next_i+1}\n"

        return obj_str