# 3. Methodology

This study proposes and evaluates a conceptual vehicular CO₂ capture system that intercepts exhaust gas at the point of production. The unit is designed to fit inside the existing exhaust pathway of a standard internal combustion engine vehicle. It draws no power from the vehicle and has no moving parts. Its only energy input is the heat already carried by the exhaust stream, which would otherwise be lost to the air as waste heat.

**The system idea.** Exhaust gas first passes through a packed bed of a solid sorbent that binds CO₂. When the bed nears saturation, waste heat from the exhaust warms it and releases the stored CO₂ as a concentrated stream. That stream is then bubbled into an onboard limewater tank, where it reacts to form solid calcium carbonate and is stored as a stable mineral. The carbon therefore passes from the sorbent, is released by heat, and is finally fixed as a solid.

**The components.** The methodology is built around three parts, developed in sequence and summarised in Figure 3.1: a sorbent matched to the CO₂ concentration, temperature, and variable flow of vehicle exhaust; a terminal storage medium that fixes the released CO₂ onboard without compressed gas tanks; and a set of equations for the chemistry of each stage, run as a time stepped Python simulation.

> **[FIGURE 3.1 HERE: Methodology flowchart.]** Place your existing Canva methodology flowchart in this paragraph. A rebuilt, cleaner version is also provided (see Figures section).

**The simulation.** The Python model computes how the whole system performs over a 77 minute window. It reports three outputs: the cumulative CO₂ captured, the regeneration energy per cycle, and the rate at which the limewater is used up.

The 77 minute length is not a fixed standard drive cycle. It is the time the bed needs to reach about 95% of its maximum loading at the model's default settings of 5 kg of sorbent and a representative inlet CO₂ level. Beyond this point the bed can take up almost no more CO₂, so a longer run would add no new information about per cycle performance. For context, standard urban test cycles are shorter than this saturation time: the WLTP cycle runs about 30 minutes and the FTP-75 cycle about 31 minutes [11], so a typical commute would contain several full capture and release cycles.

This methodology responds directly to three gaps identified in the literature review. One gap is the lack of performance data for diamine-appended MOFs under the rapid, repeated heating and cooling produced by a running engine. The simulation closes this gap by modelling adsorption and regeneration as a repeating cycle. The amount of CO₂ released at each cycle is set by a *thermally activated sigmoid release function*. This is an S-shaped curve that gives the fraction of stored CO₂ released as a function of temperature: the fraction stays near zero at low temperature, rises sharply around a midpoint temperature, and approaches one at high temperature. The function is defined and derived in Section 3.3.2.

A second gap is the absence of a physical integration design for a compact, exhaust-mounted capture unit. Section 3.4 addresses this by specifying the geometry and connections of all three subsystems within the space limits of a vehicle. A third, system-level gap is the lack of energy accounting that includes the cost of disposing of CO₂ onboard. The limewater stage addresses this, with calcium hydroxide use and calcium carbonate buildup tracked alongside sorbent loading and regeneration energy across the full run.

---

## 3.1 Sorbent Selection and MOF Architecture

A metal-organic framework (MOF) is a crystalline, highly porous solid built from metal ions joined by organic linker molecules into a repeating three dimensional network. The key feature of MOFs is **tunability**: because the metal node and the organic linker can each be chosen and chemically modified, the pore size and internal surface chemistry can be designed at the molecular level. MOFs also offer very **high surface area**, often above 1000 m²/g, which packs a large number of CO₂ binding sites into a small mass of material. This matters in a vehicle, where every kilogram of sorbent adds to the load the engine must carry.

For CO₂ capture the deciding property is not surface area alone but how well a sorbent binds CO₂ at the concentration present in the gas. Vehicle exhaust holds CO₂ at 5 to 15% by volume. This sits between the high-concentration flue gas that industrial scrubbers are built for and the very dilute air (about 420 ppm) targeted by direct air capture. Most conventional sorbents work poorly across this middle range, for the reasons compared in Table 3.1.

