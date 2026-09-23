# Onboard Capture and Mineralisation of Vehicle Exhaust CO2 Using Diamine-Appended Mg-MOF-74 and Limewater

### A Conceptual and Simulation Study

**Authors:** Advik Harihar and Panav K Bysani
**Mentor:** Yash Verma (Chemistry)
**Institution:** 10x International School, Mysore
**Presented at:** IRIS National Fair

*(Working title and author details, please confirm or edit.)*

---


# Abstract

Rising carbon dioxide from vehicles is a major contributor to climate change and to declining air quality. This study proposes and evaluates, through simulation, a conceptual onboard system that captures CO₂ directly from vehicle exhaust and stores it as a stable solid. Exhaust gas passes through a packed bed of diamine-appended Mg-MOF-74, a metal-organic framework that binds CO₂ by cooperative chemisorption, a bonding process that switches on sharply within the 5 to 15% concentration range typical of exhaust. Waste heat already present in the exhaust regenerates the sorbent, so the unit needs no electrical input and no moving parts. The released CO₂ is then bubbled into an onboard limewater (calcium hydroxide) tank, where it is fixed permanently as solid calcium carbonate. This avoids the compressed gas storage that has kept conventional capture from being practical on a vehicle.

A time-stepped Python model of the chemistry was used to estimate performance over a representative 77 minute cycle. A 5 kg bed captures about 0.8 kg of CO₂ per cycle, and the regeneration energy of about 1060 kJ is supplied entirely by waste heat. At the default regeneration temperature, about 0.3 kg of this CO₂ is released per cycle and fixed as a weighable mass of calcium carbonate.

The work is conceptual and literature-based, with all parameters drawn from published measurements. It shows that existing diamine-appended MOFs, combined with limewater mineralisation, form a thermodynamically coherent and physically integrable basis for mobile carbon capture, and it identifies the cycling, integration, and energy-accounting questions that physical testing should address next.

**Keywords:** carbon capture, metal-organic framework, Mg-MOF-74, vehicle exhaust, limewater, calcium carbonate, temperature-swing adsorption.

## Nomenclature

**Latin symbols**

| Symbol | Meaning | Unit |
|---|---|---|
| a | Gas to liquid interfacial area (mineralisation rate model) | m² m⁻³ |
| C_CO₂ | Inlet CO₂ concentration | % by volume |
| C_ref | Reference CO₂ concentration for Q_max | % by volume |
| c_MOF | Specific heat capacity of the MOF bed | kJ kg⁻¹ K⁻¹ |
| k | First-order adsorption rate constant | min⁻¹ |
| k_m | Mineralisation (precipitation) rate constant | model units |
| k_σ | Sigmoid steepness | °C⁻¹ |
| M_CaCO₃ | Molar mass of calcium carbonate | 100.09 g mol⁻¹ |
| M_Ca(OH)₂ | Molar mass of calcium hydroxide | 74.09 g mol⁻¹ |
| M_CO₂ | Molar mass of carbon dioxide | 44.01 g mol⁻¹ |
| m_MOF | Sorbent bed mass | kg |
| m_adsorbed | Mass of CO₂ adsorbed per cycle | kg |
| m_released | Mass of CO₂ released per cycle | kg |
| n_CO₂ | Moles of CO₂ | mol |
| Q_max | Maximum loading ratio of the sorbent | kg CO₂ per kg MOF |
| Q_sensible | Sensible heat to warm the bed per cycle | kJ |
| Q_desorb | Desorption energy per cycle | kJ |
| Q_total | Total regeneration energy per cycle | kJ |
| q(t) | Mass of CO₂ on the bed at time t | kg |
| q_eq | Equilibrium (maximum) CO₂ loading of the bed | kg |
| R | Universal gas constant | 8.314 J mol⁻¹ K⁻¹ |
| r | Precipitation rate (mineralisation) | model units |
| T | Regeneration temperature | °C |
| T_m | Sigmoid midpoint temperature | °C |
| T₀ | Adsorption (ambient) temperature | °C |
| t | Time | min |
| V | Volume of limewater slurry | L |
| w | Mass fraction of Ca(OH)₂ in the slurry | dimensionless |

