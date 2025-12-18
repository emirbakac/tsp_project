from reporting import summarize
from aco_tsp import run_aco, ACOParams
from sa_tsp import run_sa, SAParams


def experiment_aco(points, runs=10, opt_len=None):
    lengths, times = [], []

    for r in range(runs):
        params = ACOParams(
            num_ants=min(20, max(10, len(points) // 5)),
            alpha=1.0,
            beta=3.0,
            rho=0.2,
            iterations=120 if len(points) > 100 else 200,
            seed=67 + r,
            mp_threshold=100,
            use_multiprocessing=None
        )
        _, best_len, runtime = run_aco(points, params)
        lengths.append(best_len)
        times.append(runtime)

    ratios = [L / opt_len for L in lengths] if opt_len else None
    return summarize(lengths), summarize(times), ratios


def experiment_sa(points, runs=10, opt_len=None):
    lengths, times = [], []

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

    ratios = [L / opt_len for L in lengths] if opt_len else None
    return summarize(lengths), summarize(times), ratios
