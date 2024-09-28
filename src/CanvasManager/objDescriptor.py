from CanvasManager.screenObject import ScreenObject


def export_as_obj_file(filename: str, objects: list[ScreenObject]):
    with open(filename, "w") as f:
        f.write("# Wavefront .obj file\n")

        vertex_offset = 0
        for obj in objects:
            f.write(f"\no {obj.name}\n")
            for coord in obj.world_coords:
                f.write(f"v {coord[0]} {coord[1]} 0\n")
            vertex_offset += len(obj.world_coords)

            num_vertices = len(obj.world_coords)
            for i in range(0, num_vertices - 2):
                f.write(
                    f"f {vertex_offset - num_vertices + 1 + i} {vertex_offset - num_vertices + 1 + i + 1} {vertex_offset - num_vertices + 1 + i + 2}\n"
                )

    print(f"Successfully converted {len(objects)} objects to {filename}")
