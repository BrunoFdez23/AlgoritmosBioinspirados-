import numpy as np

# Parámetros del algoritmo
N = 10       # Tamaño del cromosoma (longitud de la cadena binaria)
POP_SIZE = 6 # Tamaño de la población
GENS = 20    # Número de generaciones
MUT_RATE = 0.1  # Probabilidad de mutación

# 1. Inicialización de la población
def init_population(size, length):
    return np.random.randint(2, size=(size, length))

# 2. Función de evaluación (cantidad de 1s en la cadena)
def fitness(ind):
    return np.sum(ind)

# 3. Selección por torneo (elige al mejor de dos aleatorios)
def selection(population):
    idx1, idx2 = np.random.choice(len(population), 2, replace=False)
    return population[idx1] if fitness(population[idx1]) > fitness(population[idx2]) else population[idx2]

# 4. Cruce de un punto
def crossover(parent1, parent2):
    point = np.random.randint(1, N - 1)  # Punto de cruce (evita extremos)
    child1 = np.concatenate([parent1[:point], parent2[point:]])
    child2 = np.concatenate([parent2[:point], parent1[point:]])
    return child1, child2

# 5. Mutación (cambia un bit aleatorio)
def mutate(individual):
    if np.random.rand() < MUT_RATE:
        idx = np.random.randint(len(individual))
        individual[idx] = 1 - individual[idx]  # Invierte el bit (0 a 1 o 1 a 0)
    return individual

# **Ejecución del Algoritmo Genético**
population = init_population(POP_SIZE, N)

for gen in range(GENS):
    new_population = []
    
    # Crear nueva población con selección, cruce y mutación
    for _ in range(POP_SIZE // 2):
        parent1, parent2 = selection(population), selection(population)
        child1, child2 = crossover(parent1, parent2)
        new_population.extend([mutate(child1), mutate(child2)])
    
    population = np.array(new_population)  # Actualizar la población
    
    # Mejor individuo de la generación
    best = max(population, key=fitness)
    print(f"Generación {gen + 1}: Mejor solución {best} -> Aptitud: {fitness(best)}")

# **Resultado final**
best_solution = max(population, key=fitness)
print("\nMejor solución final:", best_solution, "-> Aptitud:", fitness(best_solution))
