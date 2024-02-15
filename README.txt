Optimisation of 4D printing geometries via orthotropic materials and triangular subdivision generation.
- CreateSubdivision: Generates the partition using PyGmsh. Run first
- SendToAbaqus: Creates an Abaqus model with specified properties. If accounting for partitions, set partition = True in the code. Copy and paste geometry coordinates from CreateSubdivision.
- PostProcessing: Plots results

Developed by Christian Nunez Sardinha