import numpy as np
import matplotlib.pyplot as plt
import os
import math

n_pop = 10
# Load the flattened data from the text file
JOB_NAME = 'GAlgTestWholeFinal007'
filename_scores = JOB_NAME + '_Scores'
filename_curvatures = JOB_NAME + '_Curvatures'

def extract_data_from_file(filename):
    current_directory = os.getcwd()

    # Join the current directory with the file name
    filepath = os.path.join(current_directory, JOB_NAME)
    filepath = os.path.join(filepath, filename)

    # Load the file directly without changing the directory
    return np.loadtxt(filepath)

flattened_data = extract_data_from_file(filename_scores)
flattened_data_curvatures = extract_data_from_file(filename_curvatures)

# Calculate the number of generations
num_generations = math.ceil(len(flattened_data) / n_pop)

# Initialize arrays to store aggregated data
average_values = np.zeros(num_generations)
min_values = np.zeros(num_generations)
min_so_far = np.inf
min_values_so_far = []

# Calculate average and min for each generation
for i in range(num_generations):
    start_index = i * n_pop
    end_index = min((i + 1) * n_pop, len(flattened_data))
    segment = flattened_data[start_index:end_index]
    
    average_values[i] = np.mean(segment)
    min_values[i] = np.min(segment)
  
    # Check if the minimum value in the current segment is less than the overall minimum so far
    if min_values[i] < min_so_far:
        min_values_so_far.append(min_values[i])
        min_so_far = min_values[i]
    else:
        min_values_so_far.append(np.nan)

# Generate an array of integers for the x-axis (representing generations)
x_values = np.arange(1, num_generations + 1)

# Plot the average and min values for each generation
plt.plot(x_values, average_values, color='blue', label='Average', marker='o', linewidth=2, markersize=8)
plt.plot(x_values, min_values, color='red', label='Min', marker='o', linewidth=2, markersize=8)

# Plot the minimum values encountered so far
min_indices = np.where(~np.isnan(min_values_so_far))[0]
min_values_so_far = np.array(min_values_so_far)[~np.isnan(min_values_so_far)]
plt.scatter(min_indices + 1, min_values_so_far, color='green', label='Min So Far', s=100, zorder=3)

# Format the title
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title(f'Pop: {n_pop}, Gen: {num_generations}, Target Curvature: $\\kappa = 0.05$', fontsize=16)

# Plot formatting
plt.xlabel('Generation', fontsize=14)
plt.ylabel('Fitness function', fontsize=14)  # Set y-axis label
plt.grid(True, zorder=1)  # Push grid to the back
plt.legend(fontsize=14)

# Save the plot as PDF with filename based on plot title
filename = f'{JOB_NAME}b_Population_{n_pop}_Generations_{num_generations}_Target_Curvature_0.05.pdf'
plt.tight_layout()
plt.savefig(filename)

plt.show()
