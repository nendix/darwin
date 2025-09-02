"""
Darwin - Example Configuration and Presets
"""

from src.config import *

# Predefined simulation presets
SIMULATION_PRESETS = {
    'balanced': {
        'prey_count': 30,
        'predator_count': 10,
        'food_count': 60,
        'duration': 180,
        'speed': 3,
        'show_vision': False
    },
    
    'predator_dominance': {
        'prey_count': 50,
        'predator_count': 20,
        'food_count': 80,
        'duration': 240,
        'speed': 4,
        'show_vision': True
    },
    
    'survival_challenge': {
        'prey_count': 80,
        'predator_count': 30,
        'food_count': 40,  # Limited food
        'duration': 300,
        'speed': 5,
        'show_vision': False
    },
    
    'rapid_evolution': {
        'prey_count': 100,
        'predator_count': 40,
        'food_count': 200,
        'duration': 120,
        'speed': 8,
        'show_vision': True
    },
    
    'minimal_ecosystem': {
        'prey_count': 10,
        'predator_count': 4,
        'food_count': 20,
        'duration': 90,
        'speed': 2,
        'show_vision': True
    }
}

# Advanced genome configurations for special scenarios
GENOME_PRESETS = {
    'speed_focused': {
        'speed_bias': 1.5,
        'vision_bias': 1.0,
        'stamina_bias': 0.8,
        'special_bias': 1.2
    },
    
    'vision_focused': {
        'speed_bias': 0.8,
        'vision_bias': 1.8,
        'stamina_bias': 1.0,
        'special_bias': 1.1
    },
    
    'balanced_genes': {
        'speed_bias': 1.0,
        'vision_bias': 1.0,
        'stamina_bias': 1.0,
        'special_bias': 1.0
    },
    
    'extreme_specialization': {
        'speed_bias': 2.0,
        'vision_bias': 0.5,
        'stamina_bias': 0.3,
        'special_bias': 2.5
    }
}

# Environment configuration presets
ENVIRONMENT_PRESETS = {
    'harsh': {
        'energy_decay_multiplier': 1.5,
        'food_spawn_rate': 0.7,
        'reproduction_threshold': 150,
        'mutation_rate': 0.15
    },
    
    'normal': {
        'energy_decay_multiplier': 1.0,
        'food_spawn_rate': 1.0,
        'reproduction_threshold': 100,
        'mutation_rate': 0.1
    },
    
    'abundant': {
        'energy_decay_multiplier': 0.7,
        'food_spawn_rate': 1.5,
        'reproduction_threshold': 80,
        'mutation_rate': 0.08
    },
    
    'chaotic': {
        'energy_decay_multiplier': 1.2,
        'food_spawn_rate': 0.9,
        'reproduction_threshold': 120,
        'mutation_rate': 0.25
    }
}

def get_preset_configuration(preset_name: str, category: str = 'simulation'):
    """Get a predefined configuration preset"""
    presets = {
        'simulation': SIMULATION_PRESETS,
        'genome': GENOME_PRESETS,
        'environment': ENVIRONMENT_PRESETS
    }
    
    if category in presets and preset_name in presets[category]:
        return presets[category][preset_name].copy()
    
    return None

def list_available_presets():
    """List all available presets"""
    return {
        'simulation': list(SIMULATION_PRESETS.keys()),
        'genome': list(GENOME_PRESETS.keys()),
        'environment': list(ENVIRONMENT_PRESETS.keys())
    }
