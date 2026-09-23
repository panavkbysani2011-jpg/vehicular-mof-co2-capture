import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Setup Environment
output_dir = "figures"
os.makedirs(output_dir, exist_ok=True)

# Formatting for publication-quality scientific figures
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'legend.fontsize': 12,
    'lines.linewidth': 2,
    'figure.dpi': 300,
    'savefig.dpi': 300
})

# 2. Physical & Chemical Constants
k_ad = 0.04  # min^-1
Q_max_baseline = 0.25  # kg CO2 / kg MOF
C_ref = 20.0  # %
C_CO2_default = 13.5  # %
m_MOF = 5.0  # kg
Delta_H_des = 45.0  # kJ/mol
c_MOF = 0.8  # kJ/(kg*K)
T_ambient = 25.0  # C
T_mid = 90.0  # C
k_sigma = 0.08  # C^-1
M_CO2 = 44.01 / 1000.0  # kg/mol
M_CaCO3 = 100.09 / 1000.0  # kg/mol
M_CaOH2 = 74.09 / 1000.0  # kg/mol
V_slurry = 10.0  # L
rho_slurry = 1.10  # kg/L
w_slurry = 0.20  # 20 wt%
rho_bulk = 0.77  # kg/L
D_cm = 16.0  # cm
T_regen_default = 85.0 # C

# Helper Functions
def calc_q_eq(m_mof, q_max_base, deg_pct, c_co2):
    q_max_eff = q_max_base * (1.0 - deg_pct / 100.0)
    return m_mof * q_max_eff * (c_co2 / C_ref)

def calc_q_t(q_eq, t):
    return q_eq * (1.0 - np.exp(-k_ad * t))

def calc_sigma(T):
    return 1.0 / (1.0 + np.exp(-k_sigma * (T - T_mid)))

# ---------------------------------------------------------
# Figure 1: Adsorption Kinetics
# ---------------------------------------------------------
t = np.linspace(0, 77, 100)
q_eq_default = calc_q_eq(m_MOF, Q_max_baseline, 0, C_CO2_default)
q_t = calc_q_t(q_eq_default, t)

sigma_85 = calc_sigma(T_regen_default)
m_co2_rel_t = q_t * sigma_85
n_co2_rel_t = m_co2_rel_t / M_CO2
caco3_t = n_co2_rel_t * M_CaCO3

fig, ax1 = plt.subplots(figsize=(8, 6))
ax1.plot(t, q_t, color='#0366d6', label='CO2 Adsorbed q(t)')
ax1.fill_between(t, q_t * 0.9, q_t * 1.1, color='#0366d6', alpha=0.15, label='± 10% Kinetic Uncertainty')
ax1.set_xlabel('Time (min)')
ax1.set_ylabel('CO2 Adsorbed (kg)', color='#0366d6')
ax1.tick_params(axis='y', labelcolor='#0366d6')
ax1.set_xlim(0, 77)
ax1.set_ylim(0, max(q_t)*1.2)
ax1.grid(True, linestyle='--', alpha=0.6)

ax2 = ax1.twinx()
ax2.plot(t, caco3_t, color='#28a745', linestyle='--', label='Cumulative CaCO3 Mineralized')
ax2.set_ylabel('CaCO3 Mass (kg)', color='#28a745')
ax2.tick_params(axis='y', labelcolor='#28a745')
ax2.set_ylim(0, max(caco3_t)*1.2)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='lower right')
plt.title('Adsorption Kinetics and Mineralization Potential')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure1_adsorption_kinetics.png'))
plt.savefig(os.path.join(output_dir, 'figure1_adsorption_kinetics.pdf'))
plt.close()

# ---------------------------------------------------------
# Figure 2: Thermodynamic Sigmoid & Energy Intensity
# ---------------------------------------------------------
T = np.linspace(60, 130, 200)
sigma_T = calc_sigma(T)

q_t_end = calc_q_t(q_eq_default, 77)
m_co2_rel_T = q_t_end * sigma_T
Q_sensible_T = m_MOF * c_MOF * (T - T_ambient)
n_co2_ads = q_t_end / M_CO2
Q_desorb = n_co2_ads * Delta_H_des
Q_total_T = Q_sensible_T + Q_desorb

with np.errstate(divide='ignore', invalid='ignore'):
    eta_T = np.where(m_co2_rel_T > 0, Q_total_T / m_co2_rel_T, np.nan)

