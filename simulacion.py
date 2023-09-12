# Importar la biblioteca random para generar números aleatorios
import random

# Importar la clase Counter de la biblioteca collections para contar ocurrencias
from collections import Counter

# Definir el número de experimentos a realizar, se pone "_" para que sea más legible la cifra
experimentos = 1_000_000

# Crear una lista vacía para almacenar los resultados de cada experimento
resultados = []

# Realizar un millón de experimentos
for _ in range(experimentos):
    # Elegir un número aleatorio entre 1 y 6 para simular el lanzamiento de un dado
    dado = random.choice([1, 2, 3, 4, 5, 6])
    
    # Elegir una cara aleatoria para simular el lanzamiento de una moneda
    moneda = random.choice(['Cara', 'Cruz'])
    
    # Almacenar el resultado del experimento (dado, moneda) en la lista resultados
    resultados.append((dado, moneda))

# Utilizar Counter para contar la frecuencia de cada evento único (combinación de dado y moneda)
conteo = Counter(resultados)

# Iterar sobre cada evento y su frecuencia para imprimirlos
for evento, frecuencia in conteo.items():
    # Calcular y mostrar la frecuencia como un porcentaje del total de experimentos
    print(f"Evento {evento}: {frecuencia/experimentos*100:.2f}%")