**Table 3.1. Comparison of CO₂ sorbents across the exhaust-relevant range.**

| Sorbent type | Binding mechanism | Works best at | Regeneration temperature | Suitable for a vehicle? |
|---|---|---|---|---|
| Zeolites / activated carbon (physisorbents) | Weak van der Waals attraction | High CO₂ concentration | Low, but loading is poor at exhaust levels | No: too little CO₂ captured at 5 to 15% |
| Liquid monoethanolamine (MEA) | Strong chemical (carbamate) bond | Low to moderate concentration | High, 120 to 150 °C [2] | No: needs columns, pumps, and heat exchangers |
| Diamine-appended Mg-MOF-74 | Cooperative chemisorption (carbamate) | 5 to 15%, the exhaust range | Low, 60 to 80 °C [4,7] | Yes: compact and solid, with low regeneration heat |

Table 3.1 shows why this study selects **diamine-appended Mg-MOF-74**. Physisorbents need high partial pressures to hold useful amounts of CO₂, so their loading at exhaust levels is too low to justify the energy of regenerating them. Liquid amine systems bind CO₂ well at lower concentrations but need high regeneration temperatures and large fixed equipment that cannot travel on a vehicle. The diamine-appended MOF is the only option in the table that combines a strong, selective bond in the 5 to 15% range with a low regeneration temperature and a compact solid form.

The diamine grafted onto the framework in this study is **ethylenediamine (en)**, a short molecule carrying two amine groups (–NH₂) on a two carbon backbone. One amine bonds to an open magnesium site on the pore wall, anchoring the molecule, while the second amine points into the pore. This paired arrangement is what makes the cooperative capture mechanism possible. A second candidate, N,N′-dimethylethylenediamine (mmen), was considered for comparison, but ethylenediamine was adopted as the baseline because its reported capacity and kinetics are well documented at exhaust-relevant conditions.

The capture mechanism is **cooperative chemisorption**, a step-change process in which CO₂ reacts with pairs of neighbouring amine groups and the reaction then propagates along the pore channel. Its practical consequence for sorbent selection is that loading stays low until a threshold partial pressure is reached, then rises steeply to near-maximum within a narrow concentration window. This jump occurs right inside the 5 to 15% range of vehicle exhaust, so the material captures CO₂ where a vehicle actually produces it. The full molecular mechanism and net reaction are given in Section 3.3.1.

Mahajan et al. (2024) provide the quantitative anchor for the simulation [4]. They measured a working capacity of about 4 to 5 mmol of CO₂ per gram of ethylenediamine-functionalised Mg-MOF-74. This study uses that figure to set the model's maximum loading ratio, Q_max = 0.25 kg CO₂ per kg MOF (Section 3.3.1).

Two points about that measurement matter for the model. First, Mahajan et al. tested the material under direct air capture conditions (about 420 ppm), not exhaust concentrations, so their capacity is a baseline rather than an exhaust-specific value. Second, they identified the two barriers this project is built to examine: slow adsorption kinetics relative to fast-changing engine flow, and capacity loss under repeated thermal cycling. The time stepped simulation targets exactly these barriers, because it represents adsorption and regeneration as a repeating cycle rather than a single steady measurement.

---

## 3.2 Limewater as the Terminal Storage Medium

A central unsolved problem for any mobile capture system is what to do with the CO₂ once the sorbent releases it. Stationary plants compress the released CO₂ and either store it in pressurised vessels or pipe it underground. Neither option fits a vehicle: compressed gas storage adds large weight and volume, and onboard pipelines do not exist. This study solves the problem by reacting the released CO₂ with **limewater** (an aqueous calcium hydroxide, Ca(OH)₂, system), which converts it immediately into solid calcium carbonate (CaCO₃). The reaction happens on its own at ordinary pressure and needs no added energy or special equipment.

Several alkaline media can absorb CO₂. The three realistic candidates for an onboard tank are sodium hydroxide (NaOH), calcium oxide (CaO), and calcium hydroxide / limewater (Ca(OH)₂). Table 3.2 compares them.

