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
layer_atoms = [20,20,20,20,19]
input_file  = 'oxygen_vac/defect/5/rlx.in'
natoms      = 99


#tf.sort_layer(input_file,natoms,layer_atoms,num_layers)


### Computing LDOS ##########################################################################################################

# PARAMETERS (copy from sort layer function and add the comma separations) #
layers = {
'Layer 1': [(25, 'Ta'), (26, 'Ta'), (27, 'Ta'), (28, 'Ta'), (64, 'O'), (65, 'O'), (66, 'O'), (67, 'O'), (84, 'O'), (85, 'O'), (86, 'O'), (87, 'O'), (5, 'K'), (6, 'K'), (7, 'K'), (8, 'K'), (49, 'O'), (50, 'O'), (51, 'O'), (52, 'O')],
'Layer 2': [(33, 'Ta'), (34, 'Ta'), (35, 'Ta'), (36, 'Ta'), (72, 'O'), (73, 'O'), (74, 'O'), (75, 'O'), (92, 'O'), (93, 'O'), (94, 'O'), (95, 'O'), (13, 'K'), (14, 'K'), (15, 'K'), (16, 'K'), (56, 'O'), (57, 'O'), (58, 'O'), (59, 'O')],
'Layer 3': [(37, 'Ta'), (38, 'Ta'), (39, 'Ta'), (40, 'Ta'), (76, 'O'), (77, 'O'), (78, 'O'), (79, 'O'), (96, 'O'), (97, 'O'), (98, 'O'), (99, 'O'), (17, 'K'), (18, 'K'), (19, 'K'), (20, 'K'), (41, 'O'), (42, 'O'), (43, 'O'), (44, 'O')],
'Layer 4': [(21, 'Ta'), (22, 'Ta'), (23, 'Ta'), (24, 'Ta'), (60, 'O'), (61, 'O'), (62, 'O'), (63, 'O'), (80, 'O'), (81, 'O'), (82, 'O'), (83, 'O'), (1, 'K'), (2, 'K'), (3, 'K'), (4, 'K'), (45, 'O'), (46, 'O'), (47, 'O'), (48, 'O')],
'Layer 5': [(29, 'Ta'), (30, 'Ta'), (31, 'Ta'), (32, 'Ta'), (68, 'O'), (69, 'O'), (70, 'O'), (71, 'O'), (88, 'O'), (89, 'O'), (90, 'O'), (91, 'O'), (9, 'K'), (10, 'K'), (11, 'K'), (12, 'K'), (53, 'O'), (54, 'O'), (55, 'O')]
}
num_layers  = 5                                                            # Number of layers to plot
xlim        = 6                                                            # Maxmium x boundary (equivalent minimum)
ylim        = 30                                                           # Maximum y boundary
ylim_inset  = 5                                                            # Maximum y boundary for inset                                                      
nscf_file   = 'LDOS/ovac/defect/2_ovac_d_nscf.out'          
total_file  = 'LDOS/ovac/defect/ovac_d_LDOS.pdos_tot'
dir         = 'LDOS/ovac/defect/ovac_d_LDOS'
outdir      = 'LDOS/ovac/defect/FINAL(INSET)'
orientation = 'portrait'                                                  # 'portrait' or 'landscape'
save        = True
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