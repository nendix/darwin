from pathlib import Path
import matplotlib.pyplot as plt
from .simulation import World


def make_plots(world: World):
    """
    Crea e salva i grafici della simulazione:
    - andamento delle popolazioni
    - andamento del fitness medio
    """
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    gens = [s.generation + 1 for s in world.history]
    prey_pop = [s.prey_pop for s in world.history]
    pred_pop = [s.pred_pop for s in world.history]
    prey_fit = [s.prey_fitness_avg for s in world.history]
    pred_fit = [s.pred_fitness_avg for s in world.history]

    # --- Popolazioni ---
    plt.figure(figsize=(8, 4.2))
    plt.plot(gens, prey_pop, label="Prede", color=(0.47, 0.7, 1.0))
    plt.plot(gens, pred_pop, label="Predatori", color=(0.86, 0.27, 0.27))
    plt.xlabel("Generazione")
    plt.ylabel("Popolazione")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "populations.png", dpi=150)
    plt.close()

    # --- Fitness ---
    plt.figure(figsize=(8, 4.2))
    plt.plot(gens, prey_fit, label="Prey fitness media", color=(0.47, 0.7, 1.0))
    plt.plot(gens, pred_fit, label="Predator fitness media", color=(0.86, 0.27, 0.27))
    plt.xlabel("Generazione")
    plt.ylabel("Fitness media")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "fitness.png", dpi=150)
    plt.close()
