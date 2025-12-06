import re
from collections.abc import Iterator
from typing import Self

from common import Day, line_iterator


range_regex = re.compile(r'(\d+)-(\d+)')


class Range:
    """ Range utility class with inclusive low and high values """
    __slots__ = ['low', 'high']

    def __init__(self, low: int, high: int):
        if low > high:
            raise RuntimeError()
        self.low = low
        self.high = high

    def overlaps(self, other: Self) -> bool:
        if self.low < other.low:
            return self.high >= other.low
        else:
            return self.low <= other.high

    def combine(self, other: Self) -> Self | None:
        if not self.overlaps(other):
            return None
        return Range(min(self.low, other.low), max(self.high, other.high))

    def intersect_with(self, other: Self) -> Self:
        return Range(max(self.low, other.low), min(self.high, other.high))

    def __iter__(self, step=1) -> Iterator[int]:
        return iter(range(self.low, self.high + 1, step))

    def __contains__(self, num: int):
        return self.low <= num <= self.high

    def __len__(self):
        return self.high - self.low + 1


class Day5(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[list[Range], list[int]]:
        ranges: list[Range] = []
        available: list[int] = []
        li = line_iterator(input_str)
        for line in li:
            if line == '':
                break
            range_match = range_regex.fullmatch(line)
            ranges.append(Range(int(range_match[1]), int(range_match[2])))
        for line in li:
            available.append(int(line))
        return ranges, available

    def solve_part1(self, input_str: str) -> str:
        ranges, available = self.parse_input(input_str)
        res = 0
        for ing_id in available:
            for fr in ranges:
                if ing_id in fr:
                    res += 1
                    break
        return str(res)

    def solve_part2(self, input_str: str) -> str:
        ranges, _ = self.parse_input(input_str)

        while True:
            merge_count: int = 0
            new_ranges: list[Range] = []
            for r in ranges:
                merged = False
                for i in range(len(new_ranges)):
                    nr = new_ranges[i]
                    if nr.overlaps(r):
                        new_ranges[i] = nr.combine(r)
                        merged = True
                        break
                if merged:
                    merge_count += 1
                else:
                    new_ranges.append(r)
            ranges = new_ranges
            if merge_count == 0:
                break

        res = sum(len(r) for r in ranges)
        return str(res)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=5, part=1, s_class=Day5, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=5, part=2, s_class=Day5, path_prefix='..', input_file='example_input.txt')
