import numpy as np


def get_center_of_object(coords: list[tuple[float, float]]):
    xCenter = 0
    yCenter = 0

    for x, y in coords:
        xCenter += x
        yCenter += y

    xCenter = xCenter / len(coords)
    yCenter = yCenter / len(coords)

    return (xCenter, yCenter)


def calculate_angle(v1: list[float], v2: list[float]) -> float:
    vector_2 = np.array(v2)

    # Converte VUP para numpy array
    vector_1 = np.array(v1)

    # Produto escalar entre VUP e o eixo Y
    dot_product = np.dot(vector_1, vector_2)

    # Magnitudes (normas) de VUP e do eixo Y
    magnitude_vup = np.linalg.norm(vector_1)
    magnitude_y = np.linalg.norm(vector_2)

    # Cálculo do coseno do ângulo
    cos_theta = dot_product / (magnitude_vup * magnitude_y)

    # Cálculo do ângulo usando arccos (em radianos)
    theta = np.arccos(cos_theta)

    return theta
