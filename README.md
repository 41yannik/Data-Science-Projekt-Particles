# Data-Science-Projekt-Particles---Gruppe-4
Particle Life Simulator


**Course:** Data Science & AI Infrastructures (Winter 2025/26)  
**Project:** Biology-inspired algorithms - Emergent Behavior

> A high-performance, Python-based implementation of a "Particle Life" simulation. This project explores emergent complexity arising from simple, local interaction rules between agents.

---

## 📖 Project Overview

The **Particle Life Simulator** is an agent-based simulation engine designed to demonstrate how complex, organic-looking patterns (cellular structures, gliders, clusters) emerge from chaos without central orchestration.

The system simulates thousands of particles categorized into distinct types (colors). Their behavior is governed exclusively by a **forces matrix** defining attraction and repulsion rules between types within a limited radius.

**Core Inspiration:**
* [Jeffrey Ventrella's Clusters](http://www.ventrella.com/Clusters/)
* [Particle Life (Hunor Márton)](https://hunar4321.github.io/particle-life.html)

---

## Objectives & Scope

This project aims to deliver a production-grade Python application focusing on algorithmic efficiency and clean software architecture.

### 1. Core Simulation Engine
* [cite_start]**Interaction Matrix:** Implementation of an $N \times N$ matrix defining forces between at least **4 distinct particle types**[cite: 36].
* [cite_start]**Physics Logic:** Time-stepped calculation of velocity, friction, and acceleration based on distance thresholds ($r_{min}$, $r_{max}$)[cite: 33, 38, 39].
* **Boundary Conditions:** Toroidal wrapping or reflective boundaries (implementation pending).

### 2. Performance Engineering
* [cite_start]**Optimization Target:** Real-time rendering of **>2,000 particles** at 60 FPS[cite: 40].
* [cite_start]**Profiling:** Continuous bottleneck analysis using `cProfile` and `timeit`[cite: 57].
* [cite_start]**Stack:** Utilization of **NumPy** for vectorized operations and potential JIT compilation via **Numba** to bypass Python interpreter overhead[cite: 59, 102].

### 3. Visualization
* [cite_start]Real-time rendering pipeline (evaluated: `Vispy` vs `Pygame`)[cite: 106, 111].
* [cite_start]**GUI Controls:** Dynamic adjustment of interaction parameters (gravity, friction, range) during runtime[cite: 42].

### 4. Software Quality (QA/Ops)
* [cite_start]**CI/CD:** GitHub Actions pipeline for automated linting (`pylint`/`flake8`) and testing[cite: 49].
* [cite_start]**Testing Strategy:** Unit testing suite using `pytest` targeting >70% code coverage[cite: 48].
* **Standards:** Strict adherence to PEP-8 and Type Hinting.
