def value_within_range(expected: float, actual: float, delta: float):
    margin = delta * expected

    return (actual >= expected - margin) and (actual <= expected + margin)