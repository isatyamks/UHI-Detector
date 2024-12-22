import ee
import numpy as np
import matplotlib.pyplot as plt

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize(project='7')

# Import the temperature dataset.
lsmt = ee.ImageCollection("CSIC/SPEI/2_9")

# Select a specific time frame (e.g., the most recent image in the collection).
temp_image = lsmt.sort('system:time_start', False).first()

# Select the desired band (e.g., 'Tmean' for temperature)
temperature_band = temp_image.select('Tmean')

# Define visualization parameters (you can adjust the range based on your data)
vis_params = {
    'min': -10,
    'max': 50,
    'palette': ['blue', 'green', 'yellow', 'red']
}

# Convert the image to a NumPy array
temperature_array = temperature_band.visualize(min=vis_params['min'], max=vis_params['max'], palette=vis_params['palette']) \
    .clip(temperature_band.geometry()) \
    .getMapId()

# Get the image URL and download it as a NumPy array
url = temperature_array['tile_fetcher'].url_format

# Using matplotlib to display the image
import requests
from io import BytesIO
from PIL import Image

response = requests.get(url)
img = Image.open(BytesIO(response.content))

# Display the image using matplotlib
plt.figure(figsize=(10, 8))
plt.imshow(img)
plt.colorbar()
plt.title('Temperature Map')
plt.axis('off')  # Remove axes for better visualization
plt.show()
