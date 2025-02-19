import time
import os
import sys
import datetime
from collections.abc import Iterable, Callable
from typing import TypeVar, Generator


def move(
    write: Callable,
    flush: Callable,
    x: int,
    y: int,
    size: os.terminal_size,
) -> None:
    if not (1 <= x <= size.columns) or not (2 <= y <= size.lines):
        msg = f"Moved out of bounds: x[1:{size.columns}], y[2:{size.lines}]: ({x}, {y})"
        raise ValueError(msg)

    write(f"\033[{y};{x}H")
    flush()


class Estimator:
    def __init__(
        self,
        level: int,
        title: str,
        size: os.terminal_size,
        iteratable: Iterable,
        finish_callback: Callable,
        estimator_id: int,
        sys_stdout_write: Callable,
        sys_stdout_flush: Callable,
        update_callback: Callable,
        disable_terminal_chomp_chomp: bool,
    ):
        self.level = level
        self.title = title
        self.size = size
        self.iteration = 0
        self.iteratable = iteratable
        self.total = len(iteratable)  # type: ignore
        self.start_time = time.time()
        self.times = [self.start_time]
        self.avg = 0.0

        self.finish_callback = finish_callback
        self.estimator_id = estimator_id
        self.sys_stdout_write = sys_stdout_write
        self.sys_stdout_flush = sys_stdout_flush
        self.update_callback = update_callback
        self.disable_terminal_chomp_chomp = disable_terminal_chomp_chomp

    def __repr__(self):
        return f'Estimator("{self.title}", level={self.level})'

    def finish(self) -> None:
        self.finish_callback(self.estimator_id)

    def move(self, x: int, y: int) -> None:
        if not self.disable_terminal_chomp_chomp:
            move(self.sys_stdout_write, self.sys_stdout_flush, x, y, self.size)

    def clear_line(self):
        if not self.disable_terminal_chomp_chomp:
            self.sys_stdout_write("\033[K")

    def start(self) -> None:
        spacing = "  " * self.level
        completion = f"0 / {self.total} (  0.0%)"
        line = f"{spacing}> {self.title} - {completion} - total=0.0s - last=Unknown - estimate=Unknown"

        if not self.disable_terminal_chomp_chomp:
            self.move(1, self.level + 2)
            self.sys_stdout_write(line)
            self.sys_stdout_flush()
            self.ready_next_line()

        else:
            print(line)

    def stats(self) -> None:
        cur = time.time()
        total = cur - self.start_time
        last = cur - self.times[-1]

        self.times.append(cur)
        percent = self.iteration / self.total * 100

        spacing = (2 * self.level) + 2 + len(self.title) + 4
        completion = f"{self.iteration} / {self.total} ({percent:5.1f}%)"

        estimate = self.calculate_estimate(last)
        line = f"{completion} - {total=:.2f}s - {last=:.2f}s - estimate={estimate}"

        if not self.disable_terminal_chomp_chomp:
            self.move(spacing, self.level + 2)
            self.clear_line()
            self.sys_stdout_write(line)
            self.sys_stdout_flush()
            self.ready_next_line()

        else:
            print(f"{' ' * (2 * self.level)}> {self.title} - {line}")

    def ready_next_line(self) -> None:
        if not self.disable_terminal_chomp_chomp:
            self.move(1, self.level + 3)

    def calculate_estimate(self, last: float) -> str:
        times = self.times[-5:]
        avg_diff = (
            sum(times[i] - times[i - 1] for i in range(1, len(times)))
            / (len(times) - 1)
            if len(times) > 1
            else 0
        )
        linear_estimation = self.start_time + avg_diff * self.total
        self.avg = ((self.avg * (self.iteration - 1)) + last) / self.iteration
        avg_estimation = self.start_time + self.total * self.avg

        estimate = (linear_estimation + avg_estimation) / 2
        dt = datetime.datetime.fromtimestamp(estimate)

        return dt.strftime("%H:%M:%S")

    def iterate(self) -> Generator:
        self.start()

        for _ in self.iteratable:
            self.iteration += 1
            yield _
            self.stats()
            self.update_callback()

        self.finish()


