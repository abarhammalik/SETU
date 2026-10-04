# PROJECT SETU — Summary

**Subterranean Emergency Tracking & Multi-Hazard Edge AI Profiling Infrastructure**

---

## Abstract

PROJECT SETU is an articulated twin-chassis autonomous/teleoperated ground vehicle with a standalone handheld surface command console, developed for underground mine reconnaissance, hazard assessment and rescue assistance.

The central problem addressed is the lack of immediate, multi-modal situational awareness after underground incidents such as roof falls, fires, gas events, flooding and roadway collapse, when direct human entry may be unsafe and the environment may be poorly understood. SETU is designed to:

- Enter and inspect uncertain areas remotely
- Continuously measure environmental conditions
- Identify people or potential human signatures
- Map accessible surroundings
- Transmit actionable information to the surface operator

---

## System Architecture

SETU integrates multiple sensing and computing layers in one mobile platform. The perception stack combines:

- **Thermal imaging** — temperature-based detection of human-relevant heat signatures and environmental anomalies
- **NoIR / night vision** — scene visibility in zero- or low-light conditions
- **Visible camera capability** — standard optical feed
- **LiDAR / ToF ranging** — range and obstacle information for navigation and mapping
- **Multi-gas and environmental sensing** — real-time atmospheric picture
- **Audio communication** — microphone and speaker for operator-to-rover interaction
- **Onboard edge AI** — local YOLO-based person-detection pipeline (no cloud inference required)

### Co-Processor Separation

| Processing Domain | Controller | Responsibility |
| :--- | :--- | :--- |
| AI / Video Processing | Raspberry Pi edge node | Camera data, YOLO inference, video encoding |
| Real-Time Mechatronics | STM32 microcontroller | Motor control, sensor acquisition, wireless command parsing, safety logic |

This separation allows AI/video processing and time-critical vehicle functions to operate independently. Simulation and software testing are also being used for perception, mapping, communication and sensor-fusion development.

### Multi-Modal Resilience

The system combines multiple sensing modes so that operation can continue when individual sensors are degraded by darkness, dust, smoke, obstructions or changing terrain:

| Condition | Primary Sensor | Fallback |
| :--- | :--- | :--- |
| Total darkness | NoIR / night vision | Thermal imaging, ToF ranging |
| Dense dust / smoke | Thermal imaging | LiDAR / ToF, IMU dead-reckoning |
| Obstructed line-of-sight | LiDAR / ToF | Gas sensors, audio |

The rescue-assistance architecture is intended to progress from visible-person detection toward multi-sensor victim localization, including future subsurface radar-assisted detection beneath collapsed material.

---

## Prototype Status & Empirical Validation

The current prototype is approximately **65% physically complete** and has undergone practical testing rather than remaining only a conceptual design.

### Mobility & Wireless Control

- Operated in a **real local underground mine** environment as well as mine-like test conditions
- Wirelessly driven across different terrains and irregular surfaces to evaluate mobility, traction and remote control
- Wireless operation demonstrated across building levels, including control from approximately the **third floor to a basement**, with live video/data available to the operator

### Handheld Controller

- Dedicated handheld controller with an integrated display tested for field operation
- Operator can control the rover while viewing live feed, gas/environment metrics and system status
- **No laptop required** as the primary control interface

### Perception System Validation

- **Thermal images** collected in underground conditions for analysis of ambient and localized temperature variation
- **NoIR / night-vision camera** tested in very dark environments, including road-construction conditions, where human detection and scene observation were evaluated under low ambient illumination
- **Onboard Raspberry Pi** used to execute YOLO-based person detection at the edge, demonstrating local AI processing and visual alert generation
- **LiDAR / ranging** experiments and mapping simulations support development of spatial awareness and future autonomous navigation in GPS-denied underground environments

### Audio & Rescue Assistance

- Microphone and speaker allow operator-to-rover audio interaction, local alert messages and future two-way communication with persons encountered during a rescue mission
- Combined with visual and thermal sensing, this creates additional means of assessing whether a suspected location contains a person
- Architecture is being extended toward **subsurface life-detection sensing** so that breathing or other human-presence signatures can be associated with a mapped search location

---

## Environmental Monitoring

Environmental monitoring is treated as a **core function** rather than an add-on:

