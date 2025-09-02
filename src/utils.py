"""
Darwin - Utility Functions
"""

import math
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any, Tuple


def normalize_angle(angle: float) -> float:
    """Normalize angle to be between -pi and pi"""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def distance_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate distance between two points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def angle_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate angle from point 1 to point 2"""
    return math.atan2(y2 - y1, x2 - x1)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b"""
    return a + (b - a) * t


def random_position_in_world(margin: float = 50) -> Tuple[float, float]:
    """Generate a random position within world bounds with margin"""
    from .config import WORLD_WIDTH, WORLD_HEIGHT
    x = random.uniform(margin, WORLD_WIDTH - margin)
    y = random.uniform(margin, WORLD_HEIGHT - margin)
    return x, y


def is_point_in_circle(px: float, py: float, cx: float, cy: float, radius: float) -> bool:
    """Check if point is inside a circle"""
    return distance_between_points(px, py, cx, cy) <= radius


def generate_population_graph(population_history: Dict[str, List], filename: str = None) -> str:
    """Generate and save a population graph"""
    plt.figure(figsize=(12, 8))
    
    time_points = population_history.get('time', [])
    predator_counts = population_history.get('predators', [])
    prey_counts = population_history.get('prey', [])
    
    if time_points and predator_counts and prey_counts:
        plt.plot(time_points, predator_counts, 'r-', label='Predatori', linewidth=2)
        plt.plot(time_points, prey_counts, 'b-', label='Prede', linewidth=2)
        
        plt.xlabel('Tempo (secondi)')
        plt.ylabel('Numero di Individui')
        plt.title('Andamento delle Popolazioni nel Tempo')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Set colors to match the application theme
        plt.style.use('dark_background')
        
        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()
            return filename
        else:
            plt.show()
    
    return ""


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


def format_time(seconds: float) -> str:
    """Format time in seconds to MM:SS format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def save_simulation_data(statistics: Dict[str, Any], filename: str):
    """Save simulation data to file"""
    import json
    
    # Convert numpy arrays to lists for JSON serialization
    def convert_for_json(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_for_json(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(item) for item in obj]
        else:
            return obj
    
    json_data = convert_for_json(statistics)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)


def load_simulation_data(filename: str) -> Dict[str, Any]:
    """Load simulation data from file"""
    import json
    
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


class Timer:
    """Simple timer utility"""
    
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False
    
    def start(self):
        """Start the timer"""
        import time
        self.start_time = time.time()
        self.running = True
    
    def stop(self):
        """Stop the timer"""
        if self.running:
            import time
            self.elapsed_time = time.time() - self.start_time
            self.running = False
    
    def get_elapsed(self) -> float:
        """Get elapsed time"""
        if self.running:
            import time
            return time.time() - self.start_time
        return self.elapsed_time
    
    def reset(self):
        """Reset the timer"""
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False


class PerformanceMonitor:
    """Monitor application performance"""
    
    def __init__(self):
        self.frame_times = []
        self.max_samples = 60
    
    def record_frame_time(self, frame_time: float):
        """Record a frame time"""
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)
    
    def get_average_fps(self) -> float:
        """Get average FPS"""
        if not self.frame_times:
            return 0
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0
    
    def get_frame_stats(self) -> Dict[str, float]:
        """Get detailed frame statistics"""
        if not self.frame_times:
            return {}
        
        return {
            'avg_fps': self.get_average_fps(),
            'min_frame_time': min(self.frame_times),
            'max_frame_time': max(self.frame_times),
            'avg_frame_time': sum(self.frame_times) / len(self.frame_times)
        }
