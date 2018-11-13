import numpy

def transform(inline, tangent, angle):
    return inline * numpy.cos(angle) + tangent * numpy.sin(angle),

def transform_acceleration(acceleration, heading):
    """
    Transforms an acceleration from train coordinates to world coordinates
    heading - angle from north
    """

    return numpy.array([
        transform(acceleration[0], acceleration[1], heading),
        transform(acceleration[1], acceleration[0], heading),
    ])