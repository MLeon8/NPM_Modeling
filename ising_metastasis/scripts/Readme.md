Cómo ejecutar

    Configuración inicial:

bash

mkdir -p config results/simulations results/frames logs

    Ejecución estándar (usando 4 núcleos):

bash

python scripts/run_parallel.py --num_workers 4

    Ejecución con configuración personalizada:

bash

python scripts/run_parallel.py --config config/custom_params.json --num_workers 8

Parámetros clave para variar

Para explorar diferentes escenarios, modifica en parameters.json:

    Parámetros físicos:

json

"model_parameters": {
    "J": [0.5, 0.8, 1.2],       # Fuerza de interacción celular
    "beta": [0.3, 0.5, 0.7],     # Inverso de temperatura (aleatoriedad)
    "h_tip": [0.5, 0.8, 1.0]     # Intensidad de oscilación
}

    Metástasis:

json

"metastasis_settings": {
    "organs": {
        "Liver": {"probability": [0.02, 0.03, 0.04]},
        "Lung": {"probability": [0.01, 0.02, 0.03]}
    }
}

    Resolución:

json

"grid_settings": {
    "grid_size": [100, 200, 300]  # Tamaños de red a probar
}

El script run_parallel.py automáticamente generará todas las combinaciones de parámetros y ejecutará las simulaciones en paralelo, mostrando progreso y guardando resultados estructurados.