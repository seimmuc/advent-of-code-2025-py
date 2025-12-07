from collections.abc import Iterable
from dataclasses import dataclass

from common import Day, line_iterator, Grid, GridSearch, Vector, Direction


@dataclass
class Beam:
    location: Vector
    strength: int


class Day7(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[Grid[str], Vector]:
        grid: Grid[str] = Grid()
        start_search = GridSearch(search_char='S', replace_char='.', max_count=1)
        for y, line in enumerate(line_iterator(input_str)):
            line = start_search.search_line(line, y)
            grid.add_line(line)
        return grid, start_search.single_result()

    @staticmethod
    def add_beam(beams: dict[Vector, Beam], loc: Vector, strength: int):
        if loc in beams:
            b = beams[loc]
            b.strength += strength
        else:
            beams[loc] = Beam(loc, strength)

    @staticmethod
    def simulate_step(grid: Grid[str], current_beams: Iterable[Beam]) -> tuple[dict[Vector, Beam], int]:
        new_beams: dict[Vector, Beam] = {}
        splits = 0
        for beam in current_beams:
            new_loc: Vector = beam.location.move_in(Direction.Down)
            if grid.get_cell(new_loc) == '.':
                Day7.add_beam(new_beams, new_loc, beam.strength)
            if grid.get_cell(new_loc) == '^':
                Day7.add_beam(new_beams, new_loc.move_in(Direction.Left), beam.strength)
                Day7.add_beam(new_beams, new_loc.move_in(Direction.Right), beam.strength)
                splits += 1
        return new_beams, splits

    def solve_part1(self, input_str: str) -> str:
        grid, beam_start = self.parse_input(input_str)
        current_beams: dict[Vector, Beam] = {beam_start: Beam(beam_start, 1)}
        total_splits = 0
        for y in range(beam_start.y, grid.height - 1):
            current_beams, splits = self.simulate_step(grid, current_beams.values())
            total_splits += splits
        return str(total_splits)

    def solve_part2(self, input_str: str) -> str:
        grid, beam_start = self.parse_input(input_str)
        current_beams: dict[Vector, Beam] = {beam_start: Beam(beam_start, 1)}
        for y in range(beam_start.y, grid.height - 1):
            current_beams, splits = self.simulate_step(grid, current_beams.values())
        return str(sum(b.strength for b in current_beams.values()))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=7, part=1, s_class=Day7, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=7, part=2, s_class=Day7, path_prefix='..', input_file='example_input.txt')
