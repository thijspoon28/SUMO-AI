import time


class Estimator:
    def __init__(self):
        pass

    def iterate(self, iterable):
        start = time.time()
        prev = time.time()
        cycles = -1
        avg = 0
        maximum = len(iterable)

        x = 0

        print(f"{prefix} Started iterating - {maximum} items")

        for i in iterable:
            yield i
            
            cycles += 1

            cur = time.time()
            spent = cur-prev
            prev = cur

            avg = ((avg * (cycles-1)) + spent) / cycles if cycles > 0 else 0

            estimate = f"{(maximum) * avg:.2f}s"

            print(f"{prefix} Cycle {cycles}: elapsed={spent:.2f}s, total={cur-start:.2f}s, estimate={estimate}")

            x += 1

estimator = Estimator()


def estimate_iterable(iterable, interval: int = 1, prefix: str = ">"):
    start = time.time()
    prev = time.time()
    cycles = -1
    avg = 0
    maximum = len(iterable)

    x = 0

    print(f"{prefix} Started iterating - {maximum} items")

    for i in iterable:
        yield i
        
        cycles += 1

        cur = time.time()
        spent = cur-prev
        prev = cur

        avg = ((avg * (cycles-1)) + spent) / cycles if cycles > 0 else 0

        estimate = f"{(maximum) * avg:.2f}s"

        if x % interval == 0:
            x = 0
            print(f"{prefix} Cycle {cycles}: elapsed={spent:.2f}s, total={cur-start:.2f}s, estimate={estimate}")

        x += 1