**Table 3.2. Comparison of candidate CO₂ absorbers for onboard storage.**

| Property | NaOH (sodium hydroxide) | CaO (calcium oxide) | Ca(OH)₂ / limewater (chosen) |
|---|---|---|---|
| Reaction with CO₂ | 2 NaOH + CO₂ → Na₂CO₃ + H₂O | CaO + CO₂ → CaCO₃ (slow as a dry solid) | CO₂ + Ca(OH)₂ → CaCO₃ + H₂O |
| Product | Sodium carbonate (soluble) | Calcium carbonate (solid) | Calcium carbonate (solid, insoluble) |
| Permanence onboard | Product stays dissolved; can re-release | Permanent, but gas to solid contact is poor | Permanent solid precipitate |
| Safety | Strongly caustic and corrosive | Caustic; releases heat on contact with water | Mild base, low hazard, handled safely |
| Suitability for bubbling gas | Liquid, but corrosive to the tank | Dry solid, hard to bubble gas through | Liquid or slurry, ideal for a bubble diffuser |
| Cost | Moderate | Low | Low |

Limewater wins on three counts drawn from Table 3.2. Its product, calcium carbonate, is insoluble and cannot return to the gas phase, so storage is permanent. As a mild base it is far safer to carry in a passenger vehicle than caustic NaOH. Being a liquid, it lets the gas bubble through, which dry CaO cannot. NaOH instead stores its product as soluble sodium carbonate, which can re-release CO₂ and is corrosive to the tank.

The property that makes limewater a true storage medium, rather than a reversible absorber, is the **irreversibility** of the calcium carbonate step under onboard conditions. Amine sorbents form reversible carbamate bonds and give CO₂ back when heated, but calcium carbonate does not. Calcium carbonate is extremely insoluble, with a solubility product (calcite) of about 3.3 × 10⁻⁹ at 25 °C, so once it precipitates it stays solid [8].

Reversing the reaction would require thermal decomposition of calcium carbonate (CaCO₃ → CaO + CO₂), which only begins near 825 °C [8]. No part of the storage tank reaches anything close to that temperature, so the stored carbon is fixed. This gives the captured CO₂ a stable endpoint that needs no cooling, no pressure tank, and no ongoing handling. That stable endpoint is why limewater works as the final storage stage of a mobile capture cycle.

The limewater reservoir is modelled as a sealed cylindrical tank, placed downstream of the MOF bed and joined to it by a thermally insulated transfer line. A fine-bubble diffuser sits at the base of the tank. The concentrated CO₂ released during regeneration enters through this diffuser as small bubbles. Fine bubbles are used because the absorption rate depends on the gas to liquid surface area, and the total surface area increases as bubble diameter falls. Smaller bubbles therefore raise the absorption rate and let the system mineralise each batch of released CO₂ within the available time.

The baseline calcium hydroxide loading is **20% by mass**, and this value follows from a capacity calculation rather than from solubility. True limewater (a saturated solution) holds only about 1.5 g of Ca(OH)₂ per litre, roughly 0.15% by mass, which is far too little to store useful amounts of CO₂. To carry enough calcium, the tank instead holds a 20% by mass aqueous suspension of Ca(OH)₂, a lime slurry, where solid particles stay dispersed in water and dissolve as the reaction consumes them. The 20% figure balances storage capacity against the need to keep the slurry thin enough to mix and bubble through. The onboard medium is referred to throughout as limewater (a 20% Ca(OH)₂ slurry).

The storage capacity of this slurry can be written as a mass balance. For a tank holding a volume V of 20% slurry at density ρ, the initial amount of calcium hydroxide is:

    n(Ca(OH)₂) = (w · ρ · V) / M(Ca(OH)₂)

where w = 0.20 is the mass fraction and M(Ca(OH)₂) = 74.09 g/mol.
*(LaTeX: n_{Ca(OH)_2} = \dfrac{w\,\rho\,V}{M_{Ca(OH)_2}})*

