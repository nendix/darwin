"""
Darwin - Utility Functions
"""

import math
from typing import Dict, List, Any


def calculate_genome_diversity(genomes: List[Any]) -> Dict[str, float]:
    """Calculate genetic diversity metrics for a population"""
    if not genomes:
        return {}
    
    # Extract all gene values
    genes = ['speed', 'vision', 'stamina']
    if hasattr(genomes[0], 'attack_strength'):
        genes.append('attack_strength')
    if hasattr(genomes[0], 'attack_resistance'):
        genes.append('attack_resistance')
    
    diversity_metrics = {}
    
    for gene in genes:
        values = [getattr(genome, gene) for genome in genomes]
        
        # Calculate standard deviation as diversity measure
        if len(values) > 1:
            import numpy as np
            diversity_metrics[f'{gene}_diversity'] = np.std(values)
            diversity_metrics[f'{gene}_mean'] = np.mean(values)
            diversity_metrics[f'{gene}_min'] = np.min(values)
            diversity_metrics[f'{gene}_max'] = np.max(values)
        else:
            diversity_metrics[f'{gene}_diversity'] = 0
            diversity_metrics[f'{gene}_mean'] = values[0] if values else 0
            diversity_metrics[f'{gene}_min'] = values[0] if values else 0
            diversity_metrics[f'{gene}_max'] = values[0] if values else 0
    
    return diversity_metrics
