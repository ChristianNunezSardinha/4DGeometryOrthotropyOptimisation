
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
import numpy as np

########################################################################
# PARAMETERS TO CHANGE FOR TRIALS

ITERATION_NUMBER = 10
########################################################################
# PARAMETERS FOR THE CODE

# CreatePart()
MODEL_NAME = 'Model-1'
PART_NAME = 'Part-1'
POINT_1 = (0.0, 0.0)
POINT_2 = (100.0, 0.0)
POINT_3 = (0.0, 100.0)
# CreatePassiveMaterial & CreateActiveMaterial()
PASSIVE_MATERIAL_NAME = 'Passive'
ACTIVE_MATERIAL_NAME = 'Active'
## Elastic material properties:
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
# CreateCompositeLayup()
COMPOSITE_LAYUP_NAME = 'CompositeLayup-1'
THICKNESS_PASSIVE = 1.0
THICKNESS_ACTIVE = 3.0
ANGLEPLY_PASSIVE = 0.0
ANGLEPLY_ACTIVE = 90.0
# CreateAssembly()
ASSEMBLY_NAME = 'Assembly-1'
# CreateMesh()
MESH_SIZE = 5.0
# CreateStep()
STEP_NAME = 'Step-1'
STEP_INITIAL_NAME = 'Initial'
# CreateBoundaryConditions()
MAGNITUDE_TEMPERATURE_END = 0.0577
################################################################
executeOnCaeStartup()
def CreatePart(
        MODEL_NAME, PART_NAME, 
        POINT_1, POINT_2, POINT_3,
        ):
    '''
    Creates a part in Abaqus. Currently it is set to create a triangle
    '''
    s = mdb.models[MODEL_NAME].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.Line(point1=POINT_1, point2=POINT_2)
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    s.Line(point1=POINT_2, point2=POINT_3)
    s.Line(point1=POINT_3, point2=POINT_1)
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(16.4407081604004, 
        -23.6907234191895), value=30.0)
    s.ObliqueDimension(vertex1=v[2], vertex2=v[0], textPoint=(-19.7204475402832, 
        20.2531623840332), value=60.0)
    p = mdb.models[MODEL_NAME].Part(name=PART_NAME, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[MODEL_NAME].parts[PART_NAME]
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models[MODEL_NAME].parts[PART_NAME]
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

def CreateCompositeLayup(MODEL_NAME, PART_NAME, COMPOSITE_LAYUP_NAME, ANGLEPLY_PASSIVE, ANGLEPLY_ACTIVE):
    p = mdb.models[MODEL_NAME].parts[PART_NAME]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region1 = regionToolset.Region(faces=faces)
    p = mdb.models[MODEL_NAME].parts[PART_NAME]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region2 = regionToolset.Region(faces=faces)
    compositeLayup = mdb.models[MODEL_NAME].parts[PART_NAME].CompositeLayup(
        name=COMPOSITE_LAYUP_NAME, description='', elementType=SHELL, 
        offsetType=MIDDLE_SURFACE, symmetric=False, 
        thicknessAssignment=FROM_SECTION)
    compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
        thicknessType=UNIFORM, poissonDefinition=DEFAULT, temperature=GRADIENT, 
        useDensity=OFF)
    compositeLayup.ReferenceOrientation(orientationType=GLOBAL, localCsys=None, 
        fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, axis=AXIS_3)
    compositeLayup.suppress()
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-1', region=region1, 
        material=ACTIVE_MATERIAL_NAME, thicknessType=SPECIFY_THICKNESS, thickness=3.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=ANGLEPLY_ACTIVE, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-2', region=region2, 
        material=ACTIVE_MATERIAL_NAME, thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=ANGLEPLY_PASSIVE, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.resume()

def CreateAssembly(MODEL_NAME, PART_NAME, ASSEMBLY_NAME):
    a = mdb.models[MODEL_NAME].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[MODEL_NAME].parts[PART_NAME]
    a.Instance(name=ASSEMBLY_NAME, part=p, dependent=OFF)

'''
def CreatePartition(MODEL_NAME, PART_NAME, ASSEMBLY_NAME, points):
    p = mdb.models[MODEL_NAME].parts[PART_NAME]
    f, e, d = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f[0], sketchUpEdge=e[0], 
        sketchPlaneSide=SIDE1, origin=(10.0, 20.0, 0.0))
    s = mdb.models[MODEL_NAME].ConstrainedSketch(name='__profile__', 
        sheetSize=134.16, gridSpacing=3.35, transform=t)
    g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[MODEL_NAME].parts[PART_NAME]
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    for i in points:
        s.Line(point1=points[:, i], point2=points[:, i+1])
        s.CoincidentConstraint(entity1=v[i+1], entity2=g[i], addUndoState=False)
        s.CoincidentConstraint(entity1=v[i+2], entity2=g[i+1], addUndoState=False)
'''

