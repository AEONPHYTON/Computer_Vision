import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to plot the image from the CSV data
def plot_image_from_csv(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Get the image dimensions
    max_x = df['X'].max() + 1
    max_y = df['Y'].max() + 1

    # Create an empty image array
    img_array = np.zeros((max_y, max_x, 3), dtype=np.uint8)

    # Loop through the dataframe and assign RGB values to the image array
    for index, row in df.iterrows():
        x = row['X']
        y = row['Y']
        r = row['R']
        g = row['G']
        b = row['B']
        img_array[y, x] = [r, g, b]

    print(img_array)
    
    # Plot the image using matplotlib
    plt.imshow(img_array)
    plt.title(f"{csv_path}")
    plt.xlabel(f"X ({max_x} px)")
    plt.ylabel(f"Y ({max_y} px)")
    plt.show()

# Example usage
csv_path = "output_rgb_values.csv"  # Path to your CSV file
plot_image_from_csv(csv_path)
