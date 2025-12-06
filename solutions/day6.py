import operator
from dataclasses import dataclass
from functools import reduce
from typing import Literal

from common import Day


@dataclass
class MathProblem:
    operator: Literal['+', '*']
    nums: list[int]


class Day6(Day):
    @staticmethod
    def parse_input_part1(input_str: str) -> list[MathProblem]:
        lines = list(l.split() for l in input_str.split('\n') if len(l.strip()) > 0)
        problems: list[MathProblem] = []
        for items in zip(*lines, strict=True):
            problems.append(MathProblem(items[-1], list(int(n) for n in items[:-1])))
        return problems

    @staticmethod
    def parse_input_part2(input_str: str) -> list[MathProblem]:
        lines = list(l.rstrip() for l in input_str.split('\n') if l.rstrip() != '')
        line_length = max(len(l) for l in lines)
        for i in range(len(lines)):
            lines[i] = lines[i].ljust(line_length, ' ')
        nums_lns = lines[:-1]
        ops_line = lines[-1]
        problems: list[MathProblem] = []
        lgi = line_length
        for i in range(line_length - 1, -1, -1):
            if ops_line[i] == ' ':
                continue
            opr = ops_line[i]
            if opr not in ('+', '*'):
                raise ValueError(f'Invalid operator "{opr}" (column {i})')
            nums = list(int(''.join(nl[j] for nl in nums_lns if nl[j] != ' ')) for j in range(lgi - 1, i - 1, -1))
            problems.append(MathProblem(opr, nums))
            lgi = i - 1
        return problems

    @staticmethod
    def solve_all(problems: list[MathProblem]) -> int:
        result = 0
        for problem in problems:
            if problem.operator == '+':
                result += sum(problem.nums)
            elif problem.operator == '*':
                result += reduce(operator.mul, problem.nums)
            else:
                raise ValueError(f'Invalid operator "{problem.operator}"')
        return result

    def solve_part1(self, input_str: str) -> str:
        problems = self.parse_input_part1(input_str)
        return str(self.solve_all(problems))

    def solve_part2(self, input_str: str) -> str:
        problems = self.parse_input_part2(input_str)
        return str(self.solve_all(problems))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=6, part=1, s_class=Day6, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=6, part=2, s_class=Day6, path_prefix='..', input_file='example_input.txt')
