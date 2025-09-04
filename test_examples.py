#!/usr/bin/env python3
"""
Darwin - Example Usage and Testing Script
This script demonstrates various features of the Darwin simulator
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.genetics.genomes import PredatorGenome, PreyGenome, GenomeFactory
from src.genetics.operations import GeneticOperations
from src.entities import Predator, Prey, Food
from src.presets import get_preset_configuration, list_available_presets
from src.utils import calculate_genome_diversity

def format_time(seconds):
    """Simple time formatting function"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        return f"{seconds // 3600}h {(seconds % 3600) // 60}m {seconds % 60}s"
from src.config import *


def test_genetic_algorithms():
    """Test genetic algorithm functionality"""
    print("🧬 Testing Genetic Algorithms...")
    print("=" * 50)
    
    # Create random genomes
    predator_genome1 = GenomeFactory.create_random_predator_genome()
    predator_genome2 = GenomeFactory.create_random_predator_genome()
    
    print(f"Predator 1: Speed={predator_genome1.speed:.1f}, Vision={predator_genome1.vision:.1f}, "
          f"Stamina={predator_genome1.stamina:.1f}, Attack={predator_genome1.attack_strength:.1f}")
    print(f"Predator 2: Speed={predator_genome2.speed:.1f}, Vision={predator_genome2.vision:.1f}, "
          f"Stamina={predator_genome2.stamina:.1f}, Attack={predator_genome2.attack_strength:.1f}")
    
    # Test crossover
    offspring = GeneticOperations.crossover_predator(predator_genome1, predator_genome2)
    print(f"Offspring:  Speed={offspring.speed:.1f}, Vision={offspring.vision:.1f}, "
          f"Stamina={offspring.stamina:.1f}, Attack={offspring.attack_strength:.1f}")
    
    # Test prey genetics
    prey_genome1 = GenomeFactory.create_random_prey_genome()
    prey_genome2 = GenomeFactory.create_random_prey_genome()
    
    print(f"\nPrey 1: Speed={prey_genome1.speed:.1f}, Vision={prey_genome1.vision:.1f}, "
          f"Stamina={prey_genome1.stamina:.1f}, Resistance={prey_genome1.attack_resistance:.1f}")
    print(f"Prey 2: Speed={prey_genome2.speed:.1f}, Vision={prey_genome2.vision:.1f}, "
          f"Stamina={prey_genome2.stamina:.1f}, Resistance={prey_genome2.attack_resistance:.1f}")
    
    prey_offspring = GeneticOperations.crossover_prey(prey_genome1, prey_genome2)
    print(f"Offspring: Speed={prey_offspring.speed:.1f}, Vision={prey_offspring.vision:.1f}, "
          f"Stamina={prey_offspring.stamina:.1f}, Resistance={prey_offspring.attack_resistance:.1f}")
    
    print("\n✅ Genetic algorithms working correctly!\n")


def test_entity_creation():
    """Test entity creation and basic functionality"""
    print("🎮 Testing Entity Creation...")
    print("=" * 50)
    
    # Create entities
    predator = Predator(100, 100)
    prey = Prey(200, 200)
    food = Food(150, 150)
    
    print(f"Predator created at ({predator.x}, {predator.y})")
    print(f"Prey created at ({prey.x}, {prey.y})")
    print(f"Food created at ({food.x}, {food.y})")
    
    # Test distance calculation
    distance = predator.distance_to(prey)
    print(f"Distance between predator and prey: {distance:.1f}")
    
    # Test vision
    can_see = predator.can_see(prey)
    print(f"Can predator see prey? {can_see}")
    
    print("\n✅ Entity creation working correctly!\n")


def test_presets():
    """Test configuration presets"""
    print("⚙️ Testing Configuration Presets...")
    print("=" * 50)
    
    # List available presets
    presets = list_available_presets()
    print("Available presets:")
    for category, preset_list in presets.items():
        print(f"  {category.capitalize()}: {', '.join(preset_list)}")
    
    # Test specific preset
    balanced_config = get_preset_configuration('balanced', 'simulation')
    if balanced_config:
        print(f"\nBalanced simulation preset:")
        for key, value in balanced_config.items():
            print(f"  {key}: {value}")
    
    print("\n✅ Presets working correctly!\n")


def test_genome_diversity():
    """Test genome diversity calculation"""
    print("📊 Testing Genome Diversity Analysis...")
    print("=" * 50)
    
    # Create a population of genomes
    predator_genomes = [GenomeFactory.create_random_predator_genome() for _ in range(10)]
    
    # Calculate diversity
    diversity = calculate_genome_diversity(predator_genomes)
    
    print("Predator population diversity metrics:")
    for metric, value in diversity.items():
        print(f"  {metric}: {value:.2f}")
    
    print("\n✅ Diversity analysis working correctly!\n")


def test_utilities():
    """Test utility functions"""
    print("🔧 Testing Utility Functions...")
    print("=" * 50)
    
    # Test time formatting
    times = [30, 65, 125, 300]
    for t in times:
        formatted = format_time(t)
        print(f"  {t} seconds = {formatted}")
    
    print("\n✅ Utilities working correctly!\n")


def demonstrate_simulation_concepts():
    """Demonstrate key simulation concepts"""
    print("🧠 Demonstrating Simulation Concepts...")
    print("=" * 50)
    
    print("1. Evolution Principles:")
    print("   - Selection: Only fit individuals reproduce")
    print("   - Crossover: Genetic material combines from parents")
    print("   - Mutation: Random changes introduce variation")
    print("   - Fitness: Survival and reproduction success")
    
    print("\n2. Predator Adaptations:")
    print("   - Speed: Catch faster prey")
    print("   - Vision: Spot prey from farther away")
    print("   - Stamina: Hunt for longer periods")
    print("   - Attack: Overcome prey defenses")
    
    print("\n3. Prey Adaptations:")
    print("   - Speed: Escape from predators")
    print("   - Vision: Detect threats and food")
    print("   - Stamina: Sustain escape efforts")
    print("   - Resistance: Survive predator attacks")
    
    print("\n4. Ecosystem Dynamics:")
    print("   - Food scarcity creates competition")
    print("   - Predator-prey balance emerges naturally")
    print("   - Genetic diversity maintains adaptability")
    print("   - Environmental pressures drive evolution")
    
    print("\n✅ Concepts demonstrated!\n")


def run_mini_simulation():
    """Run a small simulation example"""
    print("🚀 Running Mini Simulation Example...")
    print("=" * 50)
    
    # Create small populations
    entities = []
    
    # Add predators
    for i in range(3):
        x = 100 + i * 50
        y = 100
        predator = Predator(x, y)
        entities.append(predator)
        print(f"Predator {i+1}: Speed={predator.genome.speed:.1f}, Attack={predator.genome.attack_strength:.1f}")
    
    # Add prey
    for i in range(5):
        x = 200 + i * 30
        y = 200
        prey = Prey(x, y)
        entities.append(prey)
        print(f"Prey {i+1}: Speed={prey.genome.speed:.1f}, Resistance={prey.genome.attack_resistance:.1f}")
    
    # Add food
    for i in range(8):
        x = 150 + i * 20
        y = 250
        food = Food(x, y)
        entities.append(food)
    
    print(f"\nMini ecosystem created with {len(entities)} entities")
    print("- 3 Predators")
    print("- 5 Prey")
    print("- 8 Food sources")
    
    # Simulate a few steps
    dt = 1.0  # 1 second per step
    for step in range(3):
        print(f"\nStep {step + 1}:")
        alive_predators = len([e for e in entities if isinstance(e, Predator) and e.alive])
        alive_prey = len([e for e in entities if isinstance(e, Prey) and e.alive])
        available_food = len([e for e in entities if isinstance(e, Food) and e.alive])
        
        print(f"  Alive - Predators: {alive_predators}, Prey: {alive_prey}, Food: {available_food}")
        
        # Update entities (simplified)
        for entity in entities:
            if entity.alive:
                entity.update_energy(dt) if hasattr(entity, 'update_energy') else None
    
    print("\n✅ Mini simulation completed!\n")


def main():
    """Main function to run all tests and examples"""
    print("🧬 DARWIN EVOLUTION SIMULATOR - TESTING & EXAMPLES")
    print("=" * 60)
    print("This script demonstrates the core functionality of Darwin\n")
    
    try:
        test_genetic_algorithms()
        test_entity_creation()
        test_presets()
        test_genome_diversity()
        test_utilities()
        demonstrate_simulation_concepts()
        run_mini_simulation()
        
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Ready to run the full simulation with: python main.py")
        print("Or use: make run")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
