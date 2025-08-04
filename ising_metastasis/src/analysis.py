"""
Análisis estadístico de resultados de simulaciones
Incluye cálculo de promedios, correlaciones y métricas
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

def calculate_averages(results_list):
    """
    Calcula promedios sobre múltiples simulaciones
    
    Args:
        results_list (list): Lista de resultados de simulaciones
        
    Returns:
        dict: Promedios y desviaciones estándar
    """
    avg_results = {
        'time': results_list[0]['timesteps'],
        'mean_pro': np.mean([r['pro_cells'] for r in results_list], axis=0),
        'std_pro': np.std([r['pro_cells'] for r in results_list], axis=0),
        'mean_anti': np.mean([r['anti_cells'] for r in results_list], axis=0),
        'std_anti': np.std([r['anti_cells'] for r in results_list], axis=0)
    }
    return avg_results

def analyze_metastasis_patterns(results_list, params):
    """
    Analiza patrones de aparición de metástasis
    
    Args:
        results_list (list): Lista de resultados
        params (dict): Parámetros de simulación
        
    Returns:
        pd.DataFrame: Estadísticas por órgano
    """
    organs = params['metastasis_organs'].keys()
    data = []
    
    for organ in organs:
        times = []
        for result in results_list:
            events = [e for e in result['metastasis_events'] if e['organ'] == organ]
            if events:
                times.append(events[0]['timestep'])
        
        if times:
            data.append({
                'Organ': organ,
                'Mean_Time': np.mean(times),
                'Std_Time': np.std(times),
                'Probability': params['metastasis_organs'][organ]
            })
    
    return pd.DataFrame(data)

def spatial_correlation(grid):
    """
    Calcula función de correlación espacial
    
    Args:
        grid (np.array): Matriz de estados celulares
        
    Returns:
        np.array: Función de correlación
    """
    ft = np.fft.fft2(grid)
    acf = np.fft.ifft2(ft * np.conj(ft)).real
    return acf / acf[0,0]