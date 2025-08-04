#!/usr/bin/env python3
"""
Script para ejecución paralela de múltiples simulaciones con diferentes parámetros
"""
import sys
import os
from pathlib import Path

# Configuración crítica - Añade el directorio src al path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

# Importaciones absolutas desde src
from src.simulation import run_simulation
from src.utils import save_results, generate_parameter_sweep

import argparse
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

def load_parameters(config_file):
    """Carga y valida parámetros de configuración"""
    with open(config_file) as f:
        params = json.load(f)
    
    # Validación básica
    assert params['grid_settings']['grid_size'] > 10, "Grid size too small"
    assert 0 < params['model_parameters']['J'] < 2, "J out of range"
    assert 0 < params['model_parameters']['beta'] < 3, "Beta out of range"
    
    return params

def worker(params, run_id):
    """Función que ejecuta una simulación individual"""
    print(f"Iniciando simulación {run_id} con J={params['model_parameters']['J']}, beta={params['model_parameters']['beta']}")
    try:
        results = run_simulation(params, run_id)
        return {'run_id': run_id, 'status': 'completed', 'results': results}
    except Exception as e:
        return {'run_id': run_id, 'status': 'failed', 'error': str(e)}

def main():
    parser = argparse.ArgumentParser(description='Ejecución paralela de simulaciones de nicho premetastásico')
    parser.add_argument('--num_workers', type=int, default=4, 
                       help='Número de procesos paralelos')
    parser.add_argument('--config', type=str, default='config/parameters.json',
                       help='Archivo de configuración JSON')
    args = parser.parse_args()

    # Cargar parámetros base
    config_path = PROJECT_ROOT / args.config
    base_params = load_parameters(config_path)
    
    # Generar variaciones de parámetros
    param_variations = {
        'model_parameters.J': [0.5, 0.8, 1.0, 1.2],
        'model_parameters.beta': [0.3, 0.5, 0.7]
    }
    
    # Preparar directorios de salida
    output_dir = PROJECT_ROOT / base_params['output_settings']['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    
    if base_params['simulation_control']['save_frames']:
        frames_dir = PROJECT_ROOT / base_params['simulation_control']['frames_dir']
        os.makedirs(frames_dir, exist_ok=True)

    # Generar todas las combinaciones de parámetros
    param_sets = generate_parameter_sweep(base_params, param_variations)
    
    print(f"⚡ Iniciando {len(param_sets)} simulaciones con {args.num_workers} workers...")
    start_time = datetime.now()
    
    # Ejecución paralela
    with ProcessPoolExecutor(max_workers=args.num_workers) as executor:
        futures = {executor.submit(worker, params, i): i 
                  for i, params in enumerate(param_sets)}
        
        completed = 0
        for future in as_completed(futures):
            run_id = futures[future]
            result = future.result()
            
            if result['status'] == 'completed':
                print(f"✅ Simulación {run_id} completada")
                save_path = output_dir / f"simulation_{run_id}.json"
                save_results(result['results'], run_id, param_sets[run_id], save_path)
                completed += 1
            else:
                print(f"❌ Error en simulación {run_id}: {result['error']}")
    
    # Reporte final
    duration = (datetime.now() - start_time).total_seconds()
    print(f"\n🎉 Todas las simulaciones finalizadas")
    print(f"   - Simulaciones exitosas: {completed}/{len(param_sets)}")
    print(f"   - Tiempo total: {duration:.2f} segundos")
    print(f"   - Tiempo promedio por simulación: {duration/len(param_sets):.2f} segundos")

if __name__ == "__main__":
    main()