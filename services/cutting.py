import math


def spindle_speed(vc: float, diameter: float) -> int:
    return round((1000 * vc) / (math.pi * diameter))


def feed_rate(rpm: int, teeth: int, fz: float) -> int:
    return round(rpm * teeth * fz)