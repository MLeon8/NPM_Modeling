"""
Funciones auxiliares para manejo de datos y utilidades
"""

import json
import numpy as np
from datetime import datetime
import os

def save_results(results, run_id, params, save_path):
    """
    Guarda resultados de simulación en formato JSON
    
    Args:
        results (dict): Resultados a guardar
        run_id (int): ID de la corrida
        params (dict): Parámetros de simulación
        save_path (Path): Ruta completa del archivo de salida
    """
    output = {
        'parameters': params,
        'results': results,
        'metadata': {
            'run_id': run_id,
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
        }
    }
    
    with open(save_path, 'w') as f:
        json.dump(output, f, indent=2)

def load_results(pattern="data/simulation_*.json"):
    """
    Carga múltiples resultados de simulaciones
    
    Args:
        pattern (str): Patrón para buscar archivos
        
    Returns:
        list: Lista de resultados cargados
    """
    import glob
    files = glob.glob(pattern)
    results = []
    
    for file in files:
        with open(file) as f:
            data = json.load(f)
            results.append(data)
    
    return results

def generate_parameter_sweep(base_params, variations):
    """
    Genera múltiples conjuntos de parámetros para barridos
    
    Args:
        base_params (dict): Parámetros base
        variations (dict): Variaciones a aplicar
        
    Returns:
        list: Lista de configuraciones de parámetros
    """
    param_sets = []
    
    # Ejemplo: variations = {'J': [0.5, 0.8, 1.0], 'beta': [0.3, 0.5]}
    from itertools import product
    keys = variations.keys()
    values = variations.values()
    
    for combination in product(*values):
        params = base_params.copy()
        for key, value in zip(keys, combination):
            params[key] = value
        param_sets.append(params)
    
    return param_sets
    

    
