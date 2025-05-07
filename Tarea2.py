import random
import math

def leer_case(filepath):
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']

    D = int(lines[0])
    aviones = []
    matriz_separacion = [[0] * D for _ in range(D)]

    idx = 1
    for i in range(D):
        Ek, Pk, Lk, Ci, Ck = map(float, lines[idx].split())
        avion = {
            'id': i,
            'Ek': int(Ek),
            'Pk': int(Pk),
            'Lk': int(Lk),
            'Ci': Ci,
            'Ck': Ck
        }
        aviones.append(avion)
        idx += 1

        separacion = list(map(int, lines[idx].split() + lines[idx + 1].split()))
        matriz_separacion[i] = separacion
        idx += 2

    return aviones, matriz_separacion

def es_valido(asignacion, avion, tiempo, matriz):
    for id_prev, t_prev in asignacion.items():
        if abs(tiempo - t_prev) < matriz[id_prev][avion['id']]:
            return False
    return True

def es_valido_2pistas(asignacion, avion, tiempo, pista, matriz):
    for (id_prev, pista_prev), t_prev in asignacion.items():
        if pista == pista_prev and abs(tiempo - t_prev) < matriz[id_prev][avion['id']]:
            return False
    return True

def greedy_determinista_1pista(aviones, matriz):
    asignados = {}
    ocupados = set()
    for avion in sorted(aviones, key=lambda x: x['Pk']):
        for t in range(avion['Pk'], avion['Lk'] + 1):
            if t in ocupados or t < avion['Ek']:
                continue
            if es_valido(asignados, avion, t, matriz):
                asignados[avion['id']] = t
                ocupados.add(t)
                break
    return asignados

def greedy_estocastico_1pista(aviones, matriz, seed):
    random.seed(seed)
    asignados = {}
    ocupados = set()
    pendientes = aviones.copy()
    random.shuffle(pendientes)

    for avion in pendientes:
        candidatos = [t for t in range(avion['Ek'], avion['Lk'] + 1)
                       if t not in ocupados and es_valido(asignados, avion, t, matriz)]
        if candidatos:
            t = random.choice(candidatos)
        else:
            t = avion['Lk']
        asignados[avion['id']] = t
        ocupados.add(t)
    return asignados

def greedy_determinista_2pistas(aviones, matriz):
    asignados = {}
    ocupados = {0: set(), 1: set()}
    for avion in sorted(aviones, key=lambda x: x['Pk']):
        for pista in [0, 1]:
            for t in range(avion['Pk'], avion['Lk'] + 1):
                if t in ocupados[pista] or t < avion['Ek']:
                    continue
                if es_valido_2pistas(asignados, avion, t, pista, matriz):
                    asignados[(avion['id'], pista)] = t
                    ocupados[pista].add(t)
                    break
            else:
                continue
            break
    return asignados

def greedy_estocastico_2pistas(aviones, matriz, seed):
    random.seed(seed)
    asignados = {}
    ocupados = {0: set(), 1: set()}
    pendientes = aviones.copy()
    random.shuffle(pendientes)

    for avion in pendientes:
        candidatos = []
        for pista in [0, 1]:
            for t in range(avion['Ek'], avion['Lk'] + 1):
                if t not in ocupados[pista] and es_valido_2pistas(asignados, avion, t, pista, matriz):
                    candidatos.append((t, pista))

        if candidatos:
            t, pista = random.choice(candidatos)
        else:
            t, pista = avion['Lk'], 0
        asignados[(avion['id'], pista)] = t
        ocupados[pista].add(t)
    return asignados


def costo_total(asignacion, aviones):
    total = 0
    for avion in aviones:
        t = asignacion.get(avion['id']) or asignacion.get((avion['id'], 0)) or asignacion.get((avion['id'], 1))
        if t is not None:
            if t < avion['Pk']:
                total += avion['Ci'] * (avion['Pk'] - t)
            elif t > avion['Pk']:
                total += avion['Ck'] * (t - avion['Pk'])
    return total

