<div align="center">

# 🚜 PROJECT SETU (सेतु)
### Industrial-Grade AI-Assisted Subterranean Mine Rescue & Multi-Spectral Reconnaissance Rover
**Bridging the Critical 2-to-4 Hour Emergency Inspection Delay in Degree III Gassy Underground Coal Mines**

[![Live Demo](https://img.shields.io/badge/Live_Deployment-Vercel_Production-00f0ff?style=for-the-badge&logo=vercel&logoColor=white)](https://setu-mine-rescue-rover.vercel.app)
[![SIH 2026](https://img.shields.io/badge/Smart_India_Hackathon-SIH_2026_PS_ID:_SIH26039-f59e0b?style=for-the-badge&logo=target&logoColor=white)](https://setu-mine-rescue-rover.vercel.app)
[![DGMS Ex d I Mb](https://img.shields.io/badge/Certification_Target-DGMS_%2F_PESO_Ex_d_I_Mb-10b981?style=for-the-badge&logo=shield&logoColor=white)](https://setu-mine-rescue-rover.vercel.app)

---Q

[![Atmanirbhar Bharat](https://img.shields.io/badge/National_Mission-Atmanirbhar_Bharat-ff9933?style=flat-square&logo=india&logoColor=white)](#)
[![Make In India](https://img.shields.io/badge/Initiative-Make_in_India-138808?style=flat-square)](#)
[![Edge AI](https://img.shields.io/badge/Edge_Compute-NVIDIA_Jetson_AGX_Orin_275_TOPS-76b900?style=flat-square&logo=nvidia&logoColor=white)](#)
[![ROS 2](https://img.shields.io/badge/Robotics_Middleware-ROS_2_Humble-22314E?style=flat-square&logo=ros&logoColor=white)](#)
[![LiDAR](https://img.shields.io/badge/3D_Spatial_LiDAR-Ouster_OS0--128-06b6d4?style=flat-square)](#)
[![Thermal Vision](https://img.shields.io/badge/Radiometric_Thermal-FLIR_Boson_LWIR-e11d48?style=flat-square&logo=flir&logoColor=white)](#)
[![Bio-Radar](https://img.shields.io/badge/Life_Detection-400MHz_FMCW_UWB_Radar-8b5cf6?style=flat-square)](#)
[![Motor Controller](https://img.shields.io/badge/Motor_Control-ESP32_+_BTS7960_43A-d97706?style=flat-square)](#)

[🌐 **Explore Web Platform & OCU Terminal Simulator**](https://setu-mine-rescue-rover.vercel.app) • [📹 **Watch 6 Field Demos**](https://setu-mine-rescue-rover.vercel.app/#demonstrations) • [🧭 **Interactive Schematic**](https://setu-mine-rescue-rover.vercel.app/#hardware-labeling) • [📑 **DGMS Roadmap**](https://setu-mine-rescue-rover.vercel.app/#credibility)

</div>

---

## 📑 Table of Contents
1. [Executive Summary & Problem Statement](#-executive-summary--problem-statement)
2. [Tactical Capabilities & Feature Breakdown (11 Domains)](#-tactical-capabilities--feature-breakdown)
3. [System Architecture & Data Pipelines](#-system-architecture--data-pipelines)
4. [Hardware Blueprint & 12 Subsystem Callouts](#-hardware-blueprint--12-subsystem-callouts)
5. [Multi-Gas Atmospheric Suite & Chemistry Matrix](#-multi-gas-atmospheric-suite--chemistry-matrix)
6. [Mathematical & Physics Formulations](#-mathematical--physics-formulations)
7. [Physical Validation Evidence (6 Videos + 6 Field Frames)](#-physical-validation-evidence)
8. [Cross-State Teleoperation & Long-Range Control](#-cross-state-teleoperation--long-range-control)
9. [Two-Way Trapped Worker Audio Intercom](#-two-way-trapped-worker-audio-intercom)
10. [DGMS, PESO & CIMFR Certification Roadmap](#-dgms-peso--cimfr-certification-roadmap)
11. [Repository Structure & Local Development](#-repository-structure--local-development)

---

## 🚨 Executive Summary & Problem Statement

In underground coal mining disasters (roof falls, gas explosions, strata fires, and inundations), conventional mine rescue protocols enforce a mandatory **2-to-4 hour standby delay** while surface teams assess atmospheric flammability. Entering volatile, unmapped headings risks human rescuers' lives to secondary firedamp explosions and lethal afterdamp gas concentrations.

```
CONVENTIONAL MINING PROTOCOL (HIGH DELAY & RISK):
[Disaster Event] ──> [2-to-4 Hour Atmospheric Standby] ──> [High-Risk Human Rescue Ingress] ──> [Secondary Risk]

PROJECT SETU RAPID RESPONSE PARADIGM:
[Disaster Event] ──> [Immediate SETU Rover Ingress] ──> [Real-Time 3D SLAM + 5-Gas + Bio-Radar] ──> [Surgical Human Entry]
                       ⏱️ < 15 Minutes Deployment              📊 Zero Human Life At Risk
```

**PROJECT SETU (सेतु)** is an industrial-grade, AI-assisted autonomous and teleoperated subterranean ground reconnaissance vehicle engineered to bridge this critical operational window. Built for **Degree III Gassy Coal Mines** (e.g., Jharia, Raniganj, Singareni), SETU penetrates unmapped galleries to deliver real-time **3D LIO-SAM mapping**, **FLIR radiometric thermal imaging**, **400 MHz FMCW sub-surface bio-radar respiration detection**, and **5-gas atmospheric hazard profiling** before human teams are committed.

---

## ⚡ Tactical Capabilities & Feature Breakdown

<table>
  <thead>
    <tr>
      <th width="8%">#</th>
      <th width="24%">Operational Domain</th>
      <th width="48%">Core Technical Capabilities</th>
      <th width="20%">Key Hardware / Protocols</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>01</strong></td>
      <td><strong>🚜 Mobility &amp; Remote Operation</strong></td>
      <td>
        • Articulated twin-chassis crawler with 4-wheel/4-motor independent propulsion<br/>
        • High-current BTS7960 H-bridges traversing mud, loose gravel, and <strong>33° rock slag inclines</strong><br/>
        • Planetary flipper sub-tracks delivering <strong>220 mm obstacle step climbing</strong><br/>
        • Local wireless joystick OCU + Sub-GHz LoRa mesh + <strong>Mumbai ↔ Jharkhand 4G/5G long-distance teleop</strong><br/>
        • 100 ms communication-loss failsafe watchdog with automatic motor lock
      </td>
      <td><code>BTS7960 43A</code> <code>4-Motor Drive</code> <code>LoRa Mesh</code> <code>4G/5G MQTT</code> <code>E-Stop Watchdog</code></td>
    </tr>
    <tr>
      <td><strong>02</strong></td>
      <td><strong>👁️ Multi-Modal Perception</strong></td>
      <td>
        • Synchronized dual-spectrum vision cutting through dense coal dust clouds &amp; smoke<br/>
        • <strong>FLIR Radiometric LWIR (8–14 µm, &lt;50 mK NETD)</strong> thermal imager<br/>
        • Sony IMX662 Starvis 2 RGB camera + <strong>850 nm active infrared NoIR night vision</strong><br/>
        • <strong>180° fisheye panoramic awareness</strong> &amp; thermal heat anomaly gradient tracking
      </td>
      <td><code>FLIR Boson LWIR</code> <code>850nm IR Illum</code> <code>NoIR Night Vision</code> <code>180° Fisheye</code></td>
    </tr>
    <tr>
      <td><strong>03</strong></td>
      <td><strong>🤖 Edge AI On-Board Compute</strong></td>
      <td>
        • On-board <strong>NVIDIA Jetson AGX Orin (275 TOPS)</strong> &amp; Jetson Nano processing<br/>
        • Hardware-accelerated <strong>TensorRT YOLOv10 executing in &lt; 3.0 ms per frame</strong><br/>
        • 100% local edge inference with <strong>zero reliance on cloud latency</strong><br/>
        • Direct Memory Access (DMA) multi-camera perception pipeline
      </td>
      <td><code>NVIDIA AGX Orin</code> <code>275 TOPS</code> <code>TensorRT YOLOv10</code> <code>&lt;3ms Latency</code></td>
    </tr>
    <tr>
      <td><strong>04</strong></td>
      <td><strong>🫁 Mine Safety Monitoring</strong></td>
      <td>
        • Continuous real-time 5-gas atmospheric hazard profiling suite<br/>
        • <strong>CH₄ Methane</strong> (0.01%–100% LEL) with <strong>DGMS 1.25% automatic safety interlock</strong><br/>
        • <strong>CO Toxic Gas</strong> detection &amp; Graham spontaneous coal combustion ratio calculation<br/>
        • <strong>O₂ Depletion</strong> (&lt;19.5% alarm), <strong>H₂S Stinkdamp</strong> (0.1 PPM res), &amp; <strong>CO₂ Blackdamp</strong> NDIR sensor
      </td>
      <td><code>CH₄ Methane</code> <code>CO Toxic</code> <code>H₂S Stinkdamp</code> <code>O₂ Depletion</code> <code>CO₂ Blackdamp</code></td>
    </tr>
    <tr>
      <td><strong>05</strong></td>
      <td><strong>🧱 Rescue &amp; Victim Detection</strong></td>
      <td>
        • Multi-modal life confirmation pipeline: Optical RGB + Radiometric LWIR + Bio-Radar<br/>
        • <strong>400 MHz FMCW UWB Bio-Radar</strong> penetrating up to <strong>10 meters of collapsed rubble</strong><br/>
        • 1D-CNN neural micro-Doppler filter isolating <strong>0.2–0.5 Hz human chest respiration</strong><br/>
        • Reliable trapped survivor localization in 0-lux darkness &amp; void spaces
      </td>
      <td><code>400MHz FMCW Radar</code> <code>10m Penetration</code> <code>0.2–0.5Hz Breathing</code> <code>1D-CNN AI</code></td>
    </tr>
    <tr>
      <td><strong>06</strong></td>
      <td><strong>📡 Multi-Tier Communications</strong></td>
      <td>
        • <strong>5.8 GHz COFDM digital video transmitter</strong> for non-line-of-sight FHD video around tunnel turns<br/>
        • <strong>865 MHz Sub-GHz LoRa peer-to-peer &amp; repeater mesh</strong> link<br/>
        • Wi-SUN low-power subterranean sensor networking integration<br/>
        • <strong>4G/5G cellular MQTT teleoperation bridge</strong> linking mine headings directly to surface HQ
      </td>
      <td><code>COFDM RF Link</code> <code>LoRa 865MHz</code> <code>Wi-SUN Mesh</code> <code>4G/5G Cellular</code> <code>MQTT Broker</code></td>
    </tr>
    <tr>
      <td><strong>07</strong></td>
      <td><strong>🎥 Live Situational Awareness</strong></td>
      <td>
        • Synchronized <strong>Quad-Stream HUD</strong> (Optical RGB, Thermal LWIR, NoIR, LiDAR Occupancy)<br/>
        • <strong>Sub-300 ms glass-to-glass latency</strong> on dedicated handheld dual-joystick OCU<br/>
        • Real-time gas concentrations, heading compass, and battery diagnostics on OCU TFT screen<br/>
        • Web-based incident commander dashboard for emergency rescue brigade coordination
      </td>
      <td><code>Quad Video HUD</code> <code>Sub-300ms Teleop</code> <code>Live Gas Gauge</code> <code>Battery Telemetry</code></td>
    </tr>
    <tr>
      <td><strong>08</strong></td>
      <td><strong>🗺️ Subterranean Exploration &amp; 3D SLAM</strong></td>
      <td>
        • <strong>Ouster OS0-128 digital LiDAR (128 channels, 360° laser array)</strong><br/>
        • Time-of-Flight (ToF) rangefinder sensors for precision micro-obstacle clearance<br/>
        • Real-time factor-graph <strong>3D LIO-SAM SLAM</strong> in GPS-denied cyclic room-and-pillar galleries<br/>
        • Millimeter-accurate 3D point cloud generation and hazard navigation vectors
      </td>
      <td><code>Ouster OS0-128</code> <code>3D LIO-SAM</code> <code>GPS-Denied SLAM</code> <code>ToF Rangefinders</code></td>
    </tr>
    <tr>
      <td><strong>09</strong></td>
      <td><strong>🔊 Two-Way Trapped Worker Intercom</strong></td>
      <td>
        • Onboard high-sensitivity noise-canceling microphone capturing faint survivor acoustic cries<br/>
        • Waterproof acoustic loudspeaker broadcasting surface rescue directives to trapped miners<br/>
        • Active DSP noise suppression eliminating subterranean blower and water background noise<br/>
        • Direct psychological comfort and emergency guidance during critical rescue phases
      </td>
      <td><code>Two-Way Intercom</code> <code>Acoustic Speaker</code> <code>Noise-Canceling Mic</code> <code>Duplex Voice</code></td>
    </tr>
    <tr>
      <td><strong>10</strong></td>
      <td><strong>⚡ Control &amp; Safety Architecture</strong></td>
      <td>
        • Dedicated <strong>dual-core ESP32 microcontroller</strong> running low-level 100 Hz deterministic motor loops<br/>
        • High-current BTS7960 43A motor drivers with optocoupled galvanic command isolation<br/>
        • <strong>100 ms communication loss watchdog</strong> triggering automatic motor cutoff<br/>
        • Modular hot-swappable I2C / UART sensor architecture &amp; battery monitoring
      </td>
      <td><code>ESP32 Dual Core</code> <code>BTS7960 43A</code> <code>100ms Watchdog</code> <code>Galvanic Isolation</code></td>
    </tr>
    <tr>
      <td><strong>11</strong></td>
      <td><strong>🏭 Mine-Deployment &amp; DGMS Focus</strong></td>
      <td>
        • Engineered for hazardous Indian coalfields (Jharia, Raniganj, Singareni, Korba)<br/>
        • Target explosion-proof standard: <strong>Ex d I Mb (flame path gap &lt; 0.1 mm, IEC 60079-1)</strong><br/>
        • Grade 5 titanium &amp; 316L stainless steel enclosure with non-sparking crawler tracks<br/>
        • DGMS Tech Circular 02/2021 &amp; CIMFR Dhanbad certification testing roadmap
      </td>
      <td><code>Degree III Coal Mines</code> <code>Ex d I Mb Target</code> <code>DGMS Guidelines</code> <code>PESO / CIMFR</code></td>
    </tr>
  </tbody>
</table>

---

## 🏗️ System Architecture & Data Pipelines

```mermaid
flowchart TB
    subgraph PERCEPTION ["👁️ MULTI-SPECTRAL PERCEPTION SUITE"]
        LIDAR["Ouster OS0-128 3D LiDAR\n(128 Channels / 360° Point Cloud)"]
        THERMAL["FLIR Boson LWIR 8–14µm\n(<50 mK Radiometric Thermal)"]
        NOIR["Sony IMX662 Starvis 2\n(RGB + 850nm IR NoIR Night Vision)"]
        RADAR["400 MHz FMCW UWB Bio-Radar\n(10m Rubble Penetration Array)"]
        GAS["Trolex Sentro 5-Gas Array\n(CH4, CO, H2S, O2, CO2, Temp/RH)"]
    end

    subgraph COMPUTE ["🤖 ON-BOARD EDGE AI ENGINE (NVIDIA JETSON AGX ORIN)"]
        DMA["DeepStream Direct Memory Access (DMA) Video Pipeline"]
        YOLO["TensorRT YOLOv10 Engine\n(< 3.0 ms Multi-Class Human Detection)"]
        SLAM["3D LIO-SAM Factor-Graph SLAM\n(IMU Pre-Integration & Loop Closure)"]
        DSP["1D-CNN Micro-Doppler Respiration DSP\n(0.2–0.5 Hz Breathing Extraction)"]
        DMA --> YOLO
        LIDAR --> SLAM
        RADAR --> DSP
    end

    subgraph LOW_LEVEL ["⚡ LOW-LEVEL CONTROL & SAFETY (ESP32 + BTS7960)"]
        ESP["ESP32 Dual-Core Real-Time Controller\n(100 Hz Deterministic Motor Loop)"]
        DRV["BTS7960 43A High-Current H-Bridges\n(4x Planetary Geared DC Motors)"]
        WATCHDOG["Hardware Watchdog Timer\n(100ms Signal-Loss Auto-Shutdown)"]
        ESTOP["Galvanic Fail-Safe E-Stop Relay\n(Instant Power Isolation)"]
        ESP --> DRV
        WATCHDOG --> DRV
        ESTOP --> DRV
    end

    subgraph COMMS ["📡 REDUNDANT COMMUNICATION MESH"]
        COFDM["5.8 GHz COFDM Video Transmitter\n(Uncompressed FHD Video Link)"]
        LORA["865 MHz Sub-GHz LoRa Mesh\n(Telemetry & Joystick Commands)"]
        CELLULAR["4G/5G Cellular + MQTT Broker\n(Cross-State Teleoperation Bridge)"]
        INTERCOM["Two-Way Audio Intercom\n(Acoustic Speaker + Noise-Canceling Mic)"]
    end

    subgraph GCS ["🎮 OPERATOR CONTROL UNIT (OCU) & SURFACE HQ"]
        OCU["Dedicated Handheld OCU Console\n(Dual Joysticks + TFT Quad-Feed HUD)"]
        CLOUD["Surface Command Incident Dashboard\n(Remote Web Monitoring & Briefings)"]
    end

    PERCEPTION --> COMPUTE
    COMPUTE --> COMMS
    LOW_LEVEL <--> COMMS
    COMMS <--> GCS
```

---

## 🔍 Hardware Blueprint & 12 Subsystem Callouts

```
                    ┌─────────────────────────[01] Ouster 3D LiDAR (128-CH)
                    │               ┌─────────[02] FLIR Radiometric Thermal Core
                    │               │       ┌─[03] COFDM 5.8GHz Whip Antenna
                    │               │       │
              ┌─────▼───────────────▼───────▼─────┐
              │                                   │ ◄─── [04] Raspberry Pi Optical Cam
              │         PROJECT SETU ROVER        │
              │                                   │ ◄─── [07] Dual 1200lm Cree LED Floodlights
              └─────┬───────────────┬───────┬─────┘
                    │               │       │
                    │               │       └─[06] ATEX 24V Geared Motors
                    │               └─────────[12] 48V LiFePO4 Explosion-Proof Battery
                    └─────────────────────────[05] Articulated Twin Flipper Tracks
       
       [08] Jetson AGX Orin (275 TOPS)  |  [09] 400MHz FMCW Bio-Radar Array
       [10] Fail-Safe Hardware E-Stop    |  [11] 915MHz LoRa Mesh + 9-Axis IMU
```

| Pin # | Subsystem Name | Component Specification | Primary Mission Function |
|---|---|---|---|
| **01** | **3D LiDAR Array** | Ouster OS0-128 Uniform Digital LiDAR | 128 channels, 360° point cloud generation, 865nm AR sapphire optical window for real-time LIO-SAM mapping. |
| **02** | **Multi-Spectral Vision** | FLIR Boson 640 LWIR + Sony IMX662 NoIR | Simultaneous radiometric thermal thermography (8–14 µm) and starlight night vision piercing dense dust. |
| **03** | **COFDM Video Link** | 5.8 GHz Non-Line-of-Sight Digital RF TX | Low-latency uncompressed FHD video transmission around subterranean tunnel bends and collapsed rubble. |
| **04** | **Optical Navigation Cam** | High-Framerate Forward Camera + Gimbal | Low-latency forward obstacle awareness and terrain ingress guidance with 2-axis servo pan/tilt gimbal. |
| **05** | **Articulated Twin Tracks** | Kevlar Anti-Static Rubber Crawler Tracks | Continuous ground contact across 33° rock slag and 220 mm step climbing via planetary sub-tracks. |
| **06** | **ATEX Geared Motors** | Dual 24V High-Torque Brushless DC Motors | Factory-certified flameproof sealed planetary gearboxes engineered for explosive coal dust environments. |
| **07** | **High-Beam Floodlights** | Dual 1200-Lumen Cree COB LED Array | 0-lux subterranean blackout illumination with optical diffuser lenses for obstacle navigation. |
| **08** | **Edge AI Compute** | NVIDIA Jetson AGX Orin (64GB, 275 TOPS) | Executes TensorRT YOLOv10 inference (< 3ms) and factor-graph SLAM state estimation in GPS-denied tunnels. |
| **09** | **FMCW Bio-Radar Array** | 400 MHz Ultra-Wideband (UWB) Bio-Radar | Ground-penetrating radar detecting trapped human respiration (0.2–0.5 Hz chest motion) through 10m rubble. |
| **10** | **Hardware E-Stop** | Galvanically Isolated Magnetic Relay | Instantaneous remote battery power isolation upon combustible methane threshold spike (> 1.25%). |
| **11** | **Telemetry Mesh & IMU** | 915 MHz Sub-GHz Transceiver + 9-Axis IMU | High-reliability telemetry link paired with tactical IMU for active zero-drift gyroscope heading stabilization. |
| **12** | **Explosion-Proof Battery**| 48V LiFePO4 Thermal-Runaway Enclosure | Flameproof lithium iron phosphate power module delivering 4.5 hours of continuous reconnaissance endurance. |

---

## 🫁 Multi-Gas Atmospheric Suite & Chemistry Matrix

The rear sensing column of Project SETU houses an integrated multi-gas monitoring array conforming to **DGMS Tech Circular No. 02 of 2021** and **Coal Mines Regulations (CMR) 2017**:

```
 ┌───────────────────────── REAR SENSOR COLUMN ─────────────────────────┐
 │ [CH4] Methane Dual Core  │ Pellistor Catalytic Bead + Dual-Beam NDIR │
 │ [CO]  Carbon Monoxide    │ 3-Electrode Platinum Electrochemical Cell │
 │ [H2S] Hydrogen Sulfide   │ Ultra-Sensitive Amperometric Probe        │
 │ [O2]  Oxygen Depletion   │ Lead-Free Non-Depleting Optical Cell      │
 │ [CO2] Carbon Dioxide     │ Dual-Wavelength 4.26 µm NDIR Sensor       │
 │ [TMP] Climate Probe      │ MEMS Calibrated -40°C to +85°C / 100% RH  │
 │ [DST] Aerosol Counter    │ Laser Scatter Optical Particulate Counter │
 └───────────────────────────────────────────────────────────────────────┘
```

| Gas Molecule | Sensor Chemistry | Detection Range | DGMS Safety Limit | Disaster Verification Role |
|---|---|---|---|---|
| **Methane ($\text{CH}_4$)** | Catalytic Pellistor + Dual-Beam NDIR | 0.01% – 100% LEL (0–5.0% vol) | $\le 1.25\%$ Auto-Interlock | Firedamp pocket detection; prevents electrical spark ignition. |
| **Carbon Monoxide ($\text{CO}$)** | 3-Electrode Solid-State Electrochemical | 0 – 1,000 PPM (Res: 0.5 PPM) | $\le 25\text{ PPM}$ Safe Limit | Early detection of spontaneous coal seam combustion & gob fires. |
| **Hydrogen Sulfide ($\text{H}_2\text{S}$)** | Ultra-Sensitive Amperometric Probe | 0 – 100 PPM (Res: 0.1 PPM) | $\le 10\text{ PPM}$ Evacuation | Profiles deadly sour gas released from water reservoirs & strata faults. |
| **Oxygen ($\text{O}_2$)** | Lead-Free Optical Galvanic Cell | 0 – 25.0% Volume (±0.1%) | $\ge 19.5\%$ Breathable Air | Validates safe breathable headings before human entry. |
| **Carbon Dioxide ($\text{CO}_2$)** | Dual-Wavelength 4.26 µm NDIR | 0 – 10,000 PPM (0–1.0% vol) | $\le 5,000\text{ PPM}$ ($0.5\%$) | Detects heavy suffocating blackdamp pools in low-lying dip workings. |
| **Temperature &amp; RH** | MEMS Calibrated Digital Probe | -40°C to +85°C / 0–100% RH | $\le 38^\circ\text{C}$ Heat Stress | Identifies underground strata fire proximity &amp; rescue heat indices. |
| **Coal Dust (PM2.5/10)** | Forward Laser Scatter Counter | 0 – 1,000 $\text{mg/m}^3$ | $\le 50\text{ mg/m}^3$ Explosive | Monitors explosive dust concentration &amp; LiDAR optical de-hazing. |

---

## 📐 Mathematical & Physics Formulations

### 1. Terramechanical Drawbar Pull & Soil Mechanics
Chassis traction over loose coal slag and jagged quarry rubble is governed by the **Bekker-Wong Track-Soil Interaction Model**:

$$\tau = c + \sigma \tan \phi = c + \left(\frac{W}{2 b L}\right) \tan \phi$$

$$\text{DP} = 2 b L \left[ c \left( 1 - \frac{1 - e^{-j/K}}{j/K} \right) + \left(\frac{W}{2 b L}\right) \tan \phi \left( 1 - \frac{1 - e^{-j/K}}{j/K} \right) \right] - R_c$$

*Where $b$ = track width, $L$ = ground contact length, $c$ = soil cohesion, $\phi$ = internal friction angle, $j$ = track shear displacement, $K$ = shear deformation modulus, and $R_c$ = compaction resistance.*

---

### 2. 400 MHz FMCW Bio-Radar Respiration Extraction
Micro-Doppler phase modulation induced by human chest wall displacement ($\Delta x(t) = A_r \sin(2\pi f_r t)$) under collapsed rubble is modeled as:

$$s_b(t) \approx A \exp\left(j \left[ 2\pi f_b t + \frac{4\pi}{\lambda} d_0 + \frac{4\pi}{\lambda} A_r \sin(2\pi f_r t) \right]\right)$$

$$\Delta \Phi(t) = \frac{4\pi}{\lambda} A_r \sin(2\pi f_r t) \quad \xrightarrow{\text{1D-CNN + FFT}} \quad f_r \in [0.2, 0.5]\text{ Hz (Human Breathing Cadence)}$$

---

### 3. Graham's Spontaneous Combustion Index
Atmospheric gas progression indicating active underground coal fires is computed in real time via Graham's Ratio:

$$G_R = \frac{\Delta \text{CO}}{\Delta \text{O}_2\text{ Deficit}} = \frac{[\text{CO}]}{0.265 \cdot [\text{N}_2] - [\text{O}_2]} \times 100\%$$

* $G_R < 0.5\%$: Normal subterranean baseline.
* $0.5\% \le G_R \le 1.0\%$: Early-stage superficial heating.
* $G_R > 2.0\%$: Active blazing subterranean coal seam fire.

---

### 4. 3D LIO-SAM Factor Graph Pose Optimization
GPS-denied odometry fuses 6-DOF IMU pre-integration factors with LiDAR point-to-plane and point-to-edge geometric residuals:

$$\mathcal{X}^* = \arg\min_{\mathcal{X}} \left\{ \sum_{k} \left\| \mathbf{r}_{\text{IMU}}(k, k+1) \right\|_{\boldsymbol{\Sigma}_{\text{IMU}}}^2 + \sum_{i} \left\| \mathbf{r}_{\text{LiDAR}}(i) \right\|_{\boldsymbol{\Sigma}_{\text{LiDAR}}}^2 + \sum_{j} \left\| \mathbf{r}_{\text{Loop}}(j) \right\|_{\boldsymbol{\Sigma}_{\text{Loop}}}^2 \right\}$$

---

## 📹 Physical Validation Evidence

### Exactly 6 Video Demonstrations
1. **Locomotion & Chassis Propulsion**: 4-belt articulated crawler tracks conquering 33° quarry rock debris and coal slag.
2. **3D SLAM & Sensor Fusion**: Real-time RGB-D and 3D LiDAR point cloud synthesis in unmapped corridors.
3. **Direct Handheld OCU Teleoperation**: Dual proportional joystick control delivering sub-300 ms ground response.
4. **Multi-Terrain Ingress**: Full outdoor haul road and uneven portal transit with continuous 360° LiDAR scanning.
5. **FLIR Radiometric Thermal Recon**: Dual-spectrum LWIR thermography isolating survivor heat signatures through dense dust.
6. **50 kg Obstacle Step Climbing**: Planetary flippers actively scaling stacked 50 kg cement bags with 220 mm step clearance.

### Exactly 6 Field Proving Frames
1. **Frame 01 // Road & Surface Transit**: High-speed ingress stability on compacted asphalt at 1.2 m/s with gyro drift compensation.
2. **Frame 02 // Quarry Rubble Incline**: Zero-slip traversal over loose jagged coal shale boulders on 30° unpaved inclines.
3. **Frame 03 // 50 kg Barrier Step Climb**: Front flipper tracks conquering stacked industrial cement bags without motor stall.
4. **Frame 04 // Handheld OCU YOLOv8 Night Vision**: Live 30 FPS edge AI person detection bounding boxes in 0-lux total darkness.
5. **Frame 05 // Handheld OCU Radiometric Thermal**: Calibrated LWIR thermography with sub-50 mK thermal sensitivity.
6. **Frame 06 // Handheld Rescue Mission Console**: Live multi-gas atmospheric telemetry HUD ($H_2S$, $CH_4$, $CO$, $O_2$, Temp).

---

## 🌐 Cross-State Teleoperation & Long-Range Control

Project SETU supports a hybrid multi-layer control topology allowing seamless switching between local field operation and remote disaster command:

```
[MUMBAI / HQ COMMAND POST]
   │
   ├─► Cloud MQTT Broker (AWS IoT Core / EMQX)
   │     ▲ (4G/5G Cellular Link / Sub-300ms Glass-to-Glass)
   │     │
[JHARKHAND MINE SURFACE PORTAL]
   │
   ├─► Local Surface Gateway (High-Gain Directional Yagi Antennas)
   │     ▲ (COFDM FHD Video Link + 865 MHz LoRa Mesh)
   │     │
[UNDERGROUND COLLAPSED HEADING]
   └─► PROJECT SETU ROVER (ESP32 Motor Core + NVIDIA Jetson Edge AI)
```

---

## 🔊 Two-Way Trapped Worker Audio Intercom

The onboard audio subsystem establishes a psychological and operational lifeline between trapped miners and surface commanders:

```
                  ┌─────────────────────────────────────────────────────┐
                  │          PROJECT SETU AUDIO INTERCOM SUITE          │
                  └──────────────────────────┬──────────────────────────┘
                                             │
               ┌─────────────────────────────┴─────────────────────────────┐
               ▼                                                           ▼
┌──────────────────────────────┐                           ┌──────────────────────────────┐
│  NOISE-CANCELING MICROPHONE  │                           │ WATERPROOF ACOUSTIC SPEAKER  │
│  • Sensitivity: -38 dBV/Pa   │                           │ • Max Output: 95 dB SPL @ 1m │
│  • Active DSP Noise Filter   │                           │ • Resonant Tunnel Amplifier  │
│  • Picks up faint cries      │                           │ • Broadcasts rescue orders   │
└──────────────────────────────┘                           └──────────────────────────────┘
```

---

## 📜 DGMS, PESO & CIMFR Certification Roadmap

```
PHASE 1: LAB PROTOTYPING & SENSOR INTEGRATION [COMPLETED]
├── Bench testing of 4-belt crawler chassis, BTS7960 drivers, and Jetson Orin AI
└── Validation of 5-gas telemetry, FLIR LWIR vision, and 400 MHz FMCW bio-radar

PHASE 2: SIMULATED QUARRY & MINE INGRESS PROVING [CURRENT]
├── Field testing over 33° rock inclines and 50 kg obstacle step climbing
└── Sub-300 ms teleoperation validation over COFDM video & LoRa mesh links

PHASE 3: CIMFR / PESO FLAMEPROOF TESTING (Ex d I Mb) [Q3 2026]
├── Spark ignition explosion-chamber trials in 8.5% CH4 / air mixtures (IEC 60079-1)
└── Thermal-runaway enclosure testing & flame path gap tolerance validation (< 0.1 mm)

PHASE 4: DGMS MINE RESCUE FIELD INTEGRATION & DEPLOYMENT [Q4 2026]
├── Pilot deployment with Coal India Rescue Brigades across Jharia & Raniganj coalfields
└── Production manufacturing of certified man-packable subterranean recon rovers
```

---

## 💻 Repository Structure & Local Development

```bash
SETU/
├── public/                     # Static assets served at root
│   ├── images/                 # Optimized high-resolution images & schematics
│   │   ├── frames/             # 6 Real-world field proving photo frames
│   │   ├── ocu-screens/        # 4 Handheld OCU mission display captures
│   │   └── rover-schematic/    # Physical rover chassis & sensor back cutouts
│   └── videos/                 # Optimized H.264 MP4 demonstration video assets
├── src/                        # Modular frontend source code
│   ├── index.css               # Master CSS bundle entrypoint
│   ├── js/                     # Application logic modules
│   │   ├── animations.js       # Smooth GSAP / Lenis scrolling & HUD scanlines
│   │   ├── architectureFlow.js # Interactive architecture pipeline visualizer
│   │   ├── hardwareLabeling.js # 12-Hotspot rover blueprint & 7-gas sensor suite
│   │   ├── main.js             # Application initialization & feature filters
│   │   ├── telemetrySim.js     # Live OCU canvas & multi-gas telemetry simulation
│   │   ├── themeToggle.js      # Glowing Filament Lightbulb switch (Light/Dark HUD)
│   │   ├── videoController.js  # Smooth video autoplay & IntersectionObserver
│   │   └── voiceAgent.js       # AI Voice Recon Officer with strict hover control
│   └── styles/                 # Modular CSS stylesheets
│       ├── components.css      # Badges, buttons, tech frames, and modals
│       ├── hardware-labeling.css # Blueprint pins, gas cards, and OCU tabs
│       ├── hero.css            # Full-screen moving rover video background
│       ├── navbar.css          # Header layout & glowing lightbulb button
│       ├── responsive.css      # Mobile-first responsive layout (320px to 4K)
│       ├── sections.css        # Features matrix, math proofs, and credibility
│       └── themes.css          # Dual Theme Engine (Tactical Dark / Daylight HUD)
├── index.html                  # Master web application page
├── package.json                # Project dependencies & npm build scripts
├── vercel.json                 # Vercel deployment config with video byte-ranges
├── vite.config.js              # Vite build tool configuration
└── README.md                   # Comprehensive system documentation
```

### Quickstart & Build Instructions

```bash
# 1. Clone repository
git clone https://github.com/moinkhanCreates/SETU.git
cd SETU

# 2. Install dependencies
npm install

# 3. Launch local development server (Port 3000)
npm run dev

# 4. Compile optimized production bundle
npm run build

# 5. Preview production build locally
npm run preview
```

---

<div align="center">

**PROJECT SETU — SUBTERRANEAN MINE RESCUE & RECONNAISSANCE ROVER**  
*Engineered for Smart India Hackathon 2026 (PS ID: SIH26039)*  
Developed with pride for **Atmanirbhar Bharat** & **Make in India** 🇮🇳

[**Back to Top ⬆**](#-project-setu-सेतु)

</div>
