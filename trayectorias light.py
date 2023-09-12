import numpy as np

def caminata_aleatoria(pasos, seed):
    np.random.seed(seed)  
    trayectoria = np.cumsum(2 * np.random.randint(0, 2, pasos) - 1)
    maximo = np.max(trayectoria)
    minimo = np.min(trayectoria)
    supera_nivel_1 = trayectoria[-1] > 1
    return maximo, minimo, supera_nivel_1

# Parámetros de la simulación
simulaciones = 150000
pasos = 1000000

# Creando una lista para almacenar los resultados de cada simulación
resultados = []

# Usando un bucle for para ejecutar cada simulación individualmente
for i in range(simulaciones):
    resultados.append(caminata_aleatoria(pasos, i))

# Extrayendo los máximos, mínimos y si superaron el nivel 1 de los resultados
maximos, minimos, superan_nivel_1 = zip(*resultados)

# Mostrando los resultados
max_global = np.max(maximos)
min_global = np.min(minimos)
supera_nivel_1_count = np.sum(superan_nivel_1)
print(f"Máximo global: {max_global}")
print(f"Mínimo global: {min_global}")
print(f"Número de trayectorias que superaron el nivel 1: {supera_nivel_1_count}")