Because one mole of Ca(OH)₂ captures one mole of CO₂, this also sets the maximum CO₂ the tank can hold. Taking a slurry density of about 1.1 kg/L, one litre carries roughly 220 g of Ca(OH)₂, which is about 2.97 mol, and can therefore fix about 2.97 mol (around 131 g) of CO₂ per litre. As the run proceeds, the remaining calcium hydroxide falls with every cycle:

    n(Ca(OH)₂)_remaining(t) = n(Ca(OH)₂)_initial − n(CO₂ mineralised up to time t)

*(LaTeX: n_{remaining}(t) = n_{initial} - n_{CO_2}(t))*

This declining inventory is tracked as a primary output of the simulation. It sets a hard upper bound on how much CO₂ the system can store per tank of limewater and gives the tank-sizing and service-interval relationship needed for a practical design.

---

## 3.3 Reaction Mechanisms

### 3.3.1 CO₂ Adsorption on the MOF Surface

As exhaust enters the packed MOF bed it carries CO₂ at 5 to 15% by volume, which at atmospheric pressure is a partial pressure of about 5 to 15 kPa. As set out in Table 3.1, this range sits between the flue gas handled by liquid amine scrubbers and the dilute air targeted by direct air capture, and diamine-appended Mg-MOF-74 is matched to it through cooperative chemisorption.

Mg-MOF-74 contains one dimensional hexagonal pore channels whose walls carry a high density of open magnesium sites. During post-synthetic modification, an ethylenediamine molecule is grafted at each site: its first amine bonds to the magnesium, anchoring it, and its second amine is left free inside the pore. Measured surface areas above 1000 m²/g (the BET surface area, a standard measure of the internal surface of a porous solid) give a very high number of these reactive sites per gram [4,5].

Chemisorption means CO₂ is held by an actual chemical bond, not weak surface attraction. The mechanism is *cooperative* because once CO₂ reacts at one site, the neighbouring site reacts more easily, and the reaction runs along the channel like a chain. In each step, a CO₂ molecule inserts between two adjacent amine groups: a nitrogen atom forms a covalent bond to the CO₂ carbon, a hydrogen shifts to the neighbouring amine, and the result is an ammonium carbamate ion pair, with one positive (–NH₃⁺) and one negative (–NHCOO⁻) group held together by electrostatic attraction [3,4].

Because each ion pair makes the next form more readily, loading stays near zero until a threshold partial pressure is reached, then rises steeply to near-maximum. Under the humid conditions of real exhaust, a second pathway lets one CO₂ react with a single amine, which can raise capacity further [10].

The net adsorption reaction, consuming one CO₂ per amine pair, is:

    2 (–NH₂) + CO₂ → (–NH₃⁺)(–NHCOO⁻)

**Quantitative model and parameters.** The time-dependent loading of the bed is modelled as first-order kinetic saturation:

    q(t) = q_eq · (1 − e^(−k·t))

*(LaTeX: q(t) = q_{eq}\,(1 - e^{-k t}))*

Here q(t) is the mass of CO₂ adsorbed per unit mass of MOF at time t, and the equilibrium loading q_eq is scaled to the actual inlet concentration:

    q_eq = m_MOF · Q_max · (C_CO₂ / C_ref)

*(LaTeX: q_{eq} = m_{MOF}\,Q_{max}\,\dfrac{C_{CO_2}}{C_{ref}})*

The parameter values and their sources are: the maximum loading ratio Q_max = 0.25 kg CO₂ / kg MOF, set from the working capacity of ethylenediamine-functionalised Mg-MOF-74 reported by Mahajan et al. [4] and consistent with the diamine-appended MOF isotherm modelling of Hughes et al. [7]; the rate constant k = 0.04 min⁻¹, taken from reported uptake kinetics for this material class [4,7]; and the molar enthalpy of adsorption ΔH_ads = −45 kJ/mol, consistent with published values for this framework [4,9]. (The desorption enthalpy used later is the same magnitude with opposite sign, ΔH_des = +45 kJ/mol.)

