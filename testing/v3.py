# import ee
# import geemap
# import matplotlib.pyplot as plt

# # Authenticate and initialize Earth Engine
# ee.Authenticate()
# ee.Initialize(project='7')

# # Define a region of interest (ROI)
# roi = ee.Geometry.Rectangle([-121.8, 37.0, -121.4, 37.3])  # Example: part of California

# # Load a satellite image collection (Landsat 8)
# collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
#     .filterBounds(roi) \
#     .filterDate('2021-01-01', '2021-12-31') \
#     .median()

# # Calculate NDVI
# ndvi = collection.normalizedDifference(['B5', 'B4'])  # Near-infrared (B5) and red (B4)

# # Clip the NDVI image to the ROI
# ndvi_clipped = ndvi.clip(roi)

# # Visualize NDVI with color parameters
# vis_params = {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}
# ndvi_rgb = geemap.image_to_numpy(ndvi_clipped.visualize(**vis_params), scale=30)

# # Display the NDVI map using Matplotlib
# plt.figure(figsize=(10, 10))
# plt.imshow(ndvi_rgb)
# plt.title('NDVI Map')
# plt.axis('off')
# plt.show()


