import ee
import numpy as np
import matplotlib.pyplot as plt

# Initialize the Earth Engine API
ee.Initialize(project='')

# Define Area of Interest (AOI) - Example: Rectangle
aoi = ee.Geometry.Rectangle([77.5, 28.4, 77.6, 28.5])  # Change to your coordinates

# Select a dataset - Example: MODIS Land Surface Temperature
dataset = ee.ImageCollection('MODIS/006/MOD11A1') \
    .filterDate('2023-01-01', '2023-12-31') \
    .filterBounds(aoi)

# Reduce data to mean temperature over the AOI
time_series = dataset.map(lambda img: img.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=aoi,
    scale=1000
).set('date', img.date().format('YYYY-MM-dd')))

# Convert to a list and fetch it
time_series_list = time_series.aggregate_array('date').getInfo()
temp_values = [ee.Number(img.get('LST_Day_1km')).getInfo() for img in time_series.getInfo()]

# Print a segment of the graph in ASCII format
# Normalize values for console display
min_temp, max_temp = min(temp_values), max(temp_values)
normalized = [(t - min_temp) / (max_temp - min_temp) for t in temp_values]

print("\nGraph Segment (ASCII Representation):")
rows = 10  # Number of ASCII rows
for level in np.linspace(1, 0, rows):
    row = ''.join('*' if t >= level else ' ' for t in normalized[:20])  # First 20 points
    print(row)

# Optional: Visualize the entire graph with Matplotlib
dates = [time_series_list[i] for i in range(len(temp_values))]
plt.plot(dates, temp_values, label="Temperature (LST)")
plt.xticks(rotation=45)
plt.title("Land Surface Temperature Over Time")
plt.legend()
plt.show()