**Greek symbols**

| Symbol | Meaning | Unit |
|---|---|---|
| ΔG | Gibbs free energy change of desorption | kJ mol⁻¹ |
| ΔH | Enthalpy change (general, in the derivation) | kJ mol⁻¹ |
| ΔH_ads | Molar enthalpy of adsorption | kJ mol⁻¹ |
| ΔH_des | Molar enthalpy of desorption (= −ΔH_ads) | kJ mol⁻¹ |
| ΔS | Entropy change of desorption | kJ mol⁻¹ K⁻¹ |
| ΔT | Temperature rise, T − T₀ | K |
| ρ | Density of the limewater slurry | kg L⁻¹ |
| σ(T) | Sigmoid release fraction at temperature T | dimensionless |

**Abbreviations**

| Abbreviation | Meaning |
|---|---|
| BET | Brunauer-Emmett-Teller (surface area method) |
| DAC | Direct air capture |
| en | Ethylenediamine |
| FTP-75 | Federal Test Procedure (US drive cycle) |
| MEA | Monoethanolamine |
| mmen | N,N′-dimethylethylenediamine |
| MOF | Metal-organic framework |
| TSA | Temperature-swing adsorption |
| WLTP | Worldwide Harmonised Light Vehicle Test Procedure |

# 1. Introduction

Carbon dioxide is the main greenhouse gas driving climate change, and its concentration in the atmosphere continues to rise. Road transport is one of the largest single sources of these emissions, because every internal combustion engine releases CO₂ directly into the air through its exhaust. Reducing emissions from vehicles is therefore an important part of meeting global climate goals, and it motivates the search for materials and methods that can capture CO₂ at the point where it is produced.

Most established capture technology is built for one of two extremes. Industrial amine scrubbers are designed for the high CO₂ concentrations of power-station flue gas, while direct air capture systems are designed for the very dilute CO₂ in open air, at about 420 ppm. Vehicle exhaust falls between these two, at 5 to 15% CO₂ by volume. Conventional sorbents work poorly across this middle range, which leaves vehicle exhaust under-served by current methods.

Metal-organic frameworks (MOFs) offer a way to bridge this gap. A MOF is a crystalline, highly porous solid whose internal surface chemistry can be tuned at the molecular level, and whose surface area is large enough to pack many binding sites into a small mass. When the framework is functionalised with diamine groups, it captures CO₂ by cooperative chemisorption, a step-change process that switches on within the 5 to 15% range of exhaust and regenerates at a comparatively low temperature. These properties make diamine-appended MOFs a strong candidate for a compact, vehicle-mounted capture unit.

A second problem stands in the way of any mobile system: what to do with the CO₂ once it is released from the sorbent. Stationary plants compress the gas and store or pipe it away, but compression and pressurised storage add too much weight and volume for a vehicle. This study addresses that problem by reacting the released CO₂ with onboard limewater, which converts it immediately into solid calcium carbonate and stores it permanently without any pressurisation.

The objective of this study is to evaluate, as a conceptual and simulation-based design, whether existing diamine-appended MOFs can form the basis of a practical vehicular capture system. It asks how much CO₂ such a system can capture, release, and store across a realistic drive cycle, whether the unit can be built into a vehicle within its space and energy limits, and whether the full energy and material balance, including the cost of disposing of the CO₂ onboard, is favourable.

This work is conceptual and literature-based rather than an experimental demonstration, and all model parameters are taken from published measurements. The remainder of the paper reviews the relevant literature (Section 2), sets out the methodology and simulation (Section 3), presents and discusses the results (Section 4), and states the conclusions and next steps (Section 5).

# 2. Literature Review

## 2.1 CO₂ Capture for Vehicle Exhaust

