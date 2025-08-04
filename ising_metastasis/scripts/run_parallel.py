#!/usr/bin/env python3
"""
Script para ejecución paralela de múltiples simulaciones con diferentes parámetros
"""
import sys
import os
from pathlib import Path
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
import traceback

# Configura paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.simulation import run_simulation
from src.utils import save_results, generate_parameter_sweep

def worker(params, run_id):
    """Función que ejecuta una simulación individual"""
    try:
        print(f"▶ Iniciando simulación {run_id}")
        results = run_simulation(params, run_id)
        return {
            'run_id': run_id,
            'results': results,
            'status': 'success',
            'error': None
        }
    except Exception as e:
        return {
            'run_id': run_id,
            'results': None,
            'status': 'failed',
            'error': f"{str(e)}\n{traceback.format_exc()}"
        }

def main():
    # Configuración de argumentos
    parser = argparse.ArgumentParser(description='Ejecución paralela de simulaciones')
    parser.add_argument('--num_workers', type=int, default=4, 
                       help='Número de procesos paralelos')
    parser.add_argument('--config', type=str, default='config/parameters.json',
                       help='Archivo de configuración JSON')
    args = parser.parse_args()

    # Carga y validación de parámetros
    try:
        with open(PROJECT_ROOT/args.config) as f:
            base_params = json.load(f)
        
        # Validaciones adicionales
        assert base_params['grid_settings']['grid_size'] > 10, "Grid size too small"
        assert 0 < base_params['model_parameters']['J'] < 2, "J out of range"
    except Exception as e:
        print(f"❌ Error en configuración: {str(e)}")
        sys.exit(1)

    # Preparar directorios de salida
    output_dir = PROJECT_ROOT/'results/simulations'
    os.makedirs(output_dir, exist_ok=True)

    # Generar combinaciones de parámetros
    param_variations = {
        'model_parameters.J': [0.5, 0.8, 1.0, 1.2],
        'model_parameters.beta': [0.3, 0.5, 0.7]
    }
    param_sets = generate_parameter_sweep(base_params, param_variations)

    print(f"🚀 Iniciando {len(param_sets)} simulaciones con {args.num_workers} workers...")
    start_time = datetime.now()

    # Ejecución paralela
    with ProcessPoolExecutor(max_workers=args.num_workers) as executor:
        futures = {executor.submit(worker, params, i): i 
                 for i, params in enumerate(param_sets)}
        
        success_count = 0
        for future in as_completed(futures):
            result = future.result()
            run_id = futures[future]
            
            if result['status'] == 'success':
                save_path = output_dir/f"sim_{result['run_id']}.json"
                save_results(result['results'], result['run_id'], param_sets[run_id], save_path)
                print(f"✅ Simulación {run_id} completada y guardada en {save_path}")
                success_count += 1
            else:
                print(f"❌ Error en simulación {run_id}:\n{result['error']}")
    
    # Reporte final
    duration = (datetime.now() - start_time).total_seconds()
    print(f"\n🎉 Resultados:")
    print(f"   - Simulaciones exitosas: {success_count}/{len(param_sets)}")
    print(f"   - Tiempo total: {duration:.2f} segundos")
    print(f"   - Tiempo promedio: {duration/len(param_sets):.2f} seg/simulación")

if __name__ == "__main__":
    import argparse
    main()