import numpy as np
import matplotlib.pyplot as plt

# Set publication style
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.2

# Temperature range
T = np.linspace(60, 130, 300)

# Sigmoid parameters
T_m = 90.0   # °C
k_sigma = 0.08  # °C^-1
sigma_T = 1.0 / (1.0 + np.exp(-k_sigma * (T - T_m)))

# Energy balance parameters (from Table 3 & 4)
m_mof = 5.0     # kg
c_mof = 0.8     # kJ/(kg*K)
q_adsorbed = 0.805 # kg CO2 adsorbed
M_CO2 = 0.04401 # kg/mol
delta_H = 45.0  # kJ/mol

m_released = q_adsorbed * sigma_T
Q_sensible = m_mof * c_mof * (T - 25.0)
Q_desorb = (m_released / M_CO2) * delta_H
Q_total = Q_sensible + Q_desorb
intensity = Q_total / np.maximum(m_released, 1e-4) # kJ / kg CO2 released

fig, ax1 = plt.subplots(figsize=(8.0, 5.0), dpi=300)

# Target operating window highlight (100°C - 115°C)
ax1.axvspan(100, 115, color='#10b981', alpha=0.12, label='Target Operating Window (100–115 °C)', zorder=1)

# Grid
ax1.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1', zorder=1)

# Left Axis: Sigmoid release fraction
line1 = ax1.plot(T, sigma_T, color='#2563eb', linewidth=2.8, label=r'Desorption Release Fraction $\sigma(T)$', zorder=3)
ax1.set_xlabel(r'Bed Regeneration Temperature $T$ (°C)', fontsize=12, fontweight='bold', color='#0f172a', labelpad=8)
ax1.set_ylabel(r'Desorption Release Fraction $\sigma(T)$ (Dimensionless)', fontsize=12, fontweight='bold', color='#2563eb', labelpad=8)
ax1.set_xlim(60, 130)
ax1.set_ylim(0, 1.05)
ax1.tick_params(axis='y', colors='#2563eb', labelsize=10.5)
ax1.tick_params(axis='x', colors='#334155', labelsize=10.5)

# Inflection midpoint point (90°C, 50%)
ax1.scatter([90.0], [0.50], color='#1d4ed8', s=55, zorder=5)
ax1.annotate(
    r'Inflection Midpoint ($T_m = 90$ °C, $\sigma = 0.50$)',
    xy=(90.0, 0.50),
    xytext=(65, 0.62),
    fontsize=10,
    fontweight='bold',
    color='#1e3a8a',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#eff6ff', edgecolor='#93c5fd', lw=1.2),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.15', color='#1d4ed8', lw=1.4),
    zorder=6
)

# Right Axis: Specific energy intensity
ax2 = ax1.twinx()
line2 = ax2.plot(T, intensity, color='#dc2626', linewidth=2.5, linestyle='--', label=r'Specific Energy Intensity ($Q_{\mathrm{total}} / m_{\mathrm{released}}$)', zorder=3)
ax2.set_ylabel(r'Specific Energy Intensity (kJ / kg CO$_2$ Released)', fontsize=12, fontweight='bold', color='#dc2626', labelpad=8)
ax2.set_ylim(1000, 5500)
ax2.tick_params(axis='y', colors='#dc2626', labelsize=10.5)

# Optimal point annotation at 110°C
T_opt = 110.0
sig_opt = 1.0 / (1.0 + np.exp(-k_sigma * (T_opt - T_m)))
m_rel_opt = q_adsorbed * sig_opt
q_tot_opt = (m_mof * c_mof * (T_opt - 25.0)) + ((m_rel_opt / M_CO2) * delta_H)
int_opt = q_tot_opt / m_rel_opt

ax2.scatter([T_opt], [int_opt], color='#b91c1c', s=55, zorder=5)
ax2.annotate(
    f'Optimal Yield Point ($T = 110$ °C)\n$\sigma = 91.7\%$, CaCO$_3$ = 1.68 kg\nIntensity = {int_opt:.0f} kJ/kg CO$_2$',
    xy=(T_opt, int_opt),
    xytext=(T_opt - 22, int_opt + 1200),
    fontsize=10,
    fontweight='bold',
    color='#7f1d1d',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#fef2f2', edgecolor='#fca5a5', lw=1.2),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.15', color='#dc2626', lw=1.4),
    zorder=6
)

# Combined Legend
lines = [ax1.get_legend_handles_labels()[0][0], line1[0], line2[0]]
labels = [ax1.get_legend_handles_labels()[1][0], line1[0].get_label(), line2[0].get_label()]
ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2, fontsize=9.5, frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1')

plt.title('Figure 4: Thermal Desorption Sigmoid $\sigma(T)$ and Energy Intensity vs. Regeneration Temperature', fontsize=11.5, fontweight='bold', color='#0f172a', pad=28)

plt.tight_layout()
plt.savefig('Figure_4.3_thermal_desorption_energy.png', dpi=300)
plt.savefig('Figure_4.3_thermal_desorption_energy.svg')
plt.close()
print("Generated high-res Figure_4.3_thermal_desorption_energy.png (300 DPI) and SVG")
