from CanvasManager.screenObject import ScreenObject

class objDescriptor:
    def export_as_obj_file(self, filename: str, objects: list[ScreenObject]):
        with open(filename, "w") as f:
            f.write("# Wavefront .obj file\n")

            vertex_offset = 1
            for obj in objects:
                obj_string = obj.obj_string()
                f.write(obj_string)

                # Update vertex offset for the next object
                vertex_offset += len(obj.world_coords)

        print(f"Successfully exported {len(objects)} objects to {filename}")
