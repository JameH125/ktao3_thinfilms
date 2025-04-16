import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import thinfilm as tf

# Contains all functions for data analysis of KTaO3 thin films in one script.
#  
# - Uncomment functions as necessary.
# - Must pip install thinfilm to use this script (run 'pip install -e .' in terminal of parent directory). May also
#   require pip install of setuptools.
# - Hover over functions to see parameters and descriptions.
# - Any further adjustments can be made by directly editing the functions within the thinfilm directory.


### Converting files ##########################################################################################################


# PARAMETERS #
pseudo_dir    = 'pseudo_pbe'                                   # Directory containing the pseudopotentials
pseudo        = {'K': 'k.UPF', 'Ta': 'ta.UPF', 'O': 'o.UPF'}   # Pseudopotentials dictionary
filetype      = 'out'                                          # File extension of file-to-convert (in/out/vasp)
file_input    = 'stripe/FINAL/t7/bulk/rlx.out'            # File to convert
file_output   = 'stripe/FINAL/t7/bulk/rlx.vasp'              # Write to file

#tf.convert_file(filetype,file_input,file_output,pseudo_dir,pseudo) 


### Calculating surface energies ##############################################################################################

# PARAMETERS #
e_cell      = -296.03019878                             # Energy of one unit cell (Ry)                                   
a           =    3.98650146                             # Lattice parameter (Angstrom)
data        = 'Spreadsheets/surface_energy.csv'         # Table containing surface energies
file        = 'stripe/FINAL/t7/bulk/rlx.out'
thick       = 7                                        # Thickness of thin film (uc)
phase       = 'bulk'                         
step        = 0                                         # Step Width
x           = a                                       # latx
y           = a                                       # laty 
nucell      = 7                                        # no. of unit cells
csv         = False                                                

#tf.surface_energy(e_cell,file,thick,phase,step,x,y,nucell,data=data,csvdir=data,csv=csv)


### Sorting Layers ##########################################################################################################

# PARAMETERS #
num_layers  = 5
layer_atoms = [28,40,40,40,32]
input_file  = 'stripe/FINAL/t5/8uc/stA/rlx.in'
natoms      = 180


#tf.sort_layer(input_file,natoms,layer_atoms,num_layers)


### Computing LDOS ##########################################################################################################

