import random
import math
import time
from typing import List, Tuple, Optional
from tsp_utils import compute_distance_matrix, two_opt_delta, apply_two_opt_inplace, tour_length, Tour, Point


class SAParams:
    def __init__(
        self,
        initial_temp: float = 1000.0,
        cooling_rate: float = 0.995,
        iterations_per_temp: int = 100,
        min_temp: float = 1e-3,
        seed: Optional[int] = 67
    ):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.iterations_per_temp = iterations_per_temp
        self.min_temp = min_temp
        self.seed = seed


def random_tour(n: int) -> Tour:
    """A random starting point."""
    tour = list(range(n))
    random.shuffle(tour)
    return tour

def run_sa(points: List[Point], params: SAParams) -> Tuple[Tour, float, float]:
    """
    Simulated Annealing
    """
    t0 = time.perf_counter()

    if params.seed is not None:
        random.seed(params.seed)

    dist = compute_distance_matrix(points)
    n = len(points)

    # initial solution
    current_tour = random_tour(n)
    current_len = tour_length(current_tour, dist)

    best_tour = current_tour[:] # copies the list with [:]
    best_len = current_len

    t = params.initial_temp



    while t > params.min_temp:
        for _ in range(params.iterations_per_temp):
            # avoid tiny/no-op reversals
            i = random.randint(0, n - 3)
            j = random.randint(i + 2, n - 1)

            delta = two_opt_delta(current_tour, dist, i, j)

            # accept rule
            if delta < 0:
                accept = True
            else:
                accept = (random.random() < math.exp(-delta / t))

            if accept:
                apply_two_opt_inplace(current_tour, i, j)
                current_len += delta

                if current_len < best_len:
                    best_len = current_len
                    best_tour = current_tour[:]

        t *= params.cooling_rate

    t1 = time.perf_counter()
    return best_tour, best_len, (t1 - t0)