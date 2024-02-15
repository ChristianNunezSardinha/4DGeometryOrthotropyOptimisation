import numpy as np
from matplotlib import pyplot as plt
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

########################################################################
# PARAMETERS TO CHANGE FOR TRIALS

#ITERATION_NUMBER = 10 all points must be connected from the previous one
partition = False
POINT_1 = (0.0, 0.0)
POINT_2 = (100.0, 0.0)
POINT_3 = (100.0, 10.0)
POINT_4 = (0.0, 10.0)
GEOMETRY = [POINT_1, POINT_2, POINT_3, POINT_4]
output_filename = 'C:\Temp/SubdivisionCoordinatesCantilever.txt'

########################################################################
# PARAMETERS FOR THE CODE
# General Data

MODEL_NAME = 'Model-1'
PART_NAME = 'Part-1'

# Extracting data from createSubdivision
input_file_path = output_filename
loaded_data = np.loadtxt(input_file_path, delimiter=',')
x = loaded_data[:, 0]
y = loaded_data[:, 1]
ACTIVE_ANGLE_ARRAY = np.linspace(90, 90, len(x)//4)

## Elastic material properties (not using passive at the moment)
# (quoted from Design of 3D and 4D printed continuous fibre composites via an evolutionary algorithm 
# and voxel-based Finite Elements: Application to natural fibre hygromorphs):
### Young's Modulus [N/mm^2]
E12_PASSIVE = 3000.0
E13_PASSIVE = 3000.0
E23_PASSIVE = 2700.0
E12_ACTIVE = 6682.0
E13_ACTIVE = 679.0
E23_ACTIVE = 679.0
### Poisson's Ratio [-]
MU12_PASSIVE = 0.3
MU13_PASSIVE = 0.3
MU23_PASSIVE = 0.15
MU12_ACTIVE = 0.523
MU13_ACTIVE = 0.523
MU23_ACTIVE = 0.279
### Shear Modulus
G12_PASSIVE = 600.0
G13_PASSIVE = 600.0
G23_PASSIVE = 580.0
G12_ACTIVE = 986.0
G13_ACTIVE = 986.0
G23_ACTIVE = 982.6
## Expansion
ALPHA_EXPANSION_PASSIVE = 0.01
ALPHA_EXPANSION_ACTIVE_12 = -0.0071
ALPHA_EXPANSION_ACTIVE_13 = 0.394
ALPHA_EXPANSION_ACTIVE_23 = 0.394
## Conductivity
ALPHA_CONDUCTIVITY_PASSIVE = 0.01
ALPHA_CONDUCTIVITY_ACTIVE = 100.0
## Specific Heat
SP_HEAT_PASSIVE = 1200.0
SP_HEAT_ACTIVE = 1800.0
## Density
DENSITY_PASSIVE = 1.6
DENSITY_ACTIVE = 1.5
# CreatePartition and CreateMaterialSubdivision()
PASSIVE_MATERIAL_NAME = 'Passive'
ACTIVE_MATERIAL_NAME = 'Active'
COMPOSITE_LAYUP_NAME = 'CompositeLayup-1'
THICKNESS_PASSIVE = 0.2
THICKNESS_ACTIVE = 0.1
ANGLEPLY_PASSIVE = 0.0
ANGLEPLY_ACTIVE = 90.0
# CreateAssembly()
ASSEMBLY_NAME = 'Assembly-1'
# CreateMesh()
MESH_SIZE = 1.0
# CreateStep()
STEP_NAME = 'Step-1'
STEP_INITIAL_NAME = 'Initial'
# CreateBoundaryConditions()
MAGNITUDE_TEMPERATURE_END = 0.0577
################################################################
executeOnCaeStartup()
def CreatePart(MODEL_NAME, PART_NAME, GEOMETRY):
    s = mdb.models[MODEL_NAME].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    for i in range(0, len(GEOMETRY), 1):
        if i == len(GEOMETRY)-1:
            s.Line(point1=GEOMETRY[i], point2=GEOMETRY[0])
            continue
        s.Line(point1=GEOMETRY[i], point2=GEOMETRY[i+1])
    p = mdb.models[MODEL_NAME].Part(name=PART_NAME, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[MODEL_NAME].parts[PART_NAME]
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    del mdb.models[MODEL_NAME].sketches['__profile__']

def CreatePassiveMaterial(
        MODEL_NAME, 
        PASSIVE_MATERIAL_NAME,
        E12_PASSIVE, E13_PASSIVE, E23_PASSIVE, 
        MU12_PASSIVE, MU13_PASSIVE, MU23_PASSIVE, 
        G12_PASSIVE, G13_PASSIVE, G23_PASSIVE,
        ALPHA_EXPANSION_PASSIVE, DENSITY_PASSIVE, ALPHA_CONDUCTIVITY_PASSIVE, SP_HEAT_PASSIVE
        ):
    mdb.models[MODEL_NAME].Material(name=PASSIVE_MATERIAL_NAME)
    mdb.models[MODEL_NAME].materials[PASSIVE_MATERIAL_NAME].Elastic(type=ENGINEERING_CONSTANTS, 
        table=((E12_PASSIVE, E13_PASSIVE, E23_PASSIVE, MU12_PASSIVE, MU13_PASSIVE, MU23_PASSIVE, G12_PASSIVE, G13_PASSIVE, G23_PASSIVE), ))
    mdb.models[MODEL_NAME].materials[PASSIVE_MATERIAL_NAME].Expansion(table=((ALPHA_EXPANSION_PASSIVE, ), ))
    mdb.models[MODEL_NAME].materials[PASSIVE_MATERIAL_NAME].Density(table=((DENSITY_PASSIVE, ), ))
    mdb.models[MODEL_NAME].materials[PASSIVE_MATERIAL_NAME].Conductivity(table=((ALPHA_CONDUCTIVITY_PASSIVE, ), ))
    mdb.models[MODEL_NAME].materials[PASSIVE_MATERIAL_NAME].SpecificHeat(table=((SP_HEAT_PASSIVE, ), ))
    layupOrientation = None

def CreateActiveMaterial(
        MODEL_NAME, ACTIVE_MATERIAL_NAME,
        E12_ACTIVE, E13_ACTIVE, E23_ACTIVE, 
        MU12_ACTIVE, MU13_ACTIVE, MU23_ACTIVE, 
        G12_ACTIVE, G13_ACTIVE, G23_ACTIVE,
        ALPHA_EXPANSION_ACTIVE_12, ALPHA_EXPANSION_ACTIVE_13, ALPHA_EXPANSION_ACTIVE_23, DENSITY_ACTIVE, ALPHA_CONDUCTIVITY_ACTIVE, SP_HEAT_ACTIVE
        ):
    mdb.models[MODEL_NAME].Material(name=ACTIVE_MATERIAL_NAME)
    mdb.models[MODEL_NAME].materials[ACTIVE_MATERIAL_NAME].Elastic(type=ENGINEERING_CONSTANTS, 
        table=((E12_ACTIVE, E13_ACTIVE, E23_ACTIVE, MU12_ACTIVE, MU13_ACTIVE, MU23_ACTIVE, G12_ACTIVE, G13_ACTIVE, G23_ACTIVE), ))
    mdb.models[MODEL_NAME].materials[ACTIVE_MATERIAL_NAME].Conductivity(table=((ALPHA_CONDUCTIVITY_ACTIVE, ), ))
    mdb.models[MODEL_NAME].materials[ACTIVE_MATERIAL_NAME].Expansion(type=ORTHOTROPIC, table=((
        ALPHA_EXPANSION_ACTIVE_12, ALPHA_EXPANSION_ACTIVE_13, ALPHA_EXPANSION_ACTIVE_23), ))
    mdb.models[MODEL_NAME].materials[ACTIVE_MATERIAL_NAME].SpecificHeat(table=((SP_HEAT_ACTIVE, ), ))
    mdb.models[MODEL_NAME].materials[ACTIVE_MATERIAL_NAME].Density(table=((DENSITY_ACTIVE, ), ))

def CreateAssembly(MODEL_NAME, PART_NAME, ASSEMBLY_NAME):
    a = mdb.models[MODEL_NAME].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[MODEL_NAME].parts[PART_NAME]
    a.Instance(name=ASSEMBLY_NAME, part=p, dependent=OFF)
    session.viewports['Viewport: 1'].setValues(displayedObject=a)

def CreatePartition(MODEL_NAME, PART_NAME, x, y):
    if partition:
        p = mdb.models[MODEL_NAME].parts[PART_NAME]
        f, e, d = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f[0], sketchUpEdge=e[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        s = mdb.models[MODEL_NAME].ConstrainedSketch(name='__profile__', sheetSize=300.0, gridSpacing=5.0, transform=t)
        g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)
        p = mdb.models[MODEL_NAME].parts[PART_NAME]
        p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        for i in range(0, (len(x)-1), 1):
            if (i+1) % 4 == 0:  
                continue
            s.Line(point1=(-x[i], -y[i]), point2=(-x[i+1], -y[i+1]))
        e1, d2 = p.edges, p.datums
        pickedFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
        p.PartitionFaceBySketch(sketchUpEdge=e1[0], faces=pickedFaces, sketch=s)
        p = mdb.models[MODEL_NAME].parts[PART_NAME]
        del mdb.models[MODEL_NAME].sketches['__profile__']
    else:
        pass

    

def CreateSubdivisionOrientation(MODEL_NAME, PART_NAME, x, y, ACTIVE_ANGLE_ARRAY):
    if partition:
        for i in range(0, len(x)//4, 1):
            compositeLayup = mdb.models[MODEL_NAME].parts[PART_NAME].CompositeLayup(
            name='Subsection-{}'.format(i), description='', elementType=SHELL, 
            offsetType=MIDDLE_SURFACE, symmetric=False, 
            thicknessAssignment=FROM_SECTION)
            compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
            thicknessType=UNIFORM, poissonDefinition=DEFAULT, temperature=GRADIENT, 
            useDensity=OFF)
            compositeLayup.ReferenceOrientation(orientationType=GLOBAL, localCsys=None, 
            fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, axis=AXIS_3)
            p = mdb.models[MODEL_NAME].parts[PART_NAME]
            vertex1_coordinates = (x[i*4], y[i*4], 0)
            vertex2_coordinates = (x[i*4+1], y[i*4+1], 0)
            vertex3_coordinates = (x[i*4+2], y[i*4+2], 0)
            triangle_centroid_x = (vertex1_coordinates[0] + vertex2_coordinates[0] + vertex3_coordinates[0])/3
            triangle_centroid_y = (vertex1_coordinates[1] + vertex2_coordinates[1] + vertex3_coordinates[1])/3
            faces = p.faces.findAt(((triangle_centroid_x, triangle_centroid_y, 0), ))
            region1 = regionToolset.Region(faces=faces)
            compositeLayup.CompositePly(suppressed=False, plyName='Subsection-{}-Bottom'.format(i), region=region1,
                material='Active', thicknessType=SPECIFY_THICKNESS, thickness=THICKNESS_PASSIVE, 
                orientationType=SPECIFY_ORIENT, orientationValue=0.0, 
                additionalRotationType=ROTATION_NONE, additionalRotationField='', 
                axis=AXIS_3, angle=0.0, numIntPoints=3)
            region2 = regionToolset.Region(faces=faces)
            compositeLayup.CompositePly(suppressed=False, plyName='Subsection-{}-Top'.format(i), region=region2, 
                material='Active', thicknessType=SPECIFY_THICKNESS, thickness=THICKNESS_ACTIVE, 
                orientationType=SPECIFY_ORIENT, orientationValue=ACTIVE_ANGLE_ARRAY[i], 
                additionalRotationType=ROTATION_NONE, additionalRotationField='',
                axis=AXIS_3, angle=0.0, numIntPoints=3)
            compositeLayup.resume()
    else:
        p = mdb.models[MODEL_NAME].parts['Part-1']
        f = p.faces
        faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
        region1 = regionToolset.Region(faces=faces)
        p = mdb.models[MODEL_NAME].parts['Part-1']
        f = p.faces
        faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
        region2 = regionToolset.Region(faces=faces)
        compositeLayup = mdb.models[MODEL_NAME].parts['Part-1'].CompositeLayup(
            name='CompositeLayup-1', description='', elementType=SHELL, 
            offsetType=MIDDLE_SURFACE, symmetric=False, 
            thicknessAssignment=FROM_SECTION)
        compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
            thicknessType=UNIFORM, poissonDefinition=DEFAULT, temperature=GRADIENT, 
            useDensity=OFF)
        compositeLayup.ReferenceOrientation(orientationType=GLOBAL, localCsys=None, 
            fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, axis=AXIS_3)
        compositeLayup.suppress()
        compositeLayup.CompositePly(suppressed=False, plyName='Ply-1', region=region1, 
            material='Active', thicknessType=SPECIFY_THICKNESS, thickness=THICKNESS_PASSIVE, 
            orientationType=SPECIFY_ORIENT, orientationValue=90.0, 
            additionalRotationType=ROTATION_NONE, additionalRotationField='', 
            axis=AXIS_3, angle=0.0, numIntPoints=3)
        compositeLayup.CompositePly(suppressed=False, plyName='Ply-2', region=region2, 
            material='Active', thicknessType=SPECIFY_THICKNESS, thickness=THICKNESS_ACTIVE, 
            orientationType=SPECIFY_ORIENT, orientationValue=0.0, 
            additionalRotationType=ROTATION_NONE, additionalRotationField='', 
            axis=AXIS_3, angle=0.0, numIntPoints=3)
        compositeLayup.resume()

def CreateMesh(MODEL_NAME, ASSEMBLY_NAME):
    a = mdb.models[MODEL_NAME].rootAssembly
    partInstances =(a.instances[ASSEMBLY_NAME], )
    a.seedPartInstance(regions=partInstances, size=MESH_SIZE, deviationFactor=0.1, 
        minSizeFactor=0.1)
    f1 = a.instances[ASSEMBLY_NAME].faces
    a.setMeshControls(regions=f1, elemShape=TRI, technique=STRUCTURED)
    elemType2 = mesh.ElemType(elemCode=S3RT, elemLibrary=EXPLICIT, 
        secondOrderAccuracy=OFF)
    f1 = a.instances[ASSEMBLY_NAME].faces
    region = a.Set(faces=f1, name='Set-mesh')
    a.setElementType(regions=region, elemTypes=(elemType2, elemType2))
    partInstances =(a.instances[ASSEMBLY_NAME], )
    a.generateMesh(regions=partInstances)

def CreateStep(MODEL_NAME, STEP_NAME, STEP_INITIAL_NAME):
    mdb.models[MODEL_NAME].CoupledTempDisplacementStep(name=STEP_NAME, 
        previous=STEP_INITIAL_NAME, deltmx=10.0)

def CreateBoundaryConditions(MODEL_NAME, STEP_NAME, STEP_INITIAL_NAME, MAGNITUDE_TEMPERATURE_END):
    if partition:
        a = mdb.models[MODEL_NAME].rootAssembly
        f1 = a.instances[ASSEMBLY_NAME].faces
        faces1 = f1.getSequenceFromMask(mask=('[#7fffff ]', ), )
        region = a.Set(faces=faces1, name='Set-4')
        mdb.models[MODEL_NAME].TemperatureBC(name='BC-1', createStepName=STEP_INITIAL_NAME, 
            region=region, distributionType=UNIFORM, fieldName='', magnitude=0.0)
        f1 = a.instances[ASSEMBLY_NAME].faces
        faces1 = f1.getSequenceFromMask(mask=('[#7fffff ]', ), )
        region = a.Set(faces=faces1, name='Set-5')
        mdb.models[MODEL_NAME].boundaryConditions['BC-1'].setValuesInStep(
            stepName=STEP_NAME, magnitude=MAGNITUDE_TEMPERATURE_END)
    else:
        a = mdb.models[MODEL_NAME].rootAssembly
        f1 = a.instances[ASSEMBLY_NAME].faces
        faces1 = a.instances[ASSEMBLY_NAME].faces
        region = a.Set(faces=faces1, name='Set-4')
        mdb.models[MODEL_NAME].TemperatureBC(name='BC-1', createStepName='Initial', 
            region=region, distributionType=UNIFORM, fieldName='', magnitude=0.0)
        a = mdb.models[MODEL_NAME].rootAssembly
        f1 = a.instances[ASSEMBLY_NAME].faces
        faces1 = a.instances[ASSEMBLY_NAME].faces
        region = a.Set(faces=faces1, name='Set-5')
        mdb.models[MODEL_NAME].boundaryConditions['BC-1'].setValuesInStep(
            stepName='Step-1', magnitude=MAGNITUDE_TEMPERATURE_END)

def CreateJob(MODEL_NAME, JOB_NAME, ANGLEPLY_ACTIVE, submit_job = True):
    mdb.Job(name=JOB_NAME, model=MODEL_NAME, description=str(ANGLEPLY_ACTIVE), type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, 
        multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
    if submit_job:
        mdb.jobs[JOB_NAME].submit(consistencyChecking=OFF)
        mdb.jobs[JOB_NAME].waitForCompletion()

def OpenODBandWriteResults(JOB_NAME, STEP_NAME, variable_name):
    '''
    Opens ODB file and returns displacement results at all nodes in the form of [[x1, y1, z1], [x2, y2, z2],...] in .txt format
    '''
    odb = session.openOdb(name = JOB_NAME + '.odb')
    #initial_results = odb.steps[STEP_INITIAL_NAME]
    import numpy as np
    lastStep = odb.steps[STEP_NAME]
    lastFrame = lastStep.frames[1]
    variable = lastFrame.fieldOutputs[variable_name]
    data_array = variable.values
    results_array = []
    for node_value in data_array:
        a= node_value.data
        results_array.append(a) # leave space below for for loops!
    np.savetxt(str(variable_name) + 'results' + '.txt', results_array, fmt='%s')

CreatePart(MODEL_NAME, PART_NAME, GEOMETRY)
CreateActiveMaterial(
    MODEL_NAME, ACTIVE_MATERIAL_NAME,
    E12_ACTIVE, E13_ACTIVE, E23_ACTIVE, 
    MU12_ACTIVE, MU13_ACTIVE, MU23_ACTIVE, 
    G12_ACTIVE, G13_ACTIVE, G23_ACTIVE,
    ALPHA_EXPANSION_ACTIVE_12, ALPHA_EXPANSION_ACTIVE_13, ALPHA_EXPANSION_ACTIVE_23, DENSITY_ACTIVE, ALPHA_CONDUCTIVITY_ACTIVE, SP_HEAT_ACTIVE
    )
JOB_NAME = 'Job-triangle'
CreatePartition(MODEL_NAME, PART_NAME, x, y)
CreateSubdivisionOrientation(MODEL_NAME, PART_NAME, x, y, ACTIVE_ANGLE_ARRAY)
CreateAssembly(MODEL_NAME, PART_NAME, ASSEMBLY_NAME)
CreateStep(MODEL_NAME, STEP_NAME, STEP_INITIAL_NAME)
CreateMesh(MODEL_NAME, ASSEMBLY_NAME)
CreateBoundaryConditions(MODEL_NAME, STEP_NAME, STEP_INITIAL_NAME, MAGNITUDE_TEMPERATURE_END)
CreateJob(MODEL_NAME, JOB_NAME, ANGLEPLY_ACTIVE, submit_job = True)
    
variable_name = 'U'
OpenODBandWriteResults(JOB_NAME, STEP_NAME, variable_name)
