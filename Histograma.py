import numpy as np
import matplotlib.pyplot as plt

# Número de simulaciones
num_simulations = 3000

# Pasos de tiempo
n = 10000

# Inicializar un array para almacenar los valores finales de X_n para cada simulación.
final_values = np.zeros(num_simulations)

# Recorrer cada simulación
for i in range(num_simulations):
    
    # Simular el proceso
    for t in range(1, n + 1):
        # Para una Bernoulli con p = 0.5, X_n será 1 o 0 con igual probabilidad
        X_n = np.random.choice([1, 0], p=[0.5, 0.5])
        
    # Almacena el valor final de X_n para esta simulación
    final_values[i] = X_n

# Crear el histograma
plt.figure(figsize=(10, 6))
plt.hist(final_values, bins=2, density=True, color='skyblue', edgecolor='black')
plt.xlabel('$X_{10,000}$')
plt.ylabel('Frecuencia')
plt.title('Histograma de $X_{10,000}$ para 3000 simulaciones (Bernoulli)')
plt.grid(True)
plt.show()

