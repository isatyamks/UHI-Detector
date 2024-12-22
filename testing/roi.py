import ee

ee.Authenticate()
ee.Initialize(project='')

roi = ee.Geometry.Rectangle([72.5, 18.5, 73.5, 19.5])

dataset = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterDate('2024-01-01', '2024-01-31') \
    .filterBounds(roi) \
    .sort('CLOUD_COVER')

least_cloudy = dataset.first()

info = least_cloudy.getInfo()
print("Image Information:", info)

rgb_image = least_cloudy.visualize(
    bands=['B4', 'B3', 'B2'],
    min=0, max=3000
)

export_task = ee.batch.Export.image.toDrive(
    image=rgb_image,
    description='Sentinel2_RGB_Export',
    folder='EarthEngine',
    fileNamePrefix='Sentinel2_January_2024',
    region=roi.getInfo()['coordinates'],
    scale=10,
    maxPixels=1e8
)

export_task.start()
print("Export task started. Check Google Drive for the result.")

map_url = least_cloudy.getMapId({
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 3000
})

print("Map visualization URL:", map_url)