fig, ax1 = plt.subplots(figsize=(8, 6))
ax1.plot(T, sigma_T, color='#0366d6', label='Desorption Fraction σ(T)')
ax1.set_xlabel('Regeneration Temperature (°C)')
ax1.set_ylabel('Desorption Fraction', color='#0366d6')
ax1.tick_params(axis='y', labelcolor='#0366d6')
ax1.set_xlim(60, 130)
ax1.set_ylim(0, 1.05)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.axvline(x=85, color='#6c757d', linestyle=':', label='85 °C Reference')

ax2 = ax1.twinx()
ax2.plot(T, eta_T, color='#d73a49', linestyle='--', label='Energy Intensity (kJ/kg)')
ax2.set_ylabel('Energy Intensity (kJ / kg CO2)', color='#d73a49')
ax2.tick_params(axis='y', labelcolor='#d73a49')
valid_eta = eta_T[T >= 70]
ax2.set_ylim(0, np.nanmax(valid_eta) * 1.1 if len(valid_eta) > 0 else 10000)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='center right')
plt.title('Thermodynamic Release and Energy Intensity')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure2_thermodynamic_sigmoid.png'))
plt.savefig(os.path.join(output_dir, 'figure2_thermodynamic_sigmoid.pdf'))
plt.close()

# ---------------------------------------------------------
# Figure 3: Sensitivity Matrix
# ---------------------------------------------------------
degs = np.array([0, 10, 20, 30])
c_co2s = np.array([5.0, 10.0, 13.5, 15.0])
results_mat = np.zeros((len(degs), len(c_co2s)))

for i, d in enumerate(degs):
    for j, c in enumerate(c_co2s):
        q_eq_iter = calc_q_eq(m_MOF, Q_max_baseline, d, c)
        results_mat[i, j] = calc_q_t(q_eq_iter, 77)

fig, ax = plt.subplots(figsize=(8, 6))
markers = ['o', 's', '^', 'D']
for i, d in enumerate(degs):
    ax.plot(c_co2s, results_mat[i, :], marker=markers[i], label=f'Degradation: {d}%', markersize=8)

ax.set_xlabel('Exhaust CO2 Concentration (%)')
ax.set_ylabel('Captured CO2 at 77 min (kg)')
ax.set_title('Sorbent Degradation vs. Exhaust Concentration')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_xticks(c_co2s)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure3_sensitivity_matrix.png'))
plt.savefig(os.path.join(output_dir, 'figure3_sensitivity_matrix.pdf'))
plt.close()

# ---------------------------------------------------------
# Figure 4: Slurry Endurance (10 cycles)
# ---------------------------------------------------------
total_caoh2_initial = V_slurry * rho_slurry * w_slurry
cycles = np.arange(1, 11)

caoh2_remaining = np.zeros(len(cycles) + 1)
caco3_accum = np.zeros(len(cycles) + 1)
caoh2_remaining[0] = total_caoh2_initial

m_co2_rel_per_cycle = q_t_end * calc_sigma(85.0)
n_co2_min_per_cycle = m_co2_rel_per_cycle / M_CO2
m_caoh2_used_per_cycle = n_co2_min_per_cycle * M_CaOH2
m_caco3_prod_per_cycle = n_co2_min_per_cycle * M_CaCO3

for i in range(1, 11):
    caoh2_remaining[i] = caoh2_remaining[i-1] - m_caoh2_used_per_cycle
    caco3_accum[i] = caco3_accum[i-1] + m_caco3_prod_per_cycle
    if caoh2_remaining[i] < 0:
        caoh2_remaining[i] = 0
        caco3_accum[i] = caco3_accum[i-1] + (caoh2_remaining[i-1] / M_CaOH2) * M_CaCO3

cycle_arr = np.arange(0, 11)
fig, ax1 = plt.subplots(figsize=(8, 6))

ax1.step(cycle_arr, caoh2_remaining, where='post', color='#d73a49', label='Ca(OH)2 Remaining', linewidth=2)
ax1.set_xlabel('Drive Cycle (77 min each)')
ax1.set_ylabel('Ca(OH)2 Mass (kg)', color='#d73a49')
ax1.tick_params(axis='y', labelcolor='#d73a49')
ax1.set_ylim(0, total_caoh2_initial * 1.1)
ax1.set_xlim(0, 10)
ax1.set_xticks(np.arange(0, 11))
ax1.grid(True, linestyle='--', alpha=0.6)

