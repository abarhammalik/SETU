# 🚜 PROJECT SETU (सेतु) : Subterranean Mine Rescue GCS Telemetry Dashboard

<p align="center">
  <a href="https://setu-mine-rescue-rover.vercel.app/"><img src="https://img.shields.io/badge/Live_Web_Platform-Vercel_Production-00f0ff?style=for-the-badge&logo=vercel&logoColor=white" alt="Live Platform"></a>
  <a href="https://github.com/abarhammalik/SETU-Dashboard"><img src="https://img.shields.io/badge/GitHub_Repository-SETU--Dashboard-f59e0b?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Repo"></a>
  <a href="https://setu-mine-rescue-rover.vercel.app/#credibility"><img src="https://img.shields.io/badge/Certification_Target-DGMS_%2F_PESO_Ex_d_I_Mb-10b981?style=for-the-badge&logo=shield&logoColor=white" alt="Compliance"></a>
  <br>
  <img src="https://img.shields.io/badge/National_Mission-Atmanirbhar_Bharat-ff9933?style=flat-square" alt="Atmanirbhar Bharat">
  <img src="https://img.shields.io/badge/Initiative-Make_in_India-138808?style=flat-square" alt="Make in India">
  <img src="https://img.shields.io/badge/SIH_2026-PS_ID:_SIH26039-4B5563?style=flat-square" alt="SIH PS">
  <img src="https://img.shields.io/badge/Edge_Compute-NVIDIA_AGX_Orin_275_TOPS-76b900?style=flat-square&logo=nvidia&logoColor=white" alt="Orin">
</p>

<p align="center">
  <b>Surface Ground Control Station (GCS) Console v3.2 · Telemetry & Physics Analytics Engine · SIH 2026</b>
</p>

<p align="center">
  Ground Control Station (GCS) telemetry, atmospheric analytics, and life-detection console for <b>Project SETU</b> — an industrial-grade AI-assisted autonomous and teleoperated subterranean reconnaissance rover engineered for <b>Degree III Gassy Coal Mines</b> (Smart India Hackathon Problem Statement <b>SIH26039</b>, Government of Jharkhand).
</p>

---

## 🌐 Quick Access & Ecosystem Links

