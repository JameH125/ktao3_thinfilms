import numpy as np
import pandas as pd


def polarisation(output,input,natoms,x,y,z,born_dict,table_name,dir,csv=False,lat=False,use_born=False):
    '''
    Args:
        output (str)       : path to the output file
        initial (np.array) : initial z coordinates of the atoms
        born_dict (dict)   : dictionary of Born charges for each element
        table_name (str)   : name of the output table

    Returns:
        relax_data (pd.DataFrame) : table containing the polarisation data
        total (float)             : total polarisation
    '''

    # Read output file and extract final coordinates, as well as lattice parameters

    with open(output, "r") as f:
        output_lines = f.readlines()
    with open(input, "r") as g:
        input_lines = g.readlines()

    final_coords   = []
    initial_coords = []
    params         = []

    for i, line in enumerate(output_lines):
        if "End final coordinates" in line:
            final_coords = output_lines[i-natoms:i] 
            break
    
    for i, line in enumerate(input_lines):
        if "ATOMIC_POSITIONS" in line:
            initial_coords = input_lines[i+1:i+1+natoms]  
            break

    if lat == True:        
        for i, line in enumerate(output_lines):
            if "Begin final coordinates" in line:
                params = output_lines[i+5:i+8]  
                break
        lat_x = float(params[0].split()[0])
        lat_y = float(params[1].split()[1])
        lat_z = float(params[2].split()[2])
    else:
        a = 3.98650146
        lat_x = a
        lat_y = a
        lat_z = a
        

    # Extract elements and initial and final coords, as well as lattice parameters.
    elements = [line.split()[0] for line in final_coords]
    if dir == 'z':
        fin_coord = np.array(([line.split()[-1] for line in final_coords])).astype(float)
        in_coord  = np.array(([line.split()[-1] for line in initial_coords])).astype(float)
    if dir == 'x':
        fin_coord = np.array(([line.split()[1] for line in final_coords])).astype(float)
        in_coord  = np.array(([line.split()[1] for line in initial_coords])).astype(float)
    if dir == 'y':
        fin_coord = np.array(([line.split()[2] for line in final_coords])).astype(float)
        in_coord  = np.array(([line.split()[2] for line in initial_coords])).astype(float)

    in_coord_z = np.array(([line.split()[-1] for line in initial_coords])).astype(float)

    #Assigning Born charges to the elements (for the oxygens which have the same z as the K, we assign the Born charge of O_K, else
    # we assign the Born charge of O_Ta). Then convert to microcoulombs.

    tolerance = 0.3
    born=[]
    for i in range(len(elements)):
        if elements[i] == 'K':
            born.append(born_dict['K'])
        elif elements[i] == 'Ta':
            born.append(born_dict['Ta'])
        elif elements[i] == 'O':
            if use_born == True:
                born.append(born_dict['O'])
            else:
                current_coord = in_coord_z[i]

                # Find atoms which have similar z coordinates
                matching_indices = [j for j, coord in enumerate(in_coord_z) if abs(coord - current_coord) <= tolerance]

                # Find the first non-'O' element
                for idx in matching_indices:
                            if elements[idx] == 'K':  
                                born.append(born_dict['O_K'])  # If K, append O_K
                                break  
                            elif elements[idx] == 'Ta':  
                                born.append(born_dict['O_Ta']) # If Ta, append O_Ta
                                break             

    born = [b * 1.6e-13 for b in born]

    # Calculate fractional displacement and convert to lattice displacement (lattice param for z) and then cm.
    displace = []
    
    # Uncomment if using unit cell (as starting coordinates for unit cell were not highs-symmetry positions)

    # in_coord[1] = 0.5
    # in_coord[3] = 0.5
    # in_coord[4] = 0.5

    for i in range(len(elements)):
        if dir == 'z':
            displace.append((fin_coord[i] - in_coord[i]) * 1e-8 )
        if dir == 'x':
            displace.append((fin_coord[i] - in_coord[i]) * 1e-8 )
        if dir == 'y':
            displace.append((fin_coord[i] - in_coord[i]) * 1e-8 )

    # Calculate polarisation for each atom
    pol =[]
    vol = x * lat_x * y * lat_y * z * lat_z * 1e-24
    for i in range(len(elements)):
        pol.append( born[i] * displace[i] / vol )
    

    relax_data = pd.DataFrame({"Atom": elements, "born_charge (μC)": born, "init_coord (frac)": in_coord,"final_coord (frac)": fin_coord, "displacement (cm)": displace, "dipole (μC cm)": pol})
    print(relax_data)

    # Export to csv
    if csv == True:
        relax_data.to_csv(f"relax/{table_name}.csv", index=False)
    print(f'Total Polarisation:', sum(pol), 'μC/cm^2')

    return relax_data, sum(pol)

# Define arguments

born_charges = {'K':1.156, 'Ta': 8.624, 'O_Ta': -6.408, 'O_K': -1.684}
born_charges_nom = {'K':1, 'Ta': 5, 'O': -2}
output_file = "stripe/FINAL/t6/bulk/rlx.out"
input_file  = "stripe/FINAL/t6/bulk/rlx.in"


