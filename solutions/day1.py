import math
import re
from dataclasses import dataclass
from typing import Literal

from common import Day, line_iterator


rotation_regex = re.compile(r'([R|L])(\d+)')

@dataclass
class Rotation:
    direction: Literal['R', 'L']
    distance: int


class Day1(Day):
    @staticmethod
    def parse_input(input_str: str) -> list[Rotation]:
        rotations: list[Rotation] = []
        for line in line_iterator(input_str):
            r_match = rotation_regex.match(line)
            rotations.append(Rotation(direction=r_match[1], distance=int(r_match[2])))
        return rotations

    @staticmethod
    def rotate(cur_pos: int, rotation: Rotation) -> int:
        if rotation.direction == 'R':
            cur_pos += rotation.distance
        elif rotation.direction == 'L':
            cur_pos -= rotation.distance
        return cur_pos

    def solve_part1(self, input_str: str) -> str:
        rotations = self.parse_input(input_str)
        cur_pos = 50
        zero_count: int = 0
        for rotation in rotations:
            cur_pos = self.rotate(cur_pos, rotation) % 100
            if cur_pos == 0:
                zero_count += 1
        return str(zero_count)

    def solve_part2(self, input_str: str) -> str:
        rotations = self.parse_input(input_str)
        cur_pos = 50
        click_count: int = 0
        for rotation in rotations:
            new_pos = self.rotate(cur_pos, rotation)
            if rotation.direction == 'R':
                click_count += new_pos // 100
            else:
                # subtracts 1 click if we started from 0
                click_count += math.ceil((-new_pos + 1) / 100) - int(cur_pos == 0)
            cur_pos = new_pos % 100
        return str(click_count)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=1, part=1, s_class=Day1, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=1, part=2, s_class=Day1, path_prefix='..', input_file='example_input.txt')
