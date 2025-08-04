"""
Núcleo de la simulación del modelo de Ising para nichos premetastásicos
"""
import numpy as np
from numba import jit
import json
from datetime import datetime
import os

@jit(nopython=True)
def calculate_energy(grid, J, h):
    """Calcula energía total del sistema (optimizado con Numba)"""
    energy = 0.0
    size = grid.shape[0]
    for i in range(size):
        for j in range(size):
            neighbors = (grid[(i+1)%size, j] + grid[(i-1)%size, j] +
                        grid[i, (j+1)%size] + grid[i, (j-1)%size])
            energy += -J * grid[i,j] * neighbors - h * grid[i,j]
    return energy

@jit(nopython=True)
def metropolis_step(grid, J, h, beta):
    """Paso del algoritmo de Metropolis (optimizado)"""
    size = grid.shape[0]
    for _ in range(size**2):
        i, j = np.random.randint(0, size, 2)
        delta_E = 2 * grid[i,j] * (
            J * (grid[(i+1)%size,j] + grid[(i-1)%size,j] +
                grid[i,(j+1)%size] + grid[i,(j-1)%size]) + h
        )
        if delta_E < 0 or np.random.rand() < np.exp(-beta * delta_E):
            grid[i,j] *= -1
    return grid

def run_simulation(params, run_id=0):
    """Ejecuta una simulación completa con manejo de errores"""
    try:
        # Inicialización
        size = params['grid_settings']['grid_size']
        grid = np.random.choice([-1, 1], size=(size, size))
        
        # Resultados (convertidos a tipos nativos)
        results = {
            'timesteps': [],
            'pro_cells': [],
            'anti_cells': [],
            'metastasis_events': []
        }
        
        # Bucle principal
        for t in range(params['simulation_control']['timesteps']):
            # Campo externo oscilante
            h = (params['model_parameters']['h_tmb'] + 
                params['model_parameters']['h_tip'] * 
                np.sin(2*np.pi*t/params['model_parameters']['oscillation_period']))
            
            grid = metropolis_step(
                grid,
                params['model_parameters']['J'],
                h,
                params['model_parameters']['beta']
            )
            
            # Registro de resultados (convertidos a tipos nativos)
            results['timesteps'].append(int(t))
            results['pro_cells'].append(int(np.sum(grid == 1)))
            results['anti_cells'].append(int(np.sum(grid == -1)))
        
        return results
        
    except Exception as e:
        raise RuntimeError(f"Error en simulación {run_id}: {str(e)}")