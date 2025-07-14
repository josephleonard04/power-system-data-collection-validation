import pandas as pd
import matplotlib.pyplot as plt

def _plot_total_load(fp, time_format, max_points=300):
    """
    Internal helper function to plot total load from a Zenodo dataset file.

    Parameters:
        fp (str): Path to CSV file (2016 or 2017 dataset).
        time_format (str): Explicit datetime format used in the file.
        max_points (int): Maximum number of points to display on the plot.
    """

    # Read just the header to detect timestamp column
    with open(fp, 'r', encoding='utf-8') as f:
        first_line = f.readline()
    columns = first_line.strip().split(';')
    time_col = next((col for col in columns if 'time' in col.lower()), None)

    if time_col is None:
        raise ValueError("Timestamp column not found. Expected something like 'Time stamp'.")

    # Load CSV
    df = pd.read_csv(fp, sep=';', encoding='utf-8')
    df.rename(columns={time_col: 'timestamp'}, inplace=True)

    # Clean and parse timestamp
    df['timestamp'] = (
        df['timestamp']
        .astype(str)
        .str.strip()
        .str.extract(r'([\d]{2}\.[\d]{2}\.[\d]{4} [\d]{2}:[\d]{2}:[\d]{2})')[0]
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'], format=time_format, errors='raise')

    # Set and sort index
    df = df.set_index('timestamp')
    df = df.sort_index()

    # Compute total load
    df['total_load'] = df.sum(axis=1)

    # Downsample if needed
    if len(df) > max_points:
        df_downsampled = df.iloc[::len(df)//max_points]
    else:
        df_downsampled = df

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(df_downsampled.index, df_downsampled['total_load'], label='Total Load (kW)', linewidth=1.5)
    plt.xlabel('Time')
    plt.ylabel('Total Load (kW)')
    plt.title(f'Total Industrial Load Over Full Year')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_zenodo_2016(fp, max_points=300):
    """
    Plot total load for the full year of 2016 dataset.
    """
    _plot_total_load(fp, time_format='%d.%m.%Y %H:%M:%S', max_points=max_points)

def plot_zenodo_2017(fp, max_points=300):
    """
    Plot total load for the full year of 2017 dataset.
    """
    _plot_total_load(fp, time_format='%d.%m.%Y %H:%M:%S', max_points=max_points)
