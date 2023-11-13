# Import modules

from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

# Variables

## node values (in mm)
POINT_1 = (-5.0, 20.0)
POINT_2 = (5.0, 20.0)

## Depth of part (mm)
PART_DEPTH = 2.0 

print(type(POINT_1))
## Strings
MODEL_NAME = 'Model-1'
PART_NAME = 'TRIAL_PART'

# Functions

def CreatePart(point_1, point_2, part_depth, model_name, part_name):
    '''
    Creates a part in Abaqus. Currently it is set to create a rectangle.
    '''
    Mdb()
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s1 = mdb.models[model_name].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.rectangle(point1=point_1, point2=point_2)
    p = mdb.models[model_name].Part(name=part_name, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[model_name].parts[part_name]
    p.BaseSolidExtrude(sketch=s1, depth=part_depth)
    s1.unsetPrimaryObject()
    p = mdb.models[model_name].parts[part_name]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[model_name].sketches['__profile__']

# Execute code (test)

CreatePart(POINT_1, POINT_2, PART_DEPTH, MODEL_NAME, PART_NAME)

'''
def CreatePart(point1:tuple, point2:tuple, part_depth:float, model_name:str, part_name:str):
    
    Creates a part in Abaqus. Currently it is set to create a rectangle.
    
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s1 = mdb.models[model_name].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.rectangle(point1, point2)
    p = mdb.models[model_name].Part(name=part_name, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[model_name].parts[part_name]
    p.BaseSolidExtrude(sketch=s1, part_depth)
    s1.unsetPrimaryObject()
    p = mdb.models[model_name].parts[part_name]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[model_name].sketches['__profile__']

'''