# EstimatorManager class
class EstimatorManager:
    def __init__(self):
        self.estimators: dict[int, Estimator] = {}  # type: ignore
        self.count = 0
        self.size = os.get_terminal_size()
        self.sys_stdout_write = None
        self.sys_stdout_flush = None
        self.log: list[str] = [""]  # type: ignore
        self.disable_terminal_chomp_chomp_value = False

    def push_log(self, string: str | None = None, end: bool = False):
        if end and self.log[-1]:
            self.log.append("")

        elif string:
            temp = self.log[-1] + string
            self.log[-1] = temp[: self.size.columns - 2]
            self.log.extend(
                temp[i : i + self.size.columns - 2]
                for i in range(self.size.columns - 2, len(temp), self.size.columns - 2)
            )

    def print_log(self) -> None:
        logs = self.log[-(self.size.lines - len(self.estimators) - 2) :]

        if len(self.log) > len(logs):
            logs.insert(0, "...")

        logs = ["  " + log for log in logs]

        if len(logs) > 1:
            logs[-2] = "> " + logs[-2][2:]

        self.clear_mini_terminal()
        self.move(1, self.size.lines - len(logs) + 1)

        self.sys_stdout_write("\n".join(logs))
        self.sys_stdout_flush()

    def clear_mini_terminal(self) -> None:
        for i in range(self.size.lines - len(self.estimators) - 1):
            self.move(1, len(self.estimators) + 2 + i)
            self.sys_stdout_write("\033[K")

    def custom_write(self, string: str) -> None:
        if string == "\n":
            self.push_log(end=True)

        else:
            for s in string.split("\n"):
                self.push_log(s)

    def custom_flush(self) -> None:
        self.push_log(end=True)
        self.print_log()

    def clear(self):
        self.sys_stdout_write("\n" * (self.size.lines - 2))
        self.sys_stdout_flush()
        self.move(1, 2)

    def move(self, x: int, y: int) -> None:
        if not self.disable_terminal_chomp_chomp_value:
            move(self.sys_stdout_write, self.sys_stdout_flush, x, y, self.size)

    def add(self, estimator_id: int, estimator: Estimator) -> None:
        self.estimators[estimator_id] = estimator

    def remove(self, estimator_id: int) -> None:
        del self.estimators[estimator_id]

    def initiate(self) -> None:
        if not self.disable_terminal_chomp_chomp_value:
            self.sys_stdout_write = sys.stdout.write
            self.sys_stdout_flush = sys.stdout.flush
            sys.stdout.write = self.custom_write  # type: ignore
            sys.stdout.flush = self.custom_flush  # type: ignore
            self.clear()

    def conclude(self) -> None:
        if not self.disable_terminal_chomp_chomp_value:
            self.move(1, self.size.lines)
            sys.stdout.write = self.sys_stdout_write  # type: ignore
            sys.stdout.flush = self.sys_stdout_flush  # type: ignore

    def finish(self, estimator_id: int) -> None:
        self.remove(estimator_id)
        if not self.estimators:
            self.conclude()

    def update(self) -> None:
        if not self.disable_terminal_chomp_chomp_value:
            self.print_log()

    def disable_terminal_chomp_chomp(self, value: bool) -> None:
        if self.disable_terminal_chomp_chomp_value == value:
            return

        self.disable_terminal_chomp_chomp_value = value

        if value:
            if self.sys_stdout_write is None:
                return
            self.move(1, self.size.lines)
            sys.stdout.write = self.sys_stdout_write  # type: ignore
            sys.stdout.flush = self.sys_stdout_flush  # type: ignore
        else:
            if self.sys_stdout_write is not None:
                return
            self.sys_stdout_write = sys.stdout.write
            self.sys_stdout_flush = sys.stdout.flush
            sys.stdout.write = self.custom_write  # type: ignore
            sys.stdout.flush = self.custom_flush  # type: ignore

        for estimator in self.estimators.values():
            estimator.disable_terminal_chomp_chomp = value

    def estimate(
        self,
        iteratable: Iterable,
        title: str = "Loop",
        disable_terminal_chomp_chomp: bool | None = False,
    ) -> Generator:
        self.count += 1

        if disable_terminal_chomp_chomp is not None:
            self.disable_terminal_chomp_chomp(disable_terminal_chomp_chomp)

        if not self.estimators:
            self.initiate()

        estimator = Estimator(
            level=len(self.estimators),
            title=title,
            size=self.size,
            iteratable=iteratable,
            finish_callback=self.finish,
            estimator_id=self.count,
            sys_stdout_write=self.sys_stdout_write,
            sys_stdout_flush=self.sys_stdout_flush,
            update_callback=self.update,
            disable_terminal_chomp_chomp=self.disable_terminal_chomp_chomp_value,
        )

        self.add(self.count, estimator)
        return estimator.iterate()


# Global EstimatorManager instance
manager = EstimatorManager()


T = TypeVar("T")


def estimate(
    iterable: Iterable[T],
    title: str = "Loop",
    disable_terminal_chomp_chomp: bool | None = None,
) -> Generator[T, None, None]:
    return manager.estimate(
        iterable,
        title=title,
        disable_terminal_chomp_chomp=disable_terminal_chomp_chomp,
    )
