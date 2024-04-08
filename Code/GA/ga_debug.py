# the code will need to define a population, iterate a number of times, objective, selection, crossover, mutation
import random
import numpy as np
import time
import os
import sys
import copy
#import createSubdivision
#from circle_fit import taubinSVD
start = time.time()
# PARAMETERS TO CHANGE FOR TRIALS
#ITERATION_NUMBER = 10 all points must be connected from the previous one
partition = True
second_accuracy = True
submit_job = True
cross_over = True
mutation = True
bound_mutation = True
JOB_NAME = 'GAlgTestWholeFinal008'
#JOB_NAME = 'elitisttest3'
# Conditions for POINTS: counter-clockwise. Last edge will be pinned (POINT_4 TO POINT_1)
POINT_1 = (0.0, 0.0)
POINT_2 = (100.0, 0.0)
POINT_3 = (0.0, 100.0)
#POINT_3 = (15.0, 1.0)
#POINT_4 = (0.0, 1.0)
GEOMETRY = [POINT_1, POINT_2, POINT_3]
# Extracting data from createSubdivision
partition_filename = 'C:\Temp/geometrypartitionTriangle.txt'

input_file_path = partition_filename
loaded_data = np.loadtxt(input_file_path, delimiter=',')
x = loaded_data[:, 0]
y = loaded_data[:, 1]
ACTIVE_ANGLE_ARRAY = np.linspace(90, 90, len(x)//4)

### These modules have to be imported after partitioning the geometry
import SendToAbaqus
import post_processing
# 
current_directory = os.getcwd()
newpath = os.path.join(current_directory, JOB_NAME)
if not os.path.exists(newpath):
    os.makedirs(newpath)
os.chdir(newpath)
sys.path.insert(0, current_directory)
########################################################################
# PARAMETERS FOR THE CODE
# General Data

MODEL_NAME = 'Model'
PART_NAME = 'Part-1'

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
MC = 0.552
ALPHA_EXPANSION_PASSIVE = 0.01
ALPHA_EXPANSION_ACTIVE_12 = 0.0171
ALPHA_EXPANSION_ACTIVE_13 = 0.2156
ALPHA_EXPANSION_ACTIVE_23 = 0.6385  
## Conductivity
ALPHA_CONDUCTIVITY_PASSIVE = 0.01
ALPHA_CONDUCTIVITY_ACTIVE = 10000
## Specific Heat J/(kg K)
SP_HEAT_PASSIVE = 1200.0
SP_HEAT_ACTIVE = 1800.0
## Density kg/mm^3
DENSITY_PASSIVE = 5*10**(-7)
DENSITY_ACTIVE = 5*10**(-7)
# CreatePartition and CreateMaterialSubdivision()
PASSIVE_MATERIAL_NAME = 'Passive'
ACTIVE_MATERIAL_NAME = 'Active'
COMPOSITE_LAYUP_NAME = 'CompositeLayup-1'
THICKNESS_PASSIVE = 2 #mm
THICKNESS_ACTIVE = 1 #mm
ANGLEPLY_PASSIVE = 90.0
ANGLEPLY_ACTIVE = 0.0
# CreateAssembly()
ASSEMBLY_NAME = 'Assembly-1'
# CreateMesh()
MESH_SIZE = 1.2
# CreateStep()
STEP_NAME = 'Step-1'
STEP_INITIAL_NAME = 'Initial'
# CreateBoundaryConditions()
MAGNITUDE_TEMPERATURE_END = 0.552
################################################################


class GeneticAlgorithm():

    def __init__(self):
        self.n_bits = len(x)//2
        self.n_pop = 10
        self.n_iter = 25
        self.r_cross = 0.2
        self.r_mut = 0.2
        self.bit_list = []
        self.pop_list = []
        self.selected = []
        self.k = self.n_pop // 2
        self.reference_curvature = 0.05
        self.bounds =  90

    def population(self):
        '''
        Creates a population of random values
        '''
        population_array = np.zeros((self.n_pop, self.n_bits))  # Initialize population array
        for a in range(self.n_pop):
            chromosome_passive = np.random.randint(int(-self.bounds), int(self.bounds), size=self.n_bits//2)
            chromosome_active = np.random.randint(int(-self.bounds), int(self.bounds), size=self.n_bits//2)
            chromosome = np.concatenate([chromosome_passive, chromosome_active])
            population_array[a] = chromosome
        population = np.array(population_array).tolist()
        return population
    
    def objective(self, calculated_curvature):
        '''
        Calculates the score of the chromosome by addition of bits
        '''
        return (calculated_curvature - self.reference_curvature)**2
    
    def selection(self, population, scores):
        '''
        Tournament selection.
        Returns the best chromosomes according to the score.
        '''
        selected_chrom = []
        list_to_shuffle = zip(population, scores)
        # First half: Compare pairs of individuals
        for _ in range(2):
            random.shuffle(list_to_shuffle)
            pop_list_copy, scores_copy = zip(*list_to_shuffle)
            for i in range(0, self.n_pop, 2):
                # Compare the scores of two individuals
                if scores_copy[i] < scores_copy[i+1]:
                    selected_chrom.append(pop_list_copy[i])
                else:
                    selected_chrom.append(pop_list_copy[i+1])
        return selected_chrom
    
    def crossover(self, p1, p2, cross_over = cross_over):
        '''
        Mixes two random chromosomes using a random point to splice them.
        Output is a list of two children which are segments of parent 1 and parent 2.
        '''
        c1, c2 = p1, p2  # Make copies of parents
        if cross_over:
            if random.random() < self.r_cross:
                pt = random.randint(0, self.n_bits - 1)  # Select a random crossover point
                # Swap the segments between parents
                for i in range(pt, self.n_bits):
                    c1[i], c2[i] = c2[i], c1[i]
        return [c1, c2]
        
    def mutation(self, child, mutation=mutation, contrain_mutation=False, current_generation_number=1):
        '''
        Changes a bite of the chromosome depending on random number.
        '''
        if mutation:
            for i in range(len(child)):
                if random.random() < self.r_mut:
                    if not contrain_mutation:
                        child[i] = random.randint(int(-self.bounds), int(self.bounds))
                    else:
                        #correction_factor = 1 - (current_generation_number) / (self.n_iter+1) 
                        correction_factor = 1 / np.sqrt(current_generation_number)
                        #No correction
                        # correction_factor = 1
                        child[i] = child[i] + (random.randint(int(-self.bounds), int(self.bounds)))*correction_factor
                        # Make sure it doesn't go past self.bounds
                        child[i] = max(-int(self.bounds), min(int(self.bounds), child[i]))
        return child
                        

                        
    def execute(self, MODEL_NAME):
        '''
        Main method of class. Gives a list of the best chromosome with its score.
        Will also print when a new better chromosome was calculated.
        '''
        SendToAbaqus.CreatePart(MODEL_NAME, PART_NAME, GEOMETRY)
        SendToAbaqus.CreateActiveMaterial(
            MODEL_NAME, ACTIVE_MATERIAL_NAME,
            E12_ACTIVE, E13_ACTIVE, E23_ACTIVE, 
            MU12_ACTIVE, MU13_ACTIVE, MU23_ACTIVE, 
            G12_ACTIVE, G13_ACTIVE, G23_ACTIVE,
            ALPHA_EXPANSION_ACTIVE_12, ALPHA_EXPANSION_ACTIVE_13, ALPHA_EXPANSION_ACTIVE_23, DENSITY_ACTIVE, ALPHA_CONDUCTIVITY_ACTIVE, SP_HEAT_ACTIVE
            )
        SendToAbaqus.CreatePartition(MODEL_NAME, PART_NAME, x, y, partition=partition)
        SendToAbaqus.CreateAssembly(MODEL_NAME, PART_NAME, ASSEMBLY_NAME)
        SendToAbaqus.CreateStep(MODEL_NAME, STEP_NAME, STEP_INITIAL_NAME)
        SendToAbaqus.CreateMesh(MODEL_NAME, ASSEMBLY_NAME, MESH_SIZE, second_accuracy)
        SendToAbaqus.CreateBoundaryConditions(MODEL_NAME, ASSEMBLY_NAME, STEP_NAME, STEP_INITIAL_NAME, MAGNITUDE_TEMPERATURE_END, second_accuracy=second_accuracy)
        final_scores = []
        final_curvature = []
        self.pop_list = self.population()
        best_index, best_eval = None, float('inf')
        for generation in range(1, self.n_iter+1):
            scores = np.zeros(self.n_pop)
        #print(len(self.pop_list))
            for index, a in enumerate(self.pop_list):
                FILENAME = JOB_NAME + "-" + str(generation) + "-" + str(index+1)
                print(FILENAME)
                print(self.pop_list[index])
                passive_angles = self.pop_list[index][0:(self.n_bits//2)]
                #print(passive_angles)
                #print(len(passive_angles))
                active_angles = self.pop_list[index][(self.n_bits//2):]
                #print(active_angles)
                #print(len(active_angles))
                SendToAbaqus.CreateSubdivisionOrientation(MODEL_NAME, PART_NAME, x, y, passive_angles, active_angles, THICKNESS_PASSIVE, THICKNESS_ACTIVE, partition=partition)
                SendToAbaqus.CreateJob(MODEL_NAME, FILENAME, ANGLEPLY_ACTIVE, submit_job = submit_job)
                print(FILENAME, 'Completed')
                SendToAbaqus.OpenODBandWriteResults(FILENAME, 'Step-1', 'U')
                calculated_curvature, dummy = post_processing.CalculateCurvature(FILENAME)
                print(FILENAME, 'Curvature = ', calculated_curvature)
                final_curvature.append(calculated_curvature)
                end = time.time()
                print(FILENAME, 'completed at:', end-start)
                scores[index] = (self.objective(calculated_curvature))
            
            for i in range(0, self.n_pop):
                score = scores[i]
                if score <= best_eval: # this is the only way it works!
                    best_index, best_eval = i, score
                    print('Best score: ', score, 'Generation:', generation, 'Sample', i+1)

            # Get the individual with the minimum score
            best_individual = copy.deepcopy(self.pop_list[best_index])
            final_scores.append(scores)
            self.selected = self.selection(self.pop_list, scores)
            #print(self.selected)
            children = []
            for i in range(0, self.n_pop, 2): 
                p1, p2 = self.selected[i], self.selected[i+1]   
                for c in self.crossover(p1, p2):
                    mutated = self.mutation(c, mutation, contrain_mutation=bound_mutation, current_generation_number=generation)
                    children.append(mutated)
            children[0] = best_individual
            self.pop_list = children
            #print(self.pop_list)
                
        return [final_scores, final_curvature, best_individual, best_eval]


instance = GeneticAlgorithm()
scores, curvatures, best, score = instance.execute(MODEL_NAME)
print('f(%s) = %f' % (best,score))
flattened_list = [item for sublist in scores for item in sublist]
np.savetxt(JOB_NAME + '_Scores', flattened_list)
np.savetxt(JOB_NAME + '_Curvatures', curvatures)


'''
import csv
# Save data to CSV
with open( JOB_NAME + '_Scores' + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Curvature', 'Score'])
    writer.writerows(data)
'''
'''
instance = GeneticAlgorithm()
# population test
population = instance.population()
print(population)

# selection test
made_up_scores = np.random.rand(instance.n_pop).tolist()
print(made_up_scores)
selected = instance.selection(population, made_up_scores)
print("Selected Parents:")
print(selected)

#cross over and mutation test
children = []
for i in range(0, instance.n_pop, 2): 
    p1, p2 = selected[i], selected[i+1]   
    for c in instance.crossover(p1, p2, instance.r_cross):
        instance.mutation(c, instance.r_mut)
        children.append(c)
    print(i)
print("Children after Crossover:")
print(children)
'''