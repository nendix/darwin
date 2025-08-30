from dataclasses import dataclass, asdict
import json
from pathlib import Path

CONFIG_PATH = Path("params.json")


@dataclass
class Params:
    # World
    world_w: int = 1000
    world_h: int = 700

    # Population
    population_prey: int = 40
    population_pred: int = 14
    food_count: int = 60

    # DNA bounds
    speed_min: float = 0.6
    speed_max: float = 3.0

    vision_min: float = 40.0
    vision_max: float = 220.0

    stamina_min: float = 40.0
    stamina_max: float = 240.0  # Note: stamina is DNA -> max energy

    resist_min: float = 0.0
    resist_max: float = 1.0

    strength_min: float = 0.2
    strength_max: float = 1.5

    # Simulation / GA
    generations: int = 25
    steps_per_generation: int = 2000
    elitism: int = 1
    mutation_rate: float = 0.12
    mutation_std: float = 0.12
    crossover_rate: float = 0.85
    tournament_k: int = 3

    # Energetics & movement
    prey_hunger_rate: float = 0.03  # energy lost per tick (baseline)
    predator_hunger_rate: float = 0.06
    stamina_drain_move: float = 0.03  # energy cost per move action (scaled)
    prey_food_energy: float = 40.0  # energy gained eating food
    predator_food_energy: float = 60.0  # energy gained eating prey
    attack_distance: float = 10.0

    # Rendering / UX
    fps_limit: int = 60
    draw_vision: bool = False
    sim_speed: int = 1  # steps per frame


def default_params() -> Params:
    return Params()


def load_params() -> Params:
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text())
            p = default_params()
            for k, v in data.items():
                if hasattr(p, k):
                    setattr(p, k, v)
            return p
        except Exception:
            return default_params()
    return default_params()


def save_params(p: Params):
    CONFIG_PATH.write_text(json.dumps(asdict(p), indent=2))
