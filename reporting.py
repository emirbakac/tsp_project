import statistics as stats

def summarize(values):
    return {
        "min": min(values),
        "max": max(values),
        "mean": stats.mean(values),
        "stdev": stats.pstdev(values) if len(values) > 1 else 0.0
    }


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
