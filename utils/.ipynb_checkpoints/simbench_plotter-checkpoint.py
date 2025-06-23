import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Literal

# Read SimBench CSV with proper time parsing
def _read_simbench_csv(fp: str | Path) -> pd.DataFrame:
    """
    Read a SimBench CSV, normalize 'time' column, and parse European datetime format.
    """
    df = pd.read_csv(fp, sep=";")
    time_col = [col for col in df.columns if col.lower() == "time"]
    if not time_col:
        raise ValueError("No 'time' column found.")
    df.rename(columns={time_col[0]: "time"}, inplace=True)
    df["time"] = pd.to_datetime(df["time"], dayfirst=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

#  Plot summed active or reactive load over time
def plot_simbench_total_load_over_time(
    fp: str | Path,
    kind: Literal["pload", "qload"] = "pload",
    start_time: str | None = None,
    end_time: str | None = None,
    max_points: int = 500,
):
    """
    Plot the total (summed) load over time for active or reactive load.
    """
    df = _read_simbench_csv(fp)

    if start_time:
        df = df[df["time"] >= pd.to_datetime(start_time)]
    if end_time:
        df = df[df["time"] <= pd.to_datetime(end_time)]

    cols = [c for c in df.columns if c.endswith(f"_{kind}")]
    if not cols:
        raise ValueError(f"No '{kind}' columns found in file.")

    df["total"] = df[cols].sum(axis=1)

    if len(df) > max_points:
        step = max(1, len(df) // max_points)
        df = df.iloc[::step]

    plt.figure(figsize=(12, 6))
    plt.plot(df["time"], df["total"], label=f"Total {kind.upper()}", color="tab:blue")
    label = "Active" if kind == "pload" else "Reactive"
    plt.xlabel("Time")
    plt.ylabel("Total Power (MW)")
    plt.title(f"Total {label} Load Over Time\n{start_time or 'Start'} → {end_time or 'End'}")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

# Max power per renewable type in RES profile
def plot_simbench_max_energy_by_category(
    fp: str | Path,
    start_time: str | None = None,
    end_time: str | None = None,
    max_points: int = 500,
):
    """
    Plot max RES output per energy type (PV, WP, BM, Hydro) within an optional time window.
    """
    df = _read_simbench_csv(fp)

    if start_time:
        df = df[df["time"] >= pd.to_datetime(start_time)]
    if end_time:
        df = df[df["time"] <= pd.to_datetime(end_time)]

    if len(df) > max_points:
        step = max(1, len(df) // max_points)
        df = df.iloc[::step]

    prefix_map = {"PV": "Solar", "WP": "Wind", "BM": "Biomass", "Hydro": "Hydro"}

    max_by_type = {}
    for prefix, label in prefix_map.items():
        cols = [col for col in df.columns if col.startswith(prefix)]
        if not cols:
            print(f"[!] No data found for {label}")
            continue
        max_val = df[cols].max().max()
        max_by_type[label] = round(max_val, 3)

    if not max_by_type:
        raise ValueError("No renewable energy types found.")

    # Plot
    plt.figure(figsize=(10, 6))
    ax = pd.Series(max_by_type).sort_values(ascending=False).plot(
        kind='bar', color='skyblue', edgecolor='black'
    )

    plt.ylabel("Max Power (MW)")
    plt.title(f"Maximum RES Output by Type\n{start_time or 'Start'} → {end_time or 'End'}")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{height} MW",
                    xy=(p.get_x() + p.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()
