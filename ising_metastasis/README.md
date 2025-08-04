# Modelado del Nicho Premetastásico con Modelo de Ising

Este proyecto implementa un modelo computacional basado en el modelo de Ising para estudiar la formación de nichos premetastásicos en cáncer.

## Requisitos

- Python 3.8+
- Bibliotecas: NumPy, Matplotlib, Numba, Pandas, Scipy
- Opcional: Jupyter para notebooks interactivos

Instalar dependencias:
```bash
pip install -r requirements.txt

Parámetros Clave
Parámetro		Descripción					Valores típicos
grid_size		Tamaño de la red				50-200
J			Constante de acoplamiento			0.1-1.5
beta			Inverso de temperatura				0.1-2.0
h_tmb			Campo microambiental basal			0.1-0.5
h_tip			Amplitud de oscilación				0.5-1.0
metastasis_organs	Probabilidades por órgano			{"Hígado": 0.03, ...}



## Explicación del Flujo

1. **Configuración inicial**: Se definen todos los parámetros en `parameters.json`
2. **Simulación**: 
   - `simulation.py` ejecuta el modelo de Ising con dinámica de Metropolis
   - Se puede correr una sola simulación o múltiples con diferentes parámetros
3. **Análisis**:
   - `analysis.py` procesa los resultados para calcular promedios, correlaciones, etc.
4. **Visualización**:
   - Gráficos estáticos de evolución temporal
   - Animaciones de la dinámica espacial
   - Interfaz interactiva para explorar resultados

## Parámetros a Variar para Diferentes Simulaciones

Los principales parámetros que afectan los resultados son:

1. **Parámetros físicos**:
   - `J` (acoplamiento): Controla la cohesión celular
   - `beta` (temperatura inversa): Afecta la aleatoriedad del sistema

2. **Microambiente**:
   - `h_tmb`: Campo externo basal
   - `h_tip`: Amplitud de oscilación del campo

3. **Metástasis**:
   - Probabilidades por órgano
   - Umbrales para activación

4. **Tamaño del sistema**:
   - `grid_size`: Tamaño de la red (afecta resolución y costo computacional)

Para explorar el espacio de parámetros, usar la función `generate_parameter_sweep` en `utils.py`.






