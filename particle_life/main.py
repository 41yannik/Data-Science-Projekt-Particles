import sys

import numpy as np

import particle_life.config as config
from particle_life.simulation import ParticleSystem
from particle_life.viewer import run as run_viewer


def run_console() -> None:
    if config.SEED is not None:
        np.random.seed(config.SEED)

    sim = ParticleSystem()
    step = 0

    try:
        while True:
            sim.update(config.DT)
            if step % 10 == 0:
                pos = sim.get_positions()
                mean = pos.mean(axis=0)
                first5 = pos[:5].round(2).tolist()
                print(
                    f"step={step} "
                    f"mean=({mean[0]:.2f},{mean[1]:.2f}) "
                    f"first5={first5}"
                )
            step += 1
    except KeyboardInterrupt:
        print(f"\nStopped at step {step}")


def main() -> None:
    mode = "console"

    if "--mode" in sys.argv:
        index = sys.argv.index("--mode")
        if index + 1 < len(sys.argv):
            mode = sys.argv[index + 1]

    if mode == "viewer":
        run_viewer()
    else:
        run_console()


if __name__ == "__main__":
    main()

