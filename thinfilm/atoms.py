
import numpy as np

def coord(input_file,natoms,filetype):
    '''
    Extract coordinates from QE input file.

    Args:
        input_file (str)   : path to the input file
        natoms     (int)   : number of atoms in the input file 
        filetype   (str)   : 'in' or 'out' file
    Returns:
        x_coord (np.array) : x coordinates of the atoms
        y_coord (np.array) : y coordinates of the atoms
        z_coord (np.array) : z coordinates of the atoms
        element (np.array) : element of the atoms 
    '''
    coords = []
    with open(input_file, "r") as f:
        coords = f.readlines()

    if filetype == 'in':
        for i, line in enumerate(coords):
            if "ATOMIC_POSITIONS" in line:
                coords = coords[i+1:i+natoms+1] 
                break
    elif filetype == 'out':
        for i, line in enumerate(coords):
            if "Begin final coordinates" in line:
                coords = coords[i+3:i+natoms+3] 
                break
    

    x_coord  = np.array(([line.split()[1] for line in coords])).astype(float)
    y_coord  = np.array(([line.split()[2] for line in coords])).astype(float)        
    z_coord  = np.array(([line.split()[3] for line in coords])).astype(float)
    element  = np.array(([line.split()[0] for line in coords])).astype(str)

    return x_coord,y_coord,z_coord,element