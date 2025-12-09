import heapq
import math
from collections.abc import Generator
from functools import reduce
from itertools import combinations
from typing import NamedTuple, Self

from common import Day, line_iterator


class Vector3D(NamedTuple):
    x: int
    y: int
    z: int

    @property
    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def euclidean_dist_square(self) -> int:
        return (self.x * self.x) + (self.y * self.y) + (self.z * self.z)

    @property
    def euclidean_dist(self) -> float:
        return math.sqrt(self.euclidean_dist_square)

    def __add__(self, other: Self):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Self):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __repr__(self):
        return f'Vector3D({self.x}, {self.y}, {self.z})'

    def __eq__(self, other: Self):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

class JuncBoxPair(NamedTuple):
    box1: Vector3D
    box2: Vector3D
    distance_squared: int

class JuncBoxCircuit:
    def __init__(self, boxes: Vector3D | set[Vector3D]):
        if isinstance(boxes, Vector3D):
            self.boxes: set[Vector3D] = {boxes}
        else:
            self.boxes = boxes

    def connect_to(self, other: Self) -> Self:
        return JuncBoxCircuit(self.boxes | other.boxes)

    def __len__(self):
        return len(self.boxes)

    def __hash__(self):
        return hash(tuple(self.boxes))


class Day8(Day):
    @staticmethod
    def parse_input(input_str: str) -> list[Vector3D]:
        junction_boxes: list[Vector3D] = []
        for line in line_iterator(input_str):
            x, y, z = (int(n) for n in line.split(','))
            junction_boxes.append(Vector3D(x, y, z))
        return junction_boxes

    @staticmethod
    def junction_box_pair_distances(junction_boxes: list[Vector3D]) -> Generator[JuncBoxPair]:
        for jb1, jb2 in combinations(junction_boxes, 2):
            yield JuncBoxPair(jb1, jb2, (jb1 - jb2).euclidean_dist_square)

    def solve_part1(self, input_str: str) -> str:
        junction_boxes = self.parse_input(input_str)

        # example has 20 junction boxes and requires 10 connections,
        # real input contains 1000 boxes and needs 1000 connections
        connections = 10 if len(junction_boxes) == 20 else 1000

        # Find n closest junction box pairs
        closest_distances = heapq.nsmallest(
            n=connections,
            iterable=self.junction_box_pair_distances(junction_boxes),
            key=lambda p: p.distance_squared
        )

        # Create and connect junction boxes
        circuits: dict[Vector3D, JuncBoxCircuit] = dict((b, JuncBoxCircuit(b)) for b in junction_boxes)
        for jbp in closest_distances:
            c1 = circuits[jbp.box1]
            c2 = circuits[jbp.box2]
            if c1 == c2:
                continue
            c3 = c1.connect_to(c2)
            for b in c3.boxes:
                circuits[b] = c3

        # Find largest circuits and calculate the result
        sorted_circuits = sorted(set(circuits.values()), key=len, reverse=True)
        result = reduce(lambda a, c: a * len(c), sorted_circuits[:3], 1)

        return str(result)

    def solve_part2(self, input_str: str) -> str:
        junction_boxes = self.parse_input(input_str)

        # Find all connections and sort them
        all_possible_connections = sorted(
            self.junction_box_pair_distances(junction_boxes),
            key=lambda p: p.distance_squared
        )

        # Keep making connections
        jbc = len(junction_boxes)
        circuits: dict[Vector3D, JuncBoxCircuit] = dict((b, JuncBoxCircuit(b)) for b in junction_boxes)
        last_connection: JuncBoxPair | None = None
        for connection in all_possible_connections:
            c1 = circuits[connection.box1]
            c2 = circuits[connection.box2]
            if c1 == c2:
                continue
            c3 = c1.connect_to(c2)
            if len(c3) >= jbc:
                last_connection = connection
                break
            for b in c3.boxes:
                circuits[b] = c3
        if last_connection is None:
            raise RuntimeError('Something went wrong')

        return str(last_connection.box1.x * last_connection.box2.x)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=8, part=1, s_class=Day8, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=8, part=2, s_class=Day8, path_prefix='..', input_file='example_input.txt')
