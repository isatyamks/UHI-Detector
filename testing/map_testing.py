import ee
import numpy as np
import matplotlib.pyplot as plt

ee.Initialize(project='')

aoi = ee.Geometry.Rectangle([77.5, 28.4, 77.6, 28.5])

dataset = ee.ImageCollection('MODIS/006/MOD11A1') \
    .filterDate('2023-01-01', '2023-12-31') \
    .filterBounds(aoi)

time_series = dataset.map(lambda img: img.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=aoi,
    scale=1000
).set('date', img.date().format('YYYY-MM-dd')))

time_series_list = time_series.aggregate_array('date').getInfo()
temp_values = [ee.Number(img.get('LST_Day_1km')).getInfo() for img in time_series.getInfo()]

min_temp, max_temp = min(temp_values), max(temp_values)
normalized = [(t - min_temp) / (max_temp - min_temp) for t in temp_values]

print("\nGraph Segment (ASCII Representation):")
rows = 10
for level in np.linspace(1, 0, rows):
    row = ''.join('*' if t >= level else ' ' for t in normalized[:20])
    print(row)

dates = [time_series_list[i] for i in range(len(temp_values))]
plt.plot(dates, temp_values, label="Temperature (LST)")
plt.xticks(rotation=45)
plt.title("Land Surface Temperature Over Time")
plt.legend()
plt.show()
