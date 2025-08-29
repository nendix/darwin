from dataclasses import dataclass, field
import random
from typing import Tuple, Optional
from .utils import dist, normalize, wrap, clamp
from .genetics import PreyGenome, PredatorGenome


@dataclass
class Food:
    pos: Tuple[float, float]


@dataclass
class BaseAgent:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    alive: bool = True
    energy: float = 100.0  # current energy (decreases with time and movement)
    age: int = 0

    def pos(self):
        return (self.x, self.y)

    def tick_energy(self, base_rate: float) -> bool:
        """Consume base energy per tick. Return True if still alive."""
        if not self.alive:
            return False
        self.age += 1
        self.energy -= base_rate
        if self.energy <= 0:
            self.alive = False
            return False
        return True

    def consume_for_move(self, amount: float):
        """Consume energy for movement; may kill the agent if energy hits 0."""
        self.energy = clamp(self.energy - amount, 0.0, self.energy)
        if self.energy <= 0:
            self.alive = False

    def gain_energy(self, amount: float, max_energy: float):
        self.energy = clamp(self.energy + amount, 0.0, max_energy)


@dataclass
class Prey(BaseAgent):
    dna: PreyGenome = field(default_factory=lambda: PreyGenome(1, 1, 1, 0))
    food_eaten: int = 0

    def step(self, w, h, foods, predators, params):
        if not self.tick_energy(params.prey_hunger_rate):
            return

        # dna.stamina is the maximum energy this agent can have
        max_energy = self.dna.stamina

        # detect nearest predator
        nearest_pred = None
        dmin = self.dna.vision
        for pr in predators:
            if not pr.alive:
                continue
            d = dist(self.pos(), pr.pos())
            if d < dmin:
                dmin = d
                nearest_pred = pr

        ax, ay = 0.0, 0.0
        if nearest_pred:
            dx = self.x - nearest_pred.x
            dy = self.y - nearest_pred.y
            nx, ny = normalize(dx, dy)
            ax += nx
            ay += ny
        else:
            # seek nearest food
            nearest_food = None
            dminf = 1e9
            for f in foods:
                d = dist(self.pos(), f.pos)
                if d < dminf:
                    dminf = d
                    nearest_food = f
            if nearest_food:
                dx = nearest_food.pos[0] - self.x
                dy = nearest_food.pos[1] - self.y
                nx, ny = normalize(dx, dy)
                ax += nx
                ay += ny
            else:
                # random wandering (never stay still)
                ax += random.uniform(-0.5, 0.5)
                ay += random.uniform(-0.5, 0.5)

        # movement consumes energy (use dna.speed and global drain param)
        speed = self.dna.speed
        if (ax != 0 or ay != 0) and self.energy > 1.0:
            move_cost = params.stamina_drain_move  # per-step cost
            # scale cost by speed (faster costs more) and normalized factor
            self.consume_for_move(move_cost * (0.5 + 0.5 * speed))
            self.vx += ax * 0.5 * speed
            self.vy += ay * 0.5 * speed
        else:
            self.vx *= 0.95
            self.vy *= 0.95

        # clamp speed by dna.speed
        vmax = max(0.3, speed)
        self.vx = clamp(self.vx, -vmax, vmax)
        self.vy = clamp(self.vy, -vmax, vmax)

        self.x += self.vx
        self.y += self.vy
        self.x, self.y = wrap(self.x, self.y, w, h)

        # eat food if close
        eaten = None
        for i, f in enumerate(foods):
            if dist(self.pos(), f.pos) < 8.0:
                eaten = i
                break
        if eaten is not None:
            foods.pop(eaten)
            self.food_eaten += 1
            self.gain_energy(params.prey_food_energy, max_energy)


@dataclass
class Predator(BaseAgent):
    dna: PredatorGenome = field(default_factory=lambda: PredatorGenome(1, 1, 1, 1))
    kills: int = 0

    def step(self, w, h, preys, params):
        if not self.tick_energy(params.predator_hunger_rate):
            return

        max_energy = self.dna.stamina

        # seek nearest prey
        target: Optional[Prey] = None
        dmin = self.dna.vision
        for pr in preys:
            if not pr.alive:
                continue
            d = dist(self.pos(), pr.pos())
            if d < dmin:
                dmin = d
                target = pr

        ax, ay = 0.0, 0.0
        if target:
            dx = target.x - self.x
            dy = target.y - self.y
            nx, ny = normalize(dx, dy)
            ax += nx
            ay += ny
        else:
            # random wandering if no prey
            ax += random.uniform(-0.5, 0.5)
            ay += random.uniform(-0.5, 0.5)

        speed = self.dna.speed
        if (ax != 0 or ay != 0) and self.energy > 1.0:
            move_cost = params.stamina_drain_move * 1.2
            self.consume_for_move(move_cost * (0.5 + 0.5 * speed))
            self.vx += ax * 0.6 * speed
            self.vy += ay * 0.6 * speed
        else:
            self.vx *= 0.95
            self.vy *= 0.95

        vmax = max(0.3, speed)
        self.vx = clamp(self.vx, -vmax, vmax)
        self.vy = clamp(self.vy, -vmax, vmax)

        self.x += self.vx
        self.y += self.vy
        self.x, self.y = wrap(self.x, self.y, w, h)

        # attack if close
        if target and dist(self.pos(), target.pos()) < params.attack_distance:
            advantage = self.dna.strength - target.dna.resistance
            base = 0.35 + max(0.0, advantage) * 0.35
            base = clamp(base, 0.05, 0.95)
            if random.random() < base:
                target.alive = False
                self.kills += 1
                self.gain_energy(params.predator_food_energy, max_energy)
