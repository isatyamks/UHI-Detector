# import ee
# import geemap.core as geemap

# ee.Authenticate()
# ee.Initialize(project='')


# jan_2023_climate = (
#     ee.ImageCollection('ECMWF/ERA5_LAND/MONTHLY_AGGR')
#     .filterDate('2023-01', '2023-02')
#     .first()
# )



# m = geemap.Map(center=[30, 0], zoom=2)

# vis_params = {
#     'bands': ['temperature_2m'],
#     'min': 229,
#     'max': 304,
#     'palette': 'inferno',
# }
# m.add_layer(jan_2023_climate, vis_params, 'Temperature (K)')


# cities = ee.FeatureCollection([
#     ee.Feature(ee.Geometry.Point(10.75, 59.91), {'city': 'Oslo'}),
#     ee.Feature(ee.Geometry.Point(-118.24, 34.05), {'city': 'Los Angeles'}),
#     ee.Feature(ee.Geometry.Point(103.83, 1.33), {'city': 'Singapore'}),
# ])

# m.add_layer(cities, name='Cities')
# # 
import ee
import geemap
import matplotlib.pyplot as plt

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='7')

# Define a region of interest (ROI)
roi = ee.Geometry.Rectangle([-121.8, 37.0, -121.4, 37.3])  # Example: part of California

# Load a satellite image collection (Landsat 8)
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
    .filterBounds(roi) \
    .filterDate('2021-01-01', '2021-12-31') \
    .median()

# Calculate NDVI
ndvi = collection.normalizedDifference(['B5', 'B4'])  # Near-infrared (B5) and red (B4)

# Convert the image to a NumPy array for visualization
vis_params = {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}
ndvi_rgb = geemap.image_to_numpy(ndvi.visualize(**vis_params), region=roi, scale=30)

# Display the NDVI map using Matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(ndvi_rgb)
plt.title('NDVI Map')
plt.axis('off')
plt.show()

