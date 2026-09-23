# Simulation Documentation

**Companion document to the research paper "Onboard Capture and Mineralisation of Vehicle Exhaust CO₂".**
This document explains how the simulation works. It is a technical companion and is not part of the paper itself. The code is in `co2_capture_simulation.py`.

---

## 1. Purpose

The simulation estimates how the proposed capture system behaves over time. It is a model, not a physical experiment. It takes a set of parameters measured or reported in the literature, applies the chemistry and physics of each stage as equations, and steps through time to produce numbers for how much CO₂ is captured, how much energy regeneration needs, and how much calcium carbonate is formed.

## 2. Software and libraries

The simulation is written in Python 3. It uses only two standard libraries: `math` for the exponential and other functions, and `matplotlib` for drawing the multi-cycle charts. It reads no external data files and needs no internet connection. Anyone with Python installed can run it with `python co2_capture_simulation.py`.

## 3. What the simulation models

The model follows the three physical stages of the system in order.

1. **Adsorption:** CO₂ from the exhaust binds to the MOF bed. Modelled as first-order kinetic saturation toward an equilibrium loading.
2. **Regeneration:** the bed is heated, and a temperature-dependent fraction of the stored CO₂ is released. Modelled by the sigmoid release function.
3. **Mineralisation:** the released CO₂ reacts with limewater to form solid calcium carbonate. Modelled by 1 to 1 stoichiometry, with the calcium hydroxide inventory tracked as it is used up.

## 4. What the simulation estimates (outputs)

- Equilibrium loading and the loading reached at the end of a cycle (kg CO₂).
- Regeneration energy per cycle, split into sensible heat and desorption energy (kJ).
- The release fraction and the mass of CO₂ released per cycle (kg).
- The calcium carbonate produced and the calcium hydroxide consumed (g or kg).
- For the multi-cycle mode: cumulative capture, residual loading, cumulative CaCO₃, and limewater remaining, cycle by cycle.

## 5. Assumptions

The numbers are only as good as these assumptions. They are stated openly so a reader can judge them.

1. **First-order kinetics.** Adsorption is treated as first-order approach to equilibrium with a single rate constant k. Real kinetics under fast-changing engine flow may differ.
2. **One representative concentration.** The inlet CO₂ is fixed at 13.5%, a single value in the 5 to 15% exhaust range, rather than a varying signal.
3. **Sigmoid release.** The desorption fraction follows a logistic curve derived from a two-state desorption equilibrium. It is a smooth approximation, not fitted to thermogravimetric data for this exact material.
4. **Desorption energy from adsorbed mass.** The desorption energy each cycle is computed from the CO₂ adsorbed, not only the fraction released. This is deliberately conservative, since it charges the full amount even when only part is released.
5. **Ideal mineralisation.** The reaction CO₂ + Ca(OH)₂ → CaCO₃ + H₂O is treated as going fully to completion at 1 to 1 stoichiometry, limited only by the remaining calcium hydroxide.
6. **Waste heat is sufficient.** The regeneration heat is assumed to be available from the exhaust, which is supported by the exhaust thermal power (see the paper, Section 4.2).
7. **Well-mixed, uniform bed.** The bed is treated as a single lumped mass at one temperature, with no internal gradients, and no back-pressure penalty is modelled.

## 6. Equations and method

**Equilibrium loading:** q_eq = m_MOF × Q_max × (C_CO2 / C_ref).

**Loading with time:** q(t) = q_eq − (q_eq − q_start) × e^(−k·t). Starting from an empty bed (q_start = 0) this becomes the familiar q_eq × (1 − e^(−k·t)). The q_start term lets the multi-cycle mode carry residual loading forward.

**Release fraction:** σ(T) = 1 / (1 + e^(−k_σ (T − T_m))), with midpoint T_m = 90 °C and steepness k_σ = 0.08 °C⁻¹.

**Regeneration energy:** Q_total = Q_sensible + Q_desorb, where Q_sensible = m_MOF × c_MOF × (T − T_ambient) and Q_desorb = (mass adsorbed / M_CO2) × ΔH_des.

**Mineralisation:** moles released × M_CaCO3 gives the calcium carbonate mass; the same moles are subtracted from the calcium hydroxide inventory.

**Numerical method.** The loading equation is analytic, so each timestep is exact rather than approximated. The single-cycle run uses a 1-minute step across 77 minutes; the paper (Section 3.4.2) explains why 1 minute is the right step size.

## 7. How each single-cycle number is produced

With m_MOF = 5 kg, Q_max = 0.25, C_CO2 = 13.5%, C_ref = 20%:

- q_eq = 5 × 0.25 × (13.5 / 20) = 0.844 kg
- q(77) = 0.844 × (1 − e^(−0.04 × 77)) = 0.805 kg (95.4% of q_eq)
- Q_sensible = 5 × 0.8 × (85 − 25) = 240 kJ
- n adsorbed = 0.805 / 0.04401 = 18.3 mol, so Q_desorb = 18.3 × 45 = 823 kJ
- Q_total = 240 + 823 = 1063 kJ
- σ(85) = 1 / (1 + e^(−0.08 × (85 − 90))) = 0.401
- CO₂ released = 0.805 × 0.401 = 0.323 kg (7.34 mol)
- CaCO₃ = 7.34 × 100.09 = 735 g; Ca(OH)₂ consumed = 7.34 × 74.09 = 544 g
- energy per kg released = 1063 / 0.323 = 3291 kJ/kg

These match the values reported in the paper.

## 8. Multi-cycle logic and the trade-off it reveals

The multi-cycle mode runs successive adsorb-and-regenerate events on the same bed and a finite limewater tank. Each cycle starts from the residual loading left by the previous cycle, adsorbs back toward q_eq, releases σ(T) of the total, and subtracts the mineralised moles from the calcium hydroxide inventory. If the inventory runs out, no more CO₂ can be mineralised.

Running ten cycles at 85 °C and at 110 °C (30 litre tank, about 89 mol of Ca(OH)₂) shows a trade-off. At 85 °C the bed settles into a steady state (about 0.33 kg captured per cycle) and the limewater lasts the full run. At 110 °C each cycle captures about 0.67 kg, but the limewater is exhausted by the sixth cycle, after which the bed fills with residual CO₂ that cannot be stored. A higher regeneration temperature therefore captures more per cycle but shortens the service interval. This result is discussed in the paper, Section 4.5, and drawn in Figure 4.2.

## 9. How to run it

1. Install Python 3 and matplotlib (`pip install matplotlib`).
2. Run `python co2_capture_simulation.py`.
3. The script prints the single-cycle and multi-cycle results and saves the chart `multi_cycle_results.png`.

## 10. Limitations of the simulation

The simulation is a design-stage estimate. Its parameters come from steady-state laboratory measurements, not from the transient conditions of a running engine. It does not model back-pressure, internal temperature gradients, amine degradation over many cycles, or humidity effects on capacity. These are the questions that a physical prototype would need to answer, and they are listed as future work in the paper.
