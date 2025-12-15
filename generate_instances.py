import random
import json
from typing import List
from tsp_utils import Point, brute_force_tsp_opt

random.seed(67)  # reproducible

def generate_random_points(n: int, x_max: float = 1000.0, y_max: float = 1000.0) -> List[Point]:
    """
    Generate n random points within the square defined by the coordinates [0, x_max] x [0, y_max]
    """
    points: List[Point] = []
    for _ in range(n):
        x = random.uniform(0, x_max)
        y = random.uniform(0, y_max)
        points.append((x, y))
    return points


def save_instance(filename: str, points: List[Point], optimal_tour=None, optimal_length=None):
    """
    Saves Instance in JSON format.
    """
    data = {
        "points": points
    }
    if optimal_tour is not None and optimal_length is not None:
        data["optimal_tour"] = optimal_tour
        data["optimal_length"] = optimal_length

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def main():
    # Instance sizes:
    small_n = 10
    medium_n = 50
    large_n = 150

    # --- SMALL ---
    small_points = generate_random_points(small_n)
    opt_tour, opt_len = brute_force_tsp_opt(small_points)
    save_instance("data/tsp_small.json", small_points, opt_tour, opt_len)
    print("Small instance optimal length:", opt_len)

    # --- MEDIUM ---
    medium_points = generate_random_points(medium_n)
    save_instance("data/tsp_medium.json", medium_points)

    # --- LARGE ---
    large_points = generate_random_points(large_n)
    save_instance("data/tsp_large.json", large_points)

    print("Instances generated and saved in data/ folder.")


if __name__ == "__main__":
    main()