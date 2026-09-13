import csv
import json
import os
import statistics
import time

import matplotlib.pyplot as plt

from part_a import generate_array

# Part (b): Generate input data.
# Arrays of increasing size, from 1,000 up to 10 million, each filled with
# random integers drawn uniformly from [1, X]. The same sizes and the same X
# are reused by part (c) and part (d) so results stay comparable across parts.
N_VALUES = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
X = 1_000_000

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "part_b")
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")


def summarize(n, x, arr, gen_time):
    return {
        "n": n,
        "x": x,
        "gen_time_sec": round(gen_time, 4),
        "min": min(arr),
        "max": max(arr),
        "mean": round(statistics.mean(arr), 2),
        "distinct_values": len(set(arr)),
        "distinct_ratio": round(len(set(arr)) / n, 4),
        "preview": arr[:10],
    }


def main():
    os.makedirs(PLOTS_DIR, exist_ok=True)

    rows = []
    sample_for_hist = None

    for n in N_VALUES:
        start = time.perf_counter()
        arr = generate_array(n, X)
        gen_time = time.perf_counter() - start

        row = summarize(n, X, arr, gen_time)
        rows.append(row)
        print(f"n={n:>9}  x={X}  gen_time={row['gen_time_sec']}s  "
              f"min={row['min']} max={row['max']} mean={row['mean']}  "
              f"distinct={row['distinct_values']} ({row['distinct_ratio']*100:.1f}%)  "
              f"preview={row['preview']}")

        # Keep a mid-sized dataset around to plot its distribution.
        if n == 100_000:
            sample_for_hist = arr

        del arr

    # Save summary table (small, safe to commit).
    csv_path = os.path.join(RESULTS_DIR, "summary_stats.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved summary table to {csv_path}")

    # Plot 1: dataset generation time vs input size.
    plt.figure()
    plt.plot(N_VALUES, [r["gen_time_sec"] for r in rows], marker="o")
    plt.xscale("log")
    plt.xlabel("Input size n")
    plt.ylabel("Generation time (s)")
    plt.title("Part (b): Dataset Generation Time vs n")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "generation_time.png"))
    plt.close()

    # Plot 2: value distribution for one representative dataset.
    plt.figure()
    counts, edges, _ = plt.hist(sample_for_hist, bins=50)
    plt.xlabel(f"Value (range 1 to {X:,})")
    plt.ylabel("Frequency")
    plt.title(f"Part (b): Value Distribution for n=100,000")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "distribution_n100000.png"))
    plt.close()

    # Plot 3: distinct-value ratio vs input size (side effect of fixing x).
    plt.figure()
    plt.bar([str(n) for n in N_VALUES], [r["distinct_ratio"] * 100 for r in rows])
    plt.xlabel("Input size n")
    plt.ylabel("Distinct values (% of n)")
    plt.title("Part (b): Value Saturation as n Grows Past x")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "distinct_ratio.png"))
    plt.close()

    print(f"Saved plots to {PLOTS_DIR}")

    # Persist the exact bin counts so the empirical histogram can be
    # reproduced (e.g. embedded in a report or slide) without re-shipping
    # the full 100,000-element array.
    hist_path = os.path.join(RESULTS_DIR, "distribution_n100000_bins.json")
    with open(hist_path, "w") as f:
        json.dump({
            "n": 100_000,
            "x": X,
            "bins": len(counts),
            "bin_edges": [round(e, 2) for e in edges.tolist()],
            "counts": [int(c) for c in counts.tolist()],
        }, f, indent=2)
    print(f"Saved histogram bin data to {hist_path}")


if __name__ == "__main__":
    main()
