#import time
import numpy as np

import particle_life.config as config
from particle_life.simulation import ParticleSystem


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
            # time.sleep(0.01)  # optional: CPU schonen
    except KeyboardInterrupt:
        print(f"\nStopped at step {step}")


if __name__ == "__main__":
    run_console()

