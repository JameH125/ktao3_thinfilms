import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def plot(type,file_name,tarray,outdir=None,save=False):
    '''
    Produces plots (energy or polarisation) for A and B stripe terminations (surface energy against step width). Seperate 
    plots for each thickness. Requires the input excel file to have separate sheets for each thickness, denoted as t5, t6 etc.

    Args:
        type      (str)       : type of plot to produce ('energy' or 'polarisation')
        file_name (str)       : input excel file
        tarray    (np.array)  : array containing thicknesses of slabs to plot
        save      (bool)      : save plots
        outdir    (str)       :(optional) directory to save figures
    '''

    data = {}

    # Split into phases

    for num in tarray:
        sheet_name = f"t{num}"
        data[f"data_{num}"]       = pd.read_excel(file_name, sheet_name=sheet_name)
        data[f"data_{num}A"]      = (data[f"data_{num}"])[(data[f"data_{num}"])['Phase'].str.contains('stA', na=False)]
        data[f"data_{num}B"]      = (data[f"data_{num}"])[(data[f"data_{num}"])['Phase'].str.contains('stB', na=False)]
        if num != 7:
            data[f"data_{num}cation"] = (data[f"data_{num}"])[(data[f"data_{num}"])['Phase'].str.contains('cation', na=False)]
        if type == 'energy':
            data[f"data_{num}bulk"]   = (data[f"data_{num}"])[(data[f"data_{num}"])['Phase'].str.contains('bulk', na=False)]
        if num == 5:
            data[f"data_{num}vac"]   = (data[f"data_{num}"])[(data[f"data_{num}"])['Phase'].str.contains('vac', na=False)]
    # Plots
    
    for num in tarray:
        if type == 'energy':
            plt.scatter((data[f"data_{num}A"])['Step'],(data[f"data_{num}A"])['Surface Energy (J/m^2)'],label='A',marker='o',color='#2e854d')
            plt.scatter((data[f"data_{num}B"])['Step'],(data[f"data_{num}B"])['Surface Energy (J/m^2)'],label='B',marker='o',color='#b32020')
            plt.axhline(y=data[f"data_{num}bulk"].iloc[0]['Surface Energy (J/m^2)'],label='bulk',linestyle='--',color='black')
            if num == 5:
                plt.axhline(y=data[f"data_{num}vac"].iloc[0]['Surface Energy (J/m^2)'],label='oxygen vacancy',linestyle='--',color='blue')
            if num != 7:
                plt.axhline(y=data[f"data_{num}cation"].iloc[0]['Surface Energy (J/m^2)'],label='cation',linestyle='--',color='orange')
        elif type == 'polarisation':
            plt.scatter((data[f"data_{num}A"])['Step'],(data[f"data_{num}A"])['Polarisation µC / cm^2'],label='A',marker='o',color='#2e854d')
            plt.scatter((data[f"data_{num}B"])['Step'],(data[f"data_{num}B"])['Polarisation µC / cm^2'],label='B',marker='o',color='#b32020')
            if num != 7:
                plt.axhline(y=data[f"data_{num}cation"].iloc[0]['Polarisation µC / cm^2'],label='cation',linestyle='--',color='orange')
        
        
        plt.xlabel('Step Width')
        if type == 'energy':
            plt.ylabel(r'Surface Energy / $Jm^{-2}$')
        elif type == 'polarisation':
            plt.ylabel(r'Polarisation / $\mu C cm^{-2}$')
        plt.xticks([0,1,2,3,4,5])
        plt.legend()
        plt.grid()

        if num != 7:
            if type == 'energy':
                interp_func_A = interp1d((data[f"data_{num}A"])['Step'], (data[f"data_{num}A"])['Surface Energy (J/m^2)'], kind='quadratic')
                interp_func_B = interp1d((data[f"data_{num}B"])['Step'], (data[f"data_{num}B"])['Surface Energy (J/m^2)'], kind='quadratic')
            elif type == 'polarisation':
                interp_func_A = interp1d((data[f"data_{num}A"])['Step'], (data[f"data_{num}A"])['Polarisation µC / cm^2'], kind='quadratic')
                interp_func_B = interp1d((data[f"data_{num}B"])['Step'], (data[f"data_{num}B"])['Polarisation µC / cm^2'], kind='quadratic')
            x_smooth_A = np.linspace(min((data[f"data_{num}A"])['Step']), max((data[f"data_{num}A"])['Step']), 100)
            y_smooth_A = interp_func_A(x_smooth_A)
            x_smooth_B = np.linspace(min((data[f"data_{num}B"])['Step']), max((data[f"data_{num}B"])['Step']), 100)
            y_smooth_B = interp_func_B(x_smooth_B)

            plt.plot(x_smooth_A, y_smooth_A, linestyle='-', color='#2e854d')
            plt.plot(x_smooth_B, y_smooth_B, linestyle='-', color='#b32020')
        plt.xticks([0,1,2,3,4,5])
        
        if save == True:
            if type == 'energy':
                plt.savefig(f'{outdir}/t{num}_energy.png')
            elif type == 'polarisation':
                plt.savefig(f'{outdir}/t{num}_polarisation.png')  
        plt.show()   








    # plt.plot(data_6A['step'],data_6A['Surface Energy (J/m^2)'],label='A',marker='o',color='r')
    # plt.plot(data_6B['step'],data_6B['Surface Energy (J/m^2)'],label='B',marker='o',color='b')
    # plt.axhline(y=data_6.loc[(data_6['step'] == 0), 'Surface Energy (J/m^2)'], color='blue', linestyle='-', label='bulk')
    # plt.xlabel('Step Width')
    # plt.ylabel(r'Surface Energy / $Jm^{-2}$')
    # plt.legend()
    # plt.grid()
    # # plt.savefig('Graphs/t6.png')
    # plt.show()