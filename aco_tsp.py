import random
import time
from typing import List, Tuple, Optional
from multiprocessing import Pool, cpu_count
from tsp_utils import (
    compute_distance_matrix,
    two_opt_delta,
    apply_two_opt_inplace,
    tour_length,
    Tour,
    Point
)

try:
    import numpy as np
except ImportError:
    np = None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ACOParams:
    def __init__(
        self,
        num_ants: int = 20,
        alpha: float = 1.0,        # pheromone influence
        beta: float = 3.0,         # heuristic influence (1/distance)
        rho: float = 0.2,          # evaporation rate
        q: float = 1.0,            # pheromone deposit constant
        tau0: float = 1.0,         # initial pheromone
        iterations: int = 200,
        seed: Optional[int] = 67,
        mp_threshold: int = 100,   # lower limit of points for multiprocessing
        use_multiprocessing: Optional[bool] = None,
        elite_interval: int = 5    # hybrid parameter
    ):
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.tau0 = tau0
        self.iterations = iterations
        self.seed = seed
        self.mp_threshold = mp_threshold
        self.use_multiprocessing = use_multiprocessing
        self.elite_interval = elite_interval

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _ant_worker(args):
    (
        start_city,
        pheromone,
        eta,
        alpha,
        beta,
        dist,
        seed
    ) = args

    if seed is not None:
        random.seed(seed)

    tour = _construct_tour(start_city, pheromone, eta, alpha, beta)
    tour = two_opt_local_search(tour, dist, max_iters=30)
    length = tour_length(tour, dist)

    return tour, length

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _build_eta(dist: List[List[float]]) -> List[List[float]]:
    n = len(dist)
    eta = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] > 0:
                eta[i][j] = 1.0 / dist[i][j]
    return eta

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _roulette_choice(candidates: List[int], weights: List[float]) -> int:
    total = sum(weights)
    if total <= 0:
        return random.choice(candidates)

    r = random.uniform(0, total)
    cum = 0.0
    for c, w in zip(candidates, weights):
        cum += w
        if cum >= r:
            return c
    return candidates[-1]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _construct_tour(
    start: int,
    pheromone: List[List[float]],
    eta: List[List[float]],
    alpha: float,
    beta: float
) -> Tour:

    n = len(pheromone)
    tour = [start]
    unvisited = set(range(n))
    unvisited.remove(start)

    current = start
    while unvisited:
        candidates = list(unvisited)
        weights = [
            (pheromone[current][j] ** alpha) * (eta[current][j] ** beta)
            for j in candidates
        ]
        nxt = _roulette_choice(candidates, weights)
        tour.append(nxt)
        unvisited.remove(nxt)
        current = nxt

    return tour

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def two_opt_local_search(tour: Tour, dist: List[List[float]], max_iters: int = 50) -> Tour:
    n = len(tour)
    tour = tour[:]

    for _ in range(max_iters):
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                if two_opt_delta(tour, dist, i, j) < 0:
                    apply_two_opt_inplace(tour, i, j)
                    improved = True
                    break
            if improved:
                break
        if not improved:
            break

    return tour

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_aco(points: List[Point], params: ACOParams) -> Tuple[Tour, float, float]:

    t0 = time.perf_counter()

    if params.seed is not None:
        random.seed(params.seed)

    dist = compute_distance_matrix(points)
    eta = _build_eta(dist)
    n = len(points)

    if np is not None:
        pheromone = np.full((n, n), params.tau0, dtype=float)
        np.fill_diagonal(pheromone, 0.0)
    else:
        pheromone = [[params.tau0] * n for _ in range(n)]
        for i in range(n):
            pheromone[i][i] = 0.0

    best_tour = None
    best_len = float("inf")

    if params.use_multiprocessing is not None:
        use_mp = params.use_multiprocessing
    else:
        use_mp = (n >= params.mp_threshold)

    pool = Pool(processes=min(cpu_count(), params.num_ants)) if use_mp else None

    try:
        for it in range(params.iterations):

            iter_best_tour = None
            iter_best_len = float("inf")

            if use_mp:
                starts = [random.randrange(n) for _ in range(params.num_ants)]
                seeds = (
                    [params.seed + it * 1000 + k for k in range(params.num_ants)]
                    if params.seed is not None else
                    [None] * params.num_ants
                )

                args = [
                    (starts[k], pheromone, eta, params.alpha, params.beta, dist, seeds[k])
                    for k in range(params.num_ants)
                ]

                for tour, length in pool.map(_ant_worker, args):
                    if length < iter_best_len:
                        iter_best_len = length
                        iter_best_tour = tour[:]
                    if length < best_len:
                        best_len = length
                        best_tour = tour[:]

            else:
                for _ in range(params.num_ants):
                    start = random.randrange(n)
                    tour = _construct_tour(start, pheromone, eta, params.alpha, params.beta)
                    tour = two_opt_local_search(tour, dist, max_iters=30)
                    length = tour_length(tour, dist)

                    if length < iter_best_len:
                        iter_best_len = length
                        iter_best_tour = tour[:]
                    if length < best_len:
                        best_len = length
                        best_tour = tour[:]

            if iter_best_tour is None:
                continue

            # Evaporation
            pheromone *= (1.0 - params.rho)
            if np is not None:
                np.fill_diagonal(pheromone, 0.0)

            # Hybrid Update
            if it % params.elite_interval == 0:
                source_tour = best_tour
                source_len = best_len
            else:
                source_tour = iter_best_tour
                source_len = iter_best_len

            deposit = params.q / source_len
            for i in range(n):
                a = source_tour[i]
                b = source_tour[(i + 1) % n]
                pheromone[a][b] += deposit
                pheromone[b][a] += deposit

    finally:
        if pool is not None:
            pool.close()
            pool.join()

    t1 = time.perf_counter()
    return best_tour, best_len, (t1 - t0)