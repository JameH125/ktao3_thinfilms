import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms

# Ry to eV conversion factor
ry = 13.605698066


# Chemical potential values from DFT (in Ry)
mu_ktao3 = -296.030198
mu_k     = -56.92729088 
mu_ta    = -141.71841956
mu_o     = (-64.15766454 / 2)
ktao3_form_el = (mu_ktao3 - 3*mu_o - mu_k - mu_ta)


# UC Parameters
a = 3.98650146                                                    # (Angstrom)
x = 2*a
y = 2*a


e_o_vac        = -5887.4959391089                                 # Ry
e_double_o_vac = -5854.9835289200                                 # Ry

e_o_vac_max = e_o_vac + mu_o
e_o_vac_min = e_o_vac + (mu_o + (ktao3_form_el/3))

e_double_o_vac_max = e_double_o_vac + 2*(mu_o)
e_double_o_vac_min = e_double_o_vac + 2*(mu_o + (ktao3_form_el/3))


surf_energy_ovac_min = ((e_o_vac_min - 20*(-296.03019878)) / (2*x*y) ) * 217.99
surf_energy_ovac_max = ((e_o_vac_max - 20*(-296.03019878)) / (2*x*y) ) * 217.99


surf_energy_dovac_min = ((e_double_o_vac_min - 20*(-296.03019878)) / (2*x*y) ) * 217.99
surf_energy_dovac_max = ((e_double_o_vac_max - 20*(-296.03019878)) / (2*x*y) ) * 217.99

o_pot_limit = [(ktao3_form_el/3)*ry,0]

surf_energy_ovac  = [surf_energy_ovac_min,surf_energy_ovac_max]
surf_energy_dovac = [surf_energy_dovac_min,surf_energy_dovac_max]



fig = plt.figure()
ax1 = fig.add_axes((0.1,0.3,0.8,0.6))

ax1.plot(o_pot_limit,surf_energy_ovac,marker='',color='#2e854d',label='Oxygen Vacancy')
ax1.plot(o_pot_limit,surf_energy_dovac,marker='',color='purple',label='Double Oxygen Vacancy')
ax1.axhline(y=1.134, color='goldenrod', linestyle='-',label='Bulk-terminated')
ax1.axhline(y=1.163, color='#b32020', linestyle='-',label='Cation')
ax1.axvline(x=0, color='black', linestyle='--')
ax1.text(0.1,2,'Oxygen-Rich',rotation=90)
ax1.axvline(x=(ktao3_form_el/3)*ry, color='black', linestyle='--')
ax1.text(((ktao3_form_el/3)*ry)-0.18,2,'Oxygen-Poor',rotation=90)

ax1.set_xlim(-6, 1)
ax1.grid()
ax1.legend(loc='lower right')
ax1.set_xlabel('Oxygen Chemical Potential / eV')
ax1.set_ylabel(r'Surface Energy / $Jm^{-2}$')


#mu_o dictionary
mu_o_dict = {
    '100': -0.0747,
    '200': -0.1703,
    '300': -0.2738,
    '400': -0.3824,
    '500': -0.4950,
    '600': -0.6109,
    '700': -0.7295,
    '800': -0.8505,
    '900': -0.9738,
    '1000': -1.0991
}

k_B = 8.617e-5
def pressure(mu,T):
    return np.exp((2*(mu - mu_o_dict[f'{T}'])) / (k_B*T))

temps = [300,600]
mu = np.arange(-6,2,1)

pressure_100 = pressure(mu, 300)
pressure_400 = pressure(mu, 500)
pressure_700 = pressure(mu, 700)
pressure_1000 = pressure(mu, 1000)


pressure_100_labels = [''] * len(pressure_100)
pressure_400_labels = [''] * len(pressure_400)
pressure_700_labels = [''] * len(pressure_700)
pressure_1000_labels = [''] * len(pressure_1000)

for x in range(len(pressure_100)):
    exponent_100 = str(int((np.floor(np.log10(abs(pressure_100[x]))))))
    exponent_400 = str(int((np.floor(np.log10(abs(pressure_400[x]))))))
    exponent_700 = str(int((np.floor(np.log10(abs(pressure_700[x]))))))
    exponent_1000 = str(int((np.floor(np.log10(abs(pressure_1000[x]))))))
    pressure_100_labels[x] = fr'$10^{{{exponent_100}}}$'
    pressure_400_labels[x] = fr'$10^{{{exponent_400}}}$'
    pressure_700_labels[x] = fr'$10^{{{exponent_700}}}$'
    pressure_1000_labels[x] = fr'$10^{{{exponent_1000}}}$'

ax2 = fig.add_axes((0.1,0.20,0.8,0.0))
ax2.yaxis.set_visible(False)
ax2.set_xticks(mu)
ax2.set_xticklabels(pressure_100_labels)
ax2.text(-0.04, 0.5, '100 K', transform=ax2.transAxes, ha='right', va='center')  
ax2.text(1.02, 0.5, 'Pressure / atm', transform=ax2.transAxes, ha='left', va='center')

ax3 = fig.add_axes((0.1,0.15,0.8,0.0))
ax3.yaxis.set_visible(False)
ax3.set_xticks(mu)
ax3.set_xticklabels(pressure_400_labels)
ax3.text(-0.04, 0.5, '400 K', transform=ax3.transAxes, ha='right', va='center')  
ax3.text(1.02, 0.5, 'Pressure / atm', transform=ax3.transAxes, ha='left', va='center')

ax4 = fig.add_axes((0.1,0.1,0.8,0.0))
ax4.yaxis.set_visible(False)
ax4.set_xticks(mu)
ax4.set_xticklabels(pressure_700_labels)
ax4.text(-0.04, 0.5, '700 K', transform=ax4.transAxes, ha='right', va='center')  
ax4.text(1.02, 0.5, 'Pressure / atm', transform=ax4.transAxes, ha='left', va='center')


ax4 = fig.add_axes((0.1,0.05,0.8,0.0))
ax4.yaxis.set_visible(False)
ax4.set_xticks(mu)
ax4.set_xticklabels(pressure_1000_labels)
ax4.text(-0.04, 0.5, '1000 K', transform=ax4.transAxes, ha='right', va='center')  
ax4.text(1.02, 0.5, 'Pressure / atm', transform=ax4.transAxes, ha='left', va='center')
plt.show()