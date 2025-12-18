# 🧭 Traveling Salesman Problem (TSP)
## Ant Colony Optimization (ACO) & Simulated Annealing (SA) Comparison

This project provides a **modular, reproducible experimental framework** for solving the **Traveling Salesman Problem (TSP)** using two well-known metaheuristic algorithms:

- 🐜 **Ant Colony Optimization (ACO)**
- 🔥 **Simulated Annealing (SA)**

The framework supports exact solutions for small instances, multiple independent runs, statistical performance analysis, and automatic result visualization.

---

## 📌 Problem Definition

Given **n cities** represented by 2D coordinates, the Traveling Salesman Problem asks for:

> The **shortest possible closed tour** that visits each city exactly once.

TSP is an **NP-hard** combinatorial optimization problem and is widely used to benchmark heuristic and metaheuristic algorithms.

---

## 🚀 Features

✔ Clean and modular code structure  
✔ Reproducible experiments (fixed random seeds)  
✔ Hybrid ACO with **2-opt local search**  
✔ Optional multiprocessing for large instances  
✔ Automatic TSP instance generation  
✔ Statistical summaries (min / max / mean / stdev)  
✔ CSV export for reporting  
✔ Quality & runtime plots  

---

## 📁 Project Structure

```text
.
├── aco_tsp.py            # Ant Colony Optimization (ACO)
├── sa_tsp.py             # Simulated Annealing (SA)
├── tsp_utils.py          # Distance, 2-opt, brute force solver
├── generate_instances.py # TSP instance generator
├── experiments.py        # Repeated runs & statistics
├── reporting.py          # Summaries and formatted output
├── csv_plot.py           # CSV export and matplotlib plots
├── main.py               # Program entry point
├── data/
│   ├── tsp_small.json    # n = 10 (with optimal solution)
│   ├── tsp_medium.json   # n = 50
│   └── tsp_large.json    # n = 150
└── README.md
```

---

## 🧪 Algorithms Implemented

### 🐜 Ant Colony Optimization (ACO)

ACO is a population-based metaheuristic inspired by the foraging behavior of ants.

**Key characteristics:**
- Probabilistic solution construction
- Pheromone trails with evaporation and reinforcement
- Heuristic visibility (1 / distance)
- Hybrid improvement using **2-opt local search**
- Optional multiprocessing support

**Main parameters (`ACOParams`):**
- `num_ants` – number of ants
- `alpha` – pheromone influence
- `beta` – heuristic influence
- `rho` – pheromone evaporation rate
- `iterations` – number of iterations
- `elite_interval` – global-best reinforcement frequency

---

### 🔥 Simulated Annealing (SA)

Simulated Annealing is a single-solution metaheuristic inspired by the annealing process in metallurgy.

**Key characteristics:**
- Accepts worse solutions probabilistically
- Gradual temperature cooling
- 2-opt neighborhood moves
- Strong balance between exploration and exploitation

**Main parameters (`SAParams`):**
- `initial_temp`
- `cooling_rate`
- `iterations_per_temp`
- `min_temp`

---

## 🛠 Utilities (`tsp_utils.py`)

- Euclidean distance computation
- Distance matrix construction
- Tour length calculation
- Brute-force optimal TSP solver (for small instances)
- Efficient 2-opt move and delta evaluation

---

## 📊 Experimental Setup

- **3 instance sizes**: Small, Medium, Large
- **10 independent runs** per algorithm
- Fixed but varied random seeds (`seed = 67 + run_id`)
- Metrics collected:
  - Tour length
  - Runtime
  - Approximation ratio (if optimal known)

---

## ▶️ How to Run

### 1️⃣ Generate Instances

python generate_instances.py

This creates three instances in the `data/` directory:
- `tsp_small.json` (n = 10, includes optimal solution)
- `tsp_medium.json` (n = 50)
- `tsp_large.json` (n = 150)

---

### 2️⃣ Run Experiments

python main.py

For each instance size:
- ACO and SA are executed multiple times
- Tour length and runtime statistics are collected
- Results are printed to the console

---

### 3️⃣ Generate CSV & Plots

After experiments finish, you will be prompted:

Generate plots & CSV file? (y/n):

Enter `y` to generate:
- `results_summary.csv`
- `plot_quality_vs_n.png`
- `plot_runtime_vs_n.png`

---

## 📦 Dependencies

Required:
- Python **3.8+**

Required Python packages:

pip install matplotlib

Recommended (for improved ACO performance):

pip install numpy

---

## 🔁 Reproducibility

- All algorithms use **fixed random seeds**
- Results are deterministic per run
- Full experimental reproducibility is guaranteed

---

## 📌 Notes

- Brute-force optimal solutions are computed **only** for the small instance.
- Multiprocessing is automatically enabled for large instances.
- Algorithm parameters can be tuned directly in:
  - `ACOParams` (`aco_tsp.py`)
  - `SAParams` (`sa_tsp.py`)

---

## 📜 License

This project is intended for **academic and educational use**.
