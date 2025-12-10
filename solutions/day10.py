import re
from itertools import combinations_with_replacement
from typing import NamedTuple

from common import Day, line_iterator


line_regex = re.compile(r'\[([#.]+)] ((?:\(\d+(?:,\d+)*\) )+){(\d+(?:,\d+)*)}')


MachineButton = tuple[int, ...]

class MachineDescription(NamedTuple):
    lights: tuple[bool, ...]
    buttons: tuple[MachineButton, ...]
    joltage: tuple[int, ...]


class Day10(Day):
    @staticmethod
    def parse_input(input_str: str) -> list[MachineDescription]:
        machines: list[MachineDescription] = []
        for line in line_iterator(input_str):
            line_match = line_regex.fullmatch(line)
            lights = tuple(c == '#' for c in line_match[1])
            buttons = tuple(tuple(int(n) for n in b[1:-1].split(',')) for b in line_match[2].strip().split(' '))
            joltage = tuple(int(n) for n in line_match[3].split(','))
            if len(lights) != len(joltage):
                raise RuntimeError(f'Invalid input: the number of lights ({len(lights)}) and joltage requirements '
                                   f'({len(joltage)}) do not match)')
            machines.append(MachineDescription(lights, buttons, joltage))
        return machines

    @staticmethod
    def check_lights(light_len: int, buttons: tuple[MachineButton, ...]) -> tuple[bool, ...]:
        res = [False] * light_len
        for b in buttons:
            for i in b:
                res[i] = not res[i]
        return tuple(res)

    def solve_part1(self, input_str: str) -> str:
        machine_descriptions = self.parse_input(input_str)
        res = 0
        for md in machine_descriptions:
            done = False
            seq_len = 1
            while not done:
                for sequence in combinations_with_replacement(md.buttons, seq_len):
                    if Day10.check_lights(len(md.lights), sequence) == md.lights:
                        res += len(sequence)
                        done = True
                        break
                seq_len += 1
        return str(res)

    def solve_part2(self, input_str: str) -> str:
        machine_descriptions = self.parse_input(input_str)
        return None


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=10, part=1, s_class=Day10, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=10, part=2, s_class=Day10, path_prefix='..', input_file='example_input.txt')
