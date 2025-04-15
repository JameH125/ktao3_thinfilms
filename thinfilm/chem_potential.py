import numpy as np
import matplotlib.pyplot as plt

## CHEMICAL POTENTIAL VALUES FROM DFT (in eV)

# Bulk
mu_ktao3 = -296.030198 * 13.605698066
# Elements
mu_k     = -56.92729088 * 13.605698066
mu_ta    = -141.71841956 * 13.605698066
mu_o     = (-64.15766454 / 2) * 13.605698066

# Oxides
mu_k2o   = (-584.92323852 / 4) * 13.605698066
mu_ta2o5 = (-891.00191967 / 2) * 13.605698066
mu_k2o2  = (-713.76089166 / 4) * 13.605698066

## FORMATION ENERGIES FROM DFT (in eV)     1Ry = 13.605698066 eV

ktao3_form_el = (mu_ktao3 - 3*mu_o - mu_k - mu_ta)
ktao3_form_ox = (mu_ktao3 - 0.5 * mu_k2o - 0.5 * mu_ta2o5)


print('mu_ktao3: ', mu_ktao3)
print('mu_k: ', mu_k)
print('mu_ta: ', mu_ta)
print('mu_o: ', mu_o)
print('mu_k2o: ', mu_k2o)
print('mu_ta2o5: ', mu_ta2o5)
print('mu_k2o2: ', mu_k2o2)
print('ktao3_form_el: ', ktao3_form_el)
print('ktao3_form_ox: ', ktao3_form_ox)


print((mu_ta2o5 - 2*mu_ta) / 5)
print((mu_k2o - 2*mu_k))
print((mu_k2o2 - 2*mu_k) / 2)

# Element constraints
plt.axvline(x=0, color='red', linestyle='-')
plt.axvline(x=ktao3_form_el / 3, color='red', linestyle='-')

plt.axhline(y=0, color='goldenrod', linestyle='-')
plt.axhline(y=ktao3_form_el, color='goldenrod', linestyle='-')

# Oxide constraints
xvalues = np.arange(-6, 2, 1)

def ta2o5(x):
    return (-2.5*(x + mu_o)) + 0.5*mu_ta2o5 - mu_ta
def k2o(x):
    return 0.5*(-5*(x + mu_o) +2*mu_ktao3 - mu_k2o - 2*mu_ta)
def k2o2(x):
    return 0.5*(-4*(x + mu_o) +2*mu_ktao3 - mu_k2o2 - 2*mu_ta)

xbound = [ktao3_form_el/3, ktao3_form_el/3,(-mu_k2o+mu_k2o2-mu_o),0,0,(-(mu_ta+2.5*mu_o-0.5*mu_ta2o5)/2.5)]
ybound = [0,k2o(ktao3_form_el/3),k2o2((-mu_k2o+mu_k2o2-mu_o)),k2o2(0),ta2o5(0),0]

plt.plot(xvalues, ta2o5(xvalues), color='blue', linestyle='-',label=r'$Ta_2O_5$')
plt.plot(xvalues, k2o(xvalues), color='purple', linestyle='-',label=r'$K_2O$')
plt.plot(xvalues, k2o2(xvalues), color='green', linestyle='-',label=r'$K_2O_2$')

plt.xlabel(r'$\Delta\mu_O$ (eV)')
plt.ylabel(r'$\Delta\mu_{Ta}$ (eV)')

plt.xlim(-6, 0.1)
plt.ylim(-18, 0.4)
plt.grid()
plt.fill(xbound, ybound, color='green', alpha=0.3)
plt.legend()
plt.show()


# Oxygen Vacancy Struture

mu_o_max = mu_o / 13.605698066                       # Ry
mu_o_min = (mu_o + (ktao3_form_el/3)) / 13.605698066     # Ry
a = 3.98650146
x = 2*a
y = 2*a

e_tot = -5887.4959391089                             # Ry
e_tot_1 = -5854.983529

#print(mu_o_min,mu_o_max)
e_min = e_tot + mu_o_min
e_max = e_tot + mu_o_max

e_min_1 = e_tot_1 + 2*mu_o_min
e_max_1 = e_tot_1 + 2*mu_o_max

surface_energy_min = ((e_min - 20*(-296.03019878)) / (2*x*y) ) * 217.99
surface_energy_max = ((e_max - 20*(-296.03019878)) / (2*x*y) ) * 217.99

surface_energy_min_1 = ((e_min_1 - 20*(-296.03019878)) / (2*x*y) ) * 217.99
surface_energy_max_1 = ((e_max_1 - 20*(-296.03019878)) / (2*x*y) ) * 217.99

o_pot_limit = [ktao3_form_el/3,0]

surf_energy = [surface_energy_min,surface_energy_max]
surf_energy_1 = [surface_energy_min_1,surface_energy_max_1]

plt.plot(o_pot_limit,surf_energy,marker='',color='#2e854d',label='Oxygen Vacancy')
plt.plot(o_pot_limit,surf_energy_1,marker='',color='purple',label='Double Oxygen Vacancy')
plt.axhline(y=1.134, color='goldenrod', linestyle='-',label='Bulk-terminated')
plt.axhline(y=1.163, color='#b32020', linestyle='-',label='Cation')
plt.axvline(x=0, color='black', linestyle='--',label='Oxygen-Rich')
plt.axvline(x=ktao3_form_el/3, color='black', linestyle='--',label='Oxygen-Poor')
plt.xlim(-6, 1)
plt.grid()
plt.legend()
plt.xlabel('Oxygen Chemical Potential / eV')
plt.ylabel(r'Surface Energy / $Jm^{-2}$')






plt.show()





