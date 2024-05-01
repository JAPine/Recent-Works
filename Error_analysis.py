import matplotlib.pyplot as plt
import numpy as np
import os

# Load data from file
filename = input("Enter the filename to load spectrum data from: ")
data = np.loadtxt(filename)

x = data[:, 0]
y = data[:, 1]

# Define the start and end points for each background region along the x-axis
region_points = [[0, 64], [64, 112], [112, len(x) - 1]]

# Initialize background array
background = np.zeros_like(y)

# Construct background lines for each region
for region in region_points:
    start_index, end_index = region
    region_x = x[start_index:end_index + 1]
    region_y = y[start_index:end_index + 1]
    # Create a line connecting the first and last points of the region
    slope = (region_y[-1] - region_y[0]) / (region_x[-1] - region_x[0])
    intercept = region_y[0] - slope * region_x[0]
    background[start_index:end_index + 1] = slope * region_x + intercept

# Calculate sigma array
sigma = float(input("Enter the value of sigma: "))
sigma_array = np.zeros_like(y)
sigma_array[y > background + 2 * sigma] = sigma

# Calculate +/- sigma curves
y_plus = y + sigma_array
y_minus = y - sigma_array

# Save data to files
filename_without_extension = os.path.splitext(filename)[0]

# Save data to files with appended filename
np.savetxt(f"yplus_{filename_without_extension}.txt", y_plus)
np.savetxt(f"yminus_{filename_without_extension}.txt", y_minus)
np.savetxt(f"x_{filename_without_extension}.txt", x)

# Plot curves
plt.plot(x, y, 'black', label='Original Spectrum')
plt.plot(x, y_minus, 'r:', label='Spectrum - sigma')
plt.plot(x, y_plus, 'b:', label='Spectrum + sigma')
plt.plot(x, background, 'orange', label='Background')
plt.xlabel('Binding Energy ($eV$)')
plt.ylabel('Counts')
plt.title('Spectrum Error Analysis')
plt.legend()
plt.grid(True)
plt.show()
