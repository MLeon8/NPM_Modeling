#!/usr/bin/env python3
"""
Script para visualizar células pro-tumorales y anti-tumorales
"""
import matplotlib.pyplot as plt
import json
import numpy as np
from pathlib import Path
import sys

# Configura paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

def load_simulation_data(file_path):
    """Carga los datos de una simulación"""
    with open(file_path) as f:
        return json.load(f)

def plot_cell_populations(data, save_path=None):
    """
    Grafica poblaciones celulares a lo largo del tiempo
    """
    results = data['results']
    
    plt.figure(figsize=(12, 6))
    
    # Gráfico de células pro-tumorales
    plt.plot(results['timesteps'], results['pro_cells'], 
            'r-', linewidth=2, label='Pro-tumorales (+1)')
    
    # Gráfico de células anti-tumorales
    plt.plot(results['timesteps'], results['anti_cells'], 
            'b-', linewidth=2, label='Anti-tumorales (-1)')
    
    plt.xlabel('Pasos de tiempo', fontsize=12)
    plt.ylabel('Número de células', fontsize=12)
    plt.title('Evolución de poblaciones celulares', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def main():
    # Busca el último archivo de resultados
    results_dir = PROJECT_ROOT / 'results' / 'simulations'
    result_files = sorted(results_dir.glob('*.json'), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not result_files:
        print("No se encontraron archivos de resultados")
        return
    
    # Carga el archivo más reciente
    latest_file = result_files[0]
    print(f"Visualizando resultados de: {latest_file.name}")
    
    data = load_simulation_data(latest_file)
    plot_cell_populations(data)

if __name__ == "__main__":
    main()