from collections import deque
from collections.abc import Iterator, Callable, Iterable
from itertools import combinations, pairwise, chain

from common import Day, line_iterator, Vector, Direction, LGrid, DIRECTION_TURN_CARDINAL, Grid, DIRECTIONS_CARDINAL


class Day9(Day):
    @staticmethod
    def parse_input(input_str: str) -> list[Vector]:
        red_tiles: list[Vector] = []
        for line in line_iterator(input_str):
            x, y = (int(n) for n in line.split(','))
            red_tiles.append(Vector(x, y))
        return red_tiles

    @staticmethod
    def find_largest_rectangle(corner_tiles: Iterable[Vector], check_valid: Callable[[Vector, Vector], bool] = None)\
            -> Vector:
        max_area = 0
        max_area_corners: tuple[Vector, Vector] | None = None
        for t1, t2 in combinations(corner_tiles, 2):
            if check_valid is not None and not check_valid(t1, t2):
                continue
            av = (t1 - t2)
            av = Vector(abs(av.x) + 1, abs(av.y) + 1)
            if av.area > max_area:
                max_area = av.area
                max_area_corners = t1, t2
        if max_area_corners is None:
            raise RuntimeError('no valid solution')
        return max_area

    def solve_part1(self, input_str: str) -> str:
        red_tiles = self.parse_input(input_str)
        max_area = self.find_largest_rectangle(red_tiles)
        return str(max_area)

    @staticmethod
    def walk_red_green_tiles(red_tiles: list[Vector], last_step=True) -> Iterator[tuple[Direction, Vector, bool]]:
        for c1, c2 in pairwise(chain(red_tiles, (red_tiles[0],))):
            print(c1, c2)
            if c1 == c2:
                raise RuntimeError('Received 2 identical red tiles coordinates in a row')
            if c1.y == c2.y:
                direction = Direction.Left if c2.x < c1.x else Direction.Right
            elif c1.x == c2.x:
                direction = Direction.Up if c2.y < c1.y else Direction.Down
            else:
                raise RuntimeError(f'Cannot draw a vertical or horizontal line between {c1} and {c2}')
            cur_loc = c1
            while cur_loc != c2:
                yield direction, cur_loc, cur_loc == c1
                cur_loc += direction
            if last_step:
                yield direction, cur_loc, True

    @staticmethod
    def fill_area(grid: Grid[str], fill_overlay: LGrid[str], fill_char: str, start_pos: Vector) -> bool:
        incomplete: deque[Vector] = deque((start_pos,))
        while incomplete:
            loc = incomplete.pop()
            if not grid.is_in_bounds(loc):
                return False
            if grid.get_cell(loc) == fill_char or fill_overlay.get_cell(loc) == fill_char:
                continue
            fill_overlay.set_cell(loc, fill_char)
            incomplete.extend(loc + d for d in DIRECTIONS_CARDINAL)
        return True

    @staticmethod
    def is_rectangle_filled(grid: Grid[str], fill_char: str, corner1: Vector, corner2: Vector) -> bool:
        x_from, x_to = min(corner1.x, corner2.x), max(corner1.x, corner2.x) + 1
        for y in range(min(corner1.y, corner2.y), max(corner1.y, corner2.y) + 1):
            for x in range(x_from, x_to):
                if grid.get_cell(Vector(x, y)) != fill_char:
                    return False
        return True

    def solve_part2(self, input_str: str) -> str:
        red_tiles = self.parse_input(input_str)

        # Create the grid
        grid: LGrid[str] = LGrid.create(max(c.x for c in red_tiles) + 1, max(c.y for c in red_tiles) + 1, '.')

        right_side: list[Vector] = []
        left_side: list[Vector] = []
        for d, l, _ in self.walk_red_green_tiles(red_tiles, True):
            grid.set_cell(l, 'X')
            left_side.append(l + DIRECTION_TURN_CARDINAL[d]['left'])
            right_side.append(l + DIRECTION_TURN_CARDINAL[d]['right'])

        fill_success = False
        overlay: LGrid[str]
        for side_tiles in (right_side, left_side):
            overlay = LGrid[str].create(grid.width, grid.height, '.')
            if all(self.fill_area(grid, overlay, 'X', tile) for tile in side_tiles):
                fill_success = True
                grid.merge_overlay(overlay, '.')
                break
        if not fill_success:
            raise RuntimeError('No enclosed fill space')

        max_area = self.find_largest_rectangle(red_tiles,
                                               lambda c1, c2: self.is_rectangle_filled(grid, 'X', c1, c2))

        return str(max_area)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=9, part=1, s_class=Day9, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=9, part=2, s_class=Day9, path_prefix='..', input_file='example_input.txt')
