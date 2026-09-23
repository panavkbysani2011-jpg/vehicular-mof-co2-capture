# 4. Results and Discussion

This section reports the output of the Python simulation described in Section 3.4.2 and interprets what it means for the feasibility of the proposed system. All values are computed from the model and parameters in Table 3.3 over one representative 77 minute drive cycle, with regeneration at the default temperature of 85 °C unless stated otherwise.

## 4.1 CO₂ Adsorption Over the Drive Cycle

The simulated loading of the MOF bed follows the first-order saturation curve q(t) = q_eq · (1 − e^(−k·t)). With the baseline parameters the equilibrium loading is q_eq = 0.844 kg of CO₂. The loading rises quickly in the first half of the cycle and then flattens as the bed approaches this ceiling.

At t = 77 minutes the bed holds q(77) = 0.805 kg of CO₂, which is 95.4% of the equilibrium value. This confirms the choice of cycle length: by 77 minutes the bed is effectively full, and the remaining 4.6% of capacity would take far longer to fill because the curve has flattened. A representative adsorption curve is shown in Figure 4.1.

> **[FIGURE 4.1 HERE: Adsorption curve q(t) over the 77 minute cycle.]** A rebuilt figure is provided in the Figures section.

## 4.2 Regeneration Energy

The energy needed to regenerate the bed once is the sum of two parts. The sensible heat to warm 5 kg of MOF from 25 °C to 85 °C is Q_sensible = 240 kJ. The desorption energy to release the bound CO₂, written Q_desorb, is the heat needed to break the chemical bonds holding the CO₂. It is 823 kJ, computed from the 18.3 moles of CO₂ on the bed and the 45 kJ/mol desorption enthalpy. The total is Q_total ≈ 1060 kJ per regeneration.

The desorption term is the larger of the two, at about 77% of the total. This is expected, because breaking the chemical bonds that hold CO₂ takes more energy than simply warming the solid. Dividing the total by the mass of CO₂ released gives an energy intensity of about 3300 kJ per kg of CO₂ released at 85 °C.

None of this energy is drawn from the engine or the battery. It is supplied entirely by waste heat in the exhaust. A typical car exhaust carries roughly 10 to 40 kW of thermal power, so the 1060 kJ needed for one regeneration corresponds to only about 30 to 100 seconds of exhaust heat. The thermal budget for passive regeneration is therefore met with a wide margin.

## 4.3 CO₂ Release and Mineralisation

At the default regeneration temperature of 85 °C, the sigmoid release function gives σ(85) = 0.40. Of the 0.805 kg held on the bed, 0.323 kg is released as a concentrated stream and the rest stays on the sorbent as residual loading.

The released CO₂ is bubbled into the limewater and mineralised. By the stoichiometry of CO₂ + Ca(OH)₂ → CaCO₃ + H₂O, the 0.323 kg of released CO₂ (7.34 mol) forms 0.735 kg of solid calcium carbonate and consumes 0.544 kg of calcium hydroxide. This solid is the permanent, weighable product of the cycle.

## 4.4 Effect of Regeneration Temperature

The 40% release at 85 °C is a direct result of the sigmoid being centred at 90 °C. Because the exhaust runs at 300 to 600 °C, the heat exchanger can drive the bed well above 85 °C, and doing so raises the release fraction sharply. Table 4.1 shows the effect.

**Table 4.1. Release fraction and products versus regeneration temperature (sigmoid midpoint 90 °C).**

| Regeneration T (°C) | Release fraction σ(T) | CO₂ released (kg) | CaCO₃ formed (g) |
|---|---|---|---|
| 70 | 0.17 | 0.135 | 308 |
| 80 | 0.31 | 0.250 | 568 |
| 85 (default) | 0.40 | 0.323 | 735 |
| 90 | 0.50 | 0.402 | 915 |
| 100 | 0.69 | 0.555 | 1263 |
| 110 | 0.83 | 0.670 | 1523 |
| 120 | 0.92 | 0.738 | 1678 |

At 110 to 120 °C the system releases 83 to 92% of the stored CO₂ in a single regeneration, producing about 1.5 to 1.7 kg of calcium carbonate per cycle. The default of 85 °C is therefore a conservative operating point, not a ceiling.

This is consistent with the open question flagged in Section 3.3.2 rather than a full resolution of it. The model is internally self-consistent, but reaching substantial release means driving the bed above the 60 to 80 °C window that Table 3.1 lists as the sorbent advantage. The exhaust supplies this higher temperature easily, so the low-temperature figure is best read as a minimum onset rather than the actual operating point. Whether the grafted amines stay stable under repeated heating to 110 to 120 °C is a separate question that physical testing would need to settle.

The trade-off is small. Heating the bed to 120 °C instead of 85 °C raises the sensible heat from 240 kJ to 380 kJ, but because far more CO₂ is released, the energy intensity falls from about 3300 kJ/kg to roughly 1600 kJ/kg of CO₂ released. Higher regeneration temperatures are thus both more complete and more efficient per unit of CO₂ captured, as long as they stay below the level that would damage the grafted amines.

## 4.5 Behaviour Over Repeated Cycles

The single-cycle results above assume the bed starts empty. In continuous use the bed is only partly regenerated, so residual CO₂ carries into the next cycle. To test this, the simulation was extended to ten successive cycles at two regeneration temperatures, 85 °C and 110 °C, using a 30 litre tank of 20% limewater (about 89 mol of Ca(OH)₂). The results are shown in Figure 4.2.

At 85 °C the bed reaches a steady state. The residual loading settles near 0.5 kg after the second cycle, and each cycle then captures a steady 0.33 kg. The limewater lasts the full ten cycles and still holds about 14 mol at the end.