def generar_vecinos(solucion, aviones, matriz):
    vecinos = []
    for avion in aviones:
        id = avion['id']
        t_actual = solucion.get(id)
        for delta in [-1, 1]:
            t_nuevo = t_actual + delta
            if avion['Ek'] <= t_nuevo <= avion['Lk']:
                nueva_sol = solucion.copy()
                nueva_sol[id] = t_nuevo
                if es_valido(nueva_sol, avion, t_nuevo, matriz):
                    vecinos.append(nueva_sol)
    return vecinos

def hill_climbing(solucion_inicial, aviones, matriz, max_iter=100):
    actual = solucion_inicial.copy()
    mejor_costo = costo_total(actual, aviones)
    for _ in range(max_iter):
        vecinos = generar_vecinos(actual, aviones, matriz)
        mejora = False
        for vecino in vecinos:
            costo = costo_total(vecino, aviones)
            if costo < mejor_costo:
                actual = vecino
                mejor_costo = costo
                mejora = True
                break
        if not mejora:
            break
    return actual, mejor_costo

def grasp_hillclimbing(aviones, matriz, n_reinicios=10):
    mejor_sol = None
    mejor_costo = float('inf')
    for seed in range(n_reinicios):
        sol_inicial = greedy_estocastico_1pista(aviones, matriz, seed)
        refinada, costo = hill_climbing(sol_inicial, aviones, matriz)
        if costo < mejor_costo:
            mejor_sol = refinada
            mejor_costo = costo
    return mejor_sol, mejor_costo

def generar_vecinos_2pistas(solucion, aviones, matriz):
    vecinos = []
    for avion in aviones:
        id = avion['id']
        for pista in [0, 1]:
            key = (id, pista)
            if key not in solucion:
                continue
            t_actual = solucion[key]
            for delta in [-1, 1]:
                t_nuevo = t_actual + delta
                if avion['Ek'] <= t_nuevo <= avion['Lk']:
                    nueva_sol = solucion.copy()
                    nueva_sol[key] = t_nuevo
                    if es_valido_2pistas(nueva_sol, avion, t_nuevo, pista, matriz):
                        vecinos.append(nueva_sol)
    return vecinos

def hill_climbing_2pistas(sol_inicial, aviones, matriz, max_iter=100):
    actual = sol_inicial.copy()
    mejor_costo = costo_total(actual, aviones)
    for _ in range(max_iter):
        vecinos = generar_vecinos_2pistas(actual, aviones, matriz)
        mejora = False
        for vecino in vecinos:
            costo = costo_total(vecino, aviones)
            if costo < mejor_costo:
                actual = vecino
                mejor_costo = costo
                mejora = True
                break
        if not mejora:
            break
    return actual, mejor_costo

def grasp_hillclimbing_2pistas(aviones, matriz, n_reinicios=10):
    mejor_sol = None
    mejor_costo = float('inf')
    for seed in range(n_reinicios):
        sol_inicial = greedy_estocastico_2pistas(aviones, matriz, seed)
        refinada, costo = hill_climbing_2pistas(sol_inicial, aviones, matriz)
        if costo < mejor_costo:
            mejor_sol = refinada
            mejor_costo = costo
    return mejor_sol, mejor_costo

def simulated_annealing_1pista(sol_inicial, aviones, matriz, T_init=1000, alpha=0.95, T_min=1e-3, max_iter=100):
    actual = sol_inicial.copy()
    costo_act = costo_total(actual, aviones)
    T = T_init

    while T > T_min:
        for _ in range(max_iter):
            vecino = actual.copy()
            avion = random.choice(aviones)
            id = avion['id']
            delta = random.choice([-1, 1])
            t_nuevo = vecino[id] + delta
            if avion['Ek'] <= t_nuevo <= avion['Lk'] and es_valido(vecino, avion, t_nuevo, matriz):
                vecino[id] = t_nuevo
                costo_vec = costo_total(vecino, aviones)
                delta_costo = costo_vec - costo_act
                if delta_costo < 0 or random.random() < math.exp(-delta_costo / T):
                    actual = vecino
                    costo_act = costo_vec
        T *= alpha

    return actual, costo_act

