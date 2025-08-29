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
    energy: float = 100.0  # also used as stamina pool
    age: int = 0

    def pos(self):
        return (self.x, self.y)


@dataclass
class Prey(BaseAgent):
    dna: PreyGenome = field(default_factory=lambda: PreyGenome(1, 1, 1, 0))
    food_eaten: int = 0

    def step(self, w, h, foods, predators, params):
        if not self.alive:
            return

        self.age += 1

        # consumo costante di energia (fame)
        self.energy -= params.prey_hunger_rate
        if self.energy <= 0:
            self.alive = False
            return

        # stamina dynamics
        self.energy = clamp(
            self.energy + params.stamina_recover_idle, 0.0, self.dna.stamina
        )

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
        # flee if predator near
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
                # movimento casuale se nessun predatore o cibo
                ax += random.uniform(-0.5, 0.5)
                ay += random.uniform(-0.5, 0.5)

        # apply movement based on speed and stamina
        speed = self.dna.speed
        if self.energy > 1.0 and (ax != 0 or ay != 0):
            self.energy = clamp(
                self.energy - params.stamina_drain_move, 0.0, self.dna.stamina
            )
            self.vx += ax * 0.5 * speed
            self.vy += ay * 0.5 * speed
        else:
            # slight damping if exhausted
            self.vx *= 0.95
            self.vy *= 0.95

        # clamp velocity
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
            self.energy = clamp(
                self.energy + params.prey_food_energy, 0.0, self.dna.stamina
            )


@dataclass
class Predator(BaseAgent):
    dna: PredatorGenome = field(default_factory=lambda: PredatorGenome(1, 1, 1, 1))
    kills: int = 0

    def step(self, w, h, preys, params):
        if not self.alive:
            return

        self.age += 1

        # consumo costante di energia (fame)
        self.energy -= params.predator_hunger_rate
        if self.energy <= 0:
            self.alive = False
            return

        # stamina dynamics
        self.energy = clamp(
            self.energy + params.stamina_recover_idle * 0.7, 0.0, self.dna.stamina
        )

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
            # movimento casuale se nessuna preda visibile
            ax += random.uniform(-0.5, 0.5)
            ay += random.uniform(-0.5, 0.5)

        speed = self.dna.speed
        if self.energy > 1.0 and (ax != 0 or ay != 0):
            self.energy = clamp(
                self.energy - params.stamina_drain_move * 1.2, 0.0, self.dna.stamina
            )
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
            # success chance depends on strength vs resistance
            advantage = self.dna.strength - target.dna.resistance
            base = 0.35 + max(0.0, advantage) * 0.35
            base = clamp(base, 0.05, 0.95)
            if random.random() < base:
                target.alive = False
                self.kills += 1
                self.energy = clamp(self.energy + 20.0, 0.0, self.dna.stamina)