ax2 = ax1.twinx()
ax2.step(cycle_arr, caco3_accum, where='post', color='#28a745', label='CaCO3 Accumulated', linewidth=2)
ax2.set_ylabel('CaCO3 Mass (kg)', color='#28a745')
ax2.tick_params(axis='y', labelcolor='#28a745')
ax2.set_ylim(0, max(caco3_accum)*1.2)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='center right')
plt.title('Slurry Endurance and Mineral Accumulation (10 Cycles)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure4_slurry_endurance.png'))
plt.savefig(os.path.join(output_dir, 'figure4_slurry_endurance.pdf'))
plt.close()

# ---------------------------------------------------------
# Export CSV Data
# ---------------------------------------------------------
Q_sensible_const = m_MOF * c_MOF * (T_regen_default - T_ambient)
Q_desorb_t = (q_t / M_CO2) * Delta_H_des
Q_total_t = Q_sensible_const + Q_desorb_t

df_csv = pd.DataFrame({
    'Time_min': t,
    'CO2_Adsorbed_kg': q_t,
    'CO2_Adsorbed_Upper_10pct_kg': q_t * 1.10,
    'CO2_Adsorbed_Lower_10pct_kg': q_t * 0.90,
    'CO2_Released_at_85C_kg': m_co2_rel_t,
    'CaCO3_Produced_kg': caco3_t,
    'Total_Thermal_Energy_kJ': Q_total_t
})
df_csv.to_csv('simulation_results.csv', index=False)

df_sens = pd.DataFrame(results_mat, 
                       index=[f'Degradation_{d}%' for d in degs], 
                       columns=[f'CO2_{c}%' for c in c_co2s])
df_sens.to_csv('sensitivity_matrix.csv')

# ---------------------------------------------------------
# Print Console Summary
# ---------------------------------------------------------
V_bed = m_MOF / rho_bulk
L_cm = (V_bed * 1000) / (np.pi * (D_cm / 2)**2)
delta_P = 0.76 * (L_cm / 35.0)

print("="*65)
print(" VEHICULAR EXHAUST CO2 CAPTURE SIMULATION SUMMARY")
print("="*65)
print(f"Sorbent Bed Mass:        {m_MOF:.2f} kg")
print(f"Exhaust CO2 Fraction:    {C_CO2_default:.1f} %")
print(f"Regeneration Temp:       {T_regen_default:.1f} °C")
print(f"Drive Cycle Duration:    77 min")
print("-" * 65)
print(f"Equilibrium Capacity:    {q_eq_default:.3f} kg CO2")
print(f"Captured CO2 (77 min):   {q_t_end:.3f} kg CO2 ({q_t_end/q_eq_default*100:.1f}%)")
print(f"Desorbed CO2 (85 °C):    {m_co2_rel_per_cycle:.3f} kg CO2")
print(f"Solid CaCO3 Yield:       {m_caco3_prod_per_cycle:.3f} kg")
print("-" * 65)
Q_total_85 = (m_MOF * c_MOF * (T_regen_default - T_ambient)) + ((q_t_end / M_CO2) * Delta_H_des)
eta_85 = Q_total_85 / m_co2_rel_per_cycle if m_co2_rel_per_cycle > 0 else 0
print(f"Thermal Energy Total:    {Q_total_85:.0f} kJ")
print(f"Energy Intensity:        {eta_85:.0f} kJ/kg CO2")
print("-" * 65)
print(f"Bed Volume:              {V_bed:.2f} L")
print(f"Canister Dimensions:     {D_cm:.1f} cm (D) x {L_cm:.1f} cm (L)")
print(f"Back-Pressure (Ergun):   {delta_P:.2f} kPa")
print("="*65)
print("Files Generated successfully:")
print(" - /figures/figure1_adsorption_kinetics.[png|pdf]")
print(" - /figures/figure2_thermodynamic_sigmoid.[png|pdf]")
print(" - /figures/figure3_sensitivity_matrix.[png|pdf]")
print(" - /figures/figure4_slurry_endurance.[png|pdf]")
print(" - simulation_results.csv")
print(" - sensitivity_matrix.csv")
print("="*65)
