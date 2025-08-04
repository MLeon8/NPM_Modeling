"""
Funciones auxiliares para manejo de datos
"""
import json
import numpy as np
from datetime import datetime
from pathlib import Path
import pickle
from itertools import product
from copy import deepcopy

class NumpyEncoder(json.JSONEncoder):
    """Encoder personalizado para tipos NumPy"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def save_results(results, run_id, params, save_path):
    """Guarda resultados en JSON con manejo robusto"""
    try:
        output = {
            'metadata': {
                'run_id': run_id,
                'timestamp': datetime.now().isoformat(),
                'params_hash': hash(json.dumps(params, sort_keys=True))
            },
            'parameters': params,
            'results': results
        }
        
        with open(save_path, 'w') as f:
            json.dump(output, f, indent=2, cls=NumpyEncoder)
            
    except Exception as e:
        raise IOError(f"No se pudo guardar {save_path}: {str(e)}")

def load_simulation(file_path):
    """Carga un archivo de simulación con validación"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Validación básica
        required_keys = {'metadata', 'parameters', 'results'}
        if not all(k in data for k in required_keys):
            raise ValueError("Estructura de archivo inválida")
            
        return data
        
    except Exception as e:
        raise IOError(f"Error cargando {file_path}: {str(e)}")

def generate_parameter_sweep(base_params, variations):
    """Genera combinaciones de parámetros con validación"""
    if not isinstance(base_params, dict) or not isinstance(variations, dict):
        raise ValueError("Los parámetros deben ser diccionarios")
    
    param_sets = []
    keys = list(variations.keys())
    values = list(variations.values())
    
    for combination in product(*values):
        params = deepcopy(base_params)
        
        # Actualización profunda de parámetros
        for key, value in zip(keys, combination):
            keys_path = key.split('.')
            current = params
            for k in keys_path[:-1]:
                current = current.setdefault(k, {})
            current[keys_path[-1]] = value
            
        param_sets.append(params)
    
    return param_sets

def save_large_data(data, file_path):
    """Guarda datos grandes en formato binario"""
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        raise IOError(f"Error guardando {file_path}: {str(e)}")

def load_large_data(file_path):
    """Carga datos grandes en formato binario"""
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        raise IOError(f"Error cargando {file_path}: {str(e)}")