def CreateMesh(MODEL_NAME, ASSEMBLY_NAME):
    a = mdb.models[MODEL_NAME].rootAssembly
    partInstances =(a.instances[ASSEMBLY_NAME], )
    a.seedPartInstance(regions=partInstances, size=5.0, deviationFactor=0.1, 
        minSizeFactor=0.1)
    a = mdb.models[MODEL_NAME].rootAssembly
    f1 = a.instances[ASSEMBLY_NAME].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.setMeshControls(regions=pickedRegions, elemShape=TRI, technique=STRUCTURED)
    elemType2 = mesh.ElemType(elemCode=S3RT, elemLibrary=EXPLICIT, 
        secondOrderAccuracy=OFF)
    a = mdb.models[MODEL_NAME].rootAssembly
    f1 = a.instances[ASSEMBLY_NAME].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(faces1, )
    a.setElementType(regions=pickedRegions, elemTypes=(elemType2, elemType2))
    elemType2 = mesh.ElemType(elemCode=S3RT, elemLibrary=EXPLICIT, 
        secondOrderAccuracy=OFF)
    a = mdb.models[MODEL_NAME].rootAssembly
    f1 = a.instances[ASSEMBLY_NAME].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(faces1, )
    a.setElementType(regions=pickedRegions, elemTypes=(elemType2, elemType2))
    a = mdb.models[MODEL_NAME].rootAssembly
    partInstances =(a.instances[ASSEMBLY_NAME], )
    a.generateMesh(regions=partInstances)

def CreateStep(MODEL_NAME, STEP_NAME, STEP_INITIAL_NAME):
    mdb.models[MODEL_NAME].CoupledTempDisplacementStep(name=STEP_NAME, 
        previous=STEP_INITIAL_NAME, deltmx=10.0)

def CreateBoundaryConditions(MODEL_NAME, ASSEMBLY_NAME, STEP_NAME, STEP_INITIAL_NAME, MAGNITUDE_TEMPERATURE_END):
    a = mdb.models[MODEL_NAME].rootAssembly
    f1 = a.instances[ASSEMBLY_NAME].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    region = a.Set(faces=faces1, name='Set-4')
    mdb.models[MODEL_NAME].TemperatureBC(name='BC-1', createStepName=STEP_INITIAL_NAME, 
        region=region, distributionType=UNIFORM, fieldName='', magnitude=0.0)
    f1 = a.instances[ASSEMBLY_NAME].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    region = a.Set(faces=faces1, name='Set-5')
    mdb.models[MODEL_NAME].boundaryConditions['BC-1'].setValuesInStep(
        stepName=STEP_NAME, magnitude=MAGNITUDE_TEMPERATURE_END)

def CreateJob(MODEL_NAME, JOB_NAME, ANGLEPLY_ACTIVE, submit_job = True):
    mdb.Job(name=JOB_NAME, model=MODEL_NAME, description=str(ANGLEPLY_ACTIVE), type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, 
        multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
    a = mdb.models[MODEL_NAME].rootAssembly
    if submit_job:
        mdb.jobs[JOB_NAME].submit(consistencyChecking=OFF)
        mdb.jobs[JOB_NAME].waitForCompletion()

CreatePart(
    MODEL_NAME, PART_NAME, 
    POINT_1, POINT_2, POINT_3
    )
CreateActiveMaterial(
    MODEL_NAME, ACTIVE_MATERIAL_NAME,
    E12_ACTIVE, E13_ACTIVE, E23_ACTIVE, 
    MU12_ACTIVE, MU13_ACTIVE, MU23_ACTIVE, 
    G12_ACTIVE, G13_ACTIVE, G23_ACTIVE,
    ALPHA_EXPANSION_ACTIVE_12, ALPHA_EXPANSION_ACTIVE_13, ALPHA_EXPANSION_ACTIVE_23, DENSITY_ACTIVE, ALPHA_CONDUCTIVITY_ACTIVE, SP_HEAT_ACTIVE
    )
CreateAssembly(MODEL_NAME, PART_NAME, ASSEMBLY_NAME)
CreateStep(MODEL_NAME, STEP_NAME, STEP_INITIAL_NAME)
CreateBoundaryConditions(MODEL_NAME, ASSEMBLY_NAME, STEP_NAME, STEP_INITIAL_NAME, MAGNITUDE_TEMPERATURE_END)
CreateCompositeLayup(MODEL_NAME, PART_NAME, COMPOSITE_LAYUP_NAME, 0, ANGLEPLY_ACTIVE)
CreateMesh(MODEL_NAME, ASSEMBLY_NAME)
JOB_NAME = 'Job-triangle'
CreateJob(MODEL_NAME, JOB_NAME, ANGLEPLY_ACTIVE, submit_job = True)
