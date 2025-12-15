import math
import itertools
from typing import List, Tuple

Point = Tuple[float, float]  # (x, y)
Tour = List[int]             # [0, 3, 1, 2, ...]


def euclidean_distance(p1: Point, p2: Point) -> float:
    """The euclid distance between two points (x1,y1) and (x2,y2)."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def compute_distance_matrix(points: List[Point]) -> List[List[float]]:
    """
    Computes distance matrix between all of the cities.
    dist[i][j] = From (i)th city to (j)th city
    """
    n = len(points)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = euclidean_distance(points[i], points[j])
    return dist


def tour_length(tour: Tour, dist: List[List[float]]) -> float:
    """
    Computes total length of a Tour.
    Tour: [0, 3, 1, 2] => 0->3->1->2->0 (returns to the start)
    """
    length = 0.0
    n = len(tour)
    for i in range(n):
        a = tour[i]
        b = tour[(i + 1) % n]  # return from last city to first one
        length += dist[a][b]
    return length


def brute_force_tsp_opt(points: List[Point]) -> Tuple[Tour, float]:
    """
    Find the best (optimum) tour and length with Small n (such as n <= 10) using brute-force.
    """
    n = len(points)
    dist = compute_distance_matrix(points)

    best_tour = None
    best_length = float('inf')

    cities = list(range(n))
    start = 0

    for perm in itertools.permutations(cities[1:]):
        tour = [start] + list(perm)
        length = tour_length(tour, dist)
        if length < best_length:
            best_length = length
            best_tour = tour

    return best_tour, best_length
