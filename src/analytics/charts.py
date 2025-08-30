"""
Analytics and visualization module for Darwin simulation.
Handles creation and saving of population, fitness, and genome analysis charts.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from ..simulation import World


def create_population_chart(world: World, output_dir: str = "output"):
    """Creates and saves the population trends chart."""
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    # Extract data from world history
    generations = [snapshot.generation + 1 for snapshot in world.history]
    prey_populations = [snapshot.prey_pop for snapshot in world.history]
    predator_populations = [snapshot.pred_pop for snapshot in world.history]

    plt.figure(figsize=(10, 6))
    plt.plot(
        generations,
        prey_populations,
        label="Prede",
        color=(0.47, 0.7, 1.0),
        linewidth=2.5,
        marker="o",
        markersize=4,
    )
    plt.plot(
        generations,
        predator_populations,
        label="Predatori",
        color=(0.86, 0.27, 0.27),
        linewidth=2.5,
        marker="s",
        markersize=4,
    )

    plt.xlabel("Generazione", fontsize=14)
    plt.ylabel("Popolazione", fontsize=14)
    plt.title(
        "Andamento delle Popolazioni nel Tempo", fontsize=16, fontweight="bold", pad=20
    )
    plt.legend(fontsize=12, frameon=True, fancybox=True, shadow=True)
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()

    # Add some styling
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.savefig(out_dir / "population_trends.png", dpi=200, bbox_inches="tight")
    plt.close()


def create_fitness_chart(world: World, output_dir: str = "output"):
    """Creates and saves the fitness trends chart."""
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    # Extract data from world history
    generations = [snapshot.generation + 1 for snapshot in world.history]
    prey_fitness = [snapshot.prey_fitness_avg for snapshot in world.history]
    predator_fitness = [snapshot.pred_fitness_avg for snapshot in world.history]

    plt.figure(figsize=(10, 6))
    plt.plot(
        generations,
        prey_fitness,
        label="Fitness Medio Prede",
        color=(0.47, 0.7, 1.0),
        linewidth=2.5,
        marker="o",
        markersize=4,
    )
    plt.plot(
        generations,
        predator_fitness,
        label="Fitness Medio Predatori",
        color=(0.86, 0.27, 0.27),
        linewidth=2.5,
        marker="s",
        markersize=4,
    )

    plt.xlabel("Generazione", fontsize=14)
    plt.ylabel("Fitness Medio", fontsize=14)
    plt.title("Evoluzione del Fitness Medio", fontsize=16, fontweight="bold", pad=20)
    plt.legend(fontsize=12, frameon=True, fancybox=True, shadow=True)
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()

    # Add some styling
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.savefig(out_dir / "fitness_evolution.png", dpi=200, bbox_inches="tight")
    plt.close()
