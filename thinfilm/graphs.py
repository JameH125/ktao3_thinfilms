import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Load data
cutoff_data = pd.read_csv('Convergence/cutoff_energies.csv')
kpoints_data = pd.read_csv('Convergence/k_point_energies.csv')

# Convert Ry to meV (1 Ry = 13.605704 eV * 1000 = 13605.704 meV)
cutoff_data['energy'] = 13605.704 * (cutoff_data['energy'] - cutoff_data['energy'].iloc[-1])
kpoints_data['energy'] = 13605.704 * (kpoints_data['energy'] - kpoints_data['energy'].iloc[-1])

# Data for plotting
cutoffs = cutoff_data['cutoff']
kpoints = kpoints_data['k-points']

# =============================================
# 1. Cutoff Convergence Plot with Inset
# =============================================
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.scatter(cutoffs, cutoff_data['energy'], marker='x', color='C0')
ax1.set_xlabel('Energy Cutoff (Ry)', fontsize=12)
ax1.set_ylabel('Energy (meV)', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.7)

# Add inset
inset1 = inset_axes(ax1, width="60%", height="40%", loc='upper right')
inset1.scatter(cutoffs[4:], cutoff_data['energy'][4:], marker='x', color='C0')
inset1.set_xlabel('Cutoff (Ry)', fontsize=8)
inset1.set_ylabel('Energy (meV)', fontsize=8)
inset1.grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig('Convergence/cutoff_convergence.png', dpi=600, bbox_inches='tight')
plt.show()

# =============================================
# 2. K-point Convergence Plot with Inset
# =============================================
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.scatter(kpoints, kpoints_data['energy'], marker='x', color='C1')
ax2.set_xlabel('Number of k-points', fontsize=12)
ax2.set_ylabel('Energy (meV)', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.7)

# Add inset
inset2 = inset_axes(ax2, width="40%", height="40%", loc='upper right')
inset2.scatter(kpoints[1:], kpoints_data['energy'][1:], marker='x', color='C1')
inset2.set_xlabel('Number of k-points', fontsize=8)
inset2.set_ylabel('Energy (meV)', fontsize=8)
inset2.grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig('Convergence/kpoint_convergence.png', dpi=600, bbox_inches='tight')
plt.show()