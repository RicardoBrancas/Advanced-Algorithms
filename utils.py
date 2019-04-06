def crange(start, end, modulo):
    if start >= end:
        while start < modulo:
            yield start
            start += 1
        start = 0

    while start < end:
        yield start
        start += 1
