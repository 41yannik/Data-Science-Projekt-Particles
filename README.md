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

##  Software Architecture

The system is designed with a clear separation of concerns, orchestrated by a central controller (`main.py`) which manages the flow between configuration, simulation logic, and visualization.

```mermaid
graph TD
    A[Main Controller (main.py)] --> B[Configuration & Rules (config.py)]
    A --> C[Simulation Engine (simulation.py)]
    A --> D[Visualization / GUI (viewer.py)]

    B -- Provides Data --> C
    C -- Provides State --> D

    subgraph Configuration & Rules
        B_sub1(Colors)
        B_sub2(Interaction Matrix)
    end

    subgraph Simulation Engine
        C_sub1(Particles Class)
        C_sub2(Update Loop (NumPy))
    end

    subgraph Visualization / GUI
        D_sub1(Vispy / Pygame)
        D_sub2(Draw Particles)
    end
```

### Module Breakdown:

* **Main Controller (`main.py`):** Serves as the primary orchestrator, initializing the other modules and managing the main program loop.
* **Configuration & Rules (`config.py`):** Responsible for loading and holding all static parameters of the simulation, including particle `Colors` and the crucial `Interaction Matrix` that defines inter-particle forces.
* **Simulation Engine (`simulation.py`):** This is the core logic unit. It contains the `Particles Class` (managing particle states like position and velocity) and executes the high-performance `Update Loop`, leveraging **NumPy** for efficient vectorized calculations of particle physics. It receives configuration data and computes the next state of the particles.
* **Visualization / GUI (`viewer.py`):** Handles the graphical representation of the simulation. It utilizes a chosen rendering library (`Vispy` or `Pygame`) to `Draw Particles` based on the current state provided by the Simulation Engine. It also provides `GUI` elements for dynamic parameter adjustments.

---

## Roadmap

  * **[x] Milestone 1 (19.11.2025):** Project Setup, Architecture Design, CI Pipeline.
  * **[ ] Milestone 2 (17.12.2025):** Core Logic Implementation (Physics & Interaction Matrix).
  * **[ ] Milestone 3 (17.12.2025):** Real-time Visualization & Parameter Tuning.
  * **[ ] Milestone 4 (TBA):** Performance Optimization (>2000 particles).
  * **[ ] Milestone 5 (25.02.2026):** Final Release, Documentation & Presentation.

---

##  Local Development Setup

### Prerequisites

  * Python 3.10+
  * Git

### Installation

```bash
# 1. Clone the repository
git clone [https://github.com/YOUR-ORG/particle-life.git](https://github.com/YOUR-ORG/particle-life.git)
cd particle-life

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Running the Simulation

```bash
python src/main.py
```

---

##  Team

  * **Arian Sharifi-Tabar**
  * **Yannik Huber**
  * **Wayan Schmidt**
  * **Azad Aygün**
