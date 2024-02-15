import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

output_filename = 'Uresults.txt'

input_file_path = output_filename
loaded_data = np.loadtxt(input_file_path)
x = loaded_data[:, 0]
y = loaded_data[:, 1]
z = loaded_data[:, 2]

fig = plt.figure()
ax = plt.axes(projection ='3d')
ax.scatter(x, y, z, s= 1)
ax.set_title('3D line plot geeks for geeks')
plt.show()
