# Data-Science-Projekt-Particles---Gruppe-4
Particle Life Simulator


**Course:** Data Science & AI Infrastructures (Winter 2025/26)  
**Project:** Biology-inspired algorithms - Emergent Behavior

> A high-performance, Python-based implementation of a "Particle Life" simulation. This project explores emergent complexity arising from simple, local interaction rules between agents.

---

## Project Overview

The **Particle Life Simulator** is an agent-based simulation engine designed to demonstrate how complex, organic-looking patterns (cellular structures, gliders, clusters) emerge from chaos without central orchestration.

The system simulates thousands of particles categorized into distinct types (colors). Their behavior is governed exclusively by a **forces matrix** defining attraction and repulsion rules between types within a limited radius.

**Core Inspiration:**
* [Jeffrey Ventrella's Clusters](http://www.ventrella.com/Clusters/)
* [Particle Life (Hunor Márton)](https://hunar4321.github.io/particle-life.html)

---

## Objectives & Scope

This project aims to deliver a production-grade Python application focusing on algorithmic efficiency and clean software architecture.

### 1. Core Simulation Engine
* **Interaction Matrix:** Implementation of an $N \times N$ matrix defining forces between at least **4 distinct particle types**.
* **Physics Logic:** Time-stepped calculation of velocity, friction, and acceleration based on distance thresholds ($r_{min}$, $r_{max}$).
* **Boundary Conditions:** Toroidal wrapping or reflective boundaries (implementation pending).

### 2. Performance Engineering
* **Optimization Target:** Real-time rendering of **>2,000 particles** at 60 FPS.
* **Profiling:** Continuous bottleneck analysis using `cProfile` and `timeit`.
* **Stack:** Utilization of **NumPy** for vectorized operations and potential JIT compilation via **Numba** to bypass Python interpreter overhead.

### 3. Visualization
* Real-time rendering pipeline (evaluated: `Vispy` vs `Pygame`).
* **GUI Controls:** Dynamic adjustment of interaction parameters (gravity, friction, range) during runtime.

### 4. Software Quality (QA/Ops)
* **CI/CD:** GitHub Actions pipeline for automated linting (`pylint`/`flake8`) and testing.
* **Testing Strategy:** Unit testing suite using `pytest` targeting >70% code coverage.
* **Standards:** Strict adherence to PEP-8 and Type Hinting.
