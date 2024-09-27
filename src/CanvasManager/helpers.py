def get_center_of_object(coords: list[tuple[float, float]]):
    xCenter = 0
    yCenter = 0

    for x, y in coords:
        xCenter += x
        yCenter += y

    xCenter = xCenter / len(coords)
    yCenter = yCenter / len(coords)

    return (xCenter, yCenter)
