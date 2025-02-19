from collections.abc import Callable, Generator, Iterable
import datetime
import os
import time
import sys
from typing import TypeVar


def move(
    sys_stdout_write: Callable,
    sys_stdout_flush: Callable,
    x: int,
    y: int,
    size: os.terminal_size,
) -> None:
    if x < 1 or y < 2 or x > size.columns or y > size.lines:
        msg = f"Moved out of bounds: x[1:{size.columns}], y[2:{size.lines}]: ({x}, {y})"
        raise Exception(msg)

    sys_stdout_write(f"\033[{y};{x}H")
    sys_stdout_flush()


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
        disable_terminal_chomp_chomp: bool
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
        if self.disable_terminal_chomp_chomp:
            return 
        
        move(self.sys_stdout_write, self.sys_stdout_flush, x, y, self.size)
        
    def clear_line(self):
        if self.disable_terminal_chomp_chomp:
            return 
        
        self.sys_stdout_write("\033[K")

    def start(self) -> None:
        spacing = "  " * self.level

        completion = f"0 / {self.total} (  0.0%)"
        line = f"{spacing}> {self.title} - {completion} - total=0.0s - last=Unknown - estimate=Unknown"

        if self.disable_terminal_chomp_chomp:
            print(line)
            return
        
        self.move(1, self.level + 2)

        self.sys_stdout_write(line)
        self.sys_stdout_flush()

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

        if self.disable_terminal_chomp_chomp:
            print(line)
            return

        self.move(spacing, self.level + 2)
        self.clear_line()

        self.sys_stdout_write(line)
        self.sys_stdout_flush()

        self.ready_next_line()

    def ready_next_line(self) -> None:
        if self.disable_terminal_chomp_chomp:
            return 
        
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
            self.update_callback()

        self.finish()


class EstimatorManager:
    def __init__(self):
        self.estimators: dict[int, Estimator] = {}  # type: ignore
        self.count = 0
        self.size = os.get_terminal_size()

        self.cleared = False
        self.sys_stdout_write = None
        self.sys_stdout_flush = None

        self.log: list[str] = [""]  # type: ignore

        self.disable_terminal_chomp_chomp_value = False
        
    def push_log(self, string: str | None = None, end: bool = False):
        def split_string(s: str, length: int):
            if len(s) == 0:
                return [""]
            return [s[i : i + length] for i in range(0, len(s), length)]

        if end:
            if not self.log[-1]:
                return

            self.log.append("")
            return

        if not isinstance(string, str):
            raise ValueError("Only provide string input")

        padding = 2

        temp = self.log[-1] + string
        temps = split_string(temp, self.size.columns - padding)

        self.log[-1] = temps[0]

        for t in temps[1:]:
            self.log.append(t)

        if len(self.log) - 1000 > 0:
            for i in range(0, len(self.log) - 1000):
                self.log.pop(i)

    def print_log(self) -> None:
        self.size = os.get_terminal_size()

        levels = len(self.estimators)
        amount = self.size.lines - levels - 2
        logs = self.log[-amount:]

        if len(self.log) > amount:
            logs.insert(0, "...")

        logs = ["  " + log for log in logs]

        if len(logs) > 1:
            logs[-2] = "> " + logs[-2][2:]

        self.clear_mini_terminal()
        self.move(1, self.size.lines - len(logs) + 1)

        string = "\n".join(logs)

        self.sys_stdout_write(string)
        self.sys_stdout_flush()

    def clear_mini_terminal(self) -> None:
        levels = len(self.estimators)
        for i in range(self.size.lines - levels - 1):
            self.move(1, levels + 2 + i)
            self.sys_stdout_write("\033[K")

    def custom_write(self, string: str) -> None:
        if string == "\n":
            self.push_log(end=True)
            return

        strings = string.split("\n")
        for s in strings:
            self.push_log(s)

    def custom_flush(self) -> None:
        self.push_log(end=True)
        self.print_log()

    def clear(self):
        self.sys_stdout_write("\n" * (self.size.lines - 2))
        self.sys_stdout_flush()
        self.move(1, 2)

    def move(self, x: int, y: int) -> None:
        if self.disable_terminal_chomp_chomp_value:
            return
        
        move(self.sys_stdout_write, self.sys_stdout_flush, x, y, self.size)

    def add(self, estimator_id: int, estimator: Estimator) -> None:
        self.estimators[estimator_id] = estimator

    def remove(self, estimator_id: int) -> None:
        del self.estimators[estimator_id]

    def initiate(self) -> None:
        if self.disable_terminal_chomp_chomp_value:
            return
        
        self.sys_stdout_write = sys.stdout.write
        self.sys_stdout_flush = sys.stdout.flush
        sys.stdout.write = self.custom_write  # type: ignore
        sys.stdout.flush = self.custom_flush  # type: ignore
        self.clear()

    def conclude(self) -> None:
        if self.disable_terminal_chomp_chomp_value:
            return
        
        self.move(1, self.size.lines)

        sys.stdout.write = self.sys_stdout_write  # type: ignore
        sys.stdout.flush = self.sys_stdout_flush  # type: ignore
        self.sys_stdout_write = None
        self.sys_stdout_flush = None

    def finish(self, estimator_id: int) -> None:
        self.remove(estimator_id)

        if len(self.estimators) == 0:
            self.conclude()

    def update(self) -> None:
        if self.disable_terminal_chomp_chomp_value:
            return
        
        self.print_log()

    def disable_terminal_chomp_chomp(self, value: bool) -> None:
        if self.disable_terminal_chomp_chomp_value == value:
            return

        self.disable_terminal_chomp_chomp_value = value

        if value is True:
            if self.sys_stdout_write is None:
                return
            self.move(1, self.size.lines)
            sys.stdout.write = self.sys_stdout_write  # type: ignore
            sys.stdout.flush = self.sys_stdout_flush  # type: ignore
            self.sys_stdout_write = None
            self.sys_stdout_flush = None

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
    ):
        self.count += 1

        if disable_terminal_chomp_chomp is not None:
            self.disable_terminal_chomp_chomp(disable_terminal_chomp_chomp)

        if len(self.estimators) == 0:
            self.initiate()
        
        estimator = Estimator(
            level=len(self.estimators),
            size=self.size,
            title=title,
            iteratable=iteratable,
            finish_callback=self.finish,
            estimator_id=self.count,
            sys_stdout_write=self.sys_stdout_write,
            sys_stdout_flush=self.sys_stdout_flush,
            update_callback=self.update,
            disable_terminal_chomp_chomp=self.disable_terminal_chomp_chomp_value,
        )

        self.add(self.count, estimator)

        # try:
        return estimator.iterate()
        # except Exception as exc:
            # self.disable_terminal_chomp_chomp(True)
            # raise Exception("OOO") from exc


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
