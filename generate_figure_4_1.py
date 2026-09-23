import numpy as np
import matplotlib.pyplot as plt

# Set publication style
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.2

# -------------------------------------------------------------
# Figure 4.1: Adsorption Breakthrough Curve (300 DPI High-Res)
# -------------------------------------------------------------
t = np.linspace(0, 90, 300)
q_eq = 0.844  # kg CO2
k = 0.04       # min^-1
q_t = q_eq * (1 - np.exp(-k * t))

fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=300)

# Grid
ax.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1', zorder=1)

# Equilibrium line
ax.axhline(q_eq, color='#d97706', linestyle='--', linewidth=1.8, label=f'Equilibrium Capacity $q_{{eq}} = {q_eq:.3f}$ kg', zorder=2)

# Adsorption curve
ax.plot(t, q_t, color='#2563eb', linewidth=2.8, label='Dynamic Bed Loading $q(t)$', zorder=3)
ax.fill_between(t, q_t, color='#2563eb', alpha=0.08, zorder=2)

# 77 min annotation
t_77 = 77.0
q_77 = q_eq * (1 - np.exp(-k * t_77))
ax.scatter([t_77], [q_77], color='#1d4ed8', s=60, zorder=5)
ax.vlines(t_77, 0, q_77, color='#1d4ed8', linestyle=':', linewidth=1.5, zorder=4)

ax.annotate(
    f'Cycle Cut-off ($t = 77$ min)\n$q(77) = {q_77:.3f}$ kg CO$_2$\n(95.4% of equilibrium)',
    xy=(t_77, q_77),
    xytext=(t_77 - 28, q_77 - 0.22),
    fontsize=10.5,
    fontweight='bold',
    color='#1e3a8a',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#eff6ff', edgecolor='#93c5fd', lw=1.2),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.15', color='#1d4ed8', lw=1.5),
    zorder=6
)

# Axis labels & formatting
ax.set_xlabel('Driving Time (min)', fontsize=12, fontweight='bold', color='#0f172a', labelpad=8)
ax.set_ylabel('Mass of CO$_2$ Adsorbed on Bed (kg)', fontsize=12, fontweight='bold', color='#0f172a', labelpad=8)
ax.set_xlim(0, 90)
ax.set_ylim(0, 0.95)
ax.tick_params(colors='#334155', labelsize=10.5)

ax.legend(loc='lower right', fontsize=10.5, frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1')
plt.title('Figure 3: Simulated CO$_2$ Adsorption Breakthrough Curve ($m_{\\mathrm{MOF}} = 5$ kg, $C_{\\mathrm{CO}_2} = 13.5$%)', fontsize=12, fontweight='bold', color='#0f172a', pad=12)

plt.tight_layout()
plt.savefig('Figure_4.1_adsorption_curve.png', dpi=300)
plt.close()
print("Generated clear high-res Figure_4.1_adsorption_curve.png (300 DPI)")
