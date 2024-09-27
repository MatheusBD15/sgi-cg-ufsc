import numpy as np


def translate(coords, tx, ty):
    translation_matrix = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    return apply_transformation(coords, translation_matrix)


def scale(coords, sx, sy, cx, cy):
    translate_to_center = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]])

    scaling_matrix = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

    translate_back = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]])

    resulting_matrix = np.dot(
        translate_back, np.dot(scaling_matrix, translate_to_center)
    )

    # Apply the transformation matrix to the coordinates
    return apply_transformation(coords, resulting_matrix)


def rotate_around_world(coords, angle):
    angle_rad = np.radians(angle)
    rotation_matrix = np.array(
        [
            [np.cos(angle_rad), -np.sin(angle_rad), 0],
            [np.sin(angle_rad), np.cos(angle_rad), 0],
            [0, 0, 1],
        ]
    )
    return apply_transformation(coords, rotation_matrix)


def rotate_around_point(coords, tx, ty, angle):
    angle_rad = np.radians(angle)

    translate_to_center = np.array([[1, 0, -tx], [0, 1, -ty], [0, 0, 1]])

    rotate = np.array(
        [
            [np.cos(angle_rad), -np.sin(angle_rad), 0],
            [np.sin(angle_rad), np.cos(angle_rad), 0],
            [0, 0, 1],
        ]
    )

    translate_back = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    resulting_matrix = np.dot(translate_back, np.dot(rotate, translate_to_center))

    return apply_transformation(coords, resulting_matrix)


def apply_transformation(coords, matrix):
    homogeneous_coords = np.array([list(coord) + [1] for coord in coords])
    transformed_coords = np.dot(homogeneous_coords, matrix.T)
    return [tuple(coord[:2]) for coord in transformed_coords]
