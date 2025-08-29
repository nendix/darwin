import random
from typing import List
from .genetics import (
    PreyGenome,
    PredatorGenome,
    random_prey,
    random_pred,
    crossover_prey,
    crossover_pred,
    mutate_prey,
    mutate_pred,
    tournament_select,
)
from .entities import Prey, Predator, Food
from .utils import rand_pos
from dataclasses import dataclass, field


@dataclass
class Stats:
    generation: int = 0
    prey_pop: int = 0
    pred_pop: int = 0
    prey_fitness_avg: float = 0.0
    pred_fitness_avg: float = 0.0


@dataclass
class World:
    params: any
    preys: List[Prey] = field(default_factory=list)
    predators: List[Predator] = field(default_factory=list)
    foods: List[Food] = field(default_factory=list)
    time: int = 0
    generation: int = 0

    # logging
    history: List[Stats] = field(default_factory=list)
    prey_genomes: List[PreyGenome] = field(default_factory=list)
    pred_genomes: List[PredatorGenome] = field(default_factory=list)

    def reset_population(self, prey_genomes=None, pred_genomes=None):
        W, H = self.params.world_w, self.params.world_h
        self.preys = []
        self.predators = []
        self.foods = [Food(rand_pos(W, H)) for _ in range(self.params.food_count)]
        self.time = 0

        if prey_genomes is None:
            prey_genomes = [
                random_prey(self.params) for _ in range(self.params.population_prey)
            ]
        if pred_genomes is None:
            pred_genomes = [
                random_pred(self.params) for _ in range(self.params.population_pred)
            ]

        for g in prey_genomes:
            x, y = rand_pos(W, H)
            self.preys.append(Prey(x, y, dna=g, energy=g.stamina * 0.7))
        for g in pred_genomes:
            x, y = rand_pos(W, H)
            self.predators.append(Predator(x, y, dna=g, energy=g.stamina * 0.7))

    def spawn_food_if_needed(self):
        target = self.params.food_count
        if len(
            self.foods
        ) < target and random.random() < self.params.food_spawn_rate * (
            target - len(self.foods)
        ):
            self.foods.append(Food(rand_pos(self.params.world_w, self.params.world_h)))

    def step(self):
        self.time += 1
        # predators move first to give slight advantage
        for pr in self.predators:
            if pr.alive:
                pr.step(
                    self.params.world_w, self.params.world_h, self.preys, self.params
                )
        for py in self.preys:
            if py.alive:
                py.step(
                    self.params.world_w,
                    self.params.world_h,
                    self.foods,
                    self.predators,
                    self.params,
                )

        # remove corpses
        self.preys = [p for p in self.preys if p.alive]
        self.predators = [p for p in self.predators if p.alive]

        # environment
        self.spawn_food_if_needed()

    def prey_fitness(self, p: Prey) -> float:
        # Fitness: survive longer + eat more food + distance kept from predators (implicit via survival)
        return (
            p.age * 0.2
            + p.food_eaten * 10.0
            + (p.energy / max(1.0, p.dna.stamina)) * 2.0
        )

    def pred_fitness(self, p: Predator) -> float:
        # Fitness: kills + survival + some efficiency via energy left
        return p.kills * 15.0 + p.age * 0.1 + (p.energy / max(1.0, p.dna.stamina)) * 3.0

    def end_generation(self):
        # compute fitness arrays
        prey_fit = [self.prey_fitness(p) for p in self.preys]
        pred_fit = [self.pred_fitness(p) for p in self.predators]

        # if population extinct, give small placeholders to avoid zero-length issues
        if not prey_fit:
            prey_fit = [0.01]
        if not pred_fit:
            pred_fit = [0.01]

        # genomes of survivors (or empty)
        prey_source = [p.dna for p in self.preys] or [random_prey(self.params)]
        pred_source = [p.dna for p in self.predators] or [random_pred(self.params)]

        # sort by fitness
        # Prey
        prey_pairs = list(zip(prey_source, prey_fit))
        prey_pairs.sort(key=lambda x: x[1], reverse=True)
        prey_sorted = [g for g, f in prey_pairs]
        prey_fit_sorted = [f for g, f in prey_pairs]

        # Predator
        pred_pairs = list(zip(pred_source, pred_fit))
        pred_pairs.sort(key=lambda x: x[1], reverse=True)
        pred_sorted = [g for g, f in pred_pairs]
        pred_fit_sorted = [f for g, f in pred_pairs]

        # log stats
        self.history.append(
            Stats(
                generation=self.generation,
                prey_pop=len(self.preys),
                pred_pop=len(self.predators),
                prey_fitness_avg=sum(prey_fit_sorted) / len(prey_fit_sorted),
                pred_fitness_avg=sum(pred_fit_sorted) / len(pred_fit_sorted),
            )
        )

        # build next generation using GA: elitism + tournament + crossover + mutation
        next_prey = []
        next_pred = []

        # ELITISM
        elite_prey = prey_sorted[: min(self.params.elitism, len(prey_sorted))]
        elite_pred = pred_sorted[: min(self.params.elitism, len(pred_sorted))]
        next_prey.extend(elite_prey)
        next_pred.extend(elite_pred)

        # fill rest
        while len(next_prey) < self.params.population_prey:
            p1 = tournament_select(
                prey_sorted, prey_fit_sorted, self.params.tournament_k
            )
            p2 = tournament_select(
                prey_sorted, prey_fit_sorted, self.params.tournament_k
            )
            child = crossover_prey(p1, p2, self.params.crossover_rate)
            child = mutate_prey(child, self.params)
            next_prey.append(child)

        while len(next_pred) < self.params.population_pred:
            a = tournament_select(
                pred_sorted, pred_fit_sorted, self.params.tournament_k
            )
            b = tournament_select(
                pred_sorted, pred_fit_sorted, self.params.tournament_k
            )
            child = crossover_pred(a, b, self.params.crossover_rate)
            child = mutate_pred(child, self.params)
            next_pred.append(child)

        self.prey_genomes = next_prey
        self.pred_genomes = next_pred

    def new_generation(self):
        self.generation += 1
        self.reset_population(self.prey_genomes, self.pred_genomes)
