"""
co2_capture_simulation.py
=========================
Time-stepped simulation of a conceptual vehicular CO2 capture system:
diamine-appended Mg-MOF-74 sorbent  ->  passive temperature-swing regeneration
->  limewater (Ca(OH)2) mineralisation to solid CaCO3.

This is the reference implementation for the research paper
"Onboard Capture and Mineralisation of Vehicle Exhaust CO2".
See Simulation_Documentation.md for the full explanation of the model,
its assumptions, and how each number is produced.

Run:  python co2_capture_simulation.py
Outputs: prints a results summary and (if matplotlib is available) saves
         multi_cycle_results.png in the same folder.

Authors: Advik Harihar and Panav K Bysani   Mentor: Yash Verma   10x International School, Mysore
"""

import math

# ----------------------------------------------------------------------
# 1. PARAMETERS  (values and sources are listed in Table 3.3 of the paper)
# ----------------------------------------------------------------------
M_MOF     = 5.0      # sorbent bed mass, kg
Q_MAX     = 0.25     # maximum loading ratio, kg CO2 per kg MOF
K_ADS     = 0.04     # first-order adsorption rate constant, per minute
C_CO2     = 13.5     # inlet CO2 concentration, % by volume
C_REF     = 20.0     # reference concentration for Q_max, %
DH_DES    = 45.0     # molar enthalpy of desorption, kJ/mol
C_P_MOF   = 0.8      # specific heat of the bed, kJ/(kg*K)
T_AMBIENT = 25.0     # adsorption (start) temperature, degC
T_REGEN   = 85.0     # default regeneration temperature, degC
T_MID     = 90.0     # sigmoid midpoint, degC
K_SIGMA   = 0.08     # sigmoid steepness, per degC

M_CO2     = 0.04401  # molar mass of CO2, kg/mol
M_CACO3   = 100.09   # molar mass of CaCO3, g/mol
M_CAOH2   = 74.09    # molar mass of Ca(OH)2, g/mol

# ----------------------------------------------------------------------
# 2. CORE MODEL EQUATIONS
# ----------------------------------------------------------------------
def q_equilibrium(m_mof=M_MOF, q_max=Q_MAX, c_co2=C_CO2, c_ref=C_REF):
    """Equilibrium (maximum) CO2 loading of the bed, kg. Eq. in Section 3.3.1."""
    return m_mof * q_max * (c_co2 / c_ref)

def loading(t, q_eq, q_start=0.0, k=K_ADS):
    """First-order kinetic loading after time t (min), starting from q_start (kg).
    q(t) = q_eq - (q_eq - q_start) * exp(-k t).  Reduces to q_eq(1-e^-kt) when q_start=0."""
    return q_eq - (q_eq - q_start) * math.exp(-k * t)

def sigma(T, t_mid=T_MID, k_sigma=K_SIGMA):
    """Sigmoid release fraction at regeneration temperature T (degC). Section 3.3.2."""
    return 1.0 / (1.0 + math.exp(-k_sigma * (T - t_mid)))

def regeneration_energy(mass_adsorbed_kg, T=T_REGEN):
    """Sensible + desorption energy for one regeneration, kJ.
    Desorption term uses the adsorbed mass (conservative), matching the paper."""
    q_sensible = M_MOF * C_P_MOF * (T - T_AMBIENT)
    n = mass_adsorbed_kg / M_CO2
    q_desorb = n * DH_DES
    return q_sensible, q_desorb, q_sensible + q_desorb

# ----------------------------------------------------------------------
# 3. SINGLE CYCLE  (reproduces the numbers reported in the paper)
# ----------------------------------------------------------------------
def single_cycle(t_ads=77, T=T_REGEN, verbose=True):
    q_eq = q_equilibrium()
    q77 = loading(t_ads, q_eq)
    q_sens, q_des, q_tot = regeneration_energy(q77, T)
    s = sigma(T)
    released = q77 * s
    n_rel = released / M_CO2
    caco3 = n_rel * M_CACO3          # g
    caoh2 = n_rel * M_CAOH2          # g
    if verbose:
        print("=== SINGLE CYCLE (paper reference, t_ads = %d min, T = %.0f C) ===" % (t_ads, T))
        print("  q_eq                 = %.3f kg" % q_eq)
        print("  q(%d)                = %.3f kg  (%.1f%% of q_eq)" % (t_ads, q77, 100*q77/q_eq))
        print("  Q_sensible           = %.0f kJ" % q_sens)
        print("  Q_desorb             = %.0f kJ" % q_des)
        print("  Q_total              = %.0f kJ" % q_tot)
        print("  sigma(%.0f C)         = %.3f" % (T, s))
        print("  CO2 released         = %.3f kg" % released)
        print("  CaCO3 produced       = %.0f g" % caco3)
        print("  Ca(OH)2 consumed     = %.0f g" % caoh2)
        print("  energy per kg released = %.0f kJ/kg" % (q_tot / released))
    return dict(q_eq=q_eq, q_final=q77, q_total=q_tot, released=released, caco3=caco3)

