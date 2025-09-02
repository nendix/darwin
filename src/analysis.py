"""
Darwin - Advanced Statistics and Visualization
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Dict, List, Any, Tuple
import os
from datetime import datetime

from .utils import calculate_genome_diversity


class StatisticsAnalyzer:
    """Advanced statistics analyzer for simulation data"""
    
    @staticmethod
    def analyze_evolution_trends(statistics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze evolution trends over time"""
        genome_stats = statistics.get('genome_statistics', {})
        
        analysis = {
            'predator_trends': {},
            'prey_trends': {},
            'diversity_metrics': {},
            'fitness_evolution': {}
        }
        
        # Analyze predator evolution
        if 'predators' in genome_stats:
            pred_stats = genome_stats['predators']
            analysis['predator_trends'] = {
                'speed_dominance': pred_stats.get('speed', 0) > 70,
                'vision_specialization': pred_stats.get('vision', 0) > 80,
                'attack_efficiency': pred_stats.get('attack_strength', 0) > 75,
                'balanced_evolution': all(50 <= pred_stats.get(trait, 0) <= 80 
                                        for trait in ['speed', 'vision', 'stamina', 'attack_strength'])
            }
        
        # Analyze prey evolution
        if 'prey' in genome_stats:
            prey_stats = genome_stats['prey']
            analysis['prey_trends'] = {
                'speed_adaptation': prey_stats.get('speed', 0) > 70,
                'vision_enhancement': prey_stats.get('vision', 0) > 80,
                'defense_specialization': prey_stats.get('attack_resistance', 0) > 75,
                'survival_balance': all(50 <= prey_stats.get(trait, 0) <= 80 
                                      for trait in ['speed', 'vision', 'stamina', 'attack_resistance'])
            }
        
        return analysis
    
    @staticmethod
    def generate_comprehensive_report(statistics: Dict[str, Any], output_dir: str = "reports") -> str:
        """Generate a comprehensive HTML report"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(output_dir, f"darwin_report_{timestamp}.html")
        
        # Create population graphs
        pop_graph = StatisticsAnalyzer._create_population_graph(statistics, output_dir, timestamp)
        genome_graph = StatisticsAnalyzer._create_genome_evolution_graph(statistics, output_dir, timestamp)
        
        # Generate HTML report
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Darwin Simulation Report - {timestamp}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #1a1a1a; color: #ffffff; }}
                .header {{ text-align: center; color: #4CAF50; }}
                .section {{ margin: 30px 0; padding: 20px; background-color: #2a2a2a; border-radius: 8px; }}
                .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
                .stat-box {{ background-color: #3a3a3a; padding: 15px; border-radius: 5px; text-align: center; }}
                .predator {{ color: #dc4646; }}
                .prey {{ color: #78b4ff; }}
                .food {{ color: #46c876; }}
                img {{ max-width: 100%; height: auto; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🧬 Darwin Evolution Simulator - Report</h1>
                <p>Simulazione completata il {datetime.now().strftime("%d/%m/%Y alle %H:%M:%S")}</p>
            </div>
            
            {StatisticsAnalyzer._generate_simulation_summary_html(statistics)}
            {StatisticsAnalyzer._generate_population_analysis_html(statistics, pop_graph)}
            {StatisticsAnalyzer._generate_genome_analysis_html(statistics, genome_graph)}
            {StatisticsAnalyzer._generate_evolution_trends_html(statistics)}
            
            <div class="section">
                <h2>📊 Grafici della Simulazione</h2>
                <div style="text-align: center;">
                    <h3>Andamento Popolazioni</h3>
                    <img src="{os.path.basename(pop_graph)}" alt="Population Graph">
                    <h3>Evoluzione Genomi</h3>
                    <img src="{os.path.basename(genome_graph)}" alt="Genome Evolution Graph">
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_file
    
    @staticmethod
    def _generate_simulation_summary_html(statistics: Dict[str, Any]) -> str:
        """Generate simulation summary HTML section"""
        params = statistics.get('simulation_params', {})
        final_pops = statistics.get('final_populations', {})
        
        return f"""
        <div class="section">
            <h2>📋 Riassunto Simulazione</h2>
            <div class="stat-grid">
                <div class="stat-box">
                    <h3>Durata</h3>
                    <p>{params.get('duration', 0)} secondi</p>
                </div>
                <div class="stat-box">
                    <h3>Velocità</h3>
                    <p>{params.get('speed', 1)}x</p>
                </div>
                <div class="stat-box predator">
                    <h3>Predatori Finali</h3>
                    <p>{final_pops.get('predators', 0)}</p>
                </div>
                <div class="stat-box prey">
                    <h3>Prede Finali</h3>
                    <p>{final_pops.get('prey', 0)}</p>
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def _generate_population_analysis_html(statistics: Dict[str, Any], graph_path: str) -> str:
        """Generate population analysis HTML section"""
        survival_stats = statistics.get('survival_stats', {})
        
        return f"""
        <div class="section">
            <h2>👥 Analisi Popolazioni</h2>
            <div class="stat-grid">
                <div class="stat-box predator">
                    <h3>Sopravvivenza Predatori</h3>
                    <p>{survival_stats.get('predator_survival_rate', 0):.1f}%</p>
                </div>
                <div class="stat-box prey">
                    <h3>Sopravvivenza Prede</h3>
                    <p>{survival_stats.get('prey_survival_rate', 0):.1f}%</p>
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def _generate_genome_analysis_html(statistics: Dict[str, Any], graph_path: str) -> str:
        """Generate genome analysis HTML section"""
        genome_stats = statistics.get('genome_statistics', {})
        
        predator_html = ""
        prey_html = ""
        
        if 'predators' in genome_stats:
            pred = genome_stats['predators']
            predator_html = f"""
            <div class="stat-box predator">
                <h3>Genoma Predatori</h3>
                <p>Velocità: {pred.get('speed', 0):.1f}</p>
                <p>Visione: {pred.get('vision', 0):.1f}</p>
                <p>Stamina: {pred.get('stamina', 0):.1f}</p>
                <p>Forza Attacco: {pred.get('attack_strength', 0):.1f}</p>
            </div>
            """
        
        if 'prey' in genome_stats:
            prey = genome_stats['prey']
            prey_html = f"""
            <div class="stat-box prey">
                <h3>Genoma Prede</h3>
                <p>Velocità: {prey.get('speed', 0):.1f}</p>
                <p>Visione: {prey.get('vision', 0):.1f}</p>
                <p>Stamina: {prey.get('stamina', 0):.1f}</p>
                <p>Resistenza: {prey.get('attack_resistance', 0):.1f}</p>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2>🧬 Analisi Genomi</h2>
            <div class="stat-grid">
                {predator_html}
                {prey_html}
            </div>
        </div>
        """
    
    @staticmethod
    def _generate_evolution_trends_html(statistics: Dict[str, Any]) -> str:
        """Generate evolution trends HTML section"""
        evolution_info = statistics.get('evolution_info', {})
        
        return f"""
        <div class="section">
            <h2>📈 Tendenze Evolutive</h2>
            <div class="stat-grid">
                <div class="stat-box">
                    <h3>Riproduzioni Totali</h3>
                    <p>{evolution_info.get('total_reproductions', 0)}</p>
                </div>
                <div class="stat-box">
                    <h3>Mutazioni Totali</h3>
                    <p>{evolution_info.get('total_mutations', 0)}</p>
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def _create_population_graph(statistics: Dict[str, Any], output_dir: str, timestamp: str) -> str:
        """Create population evolution graph"""
        pop_history = statistics.get('population_history', {})
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 8))
        
        time_points = pop_history.get('time', [])
        predator_counts = pop_history.get('predators', [])
        prey_counts = pop_history.get('prey', [])
        
        if time_points and predator_counts and prey_counts:
            ax.plot(time_points, predator_counts, 'r-', label='Predatori', linewidth=3, marker='o', markersize=4)
            ax.plot(time_points, prey_counts, 'b-', label='Prede', linewidth=3, marker='s', markersize=4)
            
            ax.set_xlabel('Tempo (secondi)', fontsize=14)
            ax.set_ylabel('Numero di Individui', fontsize=14)
            ax.set_title('Evoluzione delle Popolazioni nel Tempo', fontsize=16, fontweight='bold')
            ax.legend(fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # Add annotations for interesting points
            if predator_counts:
                max_pred_idx = predator_counts.index(max(predator_counts))
                ax.annotate(f'Max Predatori: {max(predator_counts)}', 
                           xy=(time_points[max_pred_idx], max(predator_counts)),
                           xytext=(10, 10), textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.3),
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
            
            if prey_counts:
                max_prey_idx = prey_counts.index(max(prey_counts))
                ax.annotate(f'Max Prede: {max(prey_counts)}', 
                           xy=(time_points[max_prey_idx], max(prey_counts)),
                           xytext=(10, -20), textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='blue', alpha=0.3),
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        graph_path = os.path.join(output_dir, f"population_graph_{timestamp}.png")
        plt.savefig(graph_path, dpi=150, bbox_inches='tight', facecolor='#1a1a1a')
        plt.close()
        
        return graph_path
    
    @staticmethod
    def _create_genome_evolution_graph(statistics: Dict[str, Any], output_dir: str, timestamp: str) -> str:
        """Create genome evolution comparison graph"""
        genome_stats = statistics.get('genome_statistics', {})
        
        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Predator genome radar chart
        if 'predators' in genome_stats:
            pred_stats = genome_stats['predators']
            traits = ['Velocità', 'Visione', 'Stamina', 'Forza Attacco']
            values = [pred_stats.get('speed', 0), pred_stats.get('vision', 0), 
                     pred_stats.get('stamina', 0), pred_stats.get('attack_strength', 0)]
            
            StatisticsAnalyzer._create_radar_chart(ax1, traits, values, 'Genoma Predatori', 'red')
        
        # Prey genome radar chart
        if 'prey' in genome_stats:
            prey_stats = genome_stats['prey']
            traits = ['Velocità', 'Visione', 'Stamina', 'Resistenza']
            values = [prey_stats.get('speed', 0), prey_stats.get('vision', 0), 
                     prey_stats.get('stamina', 0), prey_stats.get('attack_resistance', 0)]
            
            StatisticsAnalyzer._create_radar_chart(ax2, traits, values, 'Genoma Prede', 'blue')
        
        plt.tight_layout()
        graph_path = os.path.join(output_dir, f"genome_evolution_{timestamp}.png")
        plt.savefig(graph_path, dpi=150, bbox_inches='tight', facecolor='#1a1a1a')
        plt.close()
        
        return graph_path
    
    @staticmethod
    def _create_radar_chart(ax, traits, values, title, color):
        """Create a radar chart for genome visualization"""
        N = len(traits)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        values += values[:1]  # Complete the circle
        
        ax.plot(angles, values, 'o-', linewidth=2, label=title, color=color)
        ax.fill(angles, values, alpha=0.25, color=color)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(traits)
        ax.set_ylim(0, 100)
        ax.set_title(title, size=14, fontweight='bold')
        ax.grid(True)
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
