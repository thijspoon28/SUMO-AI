from collections.abc import Callable, Iterable
import datetime
import os
import time
import sys


def move(x: int, y: int, size: os.terminal_size) -> None:
    if x < 1 or y < 2 or x > size.columns or y > size.lines:
        msg = f"Moved out of bounds: x[1:{size.columns}], y[1:{size.lines}]: ({x}, {y})"
        raise Exception(msg)

    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()


class Estimator:
    def __init__(
        self,
        level: int,
        title: str,
        size: os.terminal_size,
        iteratable: Iterable,
        finish_callback: Callable,
        estimator_id: int,
    ):
        self.level = level
        self.title = title
        self.size = size

        self.iteration = 0
        self.iteratable = iteratable
        self.total = len(iteratable)

        self.start_time = time.time()
        self.times = [self.start_time]
        self.avg = 0

        self.finish_callback = finish_callback
        self.estimator_id = estimator_id

    def __repr__(self):
        return f'Estimator("{self.title}", level={self.level})'

    def finish(self) -> None:
        self.finish_callback(self.estimator_id)

    def move(self, x: int, y: int) -> None:
        move(x, y, self.size)

    def clear_line(self):
        sys.stdout.write("\033[K")

    def start(self) -> None:
        spacing = "  " * self.level

        completion = f"0 / {self.total} (  0.0%)"
        line = f"{spacing}> {self.title} - {completion} - total=0.0s - last=Unknown"

        self.move(1, self.level + 2)

        sys.stdout.write(line)
        sys.stdout.flush()

        self.ready_next_line()

    def stats(self) -> None:
        cur = time.time()
        total = cur - self.start_time
        last = cur - self.times[-1]

        self.times.append(cur)

        precent = self.iteration / self.total * 100

        spacing = (2 * self.level) + 2 + len(self.title) + 4
        completion = f"{self.iteration} / {self.total} ({precent:5.1f}%)"

        estimate = self.calculate_estimate(last)

        line = f"{completion} - {total=:.2f}s - {last=:.2f}s - estimate={estimate}"

        self.move(spacing, self.level + 2)
        self.clear_line()

        sys.stdout.write(line)
        sys.stdout.flush()

        self.ready_next_line()

    def ready_next_line(self) -> None:
        self.move(1, self.level + 3)

    def calculate_estimate(self, last: float) -> str:
        times = self.times[-5:]

        if len(times) > 1:
            diffs = (times[i] - times[i - 1] for i in range(1, len(times)))
            avg_diff = sum(diffs) / (len(times) - 1)
        else:
            avg_diff = 0

        linear_estimation = self.start_time + avg_diff * self.total

        self.avg = ((self.avg * (self.iteration - 1)) + last) / self.iteration
        estimated_total = self.total * self.avg
        avg_estimation = self.start_time + estimated_total

        linear_weight = 1
        avg_weight = 1

        weighted_linear = linear_estimation * linear_weight
        weighted_avg = avg_estimation * avg_weight

        total = linear_weight + avg_weight
        estimation = (weighted_linear + weighted_avg) / total

        dt = datetime.datetime.fromtimestamp(estimation)
        return dt.strftime("%H:%M:%S")

    def iterate(self):
        self.start()

        for idx, i in enumerate(self.iteratable):
            self.iteration += 1
            yield i
            self.stats()

        self.finish()


class EstimatorManager:
    def __init__(self):
        self.estimators: dict[int, Estimator] = {}
        self.count = 0
        self.size = os.get_terminal_size()

        self.cleared = False

    def clear(self):
        sys.stdout.write("\n" * (self.size.lines - 2))
        sys.stdout.flush()
        self.move(1, 2)

    def move(self, x: int, y: int) -> None:
        move(x, y, self.size)

    def add(self, estimator_id: int, estimator: Estimator) -> None:
        self.estimators[estimator_id] = estimator

    def remove(self, estimator_id: int) -> None:
        del self.estimators[estimator_id]

    def finish(self, estimator_id: int) -> None:
        self.remove(estimator_id)

        if len(self.estimators) == 0:
            self.move(1, self.size.lines)

    def estimate(self, iteratable: Iterable, title: str = "Loop"):
        self.count += 1

        estimator = Estimator(
            level=len(self.estimators),
            size=self.size,
            title=title,
            iteratable=iteratable,
            finish_callback=self.finish,
            estimator_id=self.count,
        )

        if len(self.estimators) == 0:
            self.clear()

        self.add(self.count, estimator)

        return estimator.iterate()


manager = EstimatorManager()


def estimate(iterable: Iterable, title: str = "Loop"):
    return manager.estimate(iterable, title=title)
