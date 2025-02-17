import os
import time
import sys
from collections import deque

class EstimatorManager:
    class Estimator:
        def __init__(self, level: int, size: os.terminal_size):
            self.level = level
            self.size = size

        def move(self, x: int, y: int) -> None:
            if x < 1 or y < 1 or x > self.size.columns or y > self.size.lines:
                raise Exception(f"Moved out of bounds: x[1:{self.size.columns}], y[1:{self.size.lines}]: ({x}, {y})")
            sys.stdout.write(f"\033[{y};{x}H")  # Move cursor to row 1, column 1
            sys.stdout.flush()

        def clear(self):
            

        def thing(self) -> None:
            os.system('cls')
            lim = self.size.columns

            for _ in range(4):
                print("X"*lim)

            for i in range(lim):
                self.move(i+1, i%2+2)
                sys.stdout.write("o")
                sys.stdout.flush()
                time.sleep(0.03)

            self.move(1, self.size.lines)


    def __init__(self):
        self.stack = deque()
        # sys.stdout.write("\n" * 10)  # Reserve space in terminal for status updates

    def move_cursor_up(self, lines=1):
        sys.stdout.write(f"\033[{lines}A")

    def move_cursor_down(self, lines=1):
        sys.stdout.write(f"\033[{lines}B")

    def clear_line(self):
        sys.stdout.write("\033[K")

    def estimate_iterable(self, iterable, title="Loop", interval=1):
        start = time.time()
        prev = time.time()
        cycles = 0
        avg = 0
        maximum = len(iterable)

        self.stack.append((title, start))

        for item in iterable:
            yield item

            cycles += 1
            cur = time.time()
            spent = cur - prev
            prev = cur
            avg = ((avg * (cycles - 1)) + spent) / cycles if cycles > 0 else spent
            estimated_total = maximum * avg
            estimated_completion = time.strftime("%H:%M:%S", time.localtime(start + estimated_total))

            sys.stdout.write("\033[H")  # Move cursor to top-left
            for idx, (t, s) in enumerate(self.stack):
                self.clear_line()
                elapsed = cur - s
                print(f"{'  ' * idx}> {t}, elapsed={elapsed:.2f}s, total={estimated_total:.2f}s, "
                      f"est_done={estimated_completion}, iteration={cycles}/{maximum}")
            sys.stdout.flush()

        self.stack.pop()

# Example usage
manager = EstimatorManager()

# for i in manager.estimate_iterable(range(5), title="Outer Loop"):
#     for j in manager.estimate_iterable(range(3), title="Middle Loop"):
#         for k in manager.estimate_iterable(range(2), title="Inner Loop"):
#             time.sleep(0.5)  # Simulating function execution
#             print(f"      [Inner Loop work: i={i}, j={j}, k={k}]\n")
x = EstimatorManager.Estimator(1, os.get_terminal_size())
x.thing()