> **Flag for the team (capacity value).** Q_max = 0.25 kg/kg corresponds to about 5.7 mmol/g, slightly above the 4 to 5 mmol/g (about 0.18 to 0.22 kg/kg) that Mahajan et al. measured under direct air capture. This is defensible because exhaust (5 to 15% CO₂) is far richer than air (about 420 ppm), so equilibrium loading should be higher. We kept 0.25 to match your Python simulation. If you prefer a conservative number tied directly to the citation, use Q_max = 0.20 kg/kg and re-run; we can update every downstream value automatically.

With m_MOF = 5 kg, C_CO₂ = 13.5%, and C_ref = 20%, the equilibrium loading is q_eq = 5 × 0.25 × (13.5 / 20) ≈ 0.844 kg CO₂. The 13.5% inlet value represents a warm, loaded engine in the upper part of the 5 to 15% range. At t = 77 min, q(77) = 0.844 × (1 − e^(−0.04 × 77)) ≈ 0.805 kg CO₂, which is about 95.4% of equilibrium. For comparison, the 45 kJ/mol adsorption enthalpy is well below the 80 to 90 kJ/mol of aqueous MEA, so less energy must be re-supplied at regeneration [1,2].

### 3.3.2 CO₂ Release and MOF Regeneration

Regeneration uses temperature-swing adsorption (TSA), meaning the bed is repeatedly heated to release CO₂ and then cooled to capture again. The heat is supplied passively by the exhaust, which leaves the engine at 300 to 600 °C, far above the temperatures needed to reverse the chemisorption bond. A coaxial heat exchanger (Section 3.4.1) carries this waste heat to the bed, so no electrical input is required.

On heating, the ammonium carbamate ion pairs decompose: the electrostatic attraction is disrupted first, then the covalent N–C bond breaks, regenerating the free amine and releasing CO₂. The net regeneration reaction is the reverse of adsorption:

    (–NH₃⁺)(–NHCOO⁻) → 2 (–NH₂) + CO₂

The bond in the framework is weaker than a carbamate in free solution, because the pore geometry and the cooperative charge environment lower the effective binding enthalpy. This is why regeneration needs a smaller temperature swing than the 120 to 150 °C of liquid MEA, and the saving grows with the number of cycles [2,4,6].

**Sigmoid release function and its derivation.** Rather than assuming complete release, the simulation uses a temperature-dependent release fraction σ(T), the fraction of stored CO₂ given up at temperature T:

    σ(T) = 1 / (1 + e^(−k_σ·(T − T_m)))

*(LaTeX: \sigma(T) = \dfrac{1}{1 + e^{-k_\sigma (T - T_m)}})*

with steepness k_σ = 0.08 °C⁻¹ and midpoint T_m = 90 °C. This S-shape (sigmoid) is not arbitrary. It follows from a simple idea: at any temperature the stored CO₂ is split between a bound form, still held on the sorbent, and a free form, released as gas, and heating shifts the balance toward the free form. Treating this as a two-state balance, with σ the released fraction and (1 − σ) the bound fraction, gives at equilibrium:

    σ / (1 − σ) = e^(−ΔG/RT),   with ΔG = ΔH − T·ΔS

Solving for σ gives the logistic form:

    σ(T) = 1 / (1 + e^((ΔH − T·ΔS)/RT))

*(LaTeX: \sigma(T) = \dfrac{1}{1 + e^{(\Delta H - T\Delta S)/RT}})*

**Why the midpoint is 90 °C.** The midpoint is where σ = 0.5, which requires the exponent to be zero, that is ΔH − T_m·ΔS = 0. Therefore:

    T_m = ΔH / ΔS

*(LaTeX: T_m = \dfrac{\Delta H}{\Delta S})*

The midpoint is the temperature at which the desorption free energy is zero, the point where release becomes thermodynamically favourable. Setting T_m = 90 °C (363 K) fixes the ratio ΔH/ΔS = 363 K for the cooperative desorption step.