* 🌐 **Official Web Platform:** [https://setu-mine-rescue-rover.vercel.app/](https://setu-mine-rescue-rover.vercel.app/)
* 💻 **GCS Dashboard GitHub Repository:** [https://github.com/abarhammalik/SETU-Dashboard](https://github.com/abarhammalik/SETU-Dashboard)
* 📹 **6 Field Video Demonstrations:** [https://setu-mine-rescue-rover.vercel.app/#demonstrations](https://setu-mine-rescue-rover.vercel.app/#demonstrations)
* 🧭 **Interactive Hardware Schematic:** [https://setu-mine-rescue-rover.vercel.app/#hardware-labeling](https://setu-mine-rescue-rover.vercel.app/#hardware-labeling)
* 🎮 **Handheld OCU Terminal Simulator:** [https://setu-mine-rescue-rover.vercel.app/#ocu-sim](https://setu-mine-rescue-rover.vercel.app/#ocu-sim)
* 📑 **DGMS & CIMFR Compliance Roadmap:** [https://setu-mine-rescue-rover.vercel.app/#credibility](https://setu-mine-rescue-rover.vercel.app/#credibility)

---

## ⚡ Key GCS Features & Capabilities (v3.2)

### 1. Dual-Mode Tactical HUD
* **0-Lux Tactical Dark HUD**: Engineered for low-light command shelters with glowing electric-cyan accents and high-contrast typography.
* **High-Visibility Enterprise Light HUD**: Optimized for bright outdoor conditions and high-ambient incident command deployments.
* **Instant Dynamic Toggle**: Single-click HUD mode switcher with automated subpixel font antialiasing and WCAG-compliant contrast.

### 2. Multi-Domain Subsystem Command Matrix
* `⌖ 01 · MISSION FLIGHT DECK`: Quad-feed low-latency subterranean camera HUD (IMX662 Low-Light Visible + FLIR Boson Radiometric LWIR Thermal + Ouster 3D Point-Cloud).
* `⌬ 02 · 5-GAS ATMOSPHERICS`: Real-time Coward explosibility triangle, Graham's spontaneous combustion ratio, and continuous multi-gas trend charts.
* `◎ 03 · FMCW BIO-RADAR ARRAY`: Sub-surface 400 MHz micro-Doppler human vital sign detector with 0.32 Hz respiration isolation and void localization.
* `◈ 04 · EDGE AI & 3D SLAM`: NVIDIA Jetson AGX Orin edge inference stream (YOLOv10 hazard detection at < 3.0 ms) and real-time 3D LIO-SAM mapping.
* `◫ 05 · SETU ECOSYSTEM & WEB`: Full hardware inventory, actuator health monitor, mesh hop topology, and external link portal.

### 3. Mission Scenario Demonstration Stepper
Six built-in operational mission scenarios with immediate multi-sensor telemetry simulation and regulatory proofs:
1. **⌖ S1 · Routine Patrol**: Baseline autonomous traversal, multi-sensor fusion stability, low-power mesh connectivity.
2. **◎ S2 · Trapped Survivor**: 400 MHz FMCW sub-surface Doppler lock through 4.2m rubble collapse; acoustic intercom unmuted.
3. **⌬ S3 · Seam Heating**: Carbon monoxide elevation (65 PPM) and Graham's Ratio 0.72 detection of invisible spontaneous combustion.
4. **⬡ S4 · DGMS CH₄ Interlock**: 1.45% methane trip crossing statutory 1.25% DGMS limit; automatic electrical power isolation.
5. **▲ S5 · Slag Incline / Tilt**: 38.5° rubble slag traversal exceeding 30° safe margin; active flipper sub-tracks compensation.
6. **⎇ S6 · Mesh Relay Hop**: Sub-1GHz LoRa signal drops to -96 dBm; autonomous mesh relay packet forwarding.

### 4. Tactical Left-Side Calibration Console
* **Real-Time Sliders**: Fine-tune $CH_4$, $O_2$, $CO$, $CO_2$, $H_2$, Mesh RSSI, and chassis tilt.
* **Interactive Life Simulation**: Toggle trapped survivor respiration signatures and sensor drift.
* **Statutory DGMS Compliance Seal**: Live tracking of DGMS Tech Circular 02/2021 interlocks and GCS mission timestamp.

---

> [!IMPORTANT]
> **OPERATIONAL SAFETY & DGMS COMPLIANCE**
> Project SETU's GCS console reserves high-visibility semantic color coding strictly for hazard status (Safe, Caution, Warning, Critical) to adhere to mining Human-Machine Interface (HMI) standards. The dashboard integrates DGMS 1.25% $CH_4$ automatic safety interlocks, Coward flammability triangle evaluation, and Graham's spontaneous coal combustion ratio.

> [!WARNING]
> **DEGREE III GASSY MINE EXPLOSION HAZARD**
> Under disaster conditions (roof falls, gas bursts, strata fires), atmosphere may contain volatile mixtures of $CH_4$, $CO$, $CO_2$, and $H_2$. Sub-surface rover hardware targets **DGMS / PESO Ex d I Mb Flameproof Enclosures** capable of containing internal explosions up to $1.0\text{ MPa}$ without igniting external firedamp.

---

## 🏗️ System Architecture & Data Pipelines

```text
               +-------------------------------------------------------------+
               |        UNDERGROUND DISASTER HAZARD ZONE (DEGREE III SEAM)   |
               +-------------------------------------------------------------+
                                              |
      [ Sentro 5-Gas Array ]      [ 400 MHz FMCW Bio-Radar ]      [ FLIR Radiometric LWIR ]
     (CH4, CO, CO2, O2, H2, N2)    (10m Sub-Rubble Vitals)         (8-14um Thermal Core)
                 \                            |                             /
                  +---------------------------+----------------------------+
                                              |
                          [ NVIDIA Jetson AGX Orin (275 TOPS) ]
                          [ TensorRT YOLOv10 (< 3.0 ms Latency) ]
                          [ 3D LIO-SAM SLAM + Ouster OS0-128 ]
                                              |
                     +------------------------+------------------------+
                     |                                                 |
         [ 5.8 GHz COFDM Video ]                           [ 865 MHz Sub-GHz LoRa ]
        (Uncompressed FHD Video)                         (Telemetry & Joystick Mesh)
                     |                                                 |
                     +------------------------+------------------------+
                                              |
               +-------------------------------------------------------------+
               |                SURFACE COMMAND GCS CONSOLE                  |
               +-------------------------------------------------------------+
                                              |
                          [ 4G/5G MQTT Cross-State Teleop Bridge ]
                          [ Streamlit Tactical GCS Console (app.py) ]
                          [ Atmospheric Physics Engine (mine_analytics.py) ]
```

---

## 🔬 Core Analytics & Mine Safety Physics

The analytical engine (`mine_analytics.py`) calculates real-time spontaneous combustion indices, stoichiometric ratios, and explosive boundaries from raw sensor telemetry.

### 1. Graham's Ratio ($GR$) — Spontaneous Coal Combustion Indicator

Graham's Ratio measures carbon monoxide production relative to oxygen depletion, distinguishing active coal seam oxidation from inert air ventilation:

$$GR = \frac{CO \text{ (ppm)} / 100}{\Delta O_2 \text{ (\% vol)}} = \frac{CO}{0.2093 \cdot N_2 - O_2}$$

| Graham's Ratio Value | Atmospheric Evaluation State | Recommended Tactical Action |
| --- | --- | --- |
| **$GR < 0.4$** | `NORMAL_BACKGROUND` | Standard rover traversal & monitoring |
| **$0.4 \le GR < 0.5$** | `POSSIBLE_HEATING` | Increase telemetry sampling frequency |
| **$0.5 \le GR < 1.0$** | `SPONTANEOUS_HEATING_CONFIRMED` | Prepare ventilation seal contingency |
| **$1.0 \le GR < 2.0$** | `SERIOUS_ADVANCED_HEATING` | Halt rover; inspect seam heat signatures |
| **$2.0 \le GR < 3.0$** | `CRITICAL_HEATING_IMMINENT_FIRE` | Alert surface rescue teams |
| **$GR \ge 3.0$** | `ACTIVE_MINE_FIRE_CONFIRMED` | Immediate evacuation of mesh sector |

---

### 2. Coward's Methane Explosibility Triangle

Methane ($CH_4$) explosibility depends strictly on the co-presence of Oxygen ($O_2$) and inert dilution gases ($N_2$):

$$5.0\% \le CH_4 \le 15.0\% \quad \text{at ambient } O_2 \ge 12.1\%$$

* **Lower Explosive Limit (LEL Line):** $CH_4 = -0.1157 \cdot (O_2 - 12.1) + 5.9$
* **Upper Explosive Limit (UEL Line):** $CH_4 = 1.5993 \cdot (O_2 - 12.1) + 5.9$
* **DGMS Mandatory Safety Interlock:** When $CH_4 \ge 1.25\%$, electrical power to drive systems is cut off immediately to prevent spark ignition.

---

### 3. Sub-Surface FMCW Bio-Radar Life Detection

* **Center Frequency:** $400\text{ MHz}$ FMCW Ultra-Wideband (UWB).
* **Penetration Depth:** Up to $10\text{ meters}$ through collapsed rock, coal, and timber debris.
* **1D-CNN Micro-Doppler Filter:** Isolates human chest displacement ($0.2\text{--}0.5\text{ Hz}$ respiration band) to confirm trapped survivor locations in 0-lux darkness.

---

## 🛠️ Installation & Running the Dashboard

### Prerequisites
* Python 3.10+
* `pip` package manager

### 1. Clone Repository & Environment Setup
```bash
git clone https://github.com/abarhammalik/SETU-Dashboard.git
cd SETU-Dashboard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the GCS Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📂 Repository Structure

```text
SETU-DASHBOARD/
│
├── .streamlit/
│   └── config.toml          # Streamlit server & UI configuration
├── app.py                  # Tactical Streamlit GCS Mission Control Console (v3.2)
├── mine_analytics.py       # Geochemical engine for mine gas physics & fire ratios
├── requirements.txt        # Core dependencies (streamlit, pandas, numpy, altair)
├── README.md               # Complete technical documentation & architecture
└── .gitignore              # Repository exclusion rules
```

---

> **PROJECT SETU GCS Dashboard** · *Smart India Hackathon 2026 (PS ID: SIH26039) · DGMS / PESO Ex d I Mb Target · Atmanirbhar Bharat & Make In India.*
