import pandas as pd
import os


def surface_energy(uc_energy,outdir,thick,phase,step,x,y,nucell,data,csvdir=None,exceldir=None,csv=False):

    '''
    Calculates the surface energy of a structure using the typical formula E_surf = (E_total - nucell*E_uc) / (2A),
    using the QE output file. Resulting table contains surface energy in both Ry/Angstrom^2 and J/m^2.


    Args:
        uc_energy (float)  : energy of one unit cell in Ry
        outdir    (str)    : path to the output file
        thick     (int)    : thickness of the slab (in z direction)
        phase     (str)    : name of surface termination
        step      (int)    : step width
        x         (float)  : x lattice parameter (Angstrom)
        y         (float)  : y lattice parameter (Angstrom)
        nucell    (int)    : number of unit cells in the slab (total atoms / 5 for KTaO3)
        data      (str)    : path to the data file (will write to a new file if it doesn't exist)
        csvdir    (str)    : path to the csv file
        exceldir  (str)    : path to the excel file
        csv       (bool)   : save data to csv file
    Returns:
        energy_table (pd.DataFrame) : table containing the surface energies
    '''

    # Open table containing surface energies

    if os.path.exists(data):
        energy_table = pd.read_csv(data)
        print("✅ Loaded data table.")
    else:
        energy_table = pd.DataFrame()
        print("⚠️ File not found. Returning an empty DataFrame.")

    # Read output file and extract total energy

    with open(outdir, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "Final energy" in line:
            energy_line = lines[i]                    
            break
    tot_energy = float(energy_line.split()[3])

    # Calculate surface energy

    surf_energy_1 = (tot_energy - (nucell*uc_energy)) / (2*x*y)       # Surface energy in Ry/Angstrom^2
    surf_energy_2 = surf_energy_1 * 217.99                              # Surface energy in J/m^2

    # Add data to table

    energy_table.loc[len(energy_table)] = [thick,step,nucell,phase,uc_energy,tot_energy,surf_energy_1,surf_energy_2]
    if csv == True:
        energy_table.to_csv(csvdir,index=False)

    print(energy_table)
    return energy_table
