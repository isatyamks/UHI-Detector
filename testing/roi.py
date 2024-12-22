import ee

ee.Authenticate()

# Initialize the library.
ee.Initialize(project='')

# Define an example region of interest (ROI)
roi = ee.Geometry.Rectangle([72.5, 18.5, 73.5, 19.5])  # Coordinates for a rectangle

# Load a dataset (e.g., Sentinel-2 surface reflectance)
dataset = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterDate('2024-01-01', '2024-01-31') \
    .filterBounds(roi) \
    .sort('CLOUD_COVER')

# Get the least cloudy image
least_cloudy = dataset.first()

# Print some information about the image
info = least_cloudy.getInfo()
print("Image Information:", info)

# Visualize specific bands (e.g., RGB)
rgb_image = least_cloudy.visualize(
    bands=['B4', 'B3', 'B2'],  # Red, Green, Blue bands
    min=0, max=3000
)

# Export the image to Google Drive (requires GEE account)
export_task = ee.batch.Export.image.toDrive(
    image=rgb_image,
    description='Sentinel2_RGB_Export',
    folder='EarthEngine',
    fileNamePrefix='Sentinel2_January_2024',
    region=roi.getInfo()['coordinates'],
    scale=10,  # Spatial resolution in meters
    maxPixels=1e8
)

export_task.start()
print("Export task started. Check Google Drive for the result.")

# Example visualization URL
map_url = least_cloudy.getMapId({
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 3000
})


print("Map visualization URL:", map_url)
