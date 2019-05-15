def crange(start, end, modulo):
    """
    Similar to a normal Python range() but can start at any arbitrary
    point and then wrap around.
    """

    if start >= end:
        while start < modulo:
            yield start
            start += 1
        start = 0

    while start < end:
        yield start
        start += 1
