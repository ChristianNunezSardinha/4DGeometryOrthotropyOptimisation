# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2023 replay file
# Internal Version: 2022_09_28-19.11.55 183150
# Run by hk21416 on Mon Nov 13 13:49:38 2023
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=184.917175292969, 
    height=109.086120605469)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
cliCommand("""# Import modules""")
cliCommand("""from abaqus import *""")
cliCommand("""from abaqusConstants import *""")
cliCommand("""# Variables""")
cliCommand("""## node values (in mm)""")
cliCommand("""POINT_1 = (-5.0, 20.0)""")
cliCommand("""POINT_2 = (-5.0, -20.0)""")
cliCommand("""POINT_3 = (5.0, -20.0)""")
cliCommand("""POINT_4 = (5.0, 20.0)""")
cliCommand("""## Depth of part (mm)""")
cliCommand("""PART_DEPTH = 2.0 """)
cliCommand("""## Strings""")
cliCommand("""MODEL_STRING = "TRIAL_MODEL\"""")
cliCommand("""MODEL_NAME = mdb.Model(name=MODEL_STRING)""")
#: The model "TRIAL_MODEL" has been created.
cliCommand("""PART_NAME = "RECTANGLE\"""")
cliCommand("""# Functions""")
cliCommand("""def CreatePart(point_1, point_2, point_3, point_4, part_depth, model_string, part_name):
    '''
    Creates a part in Abaqus. Currently it is set to create a rectangle.
    
    ARGUMENTS:
    point_1, point_2, point_3, point_4::tuple
    part_depth::float
    model_string::string
    part_name::string
    '''
    s1 = mdb.models[model_string].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.Line(point1=point_1, point2=point_4)
    s1.HorizontalConstraint(entity=g[2], addUndoState=False)
    s1.Line(point1=point_4, point2=point_3)
    s1.VerticalConstraint(entity=g[3], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s1.Line(point1=point_3, point2=point_2)
    s1.HorizontalConstraint(entity=g[4], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s1.Line(point1=point_2, point2=point_1)
    s1.VerticalConstraint(entity=g[5], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    p = mdb.models[model_string].Part(name=part_name, dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = mdb.models[model_string].parts[part_name]   
    p.BaseSolidExtrude(sketch=s1, depth=part_depth)
    s1.unsetPrimaryObject()
    p = mdb.models[model_string].parts[part_name]
    del mdb.models[model_string].sketches['__profile__']
""")
cliCommand("""# Execute code (test)""")
cliCommand("""CreatePart(POINT_1, POINT_2, POINT_3, POINT_4, PART_DEPTH, MODEL_STRING, PART_NAME)""")
p = mdb.models['TRIAL_MODEL'].parts['RECTANGLE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
mdb.models['Model-1'].Material(name='WOOD_PLA')
mdb.models['Model-1'].materials['WOOD_PLA'].Elastic(table=((6.6, 0.53), ))
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['TRIAL_MODEL'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
m = mdb.models['Model-1']
m2 = mdb.models['TRIAL_MODEL']
a.Instance(name='TRIAL_MODEL-1', model=m2)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
p = mdb.models['TRIAL_MODEL'].parts['RECTANGLE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
m = mdb.models['Model-1']
m2 = mdb.models['TRIAL_MODEL']
a.Instance(name='TRIAL_MODEL-2', model=m2)
a = mdb.models['Model-1'].rootAssembly
m = mdb.models['Model-1']
m2 = mdb.models['TRIAL_MODEL']
a.Instance(name='TRIAL_MODEL-3', model=m2)
a = mdb.models['Model-1'].rootAssembly
m = mdb.models['Model-1']
m2 = mdb.models['TRIAL_MODEL']
a.Instance(name='TRIAL_MODEL-4', model=m2)
a = mdb.models['Model-1'].rootAssembly
m = mdb.models['Model-1']
m2 = mdb.models['TRIAL_MODEL']
a.Instance(name='TRIAL_MODEL-5', model=m2)
a = mdb.models['Model-1'].rootAssembly
del a.features['TRIAL_MODEL-2']
a = mdb.models['Model-1'].rootAssembly
del a.features['TRIAL_MODEL-3']
a = mdb.models['Model-1'].rootAssembly
del a.features['TRIAL_MODEL-4']
a = mdb.models['Model-1'].rootAssembly
del a.features['TRIAL_MODEL-5']
a = mdb.models['TRIAL_MODEL'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
p = mdb.models['TRIAL_MODEL'].parts['RECTANGLE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
p = mdb.models['TRIAL_MODEL'].parts['RECTANGLE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
p = mdb.models['TRIAL_MODEL'].parts['RECTANGLE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='Material-2')
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.CircleByCenterPerimeter(center=(-8.75, -7.5), point1=(-18.75, 2.5))
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
Mdb()
#: A new model database has been created.
#: The model "Model-1" has been created.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
Mdb()
#: A new model database has been created.
#: The model "Model-1" has been created.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
mdb.saveAs(pathName='C:/Temp/Trial')
#: The model database has been saved to "C:\Temp\Trial.cae".