**Why the steepness is 0.08.** Near the midpoint, a standard mathematical approximation (a first-order expansion of the exponent around T_m) turns the expression into the simple logistic form used in the model. The steepness then works out to:

    k_σ = ΔH / (R · T_m²)

*(LaTeX: k_\sigma = \dfrac{\Delta H}{R\,T_m^{2}})*

With k_σ = 0.08 °C⁻¹ and T_m = 363 K, this corresponds to an effective transition enthalpy of about 0.08 × 8.314 × 363² ≈ 88 kJ/mol. This effective value sets the sharpness of the step and is larger than the single-bond 45 kJ/mol because cooperative desorption breaks bonds collectively rather than one at a time. The two numbers describe different things: 45 kJ/mol is the per-mole energy used in the heat balance below, while 88 kJ/mol only controls how steep the release curve is.

> **Flag for the team (regeneration window and midpoint).** A midpoint of 90 °C places *half* of the release at 90 °C. At the 60 to 80 °C window in Table 3.1, σ is only about 0.08 to 0.31, and at the default T = 85 °C, σ ≈ 0.40. So the model currently releases less than half the stored CO₂ per cycle in that window, and the literature for these diamine frameworks supports substantial release closer to 85 to 110 °C. Two clean fixes: (a) re-centre T_m to about 75 °C so half-release matches the 60 to 80 °C claim, or (b) describe the regeneration window as about 85 to 110 °C throughout. Reported cooperative differential enthalpies (about 50 to 73 kJ/mol for short diamines) are also higher than 45 kJ/mol, so you may revisit that value too. We kept all values as-is, as you requested.

The mass of CO₂ released per cycle is:

    m_CO₂,released = m_CO₂,adsorbed · σ(T)

At the default T = 85 °C: σ(85) = 1 / (1 + e^(−0.08 × (85 − 90))) = 1 / (1 + e^(0.40)) ≈ 0.40. Any CO₂ not released stays on the sorbent as residual loading and is tracked across the run.

**Regeneration energy per cycle.** The energy per cycle is the sum of the heat needed to warm the bed (sensible heat) and the heat needed to break the CO₂ bonds so the gas is released (the desorption energy):

    Q_total = Q_sensible + Q_desorb = (m_MOF · c_MOF · ΔT) + (n_CO₂ · ΔH_des)

*(LaTeX: Q_{total} = m_{MOF}\,c_{MOF}\,\Delta T + n_{CO_2}\,\Delta H_{des})*

with c_MOF = 0.8 kJ kg⁻¹ K⁻¹ and ΔH_des = 45 kJ/mol. At m_MOF = 5 kg, ΔT = 60 K (25 to 85 °C), and 0.805 kg CO₂ adsorbed: Q_sensible = 240 kJ, n_CO₂ = 0.805 / 0.044 ≈ 18.3 mol, Q_desorb = 18.3 × 45 ≈ 823 kJ, so Q_total ≈ 1063 kJ per cycle (about 1060 kJ). Dividing by the released mass at 85 °C (about 0.323 kg) gives an energy intensity of roughly 3300 kJ per kg of CO₂ released. This energy is supplied entirely by the passive exhaust heat exchanger.

### 3.3.3 CO₂ Mineralisation in Limewater

The concentrated CO₂ from regeneration is bubbled into the limewater reservoir, where it reacts irreversibly with calcium hydroxide at ambient pressure:

    CO₂(g) + Ca(OH)₂(aq) → CaCO₃(s) + H₂O(l)

The reaction is thermodynamically spontaneous under all conditions in this system, for the low-solubility reasons given in Section 3.2 [8]. The precipitation rate is modelled as r = k_m · a · [CO₂], where a is the gas to liquid interfacial area set by the diffuser. The cumulative calcium carbonate mass follows by stoichiometric conversion from the moles of CO₂ released:

    m_CaCO₃ = n_CO₂,released · M_CaCO₃