# PARAMETERS (copy from sort layer function and add the comma separations) #
layers = {
'Layer 1': [(45, 'Ta'), (46, 'Ta'), (47, 'Ta'), (48, 'Ta'), (117, 'O'), (118, 'O'), (119, 'O'), (120, 'O'), (153, 'O'), (154, 'O'), (155, 'O'), (156, 'O'), (9, 'K'), (10, 'K'), (11, 'K'), (12, 'K'), (13, 'K'), (14, 'K'), (15, 'K'), (16, 'K'), (89, 'O'), (90, 'O'), (91, 'O'), (92, 'O'), (93, 'O'), (94, 'O'), (95, 'O'), (96, 'O')],
'Layer 2': [(57, 'Ta'), (58, 'Ta'), (59, 'Ta'), (60, 'Ta'), (61, 'Ta'), (62, 'Ta'), (63, 'Ta'), (64, 'Ta'), (129, 'O'), (130, 'O'), (131, 'O'), (132, 'O'), (133, 'O'), (134, 'O'), (135, 'O'), (136, 'O'), (165, 'O'), (166, 'O'), (167, 'O'), (168, 'O'), (169, 'O'), (170, 'O'), (171, 'O'), (172, 'O'), (21, 'K'), (22, 'K'), (23, 'K'), (24, 'K'), (25, 'K'), (26, 'K'), (27, 'K'), (28, 'K'), (101, 'O'), (102, 'O'), (103, 'O'), (104, 'O'), (105, 'O'), (106, 'O'), (107, 'O'), (108, 'O')],
'Layer 3': [(65, 'Ta'), (66, 'Ta'), (67, 'Ta'), (68, 'Ta'), (69, 'Ta'), (70, 'Ta'), (71, 'Ta'), (72, 'Ta'), (137, 'O'), (138, 'O'), (139, 'O'), (140, 'O'), (141, 'O'), (142, 'O'), (143, 'O'), (144, 'O'), (173, 'O'), (174, 'O'), (175, 'O'), (176, 'O'), (177, 'O'), (178, 'O'), (179, 'O'), (180, 'O'), (29, 'K'), (30, 'K'), (31, 'K'), (32, 'K'), (33, 'K'), (34, 'K'), (35, 'K'), (36, 'K'), (73, 'O'), (74, 'O'), (75, 'O'), (76, 'O'), (77, 'O'), (78, 'O'), (79, 'O'), (80, 'O')],
'Layer 4': [(37, 'Ta'), (38, 'Ta'), (39, 'Ta'), (40, 'Ta'), (41, 'Ta'), (42, 'Ta'), (43, 'Ta'), (44, 'Ta'), (109, 'O'), (110, 'O'), (111, 'O'), (112, 'O'), (113, 'O'), (114, 'O'), (115, 'O'), (116, 'O'), (145, 'O'), (146, 'O'), (147, 'O'), (148, 'O'), (149, 'O'), (150, 'O'), (151, 'O'), (152, 'O'), (1, 'K'), (2, 'K'), (3, 'K'), (4, 'K'), (5, 'K'), (6, 'K'), (7, 'K'), (8, 'K'), (81, 'O'), (82, 'O'), (83, 'O'), (84, 'O'), (85, 'O'), (86, 'O'), (87, 'O'), (88, 'O')],
'Layer 5': [(49, 'Ta'), (50, 'Ta'), (51, 'Ta'), (52, 'Ta'), (53, 'Ta'), (54, 'Ta'), (55, 'Ta'), (56, 'Ta'), (121, 'O'), (122, 'O'), (123, 'O'), (124, 'O'), (125, 'O'), (126, 'O'), (127, 'O'), (128, 'O'), (157, 'O'), (158, 'O'), (159, 'O'), (160, 'O'), (161, 'O'), (162, 'O'), (163, 'O'), (164, 'O'), (17, 'K'), (18, 'K'), (19, 'K'), (20, 'K'), (97, 'O'), (98, 'O'), (99, 'O'), (100, 'O')]
}
num_layers  = 5                                                            # Number of layers to plot
xlim        = 6                                                            # Maxmium x boundary (equivalent minimum)
ylim        = 30                                                           # Maximum y boundary
ylim_inset  = 5                                                            # Maximum y boundary for inset                                                      
nscf_file   = 'LDOS/t5/8uc/stA/2_58s1_nscf.out'          
total_file  = 'LDOS/t5/8uc/stA/58s1_LDOS.pdos_tot'
dir         = 'LDOS/t5/8uc/stA/58s1_LDOS'
outdir      = 'LDOS/t5/8uc/stA/FINAL(INSET)'
orientation = 'landscape'                                                  # 'portrait' or 'landscape'
save        = False
title       = None                                                         # Optional: set title

#tf.ldos(layers, num_layers, xlim, ylim, ylim_inset, nscf_file, total_file, dir, outdir, orientation, save,title)


### Plots #############################################################################################

# PARAMETERS #
tarray    = [5,6]
file_name = 'Spreadsheets/surface_energy.xlsx'
outdir    = 'Graphs'
save      = False
type      = 'energy'

#tf.plot(type,file_name,tarray,save=save,outdir=outdir)


### Polarisation Calculation (Middle-Layer) #################################################################################

# PARAMETERS #
in_file      = 'stripe/FINAL/t5/bulk/rlx.in'
out_file     = 'stripe/FINAL/t5/bulk/rlx.out'
natoms       = 25
thickness    = 5
step         = 0
phase        = 'bulk'
type         = 'bulk'                                                # Change to 'cation', otherwise keep as 'bulk'
tol          = 1.0                                                   # Tolerance level to determine unit cell layer
layer_tol    = 0.5                                                   # Tolerance level within bil layer of uc layer
born         = {'K':1, 'Ta': 5, 'O': -2}                             # Born (nominal values) charges 
a            = 3.98650146                                            # Lattice parameter
latx         = 1                                                     # Factor by which uc has been increased in x
laty         = 1                                                     # Factor by which uc has been increased in y
verbosity    = 'low'                                                 # Change to 'high' to print out more info
data_file    = 'Spreadsheets/polarisation.csv'
save         = False

#tf.pol_layer(in_file,out_file,type,step,natoms,thickness,phase,tol,layer_tol,born,a,latx,laty,verbosity,save,data_file)