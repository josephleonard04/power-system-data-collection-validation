import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plot_total_elmas_load(
    filepath="raw/Time_series_18_clusters.csv",
    start_time=None,
    end_time=None,
    max_points=1000
):
    # Load CSV
    df = pd.read_csv(filepath)

    # Parse datetime and set index
    df["Time"] = pd.to_datetime(df["Time"])
    df.set_index("Time", inplace=True)

    # Ensure all cluster columns are numeric
    df = df.apply(pd.to_numeric, errors="coerce")

    # Filter by time range
    if start_time:
        df = df[df.index >= pd.to_datetime(start_time)]
    if end_time:
        df = df[df.index <= pd.to_datetime(end_time)]

    # Fast downsampling using iloc (assumes regular time intervals)
    if len(df) > max_points:
        step = max(1, int(len(df) / max_points))
        df = df.iloc[::step]

    # Compute total load
    total_load = df.sum(axis=1)

    # Plot
    plt.figure(figsize=(24, 6))
    ax = total_load.plot()
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))  # no scientific notation
    plt.title("Total Active Load – ELMAS Dataset")
    plt.xlabel("Time")
    plt.ylabel("Total Load (kWh)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()