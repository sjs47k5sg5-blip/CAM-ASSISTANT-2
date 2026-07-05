import math

EPS = 1e-9


def length(v):
    return math.hypot(v[0], v[1])


def normalize(v):
    l = length(v)

    if l < EPS:
        return (0.0, 0.0)

    return (
        v[0] / l,
        v[1] / l,
    )


def add(a, b):
    return (
        a[0] + b[0],
        a[1] + b[1],
    )


def sub(a, b):
    return (
        a[0] - b[0],
        a[1] - b[1],
    )


def mul(v, k):
    return (
        v[0] * k,
        v[1] * k,
    )


def distance(a, b):
    return length(sub(a, b))


def left_normal(v):
    return (
        -v[1],
        v[0],
    )


def right_normal(v):
    return (
        v[1],
        -v[0],
    )


def dot(a, b):
    return (
        a[0] * b[0] +
        a[1] * b[1]
    )


def cross(a, b):
    return (
        a[0] * b[1] -
        a[1] * b[0]
    )