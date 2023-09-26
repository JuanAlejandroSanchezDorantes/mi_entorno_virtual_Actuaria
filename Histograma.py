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
    # Número inicial de bolas blancas
    Y_n = 1
    # Número total inicial de bolas
    total_balls = 1
    
    # Simular el proceso
    for t in range(1, n + 1):
        # Añade una bola blanca con 50% de probabilidad, de lo contrario añade una bola negra
        new_ball = np.random.choice(['white', 'black'])
        if new_ball == 'white':
            Y_n += 1
        total_balls += 1
        
        # Actualizar X_n (martingala)
        X_n = Y_n / (total_balls + 1)
    
    # Almacena el valor final de X_n para esta simulación
    final_values[i] = X_n

# Crear el histograma
plt.figure(figsize=(10, 6))
plt.hist(final_values, bins=30, density=True, color='skyblue', edgecolor='black')
plt.xlabel('$X_{10,000}$')
plt.ylabel('Frequency')
plt.title('Histogram of $X_{10,000}$ for 3000 Simulations')
plt.grid(True)
plt.show()
