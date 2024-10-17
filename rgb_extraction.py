import numpy as np
import pandas as pd
from PIL import Image

# Function to extract RGB values and save as CSV
def extract_rgb(image_path, csv_output_path):
    # Open the image using PIL
    img = Image.open(image_path)

    # Convert the image to RGB if it's not already in that format
    img = img.convert("RGB")

    # Get the size of the image
    width, height = img.size

    # Create an empty list to store the RGB values
    rgb_values = []

    # Loop through each pixel and extract RGB values
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            rgb_values.append([x, y, r, g, b])

    # Convert the list to a Pandas DataFrame
    df = pd.DataFrame(rgb_values, columns=["X", "Y", "R", "G", "B"])

    # Save the DataFrame to a CSV file
    df.to_csv(csv_output_path, index=False)
    print(f"RGB values saved to {csv_output_path}")

file = "image_name.jpg"
image_path = file  # Path to your JPEG image
csv_output_path = "output_rgb_values.csv"  # CSV output path

extract_rgb(image_path, csv_output_path)
