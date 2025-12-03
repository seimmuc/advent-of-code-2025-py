from common import Day, line_iterator


class Day3(Day):
    @staticmethod
    def parse_input(input_str: str) -> list[list[int]]:
        banks: list[list[int]] = []
        for line in line_iterator(input_str):
            banks.append(list(map(int, line)))
        return banks

    @staticmethod
    def largest_num(bank: list[int], digits: int, min_index: int = 0, mdv: int = 9) -> tuple[int, int] | None:
        # Recursive function
        if len(bank) < digits or digits == 0:
            return None
        # Special case: find 1 digit
        if digits == 1:
            val, ind = -1, None
            for i in range(min_index, len(bank)):
                if val < bank[i] <= mdv:
                    val = bank[i]
                    ind = i
            return None if ind is None else (val, ind)
        # Find the next digit first, then the rest recursively
        while True:
            first_digit = Day3.largest_num(bank, 1, min_index, mdv)
            if first_digit is None:
                return None
            rest_digits = Day3.largest_num(bank, digits - 1, first_digit[1] + 1)
            if rest_digits is None:
                mdv = first_digit[0] - 1
                continue
            return first_digit[0] * (10 ** (digits - 1)) + rest_digits[0], rest_digits[1]

    def solve_part1(self, input_str: str) -> str:
        banks = self.parse_input(input_str)
        res = 0
        for bank in banks:
            jtg = Day3.largest_num(bank, 2)
            if jtg is not None:
                res += jtg[0]
        return str(res)

    def solve_part2(self, input_str: str) -> str:
        banks = self.parse_input(input_str)
        res = 0
        for bank in banks:
            jtg = Day3.largest_num(bank, 12)
            if jtg is not None:
                res += jtg[0]
        return str(res)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=3, part=1, s_class=Day3, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=3, part=2, s_class=Day3, path_prefix='..', input_file='example_input.txt')