*(LaTeX: m_{CaCO_3} = n_{CO_2,released}\,M_{CaCO_3})*

with M_CaCO₃ = 100.09 g/mol. This closes the system mass balance against the calcium hydroxide inventory of Section 3.2. Because the calcium carbonate builds up as a visible solid, future experiments could simply weigh it to check how much CO₂ was actually captured.

---

## 3.4 Proposed System Configuration and Simulation Framework

### 3.4.1 Three-Dimensional CAD Model

A CAD model of the integrated capture unit is developed to check that all three subsystems fit within the chassis space of a standard passenger vehicle. The model is built in Rhino, which gives precise control over the curved surfaces of the exhaust-line components.

The model places three subsystems in series: a cylindrical packed MOF bed mounted in-line with the exhaust pathway, a coaxial heat exchanger that passively harvests exhaust heat to drive regeneration, and a sealed limewater reservoir fitted with a fine-bubble diffuser. The housing is compact and vibration resistant, and the limewater tank is thermally insulated so it is not heated during regeneration.

> **[FIGURE 3.4.1 HERE: Rhino CAD model / system schematic.]** The new model must match the current design. The earlier Tinkercad render still showed a compressor, a CO₂ storage tank, and a transfer to an external facility, which this design no longer uses. The correct flow is: exhaust inlet, then MOF bed with heat exchanger, then insulated limewater chamber with diffuser, then calcium carbonate collection at the tank base. A clean labelled schematic is provided in the Figures section as a build reference for the Rhino model.

### 3.4.2 Python Simulation and Operational Algorithm

The Python simulation models system performance across the 77 minute window as a sequential algorithm that mirrors the physical pipeline. The logic is summarised in the algorithm flowchart (Figure 3.4.2), and the input and output values are listed in Table 3.3 so the flowchart can stay focused on the steps rather than the numbers. The simulation is written in Python and provided as a separate, runnable file (`co2_capture_simulation.py`). Its full implementation, assumptions, and the derivation of each reported number are set out in a separate technical document (the Simulation Documentation) rather than repeated here.

> **[FIGURE 3.4.2 HERE: Algorithm flowchart, logic only.]** The rebuilt flowchart shows the calculation steps and equations without embedding the parameter values, which are in Table 3.3.

**Table 3.3. Simulation parameters and outputs.**

| Symbol | Meaning | Value / unit | Source |
|---|---|---|---|
| m_MOF | Sorbent bed mass | 5 kg | Chassis space limit [3] |
| Q_max | Maximum loading ratio | 0.25 kg CO₂ / kg MOF | From [4], cf. [7] |
| k | Adsorption rate constant | 0.04 min⁻¹ | [4,7] |
| C_CO₂ | Inlet CO₂ concentration | 13.5% | Warm, loaded engine (upper 5 to 15%) |
| C_ref | Reference concentration | 20% | Normalisation for Q_max [4] |
| ΔH_des | Molar enthalpy of desorption | 45 kJ/mol (= −ΔH_ads) | [4,9] |
| c_MOF | Specific heat of bed | 0.8 kJ kg⁻¹ K⁻¹ | Material estimate |
| T_m, k_σ | Sigmoid midpoint, steepness | 90 °C, 0.08 °C⁻¹ | Section 3.3.2 |
| Δt | Simulation timestep | 1 min | See justification below |
| **Output** | | | |
| q_eq | Equilibrium loading | ≈ 0.844 kg CO₂ | Computed |
| q(77) | Loading at 77 min | ≈ 0.805 kg CO₂ (95.4%) | Computed |
| Q_total | Regeneration energy per cycle | ≈ 1060 kJ | Computed |
| m_CaCO₃ | Calcium carbonate per cycle | by stoichiometry | Computed |

**Algorithm steps.** The simulation reads the inputs in Table 3.3, computes q_eq, then iterates from t = 0 to 77 min in 1-minute steps, computing q(t) at each step. It then computes the regeneration energy (Q_sensible, Q_desorb, Q_total), the released fraction σ(T) and the released mass, and finally converts the released CO₂ to calcium carbonate and updates the limewater inventory.