- Gas and environmental measurements are acquired continuously and displayed to the surface operator in real time
- The rover creates a mobile hazard profile while exploring, helping the operator understand atmospheric changes along the travelled route
- The system is intended to log observations, sensor readings and detected events so that the explored area can be reviewed after the operation

---

## Communication Architecture

Communication is designed around **separation of functions**:

| Channel | Purpose | Bandwidth |
| :--- | :--- | :--- |
| Sub-GHz LoRa telemetry | Control, status, environmental data | Lower bandwidth |
| ESP-NOW video relay | Video and perception data | Higher bandwidth |

- The handheld surface controller acts as the operator's command and information point
- A **communication-loss safety mechanism** is incorporated so that invalid or absent control data places the rover into a controlled stop rather than allowing continued uncontrolled motion

---

## Current Status & Future Work

> **Disclaimer:** Project SETU is currently a technology-demonstration prototype and is not being claimed as a certified flameproof, intrinsically safe or DGMS-approved operational mining machine.

### Next Engineering Stage

- Completing the physical build
- Ruggedizing the electrical and mechanical systems
- Moving from development sensors to appropriately industrial and certifiable components
- Improving multi-modal sensor fusion
- Validating communication, mapping and rescue functions in representative underground facilities
- Formal certification and operational deployment through applicable mining-safety and certification processes

---

## Significance

The significance of SETU is its integration of mobility, communication, edge AI, thermal and night vision, LiDAR/ranging, atmospheric monitoring and rescue assistance in a **single field-oriented architecture**. Rather than replacing trained rescue personnel, the rover is designed to extend their reach by remotely inspecting difficult areas and providing information before direct exposure.

### Validated Capabilities

| Capability | Status |
| :--- | :--- |
| Physically developed prototype | ✅ ~65% complete |
| Real mine testing | ✅ Completed |
| Multi-terrain wireless operation | ✅ Validated |
| Third-floor-to-basement communication | ✅ Validated |
| Handheld live-video control | ✅ Validated |
| Local YOLO inference | ✅ Running on-device |
| Thermal captures | ✅ Underground mine imagery |
| Dark-environment human-detection | ✅ Trials completed |
| LiDAR / mapping work | ✅ Experiments & simulation |
| Audio communication | ✅ Hardware integrated |
| Real-time environmental monitoring | ✅ Multi-gas array active |

Project SETU establishes a practical foundation for an advanced underground emergency-response platform.

---

## Executive Summary

Project SETU is an underground mine-rescue and reconnaissance rover designed to provide remote situational awareness before human responders enter uncertain areas. It combines an articulated twin-chassis vehicle with a standalone handheld controller and integrated display.

**Core Sensing Stack:**
- Thermal imaging & NoIR / night vision
- Camera-based AI (YOLO person detection)
- LiDAR / ToF ranging
- Multi-gas and environmental monitoring
- Microphone / speaker communication
- Wireless telemetry

**Computing Architecture:**
- **Raspberry Pi** — local YOLO-based person detection at the edge
- **STM32 controller** — motor control, sensor acquisition, communications and safety logic
- Supported by simulation and mapping work for future autonomous navigation in GPS-denied underground spaces

**Prototype Validation Highlights:**
- ~65% physically complete
- Tested in a real local underground mine and mine-like environments
- Wirelessly driven across different terrains and irregular surfaces
- Communication and control tested from approximately the third floor to a basement while maintaining live video/data
- Handheld controller provides live feed, gas/environment monitoring and rover status without a laptop
- Thermal capture, night-vision observation and human-detection trials performed in dark environments
- LiDAR / ranging experiments and simulation support obstacle mapping and future localization
- Audio hardware enables rescue assistance and operator communication

**Future Direction:**
The sensing architecture is intended to combine visible detection, thermal signatures, ranging and future subsurface life-detection methods to help identify and locate trapped workers and guide rescue decisions. Future work includes completing the build, ruggedizing the system, integrating industrial/certifiable components, improving sensor fusion, strengthening communications, validating mapping and victim-search functions in representative mines, and progressing through applicable safety certification.

> **Core Aim:** Reduce unnecessary human exposure while increasing the quality and speed of information available to rescue teams. SETU provides a practical foundation for remotely inspecting underground hazards, monitoring atmospheric conditions, detecting potential human presence, mapping accessible areas and transmitting real-time intelligence to a surface operator.