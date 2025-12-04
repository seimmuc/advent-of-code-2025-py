from common import Day, line_iterator, LGrid, DIRECTIONS_ALL


class Day4(Day):
    @staticmethod
    def parse_input(input_str: str) -> LGrid[str]:
        grid: LGrid[str] = LGrid()
        for line in line_iterator(input_str):
            grid.add_line(list(line))
        return grid

    def solve_part1(self, input_str: str) -> str:
        grid = self.parse_input(input_str)
        res = 0
        for l, item in grid.scan_all():
            if item != '@':
                continue
            adjacent_roll_count = sum(int(v == '@') for _, v in grid.look_around(l, DIRECTIONS_ALL))
            if adjacent_roll_count < 4:
                res += 1
        return str(res)

    def solve_part2(self, input_str: str) -> str:
        grid = self.parse_input(input_str)
        res = 0

        while True:
            removed = 0
            for l, item in grid.scan_all():
                if item != '@':
                    continue
                adjacent_roll_count = sum(int(v == '@') for _, v in grid.look_around(l, DIRECTIONS_ALL))
                if adjacent_roll_count < 4:
                    grid.set_cell(l, '.')
                    removed += 1
            if removed == 0:
                break
            res += removed
        return str(res)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=4, part=1, s_class=Day4, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=4, part=2, s_class=Day4, path_prefix='..', input_file='example_input.txt')
