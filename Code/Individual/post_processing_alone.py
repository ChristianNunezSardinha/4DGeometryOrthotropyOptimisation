import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit

JOB_NAME = 'GAlgTestWholeFinal006-25-1'
# 'ConvergenceTestnow2' is for convergence test 
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
        ax.scatter(x_0, y_0, z_0, s=30, alpha=1.0)
        ax.scatter(x_1, y_1, z_1, s=30, color='red', alpha=1.0)
        ax.set_xlabel('x[m]', labelpad=14)
        ax.set_ylabel('y[m]', labelpad=14)
        ax.set_zlabel('z[m]', labelpad=14)
        ax.scatter(curvature_list_x, curvature_list_y, curvature_list_z, s= 30, color = 'black', alpha = 1.0)
        ax.legend(['Undeformed', 'Deformed', 'Selected triangle side'])
        plt.tight_layout()
        plt.show()

        #plt.scatter(x_0, z_0, color = 'green', s=1)
        plt.scatter(curvature_list_x, curvature_list_z, color='blue', s=30)
        h = curvature_list_z[len(curvature_list_z) // 2]
        x_plot = curvature_list_x[len(curvature_list_z) // 2]
        plt.scatter(x_plot, h, color='red', s=60)
        plt.xlabel('x [m]', labelpad=14, fontsize=16)  # Adjust fontsize here
        plt.ylabel('z [m]', labelpad=14, fontsize=16)  # Adjust fontsize here
        plt.grid(True)
        plt.legend(['Triangle side', 'Middle point'], fontsize=16)  # Adjust fontsize here
        plt.xticks(fontsize=16)  # Adjust fontsize of xticks
        plt.yticks(fontsize=16)  # Adjust fontsize of yticks

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

CalculateCurvature(JOB_NAME, plot = True)

# TIMOSHENKO FORMULA
ta = 1
tp = 2
t = tp/ta
delta_MC = 0.552
delta_beta = 0.2156 - 0.0171 # which parameters should I subtract if the material is orthotropic?
e = 6682/679
k_timoshenko = (6*delta_beta*delta_MC*(1+t)**2) / ((ta+tp) * (3* (1+t)**2 + (1+t) * (t**2 + (1/(t * e)))))

length = 20
MESH_SIZE_ARRAY = np.linspace(0.5,2,length)
active_thickness_array = np.logspace(0, 1, length)
passive_thickness_array = np.logspace(0, 1, length) * 2

def ConvergencePlotTest(JOB_NAME, length=length, MESH_SIZE_ARRAY= MESH_SIZE_ARRAY):
    calc_curv_array = np.zeros(length)
    circle_curv_array = np.zeros(length)
    for i in range(0,length):
        string = JOB_NAME + str(i)
        #print(string)
        calc_curv, circle_curv = CalculateCurvature(string)
        print(calc_curv)
        print('Timoshenko Curvature: ', k_timoshenko)
        calc_curv_array[i] = calc_curv
        circle_curv_array[i] = circle_curv
    plt.plot(MESH_SIZE_ARRAY, calc_curv_array)
    #timoshenko_array = np.linspace(k_timoshenko, k_timoshenko, length)
    #plt.plot(MESH_SIZE_ARRAY, timoshenko_array)
    #plt.scatter(1, k_timoshenko)
    #plt.plot(MESH_SIZE_ARRAY, circle_curv_array)
    
    plt.title('Curvature of cantilever beam of length = 10mm')
    plt.xlabel('Mesh size')
    plt.ylabel('Curvature [mm^-1]')
    legend_string_parv = JOB_NAME + 'Model curvature using Parlevliet et al.'
    legend_string_circ = JOB_NAME + 'Model curvature using circle-fit module'
    #plt.legend(legend_string_parv)
    plt.show()

#ConvergencePlotTest(JOB_NAME)
'''
ta = 5
tp = 5
t = tp/ta
k_timoshenko = (6*delta_beta*delta_MC*(1+t)**2) / ((ta+tp) * (3* (1+t)**2 + (1+t) * (t**2 + (1/(t * e)))))
'''
#print(CalculateCurvature(JOB_NAME+str(3), plot=False))

def ThicknessPlotTest(JOB_NAME, length = 20, timoshenko = True):
    calc_curv_array = np.zeros(length)
    timo_curv_array = np.zeros(length)
    circle_curv_array = np.zeros(length)
    active_thickness_array = np.logspace(0, 1, length)
    passive_thickness_array = np.logspace(0, 1, length) * 2
    #print(active_thickness_array)
    for i in range(0,length):
        string = JOB_NAME + str(i)
        #print(string)
        calc_curv, circle_curv = CalculateCurvature(string)
        ta = active_thickness_array[i]
        tp = passive_thickness_array[i]
        t = tp/ta
        k_timoshenko = (6*delta_beta*delta_MC*(1+t)**2) / ((ta+tp) * (3* (1+t)**2 + (1+t) * (t**2 + (1/(t * e)))))
        calc_curv_array[i] = calc_curv
        circle_curv_array[i] = circle_curv
        timo_curv_array[i] = k_timoshenko
        #print(JOB_NAME + str(i))
        print(calc_curv)
        print('Timoshenko Curvature: ', k_timoshenko)

    #plot the curve against thickness
        
    
    if timoshenko:
        plt.plot(active_thickness_array, timo_curv_array)
    plt.plot(active_thickness_array, calc_curv_array)
    #plt.plot(active_thickness_array, circle_curv_array)
    plt.title('Curvature of cantilever beam of $L = 10mm$')
    plt.xlabel('Active thickness $[mm]$')
    plt.ylabel('Curvature $[mm^-1]$')
    legend_string_parv = JOB_NAME + 'Model curvature using Parlevliet et al.'
    legend_string_circ = JOB_NAME + 'Model curvature using circle-fit module'
    plt.legend([legend_string_parv, 'Timoshenko Curvature', legend_string_circ])
    

    #h = curvature_list_z[len(curvature_list_z)//2]
    #L = 100
    #k = (8*h)/(L**2 + 4*h**2)
    #print(k)
'''
ThicknessPlotTest(JOB_NAME, timoshenko=True)
ThicknessPlotTest('CantileverThicknessTest_partitiontruequad', timoshenko=False)
ThicknessPlotTest('CantileverThicknessTest_partitiontri', timoshenko=False)
legend_string_parv = 'No partition: Parlevliet et al.'
legend_string_circ = 'No partition: circle-fit'
legend21 = 'Partition' + 'Parlevliet et al.' + 'Tri elements'
legend22 = 'Partition' + 'Circle-fit module' + 'Tri elements'
legend31 = 'Partition' + 'Parlevliet et al.' +'Quad elements'
plt.legend([ 'Timoshenko Bilayer', legend_string_parv, legend21, legend31])
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Set limits for the x-axis and y-axis to zoom in
plt.xlim(1.49, 1.51)
plt.ylim(0.0332, 0.0339)
'''
# Add grid
plt.grid(True)
plt.tight_layout()
# Save the figure as PDF
plt.savefig('thickness_plot_zoomed.pdf')

# Show the plot
plt.show()