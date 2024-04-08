import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit

JOB_NAME = 'ConvergenceTestA'

def extract_initial_coordinates_from_inp(JOB_NAME, inp_file_path):
    #JOB_NAME = 'Job-Cantilever-SecondAccuracyOFF'
    output_filename = JOB_NAME + 'Uresults.txt'

    input_file_path = output_filename
    x_coordinates = []
    y_coordinates = []
    z_coordinates = []

    with open(inp_file_path, 'r') as inp_file:
        lines = inp_file.readlines()
        read_coordinates = False

        for line in lines:
            if line.startswith('*Node'):
                read_coordinates = True
                continue

            if read_coordinates and line.startswith('*'):
                break  # Stop reading when encountering a new section

            if read_coordinates:
                parts = line.split(',')
                x_coordinates.append(float(parts[1]))
                y_coordinates.append(float(parts[2]))
                z_coordinates.append(float(parts[3]))

    return x_coordinates, y_coordinates, z_coordinates

def CalculateCurvature(JOB_NAME, plot = False):
    input_file_path = JOB_NAME + 'Uresults.txt'
    loaded_data = np.loadtxt(input_file_path)

    # Example usage:
    inptype_file_path = JOB_NAME + '.inp'  # Replace with the actual path to your .inp file
    x_0, y_0, z_0 = extract_initial_coordinates_from_inp(JOB_NAME, inptype_file_path)

    ux_0 = np.transpose(loaded_data[:, 0])
    uy_0 = np.transpose(loaded_data[:, 1])
    uz_0 = np.transpose(loaded_data[:, 2])

    x_1 = x_0 + ux_0
    y_1 = y_0 + uy_0
    z_1 = z_0 + uz_0

    curvature_list_x = []
    curvature_list_z = []
    curvature_list_y = []
    index_list = []
    for a in range (0, len(y_0)):
        if (y_0[a] > -0.2) & (y_0[a] < 0.2):
            curvature_list_x.append(x_1[a])
            curvature_list_z.append(z_1[a])
            curvature_list_y.append(y_1[a])
            index_list.append(a)
    sorted_coordinates = sorted(zip(curvature_list_x, curvature_list_y, curvature_list_z), key=lambda coord: coord[0])
    curvature_list_x, curvature_list_y, curvature_list_z = zip(*sorted_coordinates)
    '''
    x_middle_index = len(x_0)//2
    x_middle = x_0[x_middle_index]
    z_middle = z_1[x_middle_index]

    z_1_zeroList = z_1[index_list[6]]
    print(z_1_zeroList)
    '''
    if plot:
        fig = plt.figure()
        ax = plt.axes(projection ='3d')
        ax.scatter(x_0, y_0, z_0, s= 3)
        ax.scatter(x_1, y_1, z_1, s = 3, color = 'red')
        ax.set_xlabel('x[m]', labelpad=10)
        ax.set_ylabel('y[m]', labelpad=10)
        ax.set_zlabel('z[m]', labelpad=10)
        #ax.scatter(curvature_list_x, curvature_list_y, curvature_list_z, s= 3, color = 'black')
        plt.show()
        #plt.scatter(x_0, z_0, color = 'green', s=1)
        plt.scatter(curvature_list_x, curvature_list_z, color = 'blue', s=3)
        #plt.plot(x,z, color='blue')
        h = curvature_list_z[len(curvature_list_z)//2]
        x_plot = curvature_list_x[len(curvature_list_z)//2]
        plt.scatter(x_plot,h, color='red')
        plt.show()

    h = curvature_list_z[len(curvature_list_z)//2]
    L = 10
    curvature = (8*h)/(L**2 + 4*h**2)#
    average_curvature = curvature
    if len(curvature_list_z) % 2 == 0:

        h_0 = curvature_list_z[len(curvature_list_z)//2-1]
        curvature_0 = (8*h_0)/(L**2 + 4*h_0**2)
        average_curvature = (curvature + curvature_0) /2
    #from circle_fit import taubinSVD
    #point_coordinates = np.array(list(zip(curvature_list_x, curvature_list_z)))
    #xc, yc, r, sigma = taubinSVD(point_coordinates)
    #curvature_fit = 1/r
    #print('Circle fit: ', curvature)
    #print(k)
    return average_curvature, 1
