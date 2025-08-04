"""
Visualización interactiva de resultados
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import ipywidgets as widgets
from IPython.display import display
from pathlib import Path

try:
    from src.utils import load_simulation
except ModuleNotFoundError:
    from utils import load_simulation

def plot_time_series(results, save_path=None):
    """Genera gráfico de series temporales"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(results['timesteps'], results['pro_cells'], 
           'r-', label='Células pro-tumorales')
    ax.plot(results['timesteps'], results['anti_cells'], 
           'b-', label='Células anti-tumorales')
    
    ax.set_xlabel('Paso de tiempo')
    ax.set_ylabel('Número de células')
    ax.legend()
    ax.grid(True)
    ax.set_title('Evolución temporal de poblaciones celulares')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def interactive_results_viewer(results_dir):
    """Interfaz interactiva para explorar múltiples simulaciones"""
    results_files = list(Path(results_dir).glob('*.json'))
    
    if not results_files:
        print("No se encontraron archivos de resultados")
        return
    
    run_selector = widgets.Dropdown(
        options=[(f.name, f) for f in results_files],
        description='Simulación:'
    )
    
    def update_plot(selected_file):
        try:
            data = load_simulation(selected_file)
            plot_time_series(data['results'])
        except Exception as e:
            print(f"Error cargando {selected_file}: {str(e)}")
    
    widgets.interact(update_plot, selected_file=run_selector)

def create_comparison_plot(result_files, save_path=None):
    """Compara múltiples simulaciones en un gráfico"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for file in result_files:
        try:
            data = load_simulation(file)
            label = f"Run {data['metadata']['run_id']}"
            ax.plot(data['results']['timesteps'], 
                   data['results']['pro_cells'], 
                   label=label, alpha=0.7)
        except Exception as e:
            print(f"Error procesando {file}: {str(e)}")
    
    ax.set_xlabel('Paso de tiempo')
    ax.set_ylabel('Células pro-tumorales')
    ax.legend()
    ax.grid(True)
    ax.set_title('Comparación de simulaciones')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def terminal_plot(results_dir):
    """Visualización básica en terminal"""
    import glob
    import json
    import matplotlib.pyplot as plt
    
    files = glob.glob(f"{results_dir}/*.json")
    if not files:
        print("No se encontraron resultados")
        return
    
    plt.figure(figsize=(10, 6))
    for file in files[:5]:  # Mostrar máximo 5 simulaciones
        with open(file) as f:
            data = json.load(f)
        plt.plot(data['results']['timesteps'], 
                data['results']['pro_cells'],
                label=f"Run {data['metadata']['run_id']}")
    
    plt.xlabel('Timesteps')
    plt.ylabel('Células pro-tumorales')
    plt.legend()
    plt.grid(True)
    plt.title('Resultados de simulaciones')
    plt.show()    

def interactive_cell_plot(results_dir='results/simulations'):
    """Visualización interactiva con controles"""
    from ipywidgets import interact, IntSlider
    import glob
    
    files = glob.glob(f"{results_dir}/*.json")
    if not files:
        print("No se encontraron archivos de resultados")
        return
    
    # Cargar todos los datos
    all_data = []
    for file in files:
        with open(file) as f:
            all_data.append(json.load(f))
    
    @interact
    def show_plot(run_id=(0, len(all_data)-1), 
                 show_pro=True, 
                 show_anti=True,
                 log_scale=False):
        data = all_data[run_id]
        plt.figure(figsize=(12, 6))
        
        if show_pro:
            plt.plot(data['results']['timesteps'], 
                    data['results']['pro_cells'], 
                    'r-', label='Pro-tumorales')
        if show_anti:
            plt.plot(data['results']['timesteps'], 
                    data['results']['anti_cells'], 
                    'b-', label='Anti-tumorales')
        
        plt.xlabel('Pasos de tiempo')
        plt.ylabel('Número de células')
        plt.title(f'Simulación {run_id}')
        if log_scale:
            plt.yscale('log')
        plt.legend()
        plt.grid(True)
        plt.show()