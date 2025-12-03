import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from functools import cache
from itertools import batched
from math import log10, sqrt

from common import Day

range_regex = re.compile(r'(\d+)-(\d+)')


@cache
def iter_divs(num: int) -> Iterable[int]:
    divs = set()
    for d in range(1, int(sqrt(num)) + 1):
        if num % d == 0:
            divs.add(d)
            divs.add(num // d)
    divs.remove(num)    # Special case, we don't need this one for this puzzle
    return sorted(divs)


@dataclass
class IDRange(Iterable):
    min: int
    max: int

    @property
    def digit_count(self) -> int | None:
        dc = int(log10(abs(self.min))) + 1
        if dc != int(log10(abs(self.max))) + 1:
            return None
        return dc

    def __iter__(self) -> Iterator[int]:
        return iter(range(self.min, self.max + 1))

class Day2(Day):
    @staticmethod
    def parse_input(input_str: str) -> list[IDRange]:
        input_str = input_str.replace('\n', '')
        ranges: list[IDRange] = []
        for r in input_str.split(','):
            r_match = range_regex.fullmatch(r)
            ranges.append(IDRange(min=int(r_match[1]), max=int(r_match[2])))
        return ranges

    @staticmethod
    def is_invalid_p1(pid: int, digit_count: int) -> bool:
        if digit_count % 2 != 0:
            return False
        div = 10 ** (digit_count // 2)
        return pid // div == pid % div

    @staticmethod
    def is_invalid_p2(pid: int, digit_count: int) -> bool:
        s = str(pid)
        for d in iter_divs(digit_count):
            batches = batched(s, d, strict=True)
            first = next(batches)
            if all(b == first for b in batches):
                return True
        return False

    def solve_part1(self, input_str: str) -> str:
        ranges = self.parse_input(input_str)
        res = 0
        for rang in ranges:
            dc = rang.digit_count
            for pid in rang:
                if Day2.is_invalid_p1(pid, (int(log10(abs(pid))) + 1) if dc is None else dc):
                    res += pid
        return str(res)

    def solve_part2(self, input_str: str) -> str:
        ranges = self.parse_input(input_str)
        res = 0
        for rang in ranges:
            dc = rang.digit_count
            for pid in rang:
                if Day2.is_invalid_p2(pid, (int(log10(abs(pid))) + 1) if dc is None else dc):
                    res += pid
        return str(res)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=2, part=1, s_class=Day2, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=2, part=2, s_class=Day2, path_prefix='..', input_file='example_input.txt')