At 110 °C each cycle releases about 0.67 kg, so cumulative capture rises about twice as fast. The limewater, however, is exhausted by the sixth cycle. After that no more CO₂ can be mineralised, the released CO₂ has nowhere to go, and the residual loading on the bed climbs sharply, as seen in the second panel of Figure 4.2.

This reveals a design trade-off that the single-cycle view hides. A higher regeneration temperature captures more CO₂ per cycle but uses up the limewater faster, which shortens the service interval. A lower temperature captures less per cycle but runs longer between refills. The best operating point depends on how the two limits, the sorbent capacity and the limewater supply, are balanced for a given tank size and drive pattern. The run also shows that the system stays coherent under repeated cycling, which was the first of the three research gaps.

> **[FIGURE 4.2 HERE: Multi-cycle simulation, 85 °C versus 110 °C over ten cycles.]** File: Figure_4.2_multicycle_results.png

## 4.6 Limewater Consumption and Tank Sizing

The limewater is the only consumable in the system, so its size sets the service interval. One litre of 20% calcium hydroxide slurry holds about 2.97 mol of Ca(OH)₂ and can fix about 131 g of CO₂.

At the default 85 °C, one regeneration releases 0.323 kg of CO₂, which needs about 2.5 litres of slurry to absorb fully. The calcium hydroxide falls monotonically across the run, as tracked by the depletion equation in Section 3.2, until the tank must be refilled. A practical tank can therefore be sized for a target number of cycles between refills, and the growing layer of solid calcium carbonate gives a simple, weighable record of how much CO₂ has been captured.

## 4.7 Comparison with Conventional Capture

The results support the choice of a diamine-appended MOF over conventional methods. The energy intensity of about 3300 kJ/kg at 85 °C, falling toward 1600 kJ/kg at higher regeneration temperatures, is comparable to or below the roughly 3500 to 4000 kJ/kg reported for liquid monoethanolamine regeneration [1,2]. The main difference is that this energy is supplied free from waste heat rather than from a fuel-fired reboiler, and the regeneration temperature is far lower than the 120 to 150 °C that MEA requires.

The system also avoids the two parts of conventional capture that do not fit a vehicle. There is no compression stage and no pressurised storage, because the CO₂ is fixed as a solid the moment it is released. This is the main practical advantage of the limewater terminal stage.

## 4.8 Practical Considerations

Several practical factors decide whether the system is realistic on a real vehicle, and they are estimated here at a conceptual level.

The unit adds mass to the vehicle. The sorbent is 5 kg, a 30 litre tank of 20% limewater weighs roughly 33 kg, and the housing and heat exchanger add more, for a total on the order of 40 to 50 kg. As a rough rule, every extra 45 kg raises fuel use by about 1 to 2%, so the fuel penalty here is small.

Cost is dominated by the sorbent. Limewater is cheap, at a few units of currency per kilogram, while research-grade diamine-appended MOFs are expensive. Scalable solid-state synthesis routes are expected to lower this cost [13]. Because the sorbent is regenerated and reused, its cost is spread across the whole service life, and only the limewater is consumed and refilled.

A packed bed in the exhaust line adds flow resistance, which raises back-pressure and can slightly reduce engine efficiency. A practical design would use a low-resistance form such as pellets or an open-channel monolith. Measuring this back-pressure is one of the integration questions raised in the literature review and is left for physical testing.

The calcium carbonate produced is a stable, non-toxic solid used widely in construction, paper, and as a filler. It is therefore a usable product rather than a waste, which gives the system a small circular-economy benefit and a simple disposal route.

Finally, the limewater is water-based, so in freezing climates the tank would need protection from freezing, and water lost to evaporation would need occasional topping up. These are ordinary engineering issues, but they should be planned for.

## 4.9 How the Results Address the Three Research Gaps

The simulation gives a quantitative answer to each of the three gaps from the literature review. For the gap on cyclic performance, the model produces per-cycle capture (0.805 kg), release (0.323 kg at 85 °C), and energy (1060 kJ), which can now be studied as a function of cycle frequency and temperature. For the gap on physical integration, the 5 kg bed and a limewater tank of a few litres are shown to fit the chassis envelope, and the layout is set out in the CAD model of Section 3.4.1. For the gap on system-level energy accounting, the full balance includes the cost of onboard disposal, with calcium hydroxide use and calcium carbonate output tracked alongside regeneration energy.

## 4.10 Limitations

This study is conceptual and literature-based, so its results should be read as a feasibility estimate rather than a measured performance. The kinetic constant and capacity are taken from published data measured under steady conditions, not under the rapid, transient flow of a running engine, which is itself one of the gaps the project identifies. The sigmoid release function is a phenomenological model that reproduces the sharp, cooperative shape of desorption but is not fitted to thermogravimetric data for this exact material.

Two model simplifications should also be noted. The desorption energy is computed from the full adsorbed mass rather than only the released fraction, which makes the energy estimate conservative. And at the default 85 °C, the 60% of CO₂ that is not released would build up as residual loading over repeated cycles, which would lower the per-cycle capture unless the regeneration temperature is raised, as discussed in Section 4.4.

The desorption enthalpy of 45 kJ/mol used in the energy balance is also at the low end of the values reported for short-diamine frameworks, which span roughly 50 to 73 kJ/mol. The per-cycle regeneration energy may therefore be a slight underestimate.

## 4.11 Future Work

The clear next step is a physical prototype that can be weighed. Because each cycle produces a fixed, visible mass of calcium carbonate, a bench test could validate the model directly by comparing the measured solid mass against the predicted 0.7 to 1.7 kg per cycle. Further work should measure the adsorption rate and capacity under transient exhaust-like conditions, test the cycling stability of the grafted amines over many heating and cooling cycles, and fit the release function to thermogravimetric measurements so the midpoint and steepness are set by data rather than chosen.
