"""
Darwin - Statistics and Report Generation
"""

import matplotlib.pyplot as plt
from typing import Dict, Any
import os


class Plotter:
    """Statistics analyzer for generating simulation reports"""

    @staticmethod
    def generate_report(statistics: Dict[str, Any], output_dir: str = "reports") -> str:
        """Generate simulation reports with three matplotlib graphs"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate all graphs (overwrites existing files)
        Plotter._create_population_graph(statistics, output_dir)
        Plotter._create_predator_genome_graph(statistics, output_dir)
        Plotter._create_prey_genome_graph(statistics, output_dir)

        # Return the output directory path
        return output_dir

    @staticmethod
    def _create_population_graph(statistics: Dict[str, Any], output_dir: str) -> str:
        """Create graph showing population trends over time"""
        pop_history = statistics.get("population_history", {})

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(12, 8))

        time_points = pop_history.get("time", [])
        predator_counts = pop_history.get("predators", [])
        prey_counts = pop_history.get("prey", [])

        if time_points and predator_counts and prey_counts:
            # Plot population lines
            ax.plot(
                time_points,
                predator_counts,
                "r-",
                label="Predatori",
                linewidth=3,
                marker="o",
                markersize=3,
            )
            ax.plot(
                time_points,
                prey_counts,
                "b-",
                label="Prede",
                linewidth=3,
                marker="s",
                markersize=3,
            )

            # Styling
            ax.set_xlabel("Tempo (secondi)", fontsize=14)
            ax.set_ylabel("Numero di Individui", fontsize=14)
            ax.set_title(
                "Andamento delle Popolazioni nel Tempo",
                fontsize=16,
                fontweight="bold",
                color="white",
            )
            ax.legend(fontsize=12)
            ax.grid(True, alpha=0.3)

            # Set colors
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
        else:
            ax.text(
                0.5,
                0.5,
                "Dati popolazione non disponibili",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=16,
                color="white",
            )

        graph_path = os.path.join(output_dir, "population.png")
        plt.savefig(graph_path, dpi=150, bbox_inches="tight", facecolor="#1a1a1a")
        plt.close()

        return graph_path

    @staticmethod
    def _create_predator_genome_graph(
        statistics: Dict[str, Any], output_dir: str
    ) -> str:
        """Create bar chart showing average predator genome traits"""
        genome_stats = statistics.get("genome_statistics", {})
        predator_stats = genome_stats.get("predators", {})

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(10, 6))

        if predator_stats:
            traits = ["Velocità", "Visione", "Stamina", "Forza Attacco"]
            values = [
                predator_stats.get("speed", 0),
                predator_stats.get("vision", 0),
                predator_stats.get("stamina", 0),
                predator_stats.get("attack_strength", 0),
            ]

            bars = ax.bar(
                traits,
                values,
                color=["#ff6b6b", "#ff8787", "#ffa8a8", "#ffc9c9"],
                edgecolor="white",
                linewidth=1.5,
            )

            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + 1,
                    f"{value:.1f}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    color="white",
                )

            ax.set_ylim(0, 100)
            ax.set_ylabel("Valore Medio", fontsize=14, color="white")
            ax.set_title(
                "Genoma Medio dei Predatori",
                fontsize=16,
                fontweight="bold",
                color="white",
            )
            ax.tick_params(colors="white")
            ax.grid(True, alpha=0.3, axis="y")
        else:
            ax.text(
                0.5,
                0.5,
                "Dati genoma predatori non disponibili",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=16,
                color="white",
            )

        graph_path = os.path.join(output_dir, "predator.png")
        plt.savefig(graph_path, dpi=150, bbox_inches="tight", facecolor="#1a1a1a")
        plt.close()

        return graph_path

    @staticmethod
    def _create_prey_genome_graph(statistics: Dict[str, Any], output_dir: str) -> str:
        """Create bar chart showing average prey genome traits"""
        genome_stats = statistics.get("genome_statistics", {})
        prey_stats = genome_stats.get("prey", {})

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(10, 6))

        if prey_stats:
            traits = ["Velocità", "Visione", "Stamina", "Resistenza"]
            values = [
                prey_stats.get("speed", 0),
                prey_stats.get("vision", 0),
                prey_stats.get("stamina", 0),
                prey_stats.get("attack_resistance", 0),
            ]

            bars = ax.bar(
                traits,
                values,
                color=["#4dabf7", "#74c0fc", "#a5d8ff", "#d0ebff"],
                edgecolor="white",
                linewidth=1.5,
            )

            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + 1,
                    f"{value:.1f}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    color="white",
                )

            ax.set_ylim(0, 100)
            ax.set_ylabel("Valore Medio", fontsize=14, color="white")
            ax.set_title(
                "Genoma Medio delle Prede",
                fontsize=16,
                fontweight="bold",
                color="white",
            )
            ax.tick_params(colors="white")
            ax.grid(True, alpha=0.3, axis="y")
        else:
            ax.text(
                0.5,
                0.5,
                "Dati genoma prede non disponibili",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=16,
                color="white",
            )

        graph_path = os.path.join(output_dir, "prey.png")
        plt.savefig(graph_path, dpi=150, bbox_inches="tight", facecolor="#1a1a1a")
        plt.close()

        return graph_path