def simulated_annealing_2pistas(sol_inicial, aviones, matriz, T_init=1000, alpha=0.95, T_min=1e-3, max_iter=100):
    actual = sol_inicial.copy()
    costo_act = costo_total(actual, aviones)
    T = T_init

    while T > T_min:
        for _ in range(max_iter):
            vecino = actual.copy()
            avion = random.choice(aviones)
            id = avion['id']
            for pista in [0, 1]:
                key = (id, pista)
                if key in vecino:
                    delta = random.choice([-1, 1])
                    t_nuevo = vecino[key] + delta
                    if avion['Ek'] <= t_nuevo <= avion['Lk'] and es_valido_2pistas(vecino, avion, t_nuevo, pista, matriz):
                        vecino[key] = t_nuevo
                        costo_vec = costo_total(vecino, aviones)
                        delta_costo = costo_vec - costo_act
                        if delta_costo < 0 or random.random() < math.exp(-delta_costo / T):
                            actual = vecino
                            costo_act = costo_vec
                        break
        T *= alpha

    return actual, costo_act


if __name__ == '__main__':
    case = "case1.txt"
    print(f"\n=== Procesando {case} ===")
    aviones, matriz = leer_case(case)

    print("\n--- Greedy Determinista (1 pista) ---")
    sol_det_1 = greedy_determinista_1pista(aviones, matriz)
    print(sol_det_1)
    print(f"Costo total: {costo_total(sol_det_1, aviones):.2f}")

    print("\n--- Greedy Estocástico (1 pista) ---")
    for seed in range(10):
        sol_est_1 = greedy_estocastico_1pista(aviones, matriz, seed)
        print(f"Seed {seed}: {sol_est_1}")
        print(f"Costo total: {costo_total(sol_est_1, aviones):.2f}")

    print("\n--- Greedy Determinista (2 pistas) ---")
    sol_det_2 = greedy_determinista_2pistas(aviones, matriz)
    print(sol_det_2)
    print(f"Costo total: {costo_total(sol_det_2, aviones):.2f}")

    print("\n--- Greedy Estocástico (2 pistas) ---")
    for seed in range(10):
        sol_est_2 = greedy_estocastico_2pistas(aviones, matriz, seed)
        print(f"Seed {seed}: {sol_est_2}")
        print(f"Costo total: {costo_total(sol_est_2, aviones):.2f}")

    print("\n--- GRASP + Hill Climbing (1 pista) ---")
    grasp_sol, grasp_costo = grasp_hillclimbing(aviones, matriz, n_reinicios=10)
    print(f"Mejor solución GRASP: {grasp_sol}")
    print(f"Costo total GRASP: {grasp_costo:.2f}")

    print("\n--- GRASP + Hill Climbing (2 pistas) ---")
    grasp_sol_2, grasp_costo_2 = grasp_hillclimbing_2pistas(aviones, matriz, n_reinicios=10)
    print(f"Mejor solución GRASP 2 pistas: {grasp_sol_2}")
    print(f"Costo total GRASP 2 pistas: {grasp_costo_2:.2f}")
    
    print("\n--- Simulated Annealing (1 pista) ---")
    sol_inicial_sa1 = greedy_estocastico_1pista(aviones, matriz, seed=0)
    sa_sol_1, sa_cost_1 = simulated_annealing_1pista(sol_inicial_sa1, aviones, matriz)
    print(f"Solución final SA 1 pista: {sa_sol_1}")
    print(f"Costo total SA 1 pista: {sa_cost_1:.2f}")

    print("\n--- Simulated Annealing (2 pistas) ---")
    sol_inicial_sa2 = greedy_estocastico_2pistas(aviones, matriz, seed=0)
    sa_sol_2, sa_cost_2 = simulated_annealing_2pistas(sol_inicial_sa2, aviones, matriz)
    print(f"Solución final SA 2 pistas: {sa_sol_2}")
    print(f"Costo total SA 2 pistas: {sa_cost_2:.2f}")
