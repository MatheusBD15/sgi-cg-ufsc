from CanvasManager.screenObject import ScreenObject
import os

def export_as_obj_file(filename: str, objects: list[ScreenObject]):
    with open(filename, "w") as f:
        # Write all vertices first
        vertex_count = 1
        vertex_map = {}  # To map object vertices to global vertex indices
        colors = set()  # To keep track of all colors used
        for obj in objects:
            for coord in obj.world_coords:
                f.write(f"v {coord[0]:.1f} {coord[1]:.1f} 0.0\n")
                vertex_map[obj.name] = vertex_map.get(obj.name, []) + [vertex_count]
                vertex_count += 1
            colors.add(obj.color)

        # Write material library reference
        mtl_filename = os.path.splitext(filename)[0] + ".mtl"
        f.write(f"mtllib {os.path.basename(mtl_filename)}\n\n")

        # Write objects and their geometries
        for obj in objects:
            f.write(f"# defining a {obj.color} {obj.type}\n")
            f.write(f"o {obj.name}\n")
            f.write(f"usemtl {obj.color}\n")

            vertices = vertex_map[obj.name]
            if obj.type == "point":
                f.write(f"p {vertices[0]}\n")
            elif obj.type == "line":
                f.write(f"l {' '.join(map(str, vertices))}\n")
            elif obj.type == "wireframe":
                f.write(f"f {' '.join(map(str, vertices))}\n")

            f.write("\n")  # Add a blank line between objects for readability

    # Generate the MTL file
    generate_mtl_file(mtl_filename, colors)

    print(f"Successfully exported {len(objects)} objects to {filename}")
    print(f"Successfully generated MTL file: {mtl_filename}")

def generate_mtl_file(filename: str, colors: set):
    color_values = {
        "white": (1.00, 1.00, 1.00),
        "red": (1.00, 0.00, 0.00),
        "blue": (0.00, 0.00, 1.00),
        "orange": (1.00, 0.65, 0.00),
        "grey": (0.50, 0.50, 0.50),
        "cyan": (0.00, 1.00, 1.00),
        "purple": (0.50, 0.00, 0.50),
        "pink": (1.00, 0.75, 0.80),
        "yellow": (1.00, 1.00, 0.00)
    }

    with open(filename, "w") as f:
        f.write("# Material definitions for OBJ file\n\n")

        for color in colors:
            f.write(f"newmtl {color}\n")
            if color in color_values:
                r, g, b = color_values[color]
                f.write(f"Kd {r:.6f} {g:.6f} {b:.6f}\n")  # Diffuse color
                # f.write(f"Ka {r:.6f} {g:.6f} {b:.6f}\n")  # Ambient color (same as diffuse)
                # f.write("Ks 0.500000 0.500000 0.500000\n")  # Specular color (grey)
                # f.write("Ns 96.078431\n")  # Specular exponent
                # f.write("d 1.000000\n")  # Dissolve (opacity)
                # f.write("illum 2\n")  # Illumination model
            else:
                # Default to grey if color is unknown
                f.write("Kd 0.500000 0.500000 0.500000\n")
                # f.write("Ka 0.500000 0.500000 0.500000\n")
                # f.write("Ks 0.500000 0.500000 0.500000\n")
                # f.write("Ns 96.078431\n")
                # f.write("d 1.000000\n")
                # f.write("illum 2\n")
            f.write("\n")

    print(f"Successfully generated MTL file: {filename}")

def import_obj_file(filename: str) -> list[ScreenObject]:
    objects = []
    vertices = []
    current_object = None
    current_material = None

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == 'v':
                vertices.append((float(parts[1]), float(parts[2])))
            elif parts[0] == 'o':
                if current_object:
                    objects.append(current_object)
                current_object = {'name': parts[1], 'type': None, 'coords': [], 'color': 'white'}
            elif parts[0] == 'usemtl':
                current_material = parts[1]
                if current_object:
                    current_object['color'] = current_material
            elif parts[0] in ['p', 'l', 'f']:
                if current_object:
                    if parts[0] == 'p':
                        current_object['type'] = 'point'
                    elif parts[0] == 'l':
                        current_object['type'] = 'line'
                    else:
                        current_object['type'] = 'wireframe'

                    for index in parts[1:]:
                        current_object['coords'].append(vertices[int(index) - 1])

    if current_object:
        objects.append(current_object)

    return [ScreenObject(obj['name'], obj['type'], obj['coords'], obj['color']) for obj in objects]