# ----------------------------------------------------------------------
# 4. MULTI-CYCLE  (successive adsorb / regenerate events on the same bed,
#    with residual loading carried forward and a finite limewater tank)
# ----------------------------------------------------------------------
def multi_cycle(T=T_REGEN, n_cycles=10, t_ads=77, tank_litres=30.0,
                slurry_density=1.1, slurry_massfrac=0.20):
    q_eq = q_equilibrium()
    # limewater inventory
    caoh2_per_L = (slurry_massfrac * slurry_density * 1000.0) / M_CAOH2   # mol per litre
    caoh2_total = caoh2_per_L * tank_litres                              # mol available
    q_current = 0.0
    caoh2_left = caoh2_total
    cyc, residual, adsorbed_c, released_c = [], [], [], []
    cum_captured, cum_caco3, caoh2_remaining, energy_c = [], [], [], []
    tot_cap = 0.0; tot_caco3 = 0.0
    for i in range(1, n_cycles + 1):
        q_start = q_current
        q_after = loading(t_ads, q_eq, q_start)
        adsorbed = q_after - q_start
        released = q_after * sigma(T)
        n_rel = released / M_CO2
        # cannot mineralise more CO2 than the remaining Ca(OH)2 allows
        if n_rel > caoh2_left:
            n_rel = max(caoh2_left, 0.0)
            released = n_rel * M_CO2
        caoh2_left -= n_rel
        q_current = q_after - released
        _, _, q_tot = regeneration_energy(adsorbed, T)
        tot_cap += released
        tot_caco3 += n_rel * M_CACO3 / 1000.0   # kg
        cyc.append(i); residual.append(q_start); adsorbed_c.append(adsorbed)
        released_c.append(released); cum_captured.append(tot_cap)
        cum_caco3.append(tot_caco3); caoh2_remaining.append(max(caoh2_left, 0.0))
        energy_c.append(q_tot)
    return dict(cyc=cyc, residual=residual, adsorbed=adsorbed_c, released=released_c,
                cum_captured=cum_captured, cum_caco3=cum_caco3,
                caoh2_remaining=caoh2_remaining, caoh2_total=caoh2_total, energy=energy_c)

# ----------------------------------------------------------------------
# 5. RUN + CHARTS
# ----------------------------------------------------------------------
def main():
    single_cycle()
    print()
    r85  = multi_cycle(T=85, n_cycles=10)
    r110 = multi_cycle(T=110, n_cycles=10)
    print("=== MULTI-CYCLE (10 cycles, 30 L of 20%% Ca(OH)2 slurry) ===")
    print("  Ca(OH)2 available: %.1f mol" % r85['caoh2_total'])
    print("  %-6s %-12s %-12s %-14s %-14s" % ("cycle", "released85", "released110", "cumCO2_85", "cumCO2_110"))
    for i in range(10):
        print("  %-6d %-12.3f %-12.3f %-14.3f %-14.3f" %
              (r85['cyc'][i], r85['released'][i], r110['released'][i],
               r85['cum_captured'][i], r110['cum_captured'][i]))
    print("  Residual loading after 10 cycles: 85C = %.3f kg, 110C = %.3f kg"
          % (r85['residual'][-1], r110['residual'][-1]))

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, 2, figsize=(11, 8))
        c85, c110 = "#2563eb", "#ea580c"
        # (a) cumulative CO2 captured
        ax[0,0].plot(r85['cyc'], r85['cum_captured'], 'o-', color=c85, label="85 C")
        ax[0,0].plot(r110['cyc'], r110['cum_captured'], 's-', color=c110, label="110 C")
        ax[0,0].set_title("Cumulative CO2 captured"); ax[0,0].set_xlabel("cycle"); ax[0,0].set_ylabel("kg"); ax[0,0].legend()
        # (b) residual loading at start of each cycle
        ax[0,1].plot(r85['cyc'], r85['residual'], 'o-', color=c85, label="85 C")
        ax[0,1].plot(r110['cyc'], r110['residual'], 's-', color=c110, label="110 C")
        ax[0,1].set_title("Residual loading carried into each cycle"); ax[0,1].set_xlabel("cycle"); ax[0,1].set_ylabel("kg CO2 on bed"); ax[0,1].legend()
        # (c) cumulative CaCO3
        ax[1,0].plot(r85['cyc'], r85['cum_caco3'], 'o-', color=c85, label="85 C")
        ax[1,0].plot(r110['cyc'], r110['cum_caco3'], 's-', color=c110, label="110 C")
        ax[1,0].set_title("Cumulative CaCO3 produced"); ax[1,0].set_xlabel("cycle"); ax[1,0].set_ylabel("kg"); ax[1,0].legend()
        # (d) limewater remaining
        ax[1,1].plot(r85['cyc'], r85['caoh2_remaining'], 'o-', color=c85, label="85 C")
        ax[1,1].plot(r110['cyc'], r110['caoh2_remaining'], 's-', color=c110, label="110 C")
        ax[1,1].set_title("Ca(OH)2 remaining (limewater depletion)"); ax[1,1].set_xlabel("cycle"); ax[1,1].set_ylabel("mol"); ax[1,1].legend()
        for a in ax.flat:
            a.grid(True, alpha=0.3)
        fig.suptitle("Multi-cycle simulation: regeneration at 85 C vs 110 C", fontsize=13, fontweight="bold")
        fig.tight_layout(rect=[0,0,1,0.97])
        fig.savefig("multi_cycle_results.png", dpi=150)
        print("\nSaved chart: multi_cycle_results.png")
    except Exception as e:
        print("\n(matplotlib not available, skipped charts: %s)" % e)

if __name__ == "__main__":
    main()
