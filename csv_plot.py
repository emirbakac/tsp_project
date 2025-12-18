import csv
import matplotlib.pyplot as plt


def generate_csv_and_plots(results):

    rows = []
    ns = []
    aco_mean_len, sa_mean_len = [], []
    aco_mean_time, sa_mean_time = [], []

    for name, data in results.items():
        n = data["n"]
        ns.append(n)

        aco = data["ACO"]
        sa  = data["SA"]

        aco_mean_len.append(aco["length"]["mean"])
        sa_mean_len.append(sa["length"]["mean"])
        aco_mean_time.append(aco["time"]["mean"])
        sa_mean_time.append(sa["time"]["mean"])

        for alg, d in [("ACO", aco), ("SA", sa)]:
            rows.append({
                "instance": name,
                "n": n,
                "algorithm": alg,
                "len_min": d["length"]["min"],
                "len_max": d["length"]["max"],
                "len_mean": d["length"]["mean"],
                "len_stdev": d["length"]["stdev"],
                "time_min": d["time"]["min"],
                "time_max": d["time"]["max"],
                "time_mean": d["time"]["mean"],
                "time_stdev": d["time"]["stdev"],
            })

    # -------- CSV --------
    with open("results_summary.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    # -------- PLOTS --------
    plt.figure()
    plt.plot(ns, aco_mean_len, marker="o", label="ACO")
    plt.plot(ns, sa_mean_len, marker="o", label="SA")
    plt.xlabel("Number of cities (n)")
    plt.ylabel("Mean tour length")
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_quality_vs_n.png", dpi=200)

    plt.figure()
    plt.plot(ns, aco_mean_time, marker="o", label="ACO")
    plt.plot(ns, sa_mean_time, marker="o", label="SA")
    plt.xlabel("Number of cities (n)")
    plt.ylabel("Mean runtime (seconds)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_runtime_vs_n.png", dpi=200)
