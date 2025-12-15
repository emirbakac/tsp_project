import random
import time
from typing import List, Tuple, Optional
from tsp_utils import compute_distance_matrix, tour_length, Tour, Point

try:
    import numpy as np
except ImportError:
    np = None


class ACOParams:
    def __init__(
        self,
        num_ants: int = 30,
        alpha: float = 1.0,        # pheromone influence
        beta: float = 3.0,         # heuristic influence (1/distance)
        rho: float = 0.2,          # evaporation rate
        q: float = 1.0,            # pheromone deposit constant
        tau0: float = 1.0,         # initial pheromone
        iterations: int = 200,
        elitist: bool = True,      # reinforce global best only (stable)
        seed: Optional[int] = 67
    ):
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.tau0 = tau0
        self.iterations = iterations
        self.elitist = elitist
        self.seed = seed


def _build_eta(dist: List[List[float]]) -> List[List[float]]:
    """Heuristic matrix eta[i][j] = 1 / dist[i][j] (0 on diagonal)."""
    n = len(dist)
    eta = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] > 0:
                eta[i][j] = 1.0 / dist[i][j]
    return eta


def _roulette_choice(candidates: List[int], weights: List[float]) -> int:
    """
    Randomly pick an item from candidates proportional to weights.
    """
    total = sum(weights)
    if total <= 0:
        # fallback: uniform random
        return random.choice(candidates)

    r = random.uniform(0, total)
    cum = 0.0
    for c, w in zip(candidates, weights):
        cum += w
        if cum >= r:
            return c
    return candidates[-1] # back-up


def _construct_tour(
    start: int,
    pheromone: List[List[float]],
    eta: List[List[float]],
    alpha: float,
    beta: float
) -> Tour:
    """
    One ant builds one tour using probabilistic transition rule:
    """
    n = len(pheromone)
    tour = [start]
    unvisited = set(range(n))
    unvisited.remove(start)

    current = start
    while unvisited:
        candidates = list(unvisited)
        weights = []
        for j in candidates:
            tau = pheromone[current][j] ** alpha
            h = eta[current][j] ** beta
            weights.append(tau * h)

        nxt = _roulette_choice(candidates, weights)
        tour.append(nxt)
        unvisited.remove(nxt)
        current = nxt

    return tour


def run_aco(points: List[Point], params: ACOParams) -> Tuple[Tour, float, float]:
    """
    Runs ACO on a TSP instance given by points.
    """
    if params.seed is not None:
        random.seed(params.seed)

    dist = compute_distance_matrix(points)
    eta = _build_eta(dist)

    n = len(points)

    # initialize pheromone
    if np is not None:
        pheromone = np.full((n, n), params.tau0, dtype=float)
        np.fill_diagonal(pheromone, 0.0)
    else:
        pheromone = [[params.tau0] * n for _ in range(n)]
        for i in range(n):
            pheromone[i][i] = 0.0

    best_tour: Tour = list(range(n))
    best_len = float("inf")

    t0 = time.perf_counter()

    for it in range(params.iterations):
        all_tours: List[Tour] = []
        all_lengths: List[float] = []

        # --- each ant constructs a tour ---
        for k in range(params.num_ants):
            start_city = random.randrange(n)
            tour = _construct_tour(
                start=start_city,
                pheromone=pheromone,
                eta=eta,
                alpha=params.alpha,
                beta=params.beta
            )
            length = tour_length(tour, dist)

            all_tours.append(tour)
            all_lengths.append(length)

            if length < best_len:
                best_len = length
                best_tour = tour[:]

        # --- evaporation ---
        if np is not None:
            pheromone *= (1.0 - params.rho)
            np.fill_diagonal(pheromone, 0.0)
        else:
            for i in range(n):
                for j in range(n):
                    if i != j:
                        pheromone[i][j] *= (1.0 - params.rho)

        # --- reinforcement ---
        if params.elitist:
            # add pheromone only for global best tour
            deposit = params.q / best_len
            for i in range(n):
                a = best_tour[i]
                b = best_tour[(i + 1) % n]
                pheromone[a][b] += deposit
                pheromone[b][a] += deposit
        else:
            # elitist is true by default, I just wanted to demonstrate the implementation.
            # deposit from all ants (more explorative)
            for tour, length in zip(all_tours, all_lengths):
                deposit = params.q / length
                for i in range(n):
                    a = tour[i]
                    b = tour[(i + 1) % n]
                    pheromone[a][b] += deposit
                    pheromone[b][a] += deposit

        # ~~~~~~ Debug ~~~~~~
        # if (it + 1) % 20 == 0:
        #     print(f"Iter {it+1}/{params.iterations} best_len={best_len:.2f}")

    t1 = time.perf_counter()
    return best_tour, best_len, (t1 - t0)