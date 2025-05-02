import random
import math

# Parámetros del algoritmo
ALPHA = 1.0    # Importancia de las feromonas
BETA = 5.0     # Importancia de la heurística (1 / distancia)
EVAPORATION = 0.5  # Tasa de evaporación de feromonas
Q = 100        # Cantidad de feromonas depositadas
NUM_ANTS = 10  # Número de hormigas
NUM_ITER = 100 # Número de iteraciones

# Mapa simple: distancias entre ciudades
distances = [
    [0, 2, 2, 5, 7],
    [2, 0, 4, 8, 2],
    [2, 4, 0, 1, 3],
    [5, 8, 1, 0, 2],
    [7, 2, 3, 2, 0],
]

num_cities = len(distances)
pheromones = [[1.0 for _ in range(num_cities)] for _ in range(num_cities)]  # Inicialización

def probability(from_city, to_city, visited):
    if to_city in visited:
        return 0
    pheromone = pheromones[from_city][to_city] ** ALPHA
    visibility = (1.0 / distances[from_city][to_city]) ** BETA
    return pheromone * visibility

def choose_next_city(from_city, visited):
    probs = [probability(from_city, i, visited) for i in range(num_cities)]
    total = sum(probs)
    if total == 0:
        return random.choice([i for i in range(num_cities) if i not in visited])
    probs = [p / total for p in probs]
    r = random.random()
    cumulative = 0.0
    for i, p in enumerate(probs):
        cumulative += p
        if r <= cumulative:
            return i
    return probs.index(max(probs))  # fallback

def run_ant():
    visited = []
    current = random.randint(0, num_cities - 1)
    visited.append(current)
    while len(visited) < num_cities:
        next_city = choose_next_city(current, visited)
        visited.append(next_city)
        current = next_city
    return visited

def total_distance(path):
    dist = 0
    for i in range(len(path)):
        dist += distances[path[i]][path[(i + 1) % num_cities]]
    return dist

def update_pheromones(paths):
    global pheromones
    # Evaporación
    for i in range(num_cities):
        for j in range(num_cities):
            pheromones[i][j] *= (1 - EVAPORATION)
    # Deposición
    for path in paths:
        dist = total_distance(path)
        deposit = Q / dist
        for i in range(len(path)):
            a = path[i]
            b = path[(i + 1) % num_cities]
            pheromones[a][b] += deposit
            pheromones[b][a] += deposit  # bidireccional

best_path = None
best_dist = float('inf')

for iteration in range(NUM_ITER):
    all_paths = [run_ant() for _ in range(NUM_ANTS)]
    for path in all_paths:
        dist = total_distance(path)
        if dist < best_dist:
            best_dist = dist
            best_path = path
    update_pheromones(all_paths)

print("Mejor camino encontrado:", best_path)
print("Distancia:", best_dist)
