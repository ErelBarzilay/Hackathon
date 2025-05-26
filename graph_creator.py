import pandas as pd
import matplotlib.pyplot as plt

def plot_bus_trips_by_cluster(bus_data, cluster_name):
    # Ensure types are correct
    bus_data['trip_year'] = bus_data['trip_year'].astype(int)
    bus_data['trip_month'] = bus_data['trip_month'].astype(int)

    # Filter by the given cluster name
    filtered_data = bus_data[bus_data['cluster_nm'] == cluster_name]

    # Group by (year, month) and sum 'takin'
    monthly_takin = filtered_data.groupby(['trip_year', 'trip_month'])['takin'].sum().reset_index()

    # Create a datetime column for plotting
    monthly_takin['date'] = pd.to_datetime(
        monthly_takin['trip_year'].astype(str) + '-' + monthly_takin['trip_month'].astype(str).str.zfill(2)
    )

    # Sort by date
    monthly_takin.sort_values('date', inplace=True)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.scatter(monthly_takin['date'], monthly_takin['takin'], color='blue', alpha=0.7)
    plt.plot(monthly_takin['date'], monthly_takin['takin'], color='gray', linestyle='--', alpha=0.5)

    plt.title(f"Bus Trips in {cluster_name} Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total 'Takin' per Month")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"bus_trips_{cluster_name}.png")
    plt.show()

# Example usage
bus_data = pd.read_csv("data/bus_data.csv")
plot_bus_trips_by_cluster(bus_data, "צפון הנגב")
