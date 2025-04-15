import numpy as np
import pandas as pd


## DRAFT (NOT IN USE)
# Cell Parameters (DO NOT CHANGE)


cell_energy = -296.2974093
a = 3.98650146                                                        # Lattice parameter in Angstrom

def surface_energy_1(scf,fix,thick,phase,x,y,nucell):


    # Read output file and extract total energy

    with open(scf, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "!" in line:
            energy_line = lines[i]                    
            break
    as_cleaved_energy = float(energy_line.split()[4])

    with open(fix, "r") as g:
        line_1 = g.readlines()

    for i, lines in enumerate(line_1):
        if "Final energy" in lines:
            energy_lines = line_1[i]                    
            break
    fix_energy = float(energy_lines.split()[3])

    # Calculate surface energy

    gamma_0 = (as_cleaved_energy - (nucell*cell_energy)) / (2*x*y)      
    relax = fix_energy - as_cleaved_energy
    surf_energy_1 = gamma_0 + (relax/(x*y))   
    surf_energy_2 = surf_energy_1 * 217.99                              # Surface energy in J/m^2                     

    # Add data to table

    df = pd.DataFrame({'thick':[thick],'nucell':[nucell],'phase':[phase],'cell_energy':[cell_energy],'surf_energy_1':[surf_energy_1],'surf_energy_2':[surf_energy_2]})
    df.to_csv('method2.csv',index=False)
    



surface_energy_1('striped/thick_5/bulk1/5_bulk_scf.out','striped/thick_5/bulk1/5_bulk_rlx_u.out',5,'stripe2',a,a,5) 