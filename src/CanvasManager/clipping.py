# File: clipping.py

from vars import COHEN_SUTHERLAND as CS

def compute_outcode(x, y):
    code = CS["INSIDE"]
    if x < CS["WINDOW_MIN_X"]:
        code |= CS["LEFT"]
    elif x > CS["WINDOW_MAX_X"]:
        code |= CS["RIGHT"]
    if y < CS["WINDOW_MIN_Y"]:
        code |= CS["BOTTOM"]
    elif y > CS["WINDOW_MAX_Y"]:
        code |= CS["TOP"]
    return code

def cohen_sutherland_clip(x1, y1, x2, y2):
    outcode1 = compute_outcode(x1, y1)
    outcode2 = compute_outcode(x2, y2)

    # If it's a point (x1 == x2 and y1 == y2), we can simplify the check
    if x1 == x2 and y1 == y2:
        return [(x1, y1)] if outcode1 == CS["INSIDE"] else None

    accept = False

    while True:
        if not (outcode1 | outcode2):  # Both endpoints inside clip window
            accept = True
            break
        elif outcode1 & outcode2:  # Both endpoints outside clip window, in same region
            break
        else:
            # Failed both tests, so calculate line segment to clip
            # from an outside point to an intersection with clip edge
            x, y = 0, 0

            # At least one endpoint is outside the clip rectangle; pick it.
            outcode_out = outcode1 if outcode1 else outcode2

            # Find the intersection point;
            # use formulas y = y1 + slope * (x - x1), x = x1 + (1 / slope) * (y - y1)
            if outcode_out & CS["TOP"]:
                x = x1 + (x2 - x1) * (CS["WINDOW_MAX_Y"] - y1) / (y2 - y1)
                y = CS["WINDOW_MAX_Y"]
            elif outcode_out & CS["BOTTOM"]:
                x = x1 + (x2 - x1) * (CS["WINDOW_MIN_Y"] - y1) / (y2 - y1)
                y = CS["WINDOW_MIN_Y"]
            elif outcode_out & CS["RIGHT"]:
                y = y1 + (y2 - y1) * (CS["WINDOW_MAX_X"] - x1) / (x2 - x1)
                x = CS["WINDOW_MAX_X"]
            elif outcode_out & CS["LEFT"]:
                y = y1 + (y2 - y1) * (CS["WINDOW_MIN_X"] - x1) / (x2 - x1)
                x = CS["WINDOW_MIN_X"]

            # Now move outside point to intersection point to clip
            # and get ready for next pass.
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2)

    if accept:
        return [(x1, y1), (x2, y2)]
    else:
        return None