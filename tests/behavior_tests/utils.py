def value_within_range(expected: float, actual: float, delta: float):
    return (actual >= expected - delta) and (actual <= expected + delta)