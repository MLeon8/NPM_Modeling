"""
Visualización interactiva de resultados
Generación de gráficos y animaciones
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import ipywidgets as widgets
from IPython.display import display

def interactive_explorer(results):
    """
    Interfaz interactiva para explorar resultados
    
    Args:
        results (dict): Resultados de simulación
    """
    time_slider = widgets.IntSlider(
        min=0,
        max=len(results['timesteps'])-1,
        step=1,
        value=0,
        description='Timestep'
    )
    
    organ_selector = widgets.Dropdown(
        options=list(results['metastasis_events'].keys()) + ['All'],
        value='All',
        description='Organ'
    )
    
    @widgets.interact(timestep=time_slider, organ=organ_selector)
    def update_plot(timestep, organ):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico de estado
        ax1.imshow(results['grids'][timestep], cmap='bwr', vmin=-1, vmax=1)
        ax1.set_title(f'Estado en t={timestep}')
        
        # Gráfico temporal
        ax2.plot(results['timesteps'][:timestep+1], 
                results['pro_cells'][:timestep+1], 'r-', label='Pro-tumorales')
        ax2.plot(results['timesteps'][:timestep+1], 
                results['anti_cells'][:timestep+1], 'b-', label='Anti-tumorales')
        
        # Eventos de metástasis
        if organ != 'All':
            events = [e for e in results['metastasis_events'][organ] if e['timestep'] <= timestep]
            for event in events:
                ax2.axvline(event['timestep'], color='k', linestyle='--')
        
        ax2.legend()
        ax2.set_xlabel('Timestep')
        ax2.set_ylabel('Número de células')
        plt.tight_layout()
        plt.show()

def create_animation(results, filename='animation.mp4'):
    """
    Crea animación de la simulación
    
    Args:
        results (dict): Resultados de simulación
        filename (str): Nombre del archivo de salida
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    def update(frame):
        ax.clear()
        ax.imshow(results['grids'][frame], cmap='bwr', vmin=-1, vmax=1)
        ax.set_title(f'Timestep: {frame}')
    
    ani = FuncAnimation(fig, update, frames=len(results['grids']), 
                        interval=100)
    ani.save(filename, writer='ffmpeg')
    plt.close()