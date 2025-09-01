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


def create_best_prey_genome_chart(world: World, output_dir: str = "output"):
    """Creates and saves the average prey genome evolution chart."""
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    # Extract data from world history
    generations = []
    speed_values = []
    vision_values = []
    stamina_values = []
    resistance_values = []

    for snapshot in world.history:
        if snapshot.avg_prey_genome:
            generations.append(snapshot.generation + 1)
            genome = snapshot.avg_prey_genome
            speed_values.append(genome.speed)
            vision_values.append(genome.vision)
            stamina_values.append(genome.stamina)
            resistance_values.append(genome.resistance)

    if not generations:
        return  # No data to plot

    plt.figure(figsize=(12, 8))
    
    # Create subplots for better visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Speed evolution
    ax1.plot(generations, speed_values, color='#2E8B57', linewidth=2.5, marker='o', markersize=4)
    ax1.set_title('Average Speed Evolution', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Speed', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Vision evolution
    ax2.plot(generations, vision_values, color='#4169E1', linewidth=2.5, marker='s', markersize=4)
    ax2.set_title('Average Vision Evolution', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Vision', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    # Stamina evolution
    ax3.plot(generations, stamina_values, color='#FF6347', linewidth=2.5, marker='^', markersize=4)
    ax3.set_title('Average Stamina Evolution', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Generation', fontsize=12)
    ax3.set_ylabel('Stamina', fontsize=12)
    ax3.grid(True, alpha=0.3)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    
    # Resistance evolution
    ax4.plot(generations, resistance_values, color='#9932CC', linewidth=2.5, marker='d', markersize=4)
    ax4.set_title('Average Resistance Evolution', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Generation', fontsize=12)
    ax4.set_ylabel('Resistance', fontsize=12)
    ax4.grid(True, alpha=0.3)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    
    fig.suptitle('Average Prey Genome Evolution', fontsize=16, fontweight='bold', y=0.95)
    plt.tight_layout()
    plt.savefig(out_dir / "average_prey_genome.png", dpi=200, bbox_inches="tight")
    plt.close()


def create_best_predator_genome_chart(world: World, output_dir: str = "output"):
    """Creates and saves the average predator genome evolution chart."""
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    # Extract data from world history
    generations = []
    speed_values = []
    vision_values = []
    stamina_values = []
    strength_values = []

    for snapshot in world.history:
        if snapshot.avg_pred_genome:
            generations.append(snapshot.generation + 1)
            genome = snapshot.avg_pred_genome
            speed_values.append(genome.speed)
            vision_values.append(genome.vision)
            stamina_values.append(genome.stamina)
            strength_values.append(genome.strength)

    if not generations:
        return  # No data to plot

    plt.figure(figsize=(12, 8))
    
    # Create subplots for better visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Speed evolution
    ax1.plot(generations, speed_values, color='#2E8B57', linewidth=2.5, marker='o', markersize=4)
    ax1.set_title('Average Speed Evolution', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Speed', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Vision evolution
    ax2.plot(generations, vision_values, color='#4169E1', linewidth=2.5, marker='s', markersize=4)
    ax2.set_title('Average Vision Evolution', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Vision', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    # Stamina evolution
    ax3.plot(generations, stamina_values, color='#FF6347', linewidth=2.5, marker='^', markersize=4)
    ax3.set_title('Average Stamina Evolution', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Generation', fontsize=12)
    ax3.set_ylabel('Stamina', fontsize=12)
    ax3.grid(True, alpha=0.3)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    
    # Strength evolution
    ax4.plot(generations, strength_values, color='#DC143C', linewidth=2.5, marker='d', markersize=4)
    ax4.set_title('Average Strength Evolution', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Generation', fontsize=12)
    ax4.set_ylabel('Strength', fontsize=12)
    ax4.grid(True, alpha=0.3)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    
    fig.suptitle('Average Predator Genome Evolution', fontsize=16, fontweight='bold', y=0.95)
    plt.tight_layout()
    plt.savefig(out_dir / "average_predator_genome.png", dpi=200, bbox_inches="tight")
    plt.close()


def create_genome_comparison_chart(world: World, output_dir: str = "output"):
    """Creates a comparison chart showing the final average genomes normalized."""
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    if not world.history:
        return

    # Get the final average genomes
    final_stats = world.history[-1]
    if not final_stats.avg_prey_genome or not final_stats.avg_pred_genome:
        return

    prey_genome = final_stats.avg_prey_genome
    pred_genome = final_stats.avg_pred_genome

    # Get parameter bounds for normalization
    params = world.params
    
    # Normalize prey traits (0-1 scale)
    prey_traits = {
        'Speed': (prey_genome.speed - params.speed_min) / (params.speed_max - params.speed_min),
        'Vision': (prey_genome.vision - params.vision_min) / (params.vision_max - params.vision_min),
        'Stamina': (prey_genome.stamina - params.stamina_min) / (params.stamina_max - params.stamina_min),
        'Resistance': (prey_genome.resistance - params.resist_min) / (params.resist_max - params.resist_min)
    }
    
    # Normalize predator traits (0-1 scale)
    pred_traits = {
        'Speed': (pred_genome.speed - params.speed_min) / (params.speed_max - params.speed_min),
        'Vision': (pred_genome.vision - params.vision_min) / (params.vision_max - params.vision_min),
        'Stamina': (pred_genome.stamina - params.stamina_min) / (params.stamina_max - params.stamina_min),
        'Strength': (pred_genome.strength - params.strength_min) / (params.strength_max - params.strength_min)
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Prey genome bar chart
    traits = list(prey_traits.keys())
    values = list(prey_traits.values())
    colors = ['#2E8B57', '#4169E1', '#FF6347', '#9932CC']
    
    bars1 = ax1.bar(traits, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1)
    ax1.set_title('Average Prey Genome (Final Generation)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Normalized Value (0-1)', fontsize=12)
    ax1.set_ylim(0, 1)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, value in zip(bars1, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Predator genome bar chart
    traits = list(pred_traits.keys())
    values = list(pred_traits.values())
    colors = ['#2E8B57', '#4169E1', '#FF6347', '#DC143C']
    
    bars2 = ax2.bar(traits, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1)
    ax2.set_title('Average Predator Genome (Final Generation)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Normalized Value (0-1)', fontsize=12)
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, value in zip(bars2, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(out_dir / "average_genome_comparison.png", dpi=200, bbox_inches="tight")
    plt.close()
