import numpy as np
import pandas as pd
from thinfilm import coord

def pol_layer(para_file,output_file,type,step,natoms,thickness,phase,tol,layer_tol,born,a,latx,laty,verbosity,save,data_file):
    '''
    Determines the polarisation from the middle layer of a slab. Use for striped, bulk or cation phases.

    Args:
        para_file (str)   : Path to the paraelectric coordinates file (.in file).
        output_file (str) : Path to the output file containing the relaxed coordinates.
        type (str)        : Type of phase (if cation, change to 'caition. Else keep as 'bulk').
        step (int)        : Step width (for striped phases, else set to 0).
        natoms (int)      : Number of atoms in the system.
        thickness (int)   : Thickness of slab in the z direction.
        phase (str)       : Type of surface. For striped surfaces, they are denoted as Xuc-stA or Xuc-stB, where
                            X represents the number of unit cells in the y direction (i.e. double the step width)
        tol (float)       : Tolerance level for the middle bilayer from other layers.
        layer_tol (float) : Tolerance level within the middle bilayer from the bottom/top K atoms.
        born (dict)       : Dictionary containing the Born effective charges for each element.
        a (float)         : Lattice parameter in Angstroms.
        latx (int)        : Number of unit cells in the x direction.
        laty (int)        : Number of unit cells in the y direction.
        verbosity (str)   : Verbosity level ('high' or 'low'). Set 'high' for detailed output.
        save (bool)       : Whether to save the results to a CSV file or not.
        data_file (str)   : Path to the CSV file for saving the results.


    '''
    
    
    # Obtain paraelectric coordinates, and final relaxed coordinates, as well as elements

    out_x,out_y,out_z,el         = coord(output_file,natoms,filetype='in')
    para_x,para_y,para_z,para_el = coord(para_file,natoms,filetype='in')

    # Filter out the z coords of the K atoms, along with the unique values.

    para_z_K = para_z[para_el == 'K']
    para_z_K_sorted = np.sort(para_z_K)
    para_z_K_unq = np.unique(para_z_K_sorted)

    if verbosity == 'high':
        print(f'\nUnique z values (input coords): {para_z_K_unq}')

    # Determine the bottom and top coordinates of the K atoms corresponding to the middle layer.

    
    if len(para_z_K_unq) == thickness:
        bottom_coord = para_z_K_unq[thickness-4]
        top_coord    = para_z_K_unq[thickness-3]
    elif type == 'cation':
        bottom_coord = para_z_K_unq[thickness-2]
        top_coord    = para_z_K_unq[thickness-1]
    else:
        raise ValueError(f'There should be {thickness} unique z coordinates for the K atoms, but there are {len(para_z_K)} :(')

    # Extract the correct index of these coordinates (also corresponding to y = 0), and obtain the final relaxed coordinate
    # corresponding to the bottom and top K atoms of the middle layer, as well as the midpoint coordinate based on these.

    indices_bot = np.where(para_z_K == bottom_coord)[0]
    indices_top = np.where(para_z_K == top_coord)[0]

    for index in indices_bot:
        if para_y[index] == 0:
            bottom_index = index
            break
    for index in indices_top:
        if para_y[index] == 0:
            top_index = index
            break

    upper_rlx_coord = out_z[top_index]
    lower_rlx_coord = out_z[bottom_index]

    midpoint = (0.5 *(upper_rlx_coord - lower_rlx_coord)) + lower_rlx_coord
    if verbosity == 'high':
        print(f'\nThe z coordinate of the lower K atom in the layer is: {lower_rlx_coord} Angstroms.')
        print(f'The z coordinate of the upper K atom in the layer is: {upper_rlx_coord} Angstroms.')
        print(f'The z coordinate of the midpoint in the layer is: {midpoint} Angstroms.')

    # Filter out all atom coordinates from the relaxed ones which lie in the layer. Some coordinates may be slightly lower/
    # higher than the obtained bottom/top coordinate, so can adjust filter using a tolerance level.


    layer_indices = np.where( (out_z < (midpoint + tol)) & (out_z > (out_z[bottom_index] - tol)) )[0]


    if len(layer_indices) > (5*laty*latx):
        raise ValueError(f'The layer does not contain {5*laty*latx} atoms. Lower the tolerance level.')
    elif len(layer_indices) < (5*laty*latx):
        raise ValueError(f'The layer does not contain {5*laty*latx} atoms. Raise the tolerance level.')

    final_layer_x = []
    final_layer_y = []
    final_layer_z = []
    final_el      = []

    for item in layer_indices:
        final_layer_x.append(float(out_x[item]))
        final_layer_y.append(float(out_y[item]))
        final_layer_z.append(float(out_z[item]))
        final_el.append(str(para_el[item]))

    if verbosity == 'high':
        print(f'\nFinal elements in middle layer: {final_el}')
        print(f'Final z coordinates of middle layer: {final_layer_z}')

    displacement_vals = []

    for num in final_layer_z:
        if num < (lower_rlx_coord + layer_tol):
            displacement = float(lower_rlx_coord - num)
            displacement_vals.append(displacement)
        else:
            displacement = float(midpoint - num)
            displacement_vals.append(displacement)

    if verbosity == 'high':
        print(f'\nDisplacement of each atom (in Angstrom): {displacement_vals}\n')

    displacement_vals = [(entry * 1e-8) for entry in displacement_vals] # in cm

    # Calculate dipole moment sum, and then total polarisation
    dip_mom_tot = 0
    for num in range(len(final_el)):
        dip_mom = born[final_el[num]] * displacement_vals[num] * 1.6e-13     # in µC cm.
        dip_mom_tot = dip_mom_tot + dip_mom

    dip_mom_tot = dip_mom_tot
    vol = (latx*a) * (laty*a) * (upper_rlx_coord - midpoint) * 1e-24     # in cm^3

    pol = dip_mom_tot / vol    # in µC / cm^2

    print(f'\nTotal polarisation of middle layer: {pol} µC/cm^2\n')

    # Append to data (optional)
    if save == True:
        data = pd.read_csv(data_file)
        data.loc[len(data)] = [thickness,step,phase,pol]
        data.to_csv(data_file,index=False)
        print('Succesfully saved to csv file :)')




    
