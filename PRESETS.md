# Darwin AI - Configuration Presets

This document contains all the predefined configuration presets for the Darwin evolution simulator.

## Simulation Presets

### Balanced
A well-balanced ecosystem for standard evolution experiments.
```
Prey Count: 30
Predator Count: 10
Food Count: 60
Duration: 180 seconds
Speed: 3x
Show Vision: False
```

### Predator Dominance
Higher predator population to test prey survival strategies.
```
Prey Count: 50
Predator Count: 20
Food Count: 80
Duration: 240 seconds
Speed: 4x
Show Vision: True
```

### Survival Challenge
Limited food resources create intense competition.
```
Prey Count: 80
Predator Count: 30
Food Count: 40 (Limited food)
Duration: 300 seconds
Speed: 5x
Show Vision: False
```

### Rapid Evolution
Fast-paced simulation with abundant resources for quick evolution.
```
Prey Count: 100
Predator Count: 40
Food Count: 200
Duration: 120 seconds
Speed: 8x
Show Vision: True
```

### Minimal Ecosystem
Small population for detailed observation of individual behaviors.
```
Prey Count: 10
Predator Count: 4
Food Count: 20
Duration: 90 seconds
Speed: 2x
Show Vision: True
```

## Genome Presets

### Speed Focused
Emphasizes speed over other traits.
```
Speed Bias: 1.5x
Vision Bias: 1.0x
Stamina Bias: 0.8x
Special Bias: 1.2x
```

### Vision Focused
Prioritizes vision capabilities for better awareness.
```
Speed Bias: 0.8x
Vision Bias: 1.8x
Stamina Bias: 1.0x
Special Bias: 1.1x
```

### Balanced Genes
Equal emphasis on all genetic traits.
```
Speed Bias: 1.0x
Vision Bias: 1.0x
Stamina Bias: 1.0x
Special Bias: 1.0x
```

### Extreme Specialization
Creates highly specialized individuals with extreme trait differences.
```
Speed Bias: 2.0x
Vision Bias: 0.5x
Stamina Bias: 0.3x
Special Bias: 2.5x
```

## Environment Presets

### Harsh
Challenging environment with higher energy costs and mutation rates.
```
Energy Decay Multiplier: 1.5x
Food Spawn Rate: 0.7x
Reproduction Threshold: 150
Mutation Rate: 15%
```

### Normal
Standard environment conditions for typical simulations.
```
Energy Decay Multiplier: 1.0x
Food Spawn Rate: 1.0x
Reproduction Threshold: 100
Mutation Rate: 10%
```

### Abundant
Resource-rich environment with easier survival conditions.
```
Energy Decay Multiplier: 0.7x
Food Spawn Rate: 1.5x
Reproduction Threshold: 80
Mutation Rate: 8%
```

### Chaotic
Unpredictable environment with high mutation rates.
```
Energy Decay Multiplier: 1.2x
Food Spawn Rate: 0.9x
Reproduction Threshold: 120
Mutation Rate: 25%
```

## Usage Notes

These presets were originally implemented as Python dictionaries but have been moved to documentation to simplify the codebase. The Darwin AI system now uses its pure ALife approach without preset dependencies.

### How to Apply These Settings

1. **Simulation Settings**: Adjust population counts and simulation parameters in the UI
2. **Genome Settings**: Modify the `GenomeFactory` random generation ranges if needed
3. **Environment Settings**: Update configuration values in `config.py`

### Experimental Recommendations

- **Start with Balanced** for first-time users
- **Use Minimal Ecosystem** for detailed behavioral analysis
- **Try Survival Challenge** to observe adaptation under pressure
- **Experiment with Rapid Evolution** for quick results
- **Use Harsh environment** to test evolutionary resilience

---

*Note: These presets serve as guidelines. The beauty of the ALife system is that interesting behaviors emerge naturally from any reasonable starting configuration.*