Vehicle exhaust holds CO₂ at 5 to 15% by volume, between the high concentrations that industrial amine scrubbers are built for and the near-atmospheric levels targeted by direct air capture. Conventional sorbents struggle across this middle range. Physisorbents need high partial pressures to hold useful amounts of CO₂, and liquid amine systems consume large amounts of energy to regenerate at the lower concentrations [1,2].

Diamine-appended MOFs handle this range more effectively through cooperative chemisorption. In this mechanism, CO₂ binds to pairs of amine sites in a step-change fashion once a threshold partial pressure is crossed, so the material reaches near-maximum capacity within a narrow window rather than adsorbing gradually. This window aligns with the concentrations found in exhaust gas. Because the material reaches high working capacity at a low regeneration temperature, the ratio of capture to regeneration energy is favourable, which is a critical advantage where space and power are limited [4,9].

Mahajan et al. (2024) evaluated ethylenediamine-functionalised Mg-MOF-74 and confirmed a working capacity of about 4 to 5 mmol of CO₂ per gram. They also identified the two practical barriers that any deployment must overcome: slow adsorption kinetics relative to fast-changing flow, and capacity loss under repeated thermal cycling [4]. Their measurements were made under direct air capture conditions, so they serve as a baseline for the richer exhaust stream rather than an exhaust-specific result. Together these findings show that the material chemistry is well developed, but that engineering a system around the variable conditions of a running engine remains an open problem.

## 2.2 Recent Developments

Recent work has shifted from showing that MOFs can capture CO₂ to asking whether they can do so reliably and at scale. Xie et al. (2025) reviewed amine-functionalised MOFs broadly and documented improvements in thermal stability, adsorption capacity, and regeneration efficiency, attributing much of the progress to better control over the density and placement of amine sites within the framework [6].

Other studies have widened the question beyond capture alone. Kadota et al. (2021) showed that CO₂ can act as a direct carbon source for MOF synthesis at room temperature, raising the possibility that captured CO₂ could be turned into useful material rather than only stored [12]. On the manufacturing side, Mao et al. (2022) developed solid-state synthesis routes that produce nanoporous frameworks with consistent atomic-level structure at larger volumes, addressing a long-standing concern about whether laboratory results can be reproduced at production scale [13].

The method used to attach the amine groups also matters for durability. Peh and Zhao (2020) showed that covalently bonded amines retain capacity across repeated adsorption and regeneration cycles, while physisorbed amines degrade significantly through volatilisation and displacement [5]. This result supports the choice of covalently grafted diamine configurations for any application, such as a vehicle, where the sorbent is cycled continuously.

## 2.3 Conclusions and Research Gaps

Taken together, the literature shows that diamine-appended MOFs achieve high CO₂ capacity at regeneration temperatures well below those of conventional liquid amine (monoethanolamine) systems [4,6,9], and that humidity can further enhance uptake [10]. The field has moved past proof of concept and is now confronting the harder questions of stability, scalability, and practical use.

However, the conditions under which these results were obtained are largely controlled and steady-state, and three gaps are directly relevant to this project.

First, no reviewed study has tested diamine-appended MOFs under the rapid, repeated thermal cycling of a running engine, where temperature and flow change on the scale of seconds. It is not yet established whether the cooperative mechanism stays intact under these conditions.

Second, the physical integration of a MOF-based capture unit within an exhaust system has not been investigated, including back-pressure effects and the demands of a compact, vibration-resistant housing.

Third, system-level energy accounting for mobile capture, which must include the cost of disposing of the captured CO₂ onboard, has not been performed in the reviewed literature.

This project is motivated by these three absences. It aims to evaluate whether existing diamine-appended MOFs, in particular Mg-MOF-74 and its variants, can form the basis of a conceptual vehicular capture system that is energetically consistent and physically buildable.

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

# 5. Conclusion

