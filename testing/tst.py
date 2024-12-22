import ee
import numpy as np
import matplotlib.pyplot as plt

ee.Authenticate()
ee.Initialize(project='7')

lsmt = ee.ImageCollection("CSIC/SPEI/2_9")
temp_image = lsmt.sort('system:time_start', False).first()
temperature_band = temp_image.select('Tmean')

vis_params = {
    'min': -10,
    'max': 50,
    'palette': ['blue', 'green', 'yellow', 'red']
}

temperature_array = temperature_band.visualize(min=vis_params['min'], max=vis_params['max'], palette=vis_params['palette']) \
    .clip(temperature_band.geometry()) \
    .getMapId()

url = temperature_array['tile_fetcher'].url_format

import requests
from io import BytesIO
from PIL import Image

response = requests.get(url)
img = Image.open(BytesIO(response.content))

plt.figure(figsize=(10, 8))
plt.imshow(img)
plt.colorbar()
plt.title('Temperature Map')
plt.axis('off')
plt.show()
