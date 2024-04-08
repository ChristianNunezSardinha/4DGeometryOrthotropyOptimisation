import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Load data
partition_filename = 'C:\Temp/geometrypartitionTriangle.txt'
input_file_path = partition_filename
loaded_data = np.loadtxt(input_file_path, delimiter=',')
x = loaded_data[:, 0]
y = loaded_data[:, 1]

# Define the list of angles
JOB_NAME = 'GAlgTestWholeFinal002'
angles = [-83.0, -37.0, 75.0, -12.0, -39.0, -87.0, 90, -53.0, 61.0, 90, -21.0, 10.0, 90, -84.0, 53.0, -34.0, 79.0, 8.0, -77.0, -9.0, -29.0, -51.0, -49.0, 6.0, 63.0, -70.0, -40.0, -10.0]
#JOB_NAME = 'GAlgTestWholeFinal001_only15'
#angles = [9.0, 4.0, -12.0, -1.0, 0.0, 15, -6.0, -13.0, 0.0, 0.0, -11.0, 2.0, -14.0, -15, -11.0, 3.0, -4.0, 6.0, 7.0, -13.0, 12.0, -5.0, -11.0, -10.0, 10.0, 7.0, -9.0, -11.0]
JOB_NAME = 'GAlgTestWholeFinal003'
#angles = [34.0, -1, -71.0, 40, 90, 40, 13.0, 64.0, 90, 90, 75.0, 54.0, 51, 90, -90, -90, -7.0, -29.0, 81.0, -59.0, 3.0, -43.0, 35.0, -13.0, 20.0, 40.0, -7.0, -15.0]
angles = [-89.0, -61.0, 32.0, -66.0, 54.0, 88, -41.0, 59.0, -59.0, 8.0, -15.0, -90, -90, -90, -89.0, -29.0, -8, -5.0, -17, -37.0, -47.0, -78, -26.0, 0.0, -90.0, 39.0, -40.0, -31.0]
JOB_NAME = 'GAlgTestWholeFinal004'
angles = [80.0, 90, -30.0, 50.0, 60.0, -84.0, 32.0, -6.0, 44.0, -90, 77.0, 68.0, 23.0, 28, 62.0, -37.0, -77.0, 18.0, 30.0, -29.0, -48.0, -44.0, 67, -38.0, 49.0, 0.0, -90, 53]
JOB_NAME = 'GAlgTestWholeFinal005'
angles = [44.0, 21.261670298556492, -21.0, 49.27564927611034, 39.0, -90, 24.07968978321703, 21.573593128807154, 84.0, -83.0, -15.0, -90, -85.79898987322332, -83.75735931288071, 21.36217536194483, -59.073968315767985, -26.093313458899043, 5.899494936611664, -24.13856428626275, -73.76776695296637, -88.1686582633232, -77.76955262170047, 14.0, -7.142135623730949, -51.4454498530759, 12.955389395398896, -90, 20.87651422105797]
JOB_NAME = 'GAlgTestWholeFinal006'
angles = [-9.552453856777152, 83.16463444853004, -53.176535254457974, 5.966995473559814, 38.94466072449055, 71.32475687220236, 90, 29.34863698813652, -77.9857966518515, 86.80004318760548, 31.48415965124427, -86.70016835446278, 49.872303488463906, 90, -6.439053907421172, -15.190913303630058, 16.607252920728307, -20.925260402660953, -4.982900436158023, 3.6859909276956664, -51.90774882410944, -8.85084741226698, 37.363327088435085, -22.039297106451816, 51.91203495909316, -48.037628316813766, 34.37603886008833, -27.791294954652592]
#JOB_NAME = 'GAlgTestWholeFinal007'
#angles = 

# Reshape x and y into triangles
triangles = np.stack([x.reshape(-1, 4), y.reshape(-1, 4)], axis=2)

# Function to calculate centroid of a triangle
def centroid(triangle):
    return np.mean(triangle[:-1], axis=0)

# Function to calculate endpoint of line based on angle and centroid
def calculate_endpoints(centroid, angle, arrow_size):
    angle_rad = np.deg2rad(angle)
    dx = arrow_size * np.cos(angle_rad)
    dy = arrow_size * np.sin(angle_rad)
    x1 = centroid[0] - dx/2
    y1 = centroid[1] - dy/2
    x2 = centroid[0] + dx/2
    y2 = centroid[1] + dy/2
    return x1, y1, x2, y2

# Define arrow size
arrow_size = 8

# Plot triangles and centroids
fig, ax = plt.subplots()

for triangle in triangles:
    ax.add_patch(Polygon(triangle, closed=True, fill=None, edgecolor='black'))

centroids = np.array([centroid(triangle) for triangle in triangles])

# Plot angles for the first half of the angles list (Bottom Layer)
for centroid, angle in zip(centroids, angles[:len(angles)//2]):
    x1, y1, x2, y2 = calculate_endpoints(centroid, angle, arrow_size)
    ax.plot([x1, x2], [y1, y2], color='blue', linewidth=4)

# Plot angles for the second half of the angles list (Top Layer)
for centroid, angle in zip(centroids, angles[len(angles)//2:]):
    x1, y1, x2, y2 = calculate_endpoints(centroid, angle, arrow_size)
    ax.plot([x1, centroid[0]], [y1, centroid[1]], color='red', linewidth=4)
    ax.plot([x2, centroid[0]], [y2, centroid[1]], color='red', linewidth=4)

ax.set_xlabel('x [mm]', fontsize=14)
ax.set_ylabel('y [mm]', fontsize=14)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
#ax.set_aspect(16/9)  # Set aspect ratio to 16:9

# Create legend handles and labels
bottom_handle, = ax.plot([], [], color='blue', linewidth=4, label='Bottom Layer')
top_handle, = ax.plot([], [], color='red', linewidth=4, label='Top Layer')

# Create legend
ax.legend(handles=[bottom_handle, top_handle], loc='upper right', fontsize=14)
plt.tight_layout()

# Save the figure as PDF with job name
plt.savefig(f"{JOB_NAME}_triangleplotter.pdf")

plt.show()