This study set out to evaluate whether existing diamine-appended MOFs can form the basis of a practical vehicular CO₂ capture system. Working as a conceptual, simulation-based design, it brought together three parts: a sorbent matched to vehicle exhaust, a terminal storage medium that fixes the captured CO₂ onboard, and a time-stepped model of the chemistry at each stage. The simulation shows that the design is internally consistent: the energy it needs is available, and the mass balances close. A 5 kg bed of diamine-appended Mg-MOF-74 captures about 0.8 kg of CO₂ over a representative cycle, of which about 0.3 kg is released at the default regeneration temperature and converted into a permanent, weighable mass of calcium carbonate. The regeneration energy of roughly 1060 kJ is supplied entirely by waste exhaust heat.

The work gives a quantitative answer to each of the three gaps identified in the literature. By modelling adsorption and regeneration as a repeating cycle, it provides per-cycle figures for capture, release, and energy under engine-like conditions. By specifying the geometry and connections of the three subsystems, it indicates that the unit can be laid out within the space limits of a standard vehicle. By tracking calcium hydroxide use and calcium carbonate output alongside the energy balance, it accounts for the full cost of capture, including the onboard disposal step that conventional designs leave unsolved. The limewater stage is the key contribution here, because it stores the CO₂ as a stable solid and removes the need for compression and pressurised storage.

The main value of the system is that it operates passively. It draws no power from the vehicle, uses waste heat that would otherwise be lost, and produces an inert solid that can be measured directly. These features make it well suited to a mobile platform, where space, weight, and power are all constrained.

The findings are estimates from a literature-based model, not measured performance, and they should be read in that light. The clearest next step is a physical prototype that can be weighed, since each cycle produces a fixed mass of calcium carbonate that a bench test could compare against the predicted value. Further work should measure adsorption under transient exhaust conditions, test the cycling stability of the grafted amines, and fit the release behaviour to thermogravimetric data. Subject to these checks, this study indicates that diamine-appended MOFs combined with limewater mineralisation offer a credible pathway toward onboard carbon capture for vehicles.

## Acknowledgements

We express our sincere gratitude to our Chemistry Mentor, Yash Verma, and the science faculty at 10x International School, Mysore, for their invaluable guidance, technical reviews, and mentorship throughout the development of this project. We also thank the Scientific Review Committee of the IRIS National Fair for valuable preliminary feedback. This study builds on the published research of many groups working on metal-organic frameworks and carbon capture, whose work is cited throughout the paper.

## Declarations

**Originality.** The concept, system design, and simulation model presented in this paper are our own original work. We researched, designed, and developed this project under the mentorship of our Chemistry Mentor, Yash Verma. All external data, literature constants, and comparative baselines are drawn from peer-reviewed publications and cited accordingly.

**Authors' Contributions.** We, Advik Harihar and Panav K Bysani, collaboratively developed the conceptual system architecture, mathematical formulations, numerical modeling, interactive simulation code, and manuscript preparation under the guidance of our Chemistry Mentor, Yash Verma.

**Data and code availability.** The complete simulation model, analytical scripts, and datasets are openly available in the accompanying project repository for independent verification. All parameters and their sources are listed in the paper.

**Conflicts of interest.** We declare no conflicts of interest.

## About the Authors

**Advik Harihar** is a student at 10x International School, Mysore. His academic interests center on investing, stocks, mathematics, chemistry, and computational modeling of adsorption equations and thermodynamic behavior in metal-organic frameworks (MOFs).

**Panav K Bysani** is a student at 10x International School, Mysore. His academic interests center on business, applied chemistry, and environmental science, with a focus on practical decarbonization solutions and clean technology.

**Yash Verma (Chemistry Mentor)** holds a Master of Technology (M.Tech) from the Indian Institute of Technology (IIT) Kharagpur, where he worked as a Project Scientist for two years. His research interests span mathematical modeling and chemical engineering. He currently serves as a Chemistry Faculty member at 10x International School, Mysore, teaching IB Middle Years Programme (MYP) and IB Diploma Programme (DP) Chemistry.

---

## References

