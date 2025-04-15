import numpy as np
from thinfilm.atoms import coord

def sort_layer(indir,natoms,atom_layer,num_layer):

    '''
    Sort atoms into their corresponding layer. Layers are sorted from bottom to top.
    
    Args:
        indir (str)      : path to the input file
        natoms (int)     : number of atoms in the input file
        atom_layer (list): number of atoms in each layer
        num_layer (int)  : number of layers
    '''


    # Extract coordinates and corresponding elements from input file

    sum_atoms = sum(atom_layer)
    
    if natoms != sum_atoms:
        raise ValueError(f"Total atoms ({natoms}) do not match sum of atoms from layer input ({sum_atoms}) :(")

    x_coord,y_coord,z_coord,element = coord(indir,natoms,filetype='in')

    # Add atom number to each element and coordinate, and sort in ascending order of z-coordinate (once sorted, the z-coordinate can be removed).
    items = []
    for i in range(len(z_coord)):
        items.append((i+1,str(element[i]),float(z_coord[i])))
    sorted_items = sorted(items, key=lambda x: x[2])
    data         = [t[:-1] for t in sorted_items]


    # Create layers dictionary and append atoms to corresponding layers

    layers = {f"'Layer {i+1}'": [] for i in range(num_layer)}
    counter = 0
    for index,item in enumerate(atom_layer):
        for i in range(item):
            layers[f"'Layer {index+1}'"].append(data[counter])
            counter += 1
            if counter == natoms:
                break

    # Print layers dictionary
    for i in layers:
        print(f'{i}:',layers[i])


