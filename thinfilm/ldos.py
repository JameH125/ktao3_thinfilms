import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def ldos(layers, num_layers, xlim, ylim, ylim_inset, nscf_file, total_file, dir, outdir, orientation, save, title=None):
    '''
    Plots the layer-resolved local density of states (LDOS) for a given set of layers. Layers are taken from the output
    of the sort_layer function. The Fermi energy is extracted from the nscf file. Uses files obtained from projwfc.x run
    in Quantum Espresso.

    Args:
        layers (dict)     : Dictionary containing the layers and their corresponding atoms.
        num_layers (int)  : Number of layers to plot.
        xlim (float)      : X-axis limit for the main plot (Also serves as the minimum).
        ylim (float)      : Y-axis limit for the main plot.
        ylim_inset (float): Y-axis limit for the inset plot.
        nscf_file (str)   : Path to the nscf file containing the Fermi energy.
        total_file (str)  : Path to the total DOS file (.pdos_tot file)
        dir (str)         : Directory containing the PDOS files. Must end with the prefix of the PDOS files.
        outdir (str)      : Output directory for saving the plots.
        orientation (str) : Orientation of the plot ('landscape' or 'portrait').
        save (bool)       : Whether to save the plot or not.
        title (str)       : Title of the plot (optional)


    '''
    os.makedirs(outdir, exist_ok=True)
    layer_dos = {layer: None for layer in layers}

    # Extract Fermi Energy
    with open(nscf_file, "r") as f:
        lines = f.readlines()
    for line in lines:
        if "the Fermi energy" in line:
            fermi_energy = float(line.split()[-2])
            break

    # Read total DOS for energy values
    try:
        total_dos_data = np.loadtxt(total_file)
        energy = total_dos_data[:, 0]
    except FileNotFoundError:
        print(f"File not found: {total_file}")
        exit()

    # Sum DOS for each layer
    for layer, atoms in layers.items():
        for atom, species in atoms:
            atom_files = glob.glob(f'{dir}.pdos_atm#{atom}({species})_wfc#*')
            for filename in atom_files:
                try:
                    data = np.loadtxt(filename)
                    if layer_dos[layer] is None:
                        layer_dos[layer] = data
                    else:
                        layer_dos[layer][:, 1] += data[:, 1]
                except FileNotFoundError:
                    print(f"File not found: {filename}")

    # Save layer-resolved DOS
    for layer, dos in layer_dos.items():
        if dos is not None:
            np.savetxt(f'{outdir}/{layer}_dos.dat', dos)

    # Create figure
    if orientation == 'landscape':
        fig, axs = plt.subplots(num_layers, 1, sharex=True, figsize=(16, 12))
    elif orientation == 'portrait':
        fig, axs = plt.subplots(num_layers, 1, sharex=True, figsize=(6, 12))

    max_dos = 0
    for i in range(num_layers):
        filename = f"{outdir}/Layer {i+1}_dos.dat"
        try:
            data = np.loadtxt(filename)
            if np.max(data[:, 1]) > max_dos:
                max_dos = np.max(data[:, 1])
        except FileNotFoundError:
            print(f"File not found: {filename}")

    # Plot layers with refined inset
    for i in range(num_layers):
        filename = f"{outdir}/Layer {num_layers - i}_dos.dat"
        try:
            data = np.loadtxt(filename)
            energy = data[:, 0]
            dos = data[:, 1]
            axs[i].plot(energy, dos, color='blue', linewidth=1.5)
            axs[i].set_xlim(-xlim, xlim)
            axs[i].set_ylim(0, ylim)
            axs[i].axvline(x=fermi_energy, color='black', linestyle='--', linewidth=1)

            # Add smaller inset with translucent background
            inset = inset_axes(
                axs[i],
                width="20%", 
                height="20%",
                loc='upper right',
                borderpad=1
            )

            inset.plot(energy, dos, color='red', linewidth=1.2)
            inset.set_xlim(fermi_energy - 0.5, fermi_energy + 0.5)
            inset.set_ylim(0, ylim_inset)
            inset.axvline(x=fermi_energy, color='black', linestyle=':', linewidth=0.8)
            inset.grid(True, linestyle=':', alpha=0.3)

            # Customize tick labels with translucent background
            for label in inset.get_xticklabels() + inset.get_yticklabels():
                label.set_bbox(dict(
                    facecolor='white', 
                    alpha=0.8,  # 80% transparency
                    edgecolor='none',
                    boxstyle='round,pad=0.2'
                ))
                label.set_fontsize(8)  

        except FileNotFoundError:
            print(f"File not found: {filename}")

    # Customize plot
    axs[-1].set_xlabel('Energy (eV)', fontsize=12)
    if title is not None:
        plt.suptitle(title, fontsize=14, y=0.95)
    plt.subplots_adjust(hspace=0.5)

    # Save plot
    if save:
        if orientation == 'landscape':
            plt.savefig(f'{outdir}/LDOS_landscape.png', dpi=300, bbox_inches='tight')
        elif orientation == 'portrait':
            plt.savefig(f'{outdir}/LDOS_portrait.png', dpi=300, bbox_inches='tight')

    plt.show()