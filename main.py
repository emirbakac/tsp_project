from tsp_utils import load_instance
from experiments import experiment_aco, experiment_sa
from reporting import print_block
from csv_plot import generate_csv_and_plots


def main():
    instances = [
        ("SMALL", "data/tsp_small.json"),
        ("MEDIUM", "data/tsp_medium.json"),
        ("LARGE", "data/tsp_large.json"),
    ]

    results = {}

    for name, path in instances:
        points, opt_len = load_instance(path)
        n = len(points)

        print(f"\n\n########## {name} (n={n}) ##########")

        aco_len, aco_time, aco_ratios = experiment_aco(points, opt_len=opt_len)
        sa_len,  sa_time,  sa_ratios  = experiment_sa(points,  opt_len=opt_len)

        results[name] = {
            "n": n,
            "ACO": {
                "length": aco_len,
                "time": aco_time,
                "ratios": aco_ratios
            },
            "SA": {
                "length": sa_len,
                "time": sa_time,
                "ratios": sa_ratios
            }
        }

        print_block(f"ACO Results - {name}", aco_len, aco_time, aco_ratios)
        print_block(f"SA Results - {name}",  sa_len,  sa_time,  sa_ratios)

    choice = input("\nGenerate plots & CSV file? (y/n): ").strip().lower()
    if choice == "y":
        generate_csv_and_plots(results)
        print("CSV and plots generated.")


if __name__ == "__main__":
    main()