#Run
data, total = polarisation(output_file,input_file,30,1,1,6,born_charges, "polarisation_data",dir='z',csv=False,lat=False,use_born=False)










def sub_pol(file,natoms,thickness,layers,latx,laty,latz,dir,nom=False):

    # Extract all coordinates and corresponding elements.
    coordinates = []
    with open(file, "r") as f:
        output_lines = f.readlines()

    for i, line in enumerate(output_lines):
        if "End final coordinates" in line:
            coordinates = output_lines[i-natoms:i]  # Get atomic positions
            break

    z = np.array(([line.split()[3] for line in coordinates])).astype(float)
    y = np.array(([line.split()[2] for line in coordinates])).astype(float)
    x = np.array(([line.split()[1] for line in coordinates])).astype(float)
    elements = np.array(([line.split()[0] for line in coordinates]))

    # Determine which layers to choose

    a = (thickness+1)/2             
    if layers % 2 == 0:
        b = int(a + layers/2)        
        a = int(a - layers/2)        
    else:
        b = int(a + (layers-1)/2 + 1)
        a = int(a - (layers-1)/2)
  
    print(f'For a slab of thickness {thickness}, the middle {layers} layers correspond to the {a}th to {b-1}th layer.')
 
    # Extract coordinates correpsponding to the chosen layers; use the K atoms of each layer as reference points.
    tol = 0.5
    # print(z)
    # print(elements)
    k_z_pos = np.sort(z[np.where(elements == 'K')])[a:b+2]
    # print(k_z_pos)
    used_coords_z = []
    used_coords_y = []
    used_coords_x = []
    used_elements = []
    for j in range(len(z)):
        if z[j] <= (k_z_pos[-1] + tol) and z[j] >= (k_z_pos[0] - tol):
            used_coords_z = np.append(used_coords_z,z[j])
            used_coords_y = ((np.append(used_coords_y,y[j])).astype(float))
            used_coords_x = (np.append(used_coords_x,x[j])).astype(float)
            used_elements = np.append(used_elements,elements[j])

    
    used_coords_y = used_coords_y / laty
    used_coords_x = used_coords_x / latx
    zlen = (max(used_coords_z) - min(used_coords_z))
    used_coords_z = (used_coords_z - min(used_coords_z)) / latz
    print('Final chosen coordinates extracted.')
    print(used_coords_x)
    # print(zlen)
    

    # Write high symmetry positions (in fractional coordinates) for the chosen layers (UPDATE EACH TIME)

    high_sym_x = [0,0,0,0,0.5,0.5,0.5,0.5,0.5,0.5,0,0,0.5,0.5]
    high_sym_y = [0,0.5,0,0.5,0.25,0.75,0.25,0.75,0.25,0.75,0.25,0.75,0,0.5]
    high_sym_z = [0,0,1,1,0.5,0.5,1,1,0,0,0,0.5,0.5,0.5]
    
    
    
    # Assign Born charges to the elements (comment out if using nominal values)
    born = []

    if nom == False:
        for i in range(len(used_elements)):
            if used_elements[i] == 'K':
                born.append(born_charges['K'])
            elif used_elements[i] == 'Ta':
                born.append(born_charges['Ta'])
            elif used_elements[i] == 'O':
                if high_sym_z[i] == 0 or high_sym_z[i] == 1:
                    born.append(born_charges['O_K'])
                if high_sym_z[i] == 0.5:
                    born.append(born_charges['O_Ta'])
            else:
                print('Error in assigning Born Charges :(')
    else:
        for i in range(len(used_elements)):
            if used_elements[i] == 'K':
                born.append(born_charges_nom['K'])
            elif used_elements[i] == 'Ta':
                born.append(born_charges_nom['Ta'])
            elif used_elements[i] == 'O':
                born.append(born_charges_nom['O'])
            else:
                print('Error in assigning Born Charges :(')       

    # print(born)  
    # Calculate displacements

    if dir == 'x':
        displace = used_coords_x - high_sym_x
    if dir == 'y':
        displace = used_coords_y - high_sym_y
    if dir == 'z': 
        displace = used_coords_z - high_sym_z

    # Calculate polarisation
    dipole_sum = 0
    for i in range(len(used_elements)):
        if nom == True:
            dipole_sum += born[i] * displace[i] * 1.6e-13 * 1e-8
        else:
            dipole_sum += born[i] * displace[i] * 1.6e-13 * 1e-8
    

    print(f'Total dipole sum: {dipole_sum}')
    volume = latx * laty * zlen * 1e-24
    total_pol = dipole_sum / volume
    print(f'Total polarisation in {dir} direction: {total_pol}')


# sub_pol("striped/thick_5/2uc/stripe1/para/rlx.out",45,5,2,3.9865000248,2*3.9865000248,3.9865000248,dir='x',nom=True)
