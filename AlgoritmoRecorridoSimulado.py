import random
import math

# Mapa de distancias entre 5 ciudades
distances = [
    [0, 2, 2, 5, 7],
    [2, 0, 4, 8, 2],
    [2, 4, 0, 1, 3],
    [5, 8, 1, 0, 2],
    [7, 2, 3, 2, 0],
]

num_cities = len(distances)

def total_distance(path):
    return sum(distances[path[i]][path[(i + 1) % num_cities]] for i in range(num_cities))

def swap_two(path):
    """Intercambia dos ciudades aleatoriamente."""
    a, b = random.sample(range(num_cities), 2)
    new_path = path[:]
    new_path[a], new_path[b] = new_path[b], new_path[a]
    return new_path

def simulated_annealing():
    # Parámetros
    T = 100.0             # Temperatura inicial
    T_min = 0.1           # Temperatura mínima
    alpha = 0.995         # Factor de enfriamiento
    max_iter = 1000       # Iteraciones máximas

    current_path = list(range(num_cities))
    random.shuffle(current_path)
    current_dist = total_distance(current_path)
    best_path = current_path[:]
    best_dist = current_dist

    for _ in range(max_iter):
        if T < T_min:
            break
        new_path = swap_two(current_path)
        new_dist = total_distance(new_path)
        delta = new_dist - current_dist

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_path = new_path
            current_dist = new_dist
            if new_dist < best_dist:
                best_path = new_path
                best_dist = new_dist

        T *= alpha

    return best_path, best_dist

# Ejecutar el algoritmo
best_path, best_dist = simulated_annealing()

print("Mejor camino encontrado:", best_path)
print("Distancia total:", best_dist)
