import json
import csv
import statistics as stats
import matplotlib.pyplot as plt

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
    lengths, times = [], []
    for r in range(runs):
        params = ACOParams(
            num_ants=max(20, len(points) // 2),
            alpha=1.0,
            beta=3.0,
            rho=0.2,
            iterations=200 if len(points) <= 50 else 300,
            elitist=True,
            seed=42 + r
        )
        _, best_len, runtime = run_aco(points, params)
        lengths.append(best_len)
        times.append(runtime)

    ratios = None
    if opt_len is not None:
        ratios = [L / opt_len for L in lengths]

    return summarize(lengths), summarize(times), (summarize(ratios) if ratios else None)


def experiment_sa(points, runs=10, opt_len=None):
    lengths, times = [], []
    for r in range(runs):
        params = SAParams(
            initial_temp=1000.0,
            cooling_rate=0.995 if len(points) <= 50 else 0.997,
            iterations_per_temp=200 if len(points) <= 50 else 400,
            min_temp=1e-3,
            seed=42 + r
        )
        _, best_len, runtime = run_sa(points, params)
        lengths.append(best_len)
        times.append(runtime)

    ratios = None
    if opt_len is not None:
        ratios = [L / opt_len for L in lengths]

    return summarize(lengths), summarize(times), (summarize(ratios) if ratios else None)


def main():
    instances = [
        ("SMALL", "data/tsp_small.json"),
        ("MEDIUM", "data/tsp_medium.json"),
        ("LARGE", "data/tsp_large.json"),
    ]

    # CSV rows
    rows = []

    # For plots
    ns = []
    aco_mean_len, sa_mean_len = [], []
    aco_mean_time, sa_mean_time = [], []

    for name, path in instances:
        points, opt_len = load_instance(path)
        n = len(points)
        ns.append(n)

        # ACO
        aco_len_sum, aco_time_sum, aco_ratio_sum = experiment_aco(points, runs=10, opt_len=opt_len)
        # SA
        sa_len_sum, sa_time_sum, sa_ratio_sum = experiment_sa(points, runs=10, opt_len=opt_len)

        # collect plot values
        aco_mean_len.append(aco_len_sum["mean"])
        sa_mean_len.append(sa_len_sum["mean"])
        aco_mean_time.append(aco_time_sum["mean"])
        sa_mean_time.append(sa_time_sum["mean"])

        # helper to add row
        def add_row(alg, lsum, tsum, rsum):
            row = {
                "instance": name,
                "n": n,
                "algorithm": alg,
                "len_min": lsum["min"],
                "len_max": lsum["max"],
                "len_mean": lsum["mean"],
                "len_stdev": lsum["stdev"],
                "time_min": tsum["min"],
                "time_max": tsum["max"],
                "time_mean": tsum["mean"],
                "time_stdev": tsum["stdev"],
                "ratio_min": "" if rsum is None else rsum["min"],
                "ratio_max": "" if rsum is None else rsum["max"],
                "ratio_mean": "" if rsum is None else rsum["mean"],
                "ratio_stdev": "" if rsum is None else rsum["stdev"],
            }
            rows.append(row)

        add_row("ACO", aco_len_sum, aco_time_sum, aco_ratio_sum)
        add_row("SA",  sa_len_sum,  sa_time_sum,  sa_ratio_sum)

    # --- write CSV ---
    csv_path = "results_summary.csv"
    fieldnames = list(rows[0].keys())
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {csv_path}")

    # --- plot 1: mean tour length vs n ---
    plt.figure()
    plt.plot(ns, aco_mean_len, marker="o", label="ACO mean tour length")
    plt.plot(ns, sa_mean_len, marker="o", label="SA mean tour length")
    plt.xlabel("Number of cities (n)")
    plt.ylabel("Mean tour length")
    plt.title("Solution Quality vs Problem Size")
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_quality_vs_n.png", dpi=200)
    print("Saved plot_quality_vs_n.png")

    # --- plot 2: mean runtime vs n ---
    plt.figure()
    plt.plot(ns, aco_mean_time, marker="o", label="ACO mean runtime (sec)")
    plt.plot(ns, sa_mean_time, marker="o", label="SA mean runtime (sec)")
    plt.xlabel("Number of cities (n)")
    plt.ylabel("Mean runtime (seconds)")
    plt.title("Runtime vs Problem Size")
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_runtime_vs_n.png", dpi=200)
    print("Saved plot_runtime_vs_n.png")


if __name__ == "__main__":
    main()