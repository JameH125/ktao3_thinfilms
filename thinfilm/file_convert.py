from ase.io import *
from numpy import *

def convert_file(input,in_dir,out_dir,pseudo_dir,pseudo):

    '''
    Converts between VASP and Quantum Espresso input and output files. Note not all parameters will be filled in for in files.

    Args:
        input      (str)   : file extension of input file ('vasp','in','out')
        out_dir    (str)   : file to output  (path)
        in_dir     (str)   : file to input   (path)
        pseudo_dir (str)   : directory containing the pseudopotentials
        pseudo     (dict)  : dictionary containing the pseudopotentials
    '''

    if input == 'vasp':
        file = read(in_dir, format='vasp')
        write(out_dir,file, format='espresso-in', pseudopotentials=pseudo,pseudo_dir=pseudo_dir)
        print(f'{input} file has been succesfully converted into a QE input file :)')
    elif input == 'in':
        file = read(in_dir, format='espresso-in')
        write(out_dir,file, format='vasp', direct=True)
        print(f'{input} file has been succesfully converted into a VASP file :)')
    elif input == 'out':
        file = read(in_dir, format='espresso-out', index=-1)
        write(out_dir,file, format='vasp', direct=True)
        print(f'{input} file has been succesfully converted into a VASP file :)')