[1] Yu, C.H., Huang, C.H. and Tan, C.S. (2012). A review of CO2 capture by absorption and adsorption. *Aerosol and Air Quality Research*, 12, pp. 745-769.
[2] Zhang, Z., Borhani, T.N. and Olabi, A.G. (2020). Status and perspective of CO2 absorption process. *Energy*. doi:10.1016/j.energy.2020.118057.
[3] Project Synopsis (2024). Applications for Vehicle Exhaust; Conclusions and Research Gaps.
[4] Mahajan, S., Elfving, J. and Lahtinen, M. (2024). Evaluating the viability of ethylenediamine-functionalized Mg-MOF-74 in direct air capture: the challenges of stability and slow adsorption rate. *Journal of Environmental Chemical Engineering*, 12(2), 112193.
[5] Peh, S.B. and Zhao, D. (2020). Tying amines down for stable CO2 capture. *Science*, 369(6502), pp. 374-375.
[6] Xie, F. et al. (2025). Advances in amine-functionalized metal-organic frameworks for carbon capture. *Journal of Materials Chemistry A*, 13(2), pp. 522-544.
[7] Hughes, R. et al. (2021). Isotherm, kinetic, process modeling, and techno-economic analysis of a diamine-appended metal-organic framework for CO2 capture using fixed bed contactors. *Energy & Fuels*, 35(6), pp. 5122-5136.
[8] Haynes, W.M. (ed.) (2016). *CRC Handbook of Chemistry and Physics*, 97th edn. Boca Raton: CRC Press. (Solubility product of calcite, about 3.3 x 10^-9; thermal decomposition of calcium carbonate near 825 C.)
[9] Zhu, Z. et al. (2024). High-capacity, cooperative CO2 capture in a diamine-appended metal-organic framework through a combined chemisorptive and physisorptive mechanism. *Journal of the American Chemical Society*, 146(8), pp. 5369-5381.
[10] Holmes, H.E. et al. (2023). Optimum relative humidity enhances CO2 uptake in diamine-appended M2(dobpdc). *Chemical Engineering Journal*, 477, 147116.
[11] Standard drive-cycle durations: WLTP (UN GTR No. 15), about 30 minutes; FTP-75 (US EPA Federal Test Procedure), about 31 minutes.
[12] Kadota, K. et al. (2021). One-pot, room-temperature conversion of CO2 into porous metal-organic frameworks. *Journal of the American Chemical Society*, 143(40), pp. 16404-16408.
[13] Mao, H. et al. (2022). A scalable solid-state nanoporous network with atomic-level interaction design for carbon dioxide capture. *Science Advances*, 8(31), eabo6849.


---

## Figure files (insert at the marked [FIGURE ... HERE] points)

- **Figure 3.1** Methodology flowchart -> your existing Canva design.
- **Figure 3.4.1** System schematic -> Figure_3.4.1_system_schematic.png / .svg
- **Figure 3.4.2** Algorithm flowchart -> Figure_3.4.2_algorithm_flowchart.png / .svg
- **Figure 4.1** Adsorption curve -> Figure_4.1_adsorption_curve.png / .svg
- **Figure 4.2** Multi-cycle results (85 C vs 110 C) -> Figure_4.2_multicycle_results.png

Separate files (not part of the paper): co2_capture_simulation.py and Simulation_Documentation.md.


---

## Editorial notes (remove before final submission)

## Open items to confirm before submission

1. **Algorithm section number.** Your "Inputs" page says the Python algorithm "should go to section 3.2," but the "IRIS Edits" page puts the CAD model in 3.4.1, which implies the algorithm belongs in 3.4.2. We placed it in 3.4.2. Please confirm which numbering Mr. Verma wants.
2. **Sigmoid midpoint / regeneration window** (flag in Section 3.3.2) and **capacity value Q_max** (flag in Section 3.3.1) are science decisions kept as-is for you to resolve.
3. **Figures to insert:** Figure 3.1 (methodology flowchart), Figure 3.4.1 (Rhino CAD/schematic), Figure 3.4.2 (algorithm flowchart). Rebuilt versions of 3.4.1 and 3.4.2 are provided.
4. **Reference [8]** is filled with the CRC Handbook below; confirm your preferred citation style.

---