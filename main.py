import json
import statistics as stats
from aco_tsp import run_aco, ACOParams
from sa_tsp import run_sa, SAParams


def load_instance(path: str):
    with open(path) as f:
        data = json.load(f)
    points = data["points"]
    opt_len = data.get("optimal_length", None)
    return points, opt_len


def summarize(values):
    return {
        "min": min(values),
        "max": max(values),
        "mean": stats.mean(values),
        "stdev": stats.pstdev(values) if len(values) > 1 else 0.0
    }


def experiment_aco(points, runs=10, opt_len=None):
    lengths = []
    times = []

    for r in range(runs):
        # Shifting the seed in each run to ensure randomness
        params = ACOParams(
            num_ants = min(30, max(10, len(points) // 5)),
            alpha=1.0,
            beta=3.0,
            rho=0.2,
            iterations=120 if len(points) > 100 else 200,
            elitist=True,
            seed=67 + r
        )
        _, best_len, runtime = run_aco(points, params)
        lengths.append(best_len)
        times.append(runtime)

    summary = summarize(lengths)
    tsummary = summarize(times)

    ratios = None
    if opt_len is not None:
        ratios = [L / opt_len for L in lengths]

    return summary, tsummary, ratios


def experiment_sa(points, runs=10, opt_len=None):
    lengths = []
    times = []

    for r in range(runs):
        params = SAParams(
            initial_temp=1000.0,
            cooling_rate=0.995 if len(points) <= 50 else 0.997,
            iterations_per_temp=200 if len(points) <= 50 else 400,
            min_temp=1e-3,
            seed=67 + r
        )
        _, best_len, runtime = run_sa(points, params)
        lengths.append(best_len)
        times.append(runtime)

    summary = summarize(lengths)
    tsummary = summarize(times)

    ratios = None
    if opt_len is not None:
        ratios = [L / opt_len for L in lengths]

    return summary, tsummary, ratios


def print_block(title, length_summary, time_summary, ratios=None):
    print("\n" + "=" * 60)
    print(title)
    print("-" * 60)
    print("Tour length:")
    for k, v in length_summary.items():
        print(f"  {k:>5}: {v:.4f}")

    print("Runtime (sec):")
    for k, v in time_summary.items():
        print(f"  {k:>5}: {v:.4f}")

    if ratios is not None:
        rsum = summarize(ratios)
        print("Approx ratio (L / L*):")
        for k, v in rsum.items():
            print(f"  {k:>5}: {v:.6f}")


def main():
    instances = [
        ("SMALL", "data/tsp_small.json"),
        ("MEDIUM", "data/tsp_medium.json"),
        ("LARGE", "data/tsp_large.json"),
    ]

    for name, path in instances:
        points, opt_len = load_instance(path)
        n = len(points)
        print(f"\n\n########## {name} (n={n}) ##########")

        # ACO
        aco_len_sum, aco_time_sum, aco_ratios = experiment_aco(points, runs=10, opt_len=opt_len)
        print_block(f"ACO Results - {name}", aco_len_sum, aco_time_sum, aco_ratios)

        # SA
        sa_len_sum, sa_time_sum, sa_ratios = experiment_sa(points, runs=10, opt_len=opt_len)
        print_block(f"SA Results - {name}", sa_len_sum, sa_time_sum, sa_ratios)


if __name__ == "__main__":
    main()