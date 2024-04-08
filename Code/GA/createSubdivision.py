import numpy as np
from matplotlib import pyplot as plt
import pygmsh

# Copy-paste this in SendToAbaqus before running code. 
POINT_1 = (0.0, 0.0)
POINT_2 = (10.0, 0.0)
#POINT_3 = (0.0, 100.0)
POINT_3 = (10.0, 1.0)
POINT_4 = (0.0, 1.0)
#GEOMETRY = [POINT_1, POINT_2, POINT_3]
GEOMETRY = [POINT_1, POINT_2, POINT_3, POINT_4]
partition_filename = 'C:\Temp/cantilevergeometrypartition.txt'

## Trying square geometry
'''
POINT_1 = (0.0, 0.0)
POINT_2 = (100.0, 0.0)
POINT_3 = (100.0, 10.0)
POINT_4 = (0.0, 10.0)
GEOMETRY = [POINT_1, POINT_2, POINT_3, POINT_4]
'''
# Creating arrays with partition coordinates
def CreateSubdivision(GEOMETRY, plot=False):

    # calling pygmsh to generate a mesh.
    with pygmsh.geo.Geometry() as geom:
        geom.add_polygon(
            GEOMETRY,
            mesh_size=1, # IMPORTANT VARIABLE
        )
        mesh = geom.generate_mesh()   
    
    # transforming mesh data into x and y arrays. Triangles are stored as:
    # x = [xtriangle1_corner1, xtriangle1_corner2, xtriangle1_corner3, xtriangle1_corner1, xtriangle12_corner1...] 
    # y = [ytriangle1_corner1, ytriangle1_corner2, ytriangle1_corner3, ytriangle1_corner1, ytriangle12_corner1...] 
    points = mesh.points
    cells = mesh.cells
    triangles_block = next(cell_block for cell_block in cells if cell_block.type == "triangle")
    triangles = triangles_block.data
    connection_list_x = []
    connection_list_y = []

    for triangle_subdivision in triangles:
        triangle_points = points[triangle_subdivision]
        triangle_points = np.vstack((triangle_points, triangle_points[0])) 
        connection_list_x.extend(triangle_points[:,0])
        connection_list_y.extend(triangle_points[:,1])
        plt.plot(triangle_points[:, 0], triangle_points[:, 1], color='black')

    if plot:
        plt.plot(triangle_points[:, 0], triangle_points[:, 1], color='black', linewidth=2, markersize=8)
        plt.scatter(connection_list_x, connection_list_y, label="Mesh Points", color = 'red', marker="x", s=50)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.xlabel('x [mm]', fontsize=14)
        plt.ylabel('y [mm]', fontsize=14)
        plt.tight_layout()
        plt.show()

    return connection_list_x, connection_list_y

# Saving a .txt file with partitions for ABAQUS

def GetTxtFile(GEOMETRY, output_filename):
    x, y = CreateSubdivision(GEOMETRY, plot = True)
    data = np.column_stack((x, y))
    np.savetxt(output_filename, data, delimiter=',', fmt='%.18e')
    print('File saved')

GetTxtFile(GEOMETRY, partition_filename)