**Why a 1-minute timestep.** The adsorption process has a characteristic time of 1/k = 25 minutes, so the loading curve changes slowly compared with one minute. A 1-minute step gives 25 points across one characteristic time, which resolves both the steep early rise and the later flattening smoothly, while keeping the run to a simple 77 steps. A 30-second step would double the computation for no visible change in the curve, because k·Δt is already very small at one minute. A 2-minute step would begin to under-sample the steep early rise and the per-cycle regeneration bookkeeping. One minute is therefore the smallest step that adds no accuracy beyond it and the largest that still resolves the dynamics.

---

## Open items to confirm before submission

1. **Algorithm section number.** Your "Inputs" page says the Python algorithm "should go to section 3.2," but the "IRIS Edits" page puts the CAD model in 3.4.1, which implies the algorithm belongs in 3.4.2. We placed it in 3.4.2. Please confirm which numbering Mr. Verma wants.
2. **Sigmoid midpoint / regeneration window** (flag in Section 3.3.2) and **capacity value Q_max** (flag in Section 3.3.1) are science decisions kept as-is for you to resolve.
3. **Figures to insert:** Figure 3.1 (methodology flowchart), Figure 3.4.1 (Rhino CAD/schematic), Figure 3.4.2 (algorithm flowchart). Rebuilt versions of 3.4.1 and 3.4.2 are provided.
4. **Reference [8]** is filled with the CRC Handbook below; confirm your preferred citation style.

---

## References

[1] Yu, C.H., Huang, C.H. and Tan, C.S. (2012). A review of CO₂ capture by absorption and adsorption. *Aerosol and Air Quality Research*, 12, pp. 745–769.
[2] Zhang, Z., Borhani, T.N. and Olabi, A.G. (2020). Status and perspective of CO₂ absorption process. *Energy*. doi:10.1016/j.energy.2020.118057.
[3] Project Synopsis (2024). Applications for Vehicle Exhaust; Conclusions and Research Gaps.
[4] Mahajan, S., Elfving, J. and Lahtinen, M. (2024). Evaluating the viability of ethylenediamine-functionalized Mg-MOF-74 in direct air capture: the challenges of stability and slow adsorption rate. *Journal of Environmental Chemical Engineering*, 12(2), 112193.
[5] Peh, S.B. and Zhao, D. (2020). Tying amines down for stable CO₂ capture. *Science*, 369(6502), pp. 374–375.
[6] Xie, F. et al. (2025). Advances in amine-functionalized metal-organic frameworks for carbon capture. *Journal of Materials Chemistry A*, 13(2), pp. 522–544.
[7] Hughes, R. et al. (2021). Isotherm, kinetic, process modeling, and techno-economic analysis of a diamine-appended metal-organic framework for CO₂ capture using fixed bed contactors. *Energy & Fuels*, 35(6), pp. 5122–5136.
[8] Haynes, W.M. (ed.) (2016). *CRC Handbook of Chemistry and Physics*, 97th edn. Boca Raton: CRC Press. (Solubility product of calcite, about 3.3 × 10⁻⁹; thermal decomposition of calcium carbonate near 825 °C.)
[9] Zhu, Z. et al. (2024). High-capacity, cooperative CO₂ capture in a diamine-appended metal-organic framework through a combined chemisorptive and physisorptive mechanism. *Journal of the American Chemical Society*, 146(8), pp. 5369–5381.
[10] Holmes, H.E. et al. (2023). Optimum relative humidity enhances CO₂ uptake in diamine-appended M₂(dobpdc). *Chemical Engineering Journal*, 477, 147116.
[11] Standard drive-cycle durations: WLTP (Worldwide Harmonised Light Vehicle Test Procedure, UN GTR No. 15), about 30 minutes; FTP-75 (US EPA Federal Test Procedure), about 31 minutes.
