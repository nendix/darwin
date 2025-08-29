from dataclasses import dataclass, asdict
import json
from pathlib import Path

CONFIG_PATH = Path("params.json")


@dataclass
class GAParams:
    population_prey: int = 40
    population_pred: int = 14
    food_count: int = 60
    world_w: int = 1500
    world_h: int = 900
    vision_min: float = 40.0
    vision_max: float = 220.0
    speed_min: float = 0.6
    speed_max: float = 3.0
    stamina_min: float = 60.0
    stamina_max: float = 240.0
    resist_min: float = 0.0  # prey: resistenza agli attacchi
    resist_max: float = 1.0
    strength_min: float = 0.2  # pred: forza degli attacchi
    strength_max: float = 1.5

    # GA hyperparams
    generations: int = 25
    steps_per_generation: int = 3000
    elitism: int = 4
    mutation_rate: float = 0.12
    mutation_std: float = 0.15
    crossover_rate: float = 0.85
    tournament_k: int = 3

    # Gameplay balance
    prey_food_energy: float = 40.0
    stamina_drain_move: float = 0.03
    stamina_recover_idle: float = 0.015
    attack_distance: float = 10.0
    kill_threshold: float = 1.0  # if pred_strength - prey_resist > 0, easier kill
    food_spawn_rate: float = 0.005  # per step probability per missing food
    prey_hunger_rate: float = 0.05  # consumo energetico per tick (prede)
    predator_hunger_rate: float = 0.1  # consumo energetico per tick (predatori)

    # Rendering / UX
    fps_limit: int = 60
    draw_vision: bool = False
    sim_speed: int = 1  # steps per frame multiplier


def default_params() -> GAParams:
    return GAParams()


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def load_params() -> GAParams:
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


def save_params(p: GAParams):
    data = asdict(p)
    CONFIG_PATH.write_text(json.dumps(data, indent=2))
